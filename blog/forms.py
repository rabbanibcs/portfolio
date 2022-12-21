from django import forms
from .models import Post
from ckeditor.widgets import CKEditorWidget


category=[("wordpress","Wordpress"),("html","HTML"),
        ("photography","Photography"),("ui","UI"),
        ("mockups","Mockups"),("branding","Branding")]

class CraetePostForm(forms.Form):
    title=forms.CharField()
    category=forms.ChoiceField(choices=category)
    content=forms.CharField(widget=CKEditorWidget())
    image=forms.ImageField()


    title.widget.attrs.update({'class': 'full-width'})
    category.widget.attrs.update({'class': 'full-width'})
    
        
        