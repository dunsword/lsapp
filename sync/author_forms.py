__author__ = 'paul'

from django import forms
from models import source_author
class AuthorForm(forms.ModelForm):
    class Meta:
            model=source_author