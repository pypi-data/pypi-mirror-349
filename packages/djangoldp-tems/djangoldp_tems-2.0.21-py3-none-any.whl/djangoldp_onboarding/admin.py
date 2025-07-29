from django.contrib import admin

from djangoldp_onboarding.models import *
from djangoldp_tems.admin import TemsModelAdmin

admin.site.register(RegisterParticipant, TemsModelAdmin)
