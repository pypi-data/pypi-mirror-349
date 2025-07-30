"""
This module provides mixins for Django views that enhance CRUD operations with HTMX support,
filtering capabilities, and modal interactions.

Key Components:
- HTMXFilterSetMixin: Adds HTMX attributes to filter forms for dynamic updates
- NominopolitanMixin: Main mixin that provides CRUD view enhancements with HTMX and modal support
"""

from django import forms
from django.forms import models as model_forms
from django.db import models

from django.http import Http404
from django.urls import NoReverseMatch, path, reverse
from django.utils.decorators import classonlymethod
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render
from django.template.response import TemplateResponse

from django.conf import settings
from django.db.models.fields.reverse_related import ManyToOneRel

import json
import logging
log = logging.getLogger("nominopolitan")

from crispy_forms.helper import FormHelper
from django import forms
from django_filters import (
    FilterSet, CharFilter, DateFilter, NumberFilter, 
    BooleanFilter, ModelChoiceFilter, TimeFilter,
    ModelMultipleChoiceFilter,
)
from django_filters.filterset import filterset_factory
from neapolitan.views import Role
from .validators import NominopolitanMixinValidator
from django.db.models import Q
from functools import reduce
import operator

class AllValuesModelMultipleChoiceFilter(ModelMultipleChoiceFilter):
    """Custom filter that requires ALL selected values to match (AND logic)"""
    def filter(self, qs, value):
        if not value:
            return qs
        
        # For each value, filter for items that have that value in the M2M field
        for val in value:
            qs = qs.filter(**{f"{self.field_name}": val})
        return qs

class HTMXFilterSetMixin:
    """
    Mixin that adds HTMX attributes to filter forms for dynamic updates.
    
    Attributes:
        HTMX_ATTRS (dict): Base HTMX attributes for form fields
        FIELD_TRIGGERS (dict): Mapping of form field types to HTMX trigger events
    """

    HTMX_ATTRS: dict[str, str] = {
        'hx-get': '',
        'hx-include': '[name]',  # Include all named form fields
    }

    FIELD_TRIGGERS: dict[type[forms.Widget] | str, str] = {
        forms.DateInput: 'change',
        forms.TextInput: 'keyup changed delay:300ms',
        forms.NumberInput: 'keyup changed delay:300ms',
        'default': 'change'
    }

    def setup_htmx_attrs(self) -> None:
        """Configure HTMX attributes for form fields and setup crispy form helper."""
        for field in self.form.fields.values():
            widget_class: type[forms.Widget] = type(field.widget)
            trigger: str = self.FIELD_TRIGGERS.get(widget_class, self.FIELD_TRIGGERS['default'])
            attrs: dict[str, str] = {**self.HTMX_ATTRS, 'hx-trigger': trigger}
            field.widget.attrs.update(attrs)

        # self.helper = FormHelper()
        # self.helper.form_tag = False
        # self.helper.disable_csrf = True

        # bootstrap5
        # self.helper.wrapper_class = 'col-auto'
        # self.helper.template = 'bootstrap5/layout/inline_field.html'

        # Use Tailwind-specific classes instead of Bootstrap
        # self.helper.label_class = 'block text-sm font-medium text-gray-700'
        # self.helper.field_class = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'
        # self.helper.template = 'tailwind/layout/inline_field.html'


class NominopolitanMixin:
    """
    Main mixin that enhances Django CRUD views with HTMX support, filtering, and modal functionality.
    
    Attributes:
        namespace (str | None): URL namespace for the view
        templates_path (str): Path to template directory
        base_template_path (str): Path to base template
        use_crispy (bool | None): Enable crispy-forms if installed
        exclude (list[str]): Fields to exclude from list view
        properties (list[str]): Model properties to include in list view
        use_htmx (bool | None): Enable HTMX functionality

        use_modal (bool | None): Enable modal dialogs
        modal_id (str | None): Custom modal element ID
        modal_target (str | None): Allows override of the default modal target
            which is #nominopolitanModalContent. Useful if for example
            the project has a modal with a different id available
            in the base template.

    """

    # namespace if appropriate
    namespace: str | None = None

    # template parameters
    templates_path: str = f"nominopolitan/{getattr(settings, 'NOMINOPOLITAN_CSS_FRAMEWORK', 'daisyui')}"
    base_template_path: str = f"{templates_path}/base.html"

    # forms
    use_crispy: bool | None = None

    # field and property inclusion scope
    exclude: list[str] = []
    properties: list[str] = []
    properties_exclude: list[str] = []

    # for the detail view
    detail_fields: list[str] = []
    detail_exclude: list[str] = []
    detail_properties: list[str] = []
    detail_properties_exclude: list[str] = []

    # form fields (if no form_class is specified)
    form_fields: list[str] = []
    form_fields_exclude: list[str] = []

    # htmx
    use_htmx: bool | None = None
    default_htmx_target: str = '#content'
    hx_trigger: str | dict[str, str] | None = None

    # modals (if htmx is active)
    use_modal: bool | None = None
    modal_id: str | None = None
    modal_target: str | None = None

    # table display parameters
    table_pixel_height_other_page_elements: int | float = 0  # px pixels
    table_max_height: int = 70 # expressed as vh units (ie percentage) of the remaining blank space 
        # after subtracting table_pixel_height_other_page_elements

    table_max_col_width: int = None # Expressed in ch units
    table_header_min_wrap_width: int = None  # Expressed in ch units

    table_classes: str = ''
    action_button_classes: str = ''
    extra_button_classes: str = ''

    # Add this class attribute to control M2M filter logic
    m2m_filter_and_logic = False  # False for OR logic (default), True for AND logic

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get all attributes that should be validated
        config_dict = {
            attr: getattr(self, attr)
            for attr in NominopolitanMixinValidator.__fields__.keys()
            if hasattr(self, attr)
        }
        
        try:
            validated_settings = NominopolitanMixinValidator(**config_dict)
            # Update instance attributes with validated values
            for field_name, value in validated_settings.dict().items():
                setattr(self, field_name, value)
        except ValueError as e:
            class_name = self.__class__.__name__
            raise ImproperlyConfigured(
                f"Invalid configuration in class '{class_name}': {str(e)}"
            )

        # determine the starting list of fields (before exclusions)
        if not self.fields or self.fields == '__all__':
            # set to all fields in model
            self.fields = self._get_all_fields()
        elif type(self.fields) == list:
            # check all are valid fields
            all_fields = self._get_all_fields()
            for field in self.fields:
                if field not in all_fields:
                    raise ValueError(f"Field {field} not defined in {self.model.__name__}")
        elif type(self.fields) != list:
            raise TypeError("fields must be a list")        
        else:
            raise ValueError("fields must be '__all__', a list of valid fields or not defined")

        # exclude fields
        if type(self.exclude) == list:
            self.fields = [field for field in self.fields if field not in self.exclude]
        else:
            raise TypeError("exclude must be a list")

        if self.properties:
            if self.properties == '__all__':
                # Set self.properties to a list of every property in self.model
                self.properties = self._get_all_properties()
            elif type(self.properties) == list:
                # check all are valid properties
                all_properties = self._get_all_properties()
                for prop in self.properties:
                    if prop not in all_properties:
                        raise ValueError(f"Property {prop} not defined in {self.model.__name__}")
            elif type(self.properties) != list:
                raise TypeError("properties must be a list or '__all__'")
            
        # exclude properties
        if type(self.properties_exclude) == list:
            self.properties = [prop for prop in self.properties if prop not in self.properties_exclude]
        else:
            raise TypeError("properties_exclude must be a list")

        # determine the starting list of detail_fields (before exclusions)
        if self.detail_fields == '__all__':
            # Set self.detail_fields to a list of every field in self.model
            self.detail_fields = self._get_all_fields()        
        elif not self.detail_fields or self.detail_fields == '__fields__':
            # Set self.detail_fields to self.fields
            self.detail_fields = self.fields
        elif type(self.detail_fields) == list:
            # check all are valid fields
            all_fields = self._get_all_fields()
            for field in self.detail_fields:
                if field not in all_fields:
                    raise ValueError(f"detail_field {field} not defined in {self.model.__name__}")
        elif type(self.detail_fields) != list:
            raise TypeError("detail_fields must be a list or '__all__' or '__fields__' or a list of fields")

        # exclude detail_fields
        if type(self.detail_exclude) == list:
            self.detail_fields = [field for field in self.detail_fields 
                                  if field not in self.detail_exclude]
        else:
            raise TypeError("detail_fields_exclude must be a list")

        # add specified detail_properties            
        if self.detail_properties:
            if self.detail_properties == '__all__':
                # Set self.detail_properties to a list of every property in self.model
                self.detail_properties = self._get_all_properties()
            elif self.detail_properties == '__properties__':
                # Set self.detail_properties to a list of every property in self.model
                self.detail_properties = self.properties
            elif type(self.detail_properties) == list:
                # check all are valid properties
                all_properties = self._get_all_properties()
                for prop in self.detail_properties:
                    if prop not in all_properties:
                        raise ValueError(f"Property {prop} not defined in {self.model.__name__}")
            elif type(self.detail_properties) != list:
                raise TypeError("detail_properties must be a list or '__all__' or '__properties__'")

        # exclude detail_properties
        if type(self.detail_properties_exclude) == list:
            self.detail_properties = [prop for prop in self.detail_properties 
                                  if prop not in self.detail_properties_exclude]
        else:
            raise TypeError("detail_properties_exclude must be a list")

        # Process form_fields last, after all other field processing is complete
        all_editable = self._get_all_editable_fields()
        
        if not self.form_fields:
            # Default to editable fields from detail_fields
            self.form_fields = [
                f for f in self.detail_fields 
                if f in all_editable
            ]
        elif self.form_fields == '__all__':
            self.form_fields = all_editable
        elif self.form_fields == '__fields__':
            self.form_fields = [
                f for f in self.fields 
                if f in all_editable
            ]
        else:
            # Validate that specified fields exist and are editable
            invalid_fields = [f for f in self.form_fields if f not in all_editable]
            if invalid_fields:
                raise ValueError(
                    f"The following form_fields are not editable fields in {self.model.__name__}: "
                    f"{', '.join(invalid_fields)}"
                )

        # Process form fields exclusions
        if self.form_fields_exclude:
            self.form_fields = [
                f for f in self.form_fields 
                if f not in self.form_fields_exclude
            ]
            
    def list(self, request, *args, **kwargs):
        """
        Handle GET requests for list view, including filtering and pagination.
        """
        queryset = self.get_queryset()
        filterset = self.get_filterset(queryset)
        if filterset is not None:
            queryset = filterset.qs

        if not self.allow_empty and not queryset.exists():
            raise Http404

        paginate_by = self.get_paginate_by()
        if paginate_by is None:
            # Unpaginated response
            self.object_list = queryset
            context = self.get_context_data(
                page_obj=None,
                is_paginated=False,
                paginator=None,
                filterset=filterset,
                sort=request.GET.get('sort', ''),  # Add sort to context
                use_htmx=self.get_use_htmx(),
            )
        else:
            # Paginated response
            page = self.paginate_queryset(queryset, paginate_by)
            self.object_list = page.object_list
            context = self.get_context_data(
                page_obj=page,
                is_paginated=page.has_other_pages(),
                paginator=page.paginator,
                filterset=filterset,
                sort=request.GET.get('sort', ''),  # Add sort to context
                use_htmx=self.get_use_htmx(),
            )

        return self.render_to_response(context)

    def get_table_pixel_height_other_page_elements(self) -> str:
        """ Returns the height of other elements on the page that the table is
        displayed on. After subtracting this (in pixels) from the page height,
        the table height will be calculated (in a css style in list.html) as
        {{ get_table_max_height }}% of the remaining viewport height.
        """
        return f"{self.table_pixel_height_other_page_elements or 0}px" #px

    def get_table_max_height(self) -> int:
        """Returns the proportion of visible space on the viewport after subtracting
        the height of other elements on the page that the table is displayed on, 
        as represented by get_table_pixel_height_other_page_elements().

        The table height is calculated in a css style for max-table-height in list.html.
        """
        return self.table_max_height

    def get_table_max_col_width(self):
        # The max width for the table columns in object_list.html - in characters
        return f"{self.table_max_col_width}ch" or '25ch'
    
    def get_table_header_min_wrap_width(self):
        # The max width for the table columns in object_list.html - in characters
        if self.table_header_min_wrap_width is None:
            return self.get_table_max_col_width()
        elif int(self.table_header_min_wrap_width) > int(self.table_max_col_width):
            return self.get_table_max_col_width()
        else:
            return f"{self.table_header_min_wrap_width}ch" #ch
    
    def get_table_classes(self):
        """
        Get the table classes.
        """
        return self.table_classes

    def get_action_button_classes(self):
        """
        Get the action button classes.
        """
        return self.action_button_classes
    
    def get_extra_button_classes(self):
        """
        Get the extra button classes.
        """
        return self.extra_button_classes

    def get_framework_styles(self):
        """
        Get framework-specific styles. Override this method and add 
        the new framework name as a key to the returned dictionary.
        
        Returns:
            dict: Framework-specific style configurations
        """
        
        return {
            'bootstrap5': {
                # base class for all buttons
                'base': 'btn ',
                # attributes for filter form fields
                'filter_attrs': {
                    'text': {'class': 'form-control form-control-sm small py-1'},
                    'select': {'class': 'form-select form-select-sm small py-1'},
                    'multiselect': {
                        'class': 'form-select form-select-sm small', 
                        'size': '5',
                        'style': 'min-height: 8rem; padding: 0.25rem;'
                    },
                    'date': {'class': 'form-control form-control-sm small py-1', 'type': 'date'},
                    'number': {'class': 'form-control form-control-sm small py-1', 'step': 'any'},
                    'time': {'class': 'form-control form-control-sm small py-1', 'type': 'time'},
                    'default': {'class': 'form-control form-control-sm small py-1'},
                },
                # set colours for the action buttons
                'actions': {
                    'View': 'btn-info',
                    'Edit': 'btn-primary',
                    'Delete': 'btn-danger'
                },
                # default colour for extra action buttons
                'extra_default': 'btn-primary',
                # modal class attributes
                'modal_attrs': f'data-bs-toggle="modal" data-bs-target="{self.get_modal_id()}"',
            },
            'daisyUI': {
                # base class for all buttons
                'base': 'btn ',
                # attributes for filter form fields
                'filter_attrs': {
                    'text': {'class': 'input input-bordered input-sm w-full text-xs h-10 min-h-10'},
                    'select': {'class': 'select select-bordered select-sm w-full text-xs h-10 min-h-10'},
                    'multiselect': {
                        'class': 'select select-bordered select-sm w-full text-xs', 
                        'size': '5',
                        'style': 'min-height: 8rem; max-height: 8rem; overflow-y: auto;'
                    },
                    'date': {'class': 'input input-bordered input-sm w-full text-xs h-10 min-h-10', 'type': 'date'},
                    'number': {'class': 'input input-bordered input-sm w-full text-xs h-10 min-h-10', 'step': 'any'},
                    'time': {'class': 'input input-bordered input-sm w-full text-xs h-10 min-h-10', 'type': 'time'},
                    'default': {'class': 'input input-bordered input-sm w-full text-xs h-10 min-h-10'},
                },
                # set colours for the action buttons
                'actions': {
                    'View': 'btn-info',
                    'Edit': 'btn-primary',
                    'Delete': 'btn-error'
                },
                # default colour for extra action buttons
                'extra_default': 'btn-primary',
                # modal class attributes
                'modal_attrs': f'onclick="{self.get_modal_id()[1:]}.showModal()"', 
            },
        }

    def get_filter_queryset_for_field(self, field_name, model_field):
        """Get an efficiently filtered and sorted queryset for filter options."""
        
        # Start with an empty queryset
        queryset = model_field.related_model.objects
        
        # Define model_fields early to ensure it exists in all code paths
        model_fields = [f.name for f in model_field.related_model._meta.fields]
        
        # Apply custom filters if defined
        filter_options = getattr(self, 'filter_queryset_options', {})
        if field_name in filter_options:
            filters = filter_options[field_name]
            if callable(filters):
                try:
                    # Add error handling for the callable
                    from datetime import datetime  # Ensure datetime is available
                    result = filters(self.request, field_name, model_field)
                    if isinstance(result, models.QuerySet):
                        queryset = result
                    else:
                        queryset = queryset.filter(**result)
                except Exception as e:
                    import logging
                    logging.error(f"Error in filter callable for {field_name}: {str(e)}")
            elif isinstance(filters, dict):
                # Apply filter dict directly
                queryset = queryset.filter(**filters)
            elif isinstance(filters, (int, str)):
                # Handle simple ID/PK filtering
                queryset = queryset.filter(pk=filters)
        else:
            # No filters specified, get all records
            queryset = queryset.all()
        
        # Check if we should sort by a specific field
        sort_options = getattr(self, 'filter_sort_options', {})
        if field_name in sort_options:
            sort_field = sort_options[field_name]
            return queryset.order_by(sort_field)
        
        # If no specified sort field but model has common name fields, use that
        for field in ['name', 'title', 'label', 'display_name']:
            if field in model_fields:
                return queryset.order_by(field)
        
        # Only if really necessary, fall back to string representation sorting
        sorted_objects = sorted(list(queryset), key=lambda x: str(x).lower())
        pk_list = [obj.pk for obj in sorted_objects]
        
        if not pk_list:  # Empty list case
            return queryset.none()
            
        # Return ordered queryset
        from django.db.models import Case, When, Value, IntegerField
        preserved_order = Case(
            *[When(pk=pk, then=Value(i)) for i, pk in enumerate(pk_list)],
            output_field=IntegerField(),
        )
        
        return queryset.filter(pk__in=pk_list).order_by(preserved_order)

    def get_filterset(self, queryset=None):
        """
        Create a dynamic FilterSet class based on provided parameters:
            - filterset_class (in which case the provided class is used); or
            - filterset_fields (in which case a dynamic class is created)
        
        Args:
            queryset: Optional queryset to filter
            
        Returns:
            FilterSet: Configured filter set instance or None
        """
        filterset_class = getattr(self, "filterset_class", None)
        filterset_fields = getattr(self, "filterset_fields", None)

        if filterset_class is not None or filterset_fields is not None:
            # Check if any filter params (besides page/sort) are present
            filter_keys = [k for k in self.request.GET.keys() if k != 'page' and k != 'sort']
            if filter_keys and 'page' in self.request.GET:
                # Remember we need to reset pagination
                setattr(self, '_reset_pagination', True)

        if filterset_class is None and filterset_fields is not None:
            use_htmx = self.get_use_htmx()
            use_crispy = self.get_use_crispy()

            class DynamicFilterSet(HTMXFilterSetMixin, FilterSet):
                """
                Dynamically create a FilterSet class based on the model fields.
                This class inherits from HTMXFilterSetMixin to add HTMX functionality
                and FilterSet for Django filtering capabilities.
                """
                framework = getattr(settings, 'NOMINOPOLITAN_CSS_FRAMEWORK', 'daisyui')
                BASE_ATTRS = self.get_framework_styles()[framework]['filter_attrs']
                
                # Dynamically create filter fields based on the model's fields
                for field_name in filterset_fields:
                    model_field = self.model._meta.get_field(field_name)
                    
                    # Handle GeneratedField special case
                    field_to_check = model_field.output_field if isinstance(model_field, models.GeneratedField) else model_field
                    # Check if BASE_ATTRS is structured by field type
                    if isinstance(BASE_ATTRS, dict) and ('text' in BASE_ATTRS or 'select' in BASE_ATTRS):
                        # Get appropriate attributes based on field type
                        if isinstance(field_to_check, models.ManyToManyField):
                            field_attrs = BASE_ATTRS.get('multiselect', BASE_ATTRS.get('select', BASE_ATTRS.get('default', {}))).copy()
                        elif isinstance(field_to_check, models.ForeignKey):
                            field_attrs = BASE_ATTRS.get('select', BASE_ATTRS.get('default', {})).copy()
                        elif isinstance(field_to_check, (models.CharField, models.TextField)):
                            field_attrs = BASE_ATTRS.get('text', BASE_ATTRS.get('default', {})).copy()
                        elif isinstance(field_to_check, models.DateField):
                            field_attrs = BASE_ATTRS.get('date', BASE_ATTRS.get('default', {})).copy()
                        elif isinstance(field_to_check, (models.IntegerField, models.DecimalField, models.FloatField)):
                            field_attrs = BASE_ATTRS.get('number', BASE_ATTRS.get('default', {})).copy()
                        elif isinstance(field_to_check, models.TimeField):
                            field_attrs = BASE_ATTRS.get('time', BASE_ATTRS.get('default', {})).copy()
                        elif isinstance(field_to_check, models.BooleanField):
                            field_attrs = BASE_ATTRS.get('select', BASE_ATTRS.get('default', {})).copy()
                        else:
                            field_attrs = BASE_ATTRS.get('default', {}).copy()
                    else:
                        # Legacy behavior - use the same attributes for all fields
                        field_attrs = BASE_ATTRS.copy()


                    # Create appropriate filter based on field type
                    if isinstance(field_to_check, models.ManyToManyField):
                        # Add max-height and other useful styles to the select widget
                        field_attrs.update({
                            'style': 'max-height: 200px; overflow-y: auto;',
                            'class': field_attrs.get('class', '') + ' select2',  # Add select2 class if you want to use Select2
                        })
                        
                        # Choose between OR logic (ModelMultipleChoiceFilter) or AND logic (AllValuesModelMultipleChoiceFilter)
                        filter_class = AllValuesModelMultipleChoiceFilter if self.m2m_filter_and_logic else ModelMultipleChoiceFilter
                        
                        locals()[field_name] = filter_class(
                            queryset=self.get_filter_queryset_for_field(field_name, model_field),
                            widget=forms.SelectMultiple(attrs=field_attrs)
                        )
                    elif isinstance(field_to_check, (models.CharField, models.TextField)):
                        locals()[field_name] = CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs=field_attrs))
                    elif isinstance(field_to_check, models.DateField):
                        if 'type' not in field_attrs:
                            field_attrs['type'] = 'date'
                        locals()[field_name] = DateFilter(widget=forms.DateInput(attrs=field_attrs))
                    elif isinstance(field_to_check, (models.IntegerField, models.DecimalField, models.FloatField)):
                        if 'step' not in field_attrs:
                            field_attrs['step'] = 'any'
                        locals()[field_name] = NumberFilter(widget=forms.NumberInput(attrs=field_attrs))
                    elif isinstance(field_to_check, models.BooleanField):
                        locals()[field_name] = BooleanFilter(widget=forms.Select(
                            attrs=field_attrs, choices=((None, '---------'), (True, True), (False, False))))
                    elif isinstance(field_to_check, models.ForeignKey):
                        locals()[field_name] = ModelChoiceFilter(
                            queryset=self.get_filter_queryset_for_field(field_name, model_field),
                            widget=forms.Select(attrs=field_attrs)
                        )
                    elif isinstance(field_to_check, models.TimeField):
                        if 'type' not in field_attrs:
                            field_attrs['type'] = 'time'
                        locals()[field_name] = TimeFilter(widget=forms.TimeInput(attrs=field_attrs))
                    else:
                        locals()[field_name] = CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs=field_attrs))

                class Meta:
                    model = self.model
                    fields = filterset_fields
               
                def __init__(self, *args, **kwargs):
                    """Initialize the FilterSet and set up HTMX attributes if needed."""
                    super().__init__(*args, **kwargs)
                    if use_htmx:
                        self.setup_htmx_attrs()
                        
            filterset_class = DynamicFilterSet

        if filterset_class is None:
            return None

        return filterset_class(
            self.request.GET,
            queryset=queryset,
            request=self.request,
        )

    def paginate_queryset(self, queryset, page_size):
        """
        Override paginate_queryset to reset to page 1 when filters are applied.
        """
        # If filters were applied, modify the GET request temporarily to force page 1
        original_GET = None
        if hasattr(self, '_reset_pagination') and self._reset_pagination:
            # Store original GET
            original_GET = self.request.GET
            # Create a copy we can modify
            modified_GET = self.request.GET.copy()
            # Set page to 1
            modified_GET['page'] = '1'
            # Replace with our modified version temporarily
            self.request.GET = modified_GET
            # Clean up flag
            delattr(self, '_reset_pagination')
        
        # Call parent implementation
        try:
            return super().paginate_queryset(queryset, page_size)
        finally:
            # Restore original GET if we modified it
            if original_GET is not None:
                self.request.GET = original_GET


    def _get_all_fields(self):
        fields = [field.name for field in self.model._meta.get_fields()]
            
        # Exclude reverse relations
        fields = [
            field.name for field in self.model._meta.get_fields()
            if not isinstance(field, ManyToOneRel)
        ]
        return fields

    def _get_all_editable_fields(self):
        """Gets all editable fields in model"""
        return [
            field.name 
            for field in self.model._meta.get_fields() 
            if hasattr(field, 'editable') and field.editable
        ]

    def _get_all_properties(self):
        return [name for name in dir(self.model)
                    if isinstance(getattr(self.model, name), property) and name != 'pk'
                ]
    
    def get_model_session_key(self):
        """Generate a unique key for this model within the nominopolitan session dict."""
        app_name = self.model._meta.app_label
        return f"{app_name}_{self.url_base}"

    def get_session_data(self) -> dict|None:
        """Retrieve the session data for this model from the nominopolitan session dict."""
        nominopolitan_data = self.request.session.get('nominopolitan', {})
        return nominopolitan_data.get(self.get_model_session_key(), None)

    def set_session_data_key(self, data: dict):
        """Update the session data for this model within the nominopolitan session dict."""
        nominopolitan_data = self.request.session.get('nominopolitan', {})
        model_key = self.get_model_session_key()
        
        if model_key not in nominopolitan_data:
            nominopolitan_data[model_key] = data
        else:
            # Update existing data
            nominopolitan_data[model_key].update(data)
        
        self.request.session['nominopolitan'] = nominopolitan_data
        return nominopolitan_data[model_key]

    def get_session_data_key(self, key: str):
        """Retrieve a specific key from the session data for this model."""
        session_data = self.get_session_data()
        if session_data:
            return session_data.get(key, None)
        return None

    def get_original_target(self):
        """
        Retrieve the original HTMX target from the session.

        This method is called in get_context_data() to provide the original target
        in the context for templates.

        Returns:
            str or None: The original HTMX target or None if not set
        """
        session_data = self.get_session_data()

        if not session_data:
            return None        
        return session_data.get('original_target', None)

    def get_use_htmx(self):
        """
        Determine if HTMX should be used.

        This method is called in multiple places, including get_context_data(),
        get_htmx_target(), and get_use_modal(), to check if HTMX functionality
        should be enabled.

        Returns:
            bool: True if HTMX should be used, False otherwise
        """
        return self.use_htmx is True

    def get_use_modal(self):
        """
        Determine if modal functionality should be used.

        This method is called in get_context_data() to set the 'use_modal' context
        variable for templates. It requires HTMX to be enabled.

        Returns:
            bool: True if modal should be used and HTMX is enabled, False otherwise
        """
        result = self.use_modal is True and self.get_use_htmx()
        return result
    
    def get_modal_id(self):
        """
        Get the ID for the modal element.

        This method is called in get_framework_styles() to set the modal attributes

        Returns:
            str: The modal ID with a '#' prefix
        """
        modal_id = self.modal_id or 'nominopolitanBaseModal'
        return f'#{modal_id}'
    
    def get_modal_target(self):
        """
        Get the target element ID for the modal content.

        This method is called in get_htmx_target() when use_modal is True to
        determine where to render the modal content.

        Returns:
            str: The modal target ID with a '#' prefix
        """
        modal_target = self.modal_target or 'nominopolitanModalContent'
        return f'#{modal_target}'
    
    def get_hx_trigger(self):
        """
        Get the HX-Trigger value for HTMX responses.

        This method is called in render_to_response() to set the HX-Trigger header
        for HTMX responses. It handles string, numeric, and dictionary values for
        the hx_trigger attribute.

        Returns:
            str or None: The HX-Trigger value as a string, or None if not applicable
        """
        if not self.get_use_htmx() or not self.hx_trigger:
            return None
            
        if isinstance(self.hx_trigger, (str, int, float)):
            return str(self.hx_trigger)
        elif isinstance(self.hx_trigger, dict):
            # Validate all keys are strings
            if not all(isinstance(k, str) for k in self.hx_trigger.keys()):
                raise TypeError("HX-Trigger dict keys must be strings")
            return json.dumps(self.hx_trigger)
        else:
            raise TypeError("hx_trigger must be either a string or dict with string keys")

    def get_htmx_target(self):
        """
        Determine the HTMX target for rendering responses.

        This method is called in get_context_data() to set the htmx_target context
        variable for templates. It handles different scenarios based on whether
        HTMX and modal functionality are enabled.

        Returns:
            str or None: The HTMX target as a string with '#' prefix, or None if not applicable
        """
        # only if using htmx
        if not self.get_use_htmx():
            htmx_target = None
        elif self.use_modal:
            htmx_target = self.get_modal_target()
        elif hasattr(self.request, 'htmx') and self.request.htmx.target:
            # return the target of the original list request
            htmx_target = self.get_original_target()
        else:
            htmx_target = self.default_htmx_target  # Default target for non-HTMX requests

        return htmx_target

    def get_use_crispy(self):
        """
        Determine if crispy forms should be used.

        This method is called in get_context_data() to set the 'use_crispy' context
        variable for templates. It checks if the crispy_forms app is installed and
        if the use_crispy attribute is explicitly set.

        Returns:
            bool: True if crispy forms should be used, False otherwise

        Note:
            - If use_crispy is explicitly set to True but crispy_forms is not installed,
              it logs a warning and returns False.
            - If use_crispy is not set, it returns True if crispy_forms is installed,
              False otherwise.
        """
        use_crispy_set = self.use_crispy is not None
        crispy_installed = "crispy_forms" in settings.INSTALLED_APPS

        if use_crispy_set:
            if self.use_crispy is True and not crispy_installed:
                log.warning("use_crispy is set to True, but crispy_forms is not installed. Forcing to False.")
                return False
            return self.use_crispy
        return crispy_installed

    @staticmethod
    def get_url(role, view_cls):
        """
        Generate a URL pattern for a specific role and view class.

        This method is used internally by the get_urls method to create individual URL patterns.

        Args:
            role (Role): The role for which to generate the URL.
            view_cls (class): The view class for which to generate the URL.

        Returns:
            path: A Django URL pattern for the specified role and view class.
        """
        return path(
            role.url_pattern(view_cls),
            view_cls.as_view(role=role),
            name=f"{view_cls.url_base}-{role.url_name_component}",
        )

    @classonlymethod
    def get_urls(cls, roles=None):
        """
        Generate a list of URL patterns for all roles or specified roles.

        This method is typically called from the urls.py file of a Django app to generate
        URL patterns for all CRUD views associated with a model.

        Args:
            roles (iterable, optional): An iterable of Role objects. If None, all roles are used.

        Returns:
            list: A list of URL patterns for the specified roles.
        """
        if roles is None:
            roles = iter(Role)
        return [NominopolitanMixin.get_url(role, cls) for role in roles]

    def reverse(self, role, view, object=None):
        """
        Override of neapolitan's reverse method.
        
        Generates a URL for a given role, view, and optional object.
        Handles namespaced and non-namespaced URLs.

        Args:
            role (Role): The role for which to generate the URL.
            view (View): The view class for which to generate the URL.
            object (Model, optional): The model instance for detail, update, and delete URLs.

        Returns:
            str: The generated URL.

        Raises:
            ValueError: If object is None for detail, update, and delete URLs.
        """
        url_name = (
            f"{view.namespace}:{view.url_base}-{role.url_name_component}"
            if view.namespace
            else f"{view.url_base}-{role.url_name_component}"
        )
        url_kwarg = view.lookup_url_kwarg or view.lookup_field

        match role:
            case Role.LIST | Role.CREATE:
                return reverse(url_name)
            case _:
                if object is None:
                    raise ValueError("Object required for detail, update, and delete URLs")
                return reverse(
                    url_name,
                    kwargs={url_kwarg: getattr(object, view.lookup_field)},
                )

    def maybe_reverse(self, view, object=None):
        """
        Override of neapolitan's maybe_reverse method.
        
        Attempts to reverse a URL, returning None if it fails.

        Args:
            view (View): The view class for which to generate the URL.
            object (Model, optional): The model instance for detail, update, and delete URLs.

        Returns:
            str or None: The generated URL if successful, None otherwise.
        """
        try:
            return self.reverse(view, object)
        except NoReverseMatch:
            return None
    

    def _apply_crispy_helper(self, form_class):
        """Helper method to apply crispy form settings to a form class."""
        if not self.get_use_crispy():
            return form_class
        
        # Create a new instance to check if it has a helper
        _temp_form = form_class()
        has_helper = hasattr(_temp_form, 'helper')
        
        if not has_helper:
            # log.debug(f"Adding FormHelper to {form_class.__name__} with form_tag=False and disable_csrf=True")
            old_init = form_class.__init__
            
            def new_init(self, *args, **kwargs):
                old_init(self, *args, **kwargs)
                self.helper = FormHelper()
                self.helper.form_tag = False
                self.helper.disable_csrf = True
            
            form_class.__init__ = new_init
        else:
            old_init = form_class.__init__
            
            def new_init(self, *args, **kwargs):
                old_init(self, *args, **kwargs)
                
                # Check if form_tag has been explicitly set to True
                if self.helper.form_tag is True:
                    # log.debug(f"Overriding form_tag=True to False in {self.__class__.__name__}")
                    self.helper.form_tag = False
                
                # Check if disable_csrf has been explicitly set to False
                if self.helper.disable_csrf is False:
                    # log.debug(f"Overriding disable_csrf=False to True in {self.__class__.__name__}")
                    self.helper.disable_csrf = True
            
            form_class.__init__ = new_init
        
        return form_class

    def get_form_class(self):
        """Override get_form_class to use form_fields for form generation."""

        # Use explicitly defined form class if provided
        if self.form_class is not None:
            return self._apply_crispy_helper(self.form_class)
        
        # Generate a default form class using form_fields
        if self.model is not None and self.form_fields:
            # Configure HTML5 input widgets for date/time fields
            widgets = {}
            for field in self.model._meta.get_fields():
                if field.name not in self.form_fields:
                    continue
                if isinstance(field, models.DateField):
                    widgets[field.name] = forms.DateInput(
                        attrs={'type': 'date', 'class': 'form-control'}
                    )
                elif isinstance(field, models.DateTimeField):
                    widgets[field.name] = forms.DateTimeInput(
                        attrs={'type': 'datetime-local', 'class': 'form-control'}
                    )
                elif isinstance(field, models.TimeField):
                    widgets[field.name] = forms.TimeInput(
                        attrs={'type': 'time', 'class': 'form-control'}
                    )

            # Create the form class with our configured widgets
            form_class = model_forms.modelform_factory(
                self.model,
                fields=self.form_fields,
                widgets=widgets
            )

            # Apply crispy forms if enabled
            if self.get_use_crispy():
                old_init = form_class.__init__

                def new_init(self, *args, **kwargs):
                    old_init(self, *args, **kwargs)
                    self.helper = FormHelper()
                    self.helper.form_tag = False
                    self.helper.disable_csrf = True

                form_class.__init__ = new_init

            return form_class

        msg = (
            "'%s' must either define 'form_class' or both 'model' and "
            "'form_fields', or override 'get_form_class()'"
        )
        raise ImproperlyConfigured(msg % self.__class__.__name__)

    def get_prefix(self):
        """
        Generate a prefix for URL names.

        This method is used in get_context_data to create namespaced URL names.

        Returns:
            str: A prefix string for URL names, including namespace if set.
        """
        return f"{self.namespace}:{self.url_base}" if self.namespace else self.url_base

    def safe_reverse(self, viewname, kwargs=None):
        """
        Safely attempt to reverse a URL, returning None if it fails.

        This method is used in get_context_data to generate URLs for various views.

        Args:
            viewname (str): The name of the view to reverse.
            kwargs (dict, optional): Additional keyword arguments for URL reversing.

        Returns:
            str or None: The reversed URL if successful, None otherwise.
        """
        try:
            return reverse(viewname, kwargs=kwargs)
        except NoReverseMatch:
            return None

    def get_template_names(self):
        """
        Determine the appropriate template names for the current view.

        This method is called by Django's template rendering system to find the correct template.
        It overrides the default behavior to include custom template paths.

        Returns:
            list: A list of template names to be used for rendering.

        Raises:
            ImproperlyConfigured: If neither template_name nor model and template_name_suffix are defined.
        """
        if self.template_name is not None:
            return [self.template_name]

        if self.model is not None and self.template_name_suffix is not None:
            names = [
                f"{self.model._meta.app_label}/"
                f"{self.model._meta.object_name.lower()}"
                f"{self.template_name_suffix}.html",
                f"{self.templates_path}/object{self.template_name_suffix}.html",
            ]
            return names
        msg = (
            "'%s' must either define 'template_name' or 'model' and "
            "'template_name_suffix', or override 'get_template_names()'"
        )
        raise ImproperlyConfigured(msg % self.__class__.__name__)

    def get_queryset(self):
        """
        Get the queryset for the view, applying sorting if specified.
        Always includes a secondary sort by primary key for stable pagination.
        """
        queryset = super().get_queryset()
        sort_param = self.request.GET.get('sort')
        
        if sort_param:
            # Handle descending sort (prefixed with '-')
            descending = sort_param.startswith('-')
            field_name = sort_param[1:] if descending else sort_param
            
            # Get all valid field names and properties
            valid_fields = {f.name: f.name for f in self.model._meta.fields}
            # Add any properties that are sortable
            valid_fields.update({p: p for p in getattr(self, 'properties', [])})
            
            # Try to match the sort parameter to a valid field
            # First try exact match
            if field_name in valid_fields:
                sort_field = valid_fields[field_name]
            else:
                # Try case-insensitive match
                matches = {k.lower(): v for k, v in valid_fields.items()}
                sort_field = matches.get(field_name.lower())
                
            if sort_field:
                # Re-add the minus sign if it was descending
                if descending:
                    sort_field = f'-{sort_field}'
                    # Add secondary sort by -pk for descending
                    queryset = queryset.order_by(sort_field, '-pk')
                else:
                    # Add secondary sort by pk for ascending
                    queryset = queryset.order_by(sort_field, 'pk')
        else:
            # If no sort specified, sort by pk as default
            queryset = queryset.order_by('pk')
            
        return queryset

    def get_context_data(self, **kwargs):
        """
        Prepare and return the context data for template rendering.

        This method extends the base context with additional data specific to the view,
        including URLs for CRUD operations, HTMX-related settings, and related object information.

        Args:
            **kwargs: Additional keyword arguments passed to the method.

        Returns:
            dict: The context dictionary containing all the data for template rendering.
        """
        context = super().get_context_data(**kwargs)

        # Generate and add URLs for create, update, and delete operations
        view_name = f"{self.get_prefix()}-{Role.CREATE.value}"
        context["create_view_url"] = self.safe_reverse(view_name)

        if self.object:
            update_view_name = f"{self.get_prefix()}-{Role.UPDATE.value}"
            context["update_view_url"] = self.safe_reverse(update_view_name, kwargs={"pk": self.object.pk})
            delete_view_name = f"{self.get_prefix()}-{Role.DELETE.value}"
            context["delete_view_url"] = self.safe_reverse(delete_view_name, kwargs={"pk": self.object.pk})

        # Set header title for partial updates
        context["header_title"] = f"{self.url_base.title()}-{self.role.value.title()}"

        # Add template and feature configuration
        context["base_template_path"] = self.base_template_path
        context['framework_template_path'] = self.templates_path
        context["use_crispy"] = self.get_use_crispy()
        context["use_htmx"] = self.get_use_htmx()
        context['use_modal'] = self.get_use_modal()
        context["original_target"] = self.get_original_target()

        # Set table styling parameters
        context['table_pixel_height_other_page_elements'] = self.get_table_pixel_height_other_page_elements()
        context['get_table_max_height'] = self.get_table_max_height()
        context['table_max_col_width'] = f"{self.get_table_max_col_width()}"
        context['table_header_min_wrap_width'] = f"{self.get_table_header_min_wrap_width()}"
        context['table_classes'] = self.get_table_classes()

        # Add HTMX-specific context if enabled
        if self.get_use_htmx():
            context["htmx_target"] = self.get_htmx_target()

        # Add related fields information for list view
        if self.role == Role.LIST and hasattr(self, "object_list"):
            context["related_fields"] = {
                field.name: field.related_model._meta.verbose_name
                for field in self.model._meta.fields
                if field.is_relation
            }

        # Add related objects information for detail view
        if self.role == Role.DETAIL and hasattr(self, "object"):
            context["related_objects"] = {
                field.name: str(getattr(self.object, field.name))
                for field in self.model._meta.fields
                if field.is_relation and getattr(self.object, field.name)
            }

        # Add sort parameter to context
        context['sort'] = self.request.GET.get('sort', '')

        return context

    def get_success_url(self):
        """
        Determine the URL to redirect to after a successful form submission.

        This method constructs the appropriate success URL based on the current role
        (CREATE, UPDATE, DELETE) and the view's configuration. It uses the namespace
        and url_base attributes to generate the correct URL patterns.

        Returns:
            str: The URL to redirect to after a successful form submission.

        Raises:
            AssertionError: If the model is not defined for this view.
        """
        assert self.model is not None, (
            "'%s' must define 'model' or override 'get_success_url()'"
            % self.__class__.__name__
        )

        url_name = (
            f"{self.namespace}:{self.url_base}-list"
            if self.namespace
            else f"{self.url_base}-list"
        )

        if self.role in (Role.DELETE, Role.UPDATE, Role.CREATE):
            success_url = reverse(url_name)
        else:
            detail_url = (
                f"{self.namespace}:{self.url_base}-detail"
                if self.namespace
                else f"{self.url_base}-detail"
            )
            success_url = reverse(detail_url, kwargs={"pk": self.object.pk})

        return success_url

    def render_to_response(self, context={}):
        """
        Render the response, handling both HTMX and regular requests.
        """
        template_names = self.get_template_names()
        
        # Try the first template (app-specific), fall back to second (generic)
        from django.template.loader import get_template
        from django.template.exceptions import TemplateDoesNotExist

        try:
            # try to use overriden template if it exists
            template_name = template_names[0]
            # this call check if valid template
            template = get_template(template_name)
        except TemplateDoesNotExist:
            # log.debug(f"Template {template_name} not found, falling back to {template_names[1]}")
            template_name = template_names[1]
            template = get_template(template_name)
            # log.debug(f"Found template {template_name} at {template.origin.name}")
        except Exception as e:
            log.error(f"Unexpected error checking template {template_name}: {str(e)}")
            template_name = template_names[1]
        
        # log.debug(f"Rendering template_name: {template_name}")

        # add to session here (template name may change later)
        self.set_session_data_key({'original_template': template_name})

        # log.debug(f"context: \n{json.dumps(context, indent=4, default=str)}")

        if self.request.htmx:
            if self.role == Role.LIST:
                # this is the list view
                if not self.get_original_target():
                    self.set_session_data_key({'original_target': f"#{self.request.htmx.target}"})

            if self.request.headers.get('X-Filter-Sort-Request'):
                template_name=f"{template_name}#filtered_results"
            else:
                template_name=f"{template_name}#nm_content"

            response = render(
                request=self.request,
                template_name=f"{template_name}",
                context=context,
            )
            response['HX-Trigger'] = self.get_hx_trigger()
            return response
        else:
            return TemplateResponse(
                request=self.request, template=template_name, context=context
            )
