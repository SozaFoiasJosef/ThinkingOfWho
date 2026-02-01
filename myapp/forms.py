from django import forms
from .models import Room, Image
 
class RoomForm(forms.ModelForm):
    name = forms.CharField(
        label='',
        max_length=63,
        widget=forms.TextInput(attrs={'placeholder': 'Game Name'})
    )

    isSearchable = forms.BooleanField(
        label='Searchable',
        required=False,
        initial=True,
    )

    class Meta:
        model = Room
        fields = ('name', 'isSearchable')

class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='',
        widget=forms.FileInput(attrs={'placeholder': 'Image'})
    )  
    title = forms.CharField(
        label='',
        max_length=65,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Image Title'})
    )

    class Meta:
        model = Image
        fields = ('image', 'title')