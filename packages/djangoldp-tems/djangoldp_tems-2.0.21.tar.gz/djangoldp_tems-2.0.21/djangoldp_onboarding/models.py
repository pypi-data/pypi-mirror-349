from django.db import models
from djangoldp_tems.models.__base_model import baseTEMSModel
from djangoldp.permissions import LDPBasePermission,CreateOnly, AuthenticatedOnly, ReadAndCreate, OwnerPermissions
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.core.exceptions import ValidationError
#Email imports
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context, Template

from django.utils.html import strip_tags
import re

def get_default_email_sender_djangoldp_instance():
    '''
    :return: the configured email host if it can find one, or None
    '''
    email_from = (getattr(settings, 'DEFAULT_FROM_EMAIL', False) or getattr(settings, 'EMAIL_HOST_USER', False))
    if not email_from:
        jabber_host = getattr(settings, 'JABBER_DEFAULT_HOST', False)

        if jabber_host:
            return "noreply@" + jabber_host
        return None

    return email_from

class ReadCreateAndChange(LDPBasePermission):
  permissions = {'view', 'add', 'change'}


class RegisterParticipant(baseTEMSModel):
    status = models.CharField(max_length=32,default="pending", choices=(('pending', 'Pending'),('approved', 'Approve'), ('rejected', 'Reject')), verbose_name="Validation Status")
    firstname = models.CharField(max_length=255,verbose_name="first name")
    lastname = models.CharField(max_length=255,verbose_name="last name")
    email = models.EmailField(verbose_name="email")
    organisation = models.CharField(max_length=255,verbose_name="organisation name")
    organisationAddress = models.CharField(max_length=255,
        verbose_name="organisation Address", null=True, blank=True
    )
    organisationRegistrationNumber = models.CharField(max_length=255,
        verbose_name="organisation Registration Number", null=True, blank=True
    )
    optin_register = models.BooleanField(
        verbose_name="Accepts Terms and Conditions",
        default=False,
    )

    class Meta(baseTEMSModel.Meta):
        serializer_fields = baseTEMSModel.Meta.serializer_fields + [
            "status",
            "firstname",
            "lastname",
            "email",
            "organisation",
            "organisationAddress",
            "organisationRegistrationNumber",
            "optin_register",
        ]
        verbose_name = "RegisterParticipant"
        verbose_name_plural = "RegisterParticipants"
        rdf_type = ["tems:RegisterParticipant"]
        permission_classes = [(AuthenticatedOnly&ReadAndCreate)|CreateOnly]
        
    def __str__(self):
        return self.organisation
        
    def save(self, *args, **kwargs):
      if self._state.adding and not self.optin_register:
          raise ValidationError("You must accept the Terms and Conditions.")
      super().save(*args, **kwargs)

    
      
    

@receiver(post_save, sender=RegisterParticipant)
def send_organisation_confirmation_email(sender, instance, created, **kwargs):
  from_mail = get_default_email_sender_djangoldp_instance()
  if created:
    ### Notify the admins of the new request
    admin_list = getattr(settings, 'TEMS_ADMIN_MAILS', False)
    if admin_list:
      email_subject = "A new organisation is pending approval"

      html_template = get_template('email/notify_admin_creation.html')

      d = {"emailSender": {
          "base_url": settings.BASE_URL,
          "organisation_name": instance.organisation,
        }
      }

      html_content = html_template.render(d['emailSender'])
      html_without_css = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL)
      text_content = strip_tags(html_without_css)

      for admin in admin_list:
        email = EmailMultiAlternatives( 
            subject=email_subject,
            body=text_content,
            from_email=from_mail,
            to=[admin],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
  
  if not created:
    ### Notify the requester
    if instance.status == "rejected" or instance.status == "approved":
      if instance.status == 'approved':
        email_subject = f"Your application to TEMS with the organization {instance.organisation} has been accepted"
        html_template = get_template('email/notify_requester_approve.html')
      else:
        email_subject = f"Your organisation {instance.organisation} was {instance.status}"
        html_template = get_template('email/notify_requester_rejected.html')

      d = {"emailSender": {
          "base_url": settings.BASE_URL,
          "fullname": f"{instance.firstname} {instance.lastname}",
          "email": f"{instance.email}",
        }
      }

      html_content = html_template.render(d['emailSender'])
      html_without_css = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL)
      text_content = strip_tags(html_without_css)

      email = EmailMultiAlternatives( 
          subject=email_subject,
          body=text_content,
          from_email=from_mail,
          to=[instance.email],
      )
      email.attach_alternative(html_content, "text/html")
      email.send()

  