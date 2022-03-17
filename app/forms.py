from django import forms

from app.models import Person, City


class PersonCreationForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # mijoz tomonidan noto'g'ri kiritilgan ma'lumotlar; e'tibor bermang va bo'sh City so'rovlar to'plamiga qayting
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')