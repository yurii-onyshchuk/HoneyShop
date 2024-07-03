from django.forms.widgets import TextInput


class CityAutocompleteWidget(TextInput):
    template_name = 'external_api_services/widgets/city_input_widget.html'


class DepartmentAutocompleteWidget(TextInput):
    template_name = 'external_api_services/widgets/department_input_widget.html'
