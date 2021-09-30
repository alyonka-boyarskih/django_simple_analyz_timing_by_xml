import os

from bootstrap_datepicker_plus import DatePickerInput

from django import forms
from django.core.exceptions import ValidationError
from django.forms.forms import Form
from django.utils.translation import gettext_lazy as _

from core.utils import get_files

FILES_CHOICES = [(os.path.join("core/test_xml_files/", file), file) for file in get_files(path="core/test_xml_files/")]


class UploadFileForm(Form):

    file_choice = forms.ChoiceField(initial='Выберите файл из списка',
                             choices=FILES_CHOICES,
                             widget=forms.Select(),)
    date_start = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=DatePickerInput(format='%d-%m-%Y')
    )
    date_end = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=DatePickerInput(format='%d-%m-%Y')
    )

    @staticmethod
    def validate_dates(date_start, date_end):
        if not date_start and not date_end:
            return

        if date_start > date_end:
            raise ValidationError(_("Дата начальная должна быть меньше даты конечной"))

    def clean(self):
        cleaned_data = super().clean()
        date_start = cleaned_data.get("date_start")
        date_end = cleaned_data.get("date_end")

        self.validate_dates(date_start, date_end)

        return self.cleaned_data
