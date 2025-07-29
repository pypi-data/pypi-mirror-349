from django import forms
from django.utils.translation import gettext_lazy as _

from .models import RegisterParticipant

class ParticipantRegistrationForm(forms.ModelForm):
    class Meta:
        model = RegisterParticipant
        fields = [
            "firstname",
            "lastname",
            "email",
            "organisation",
            "organisationAddress",
            "organisationRegistrationNumber",
            "optin_register",
        ]
        widgets = {
            "firstname": forms.TextInput(
                attrs={
                    "placeholder": _("Enter your first name"),
                }
            ),
            "lastname": forms.TextInput(
                attrs={
                    "placeholder": _("Enter your last name"),
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": _("Enter your email"),
                }
            ),
            "organisation": forms.TextInput(
                attrs={
                    "placeholder": _("Enter your organisation"),
                }
            ),
            "organisationAddress": forms.TextInput(
                attrs={
                    "placeholder": _("Enter your organisation address"),
                }
            ),
            "organisationRegistrationNumber": forms.TextInput(
                attrs={
                    "placeholder": _("Enter your organisation registration number"),
                }
            ),
            "optin_register": forms.CheckboxInput(
              attrs={
                "required":("true"),
              }
            ),
        }
