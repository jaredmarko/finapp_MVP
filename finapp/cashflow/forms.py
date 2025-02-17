from django import forms
from .models import TransactionFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = TransactionFile
        fields = ['file']

