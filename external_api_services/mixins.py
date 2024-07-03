from accounts.models import Address
from external_api_services.services.nova_poshta_api_service import get_city_info


class CityChooseMixin:
    def get_form(self, form_class=None):
        """Get an instance of the form and add the 'city_id' as attribute to the city field."""
        form = super().get_form(form_class)
        try:
            city_info = get_city_info(form.initial['city'])
            if city_info:
                city_ref = city_info['data'][0]['Addresses'][0]['Ref']
                delivery_city_ref = city_info['data'][0]['Addresses'][0]['DeliveryCity']
                form.fields['city'].widget.attrs.update({'data-city-ref': city_ref})
                form.fields['city'].widget.attrs.update({'data-delivery-city-ref': delivery_city_ref})
            else:
                form.initial['city'] = ''
        except Address.DoesNotExist:
            pass
        finally:
            return form
