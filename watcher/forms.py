from django import forms
from .models import Room, FoodInfo

class RoomForm(forms.ModelForm):

    contact = forms.BooleanField(help_text="가맹점은 체크하세요",required=False)
    image = forms.ImageField(label='Image',required=False)
    class Meta:
        model = Room
        fields = ('name', 'address','image','contact','latitude', 'longitude', 'notice', 'spec')


class FoodForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = FoodInfo
        fields = ('foodName','rank','image',)



