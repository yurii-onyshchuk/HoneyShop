from django.forms.widgets import TextInput


class CityAutocompleteWidget(TextInput):
    template_name = 'checkout/widgets/city_input_widget.html'
