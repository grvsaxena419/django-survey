from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from .survey import Survey

user_model = get_user_model()


class Response(models.Model):

    """
    A Response object is a collection of questions and answers with a
    unique interview uuid.
    """

    created = models.DateTimeField(_("Creation date"), auto_now_add=True)
    updated = models.DateTimeField(_("Update date"), auto_now=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name=_("Survey"), related_name="responses")
    user = models.ForeignKey(user_model, on_delete=models.SET_NULL, verbose_name=_("User"), null=True, blank=True)
    interview_uuid = models.CharField(_("Interview unique identifier"), max_length=36)
    subscriber_uuid = models.CharField(_("Subscriber unique identifier"), max_length=36, null=True, blank=True)

    class Meta:
        verbose_name = _("Set of answers to surveys")
        verbose_name_plural = _("Sets of answers to surveys")

    def __str__(self):
        msg = f"Response to {self.survey} by {self.user}"
        msg += f" on {self.created}"
        return msg
