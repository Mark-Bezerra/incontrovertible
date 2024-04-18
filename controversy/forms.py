from django import forms
from .models import Controversy, Data_Point

DATA_SETS = (
    ('data','DATA'),
    ('opinion','OPINION'),
    ('advice','ADVICE'),
)

class ControversyForm(forms.Form):
    class Meta:
        model = Controversy
        fields = ["name", "description", "post"]

class Data_PointForm(forms.ModelForm):
    class Meta:
        model = Data_Point
        fields = ["controversy", "name", "description", "url", "data_set", "boolean"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["controversy"].disabled = True