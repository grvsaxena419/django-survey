from datetime import timedelta, datetime

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


def in_duration_day():
    return now() + timedelta(days=settings.DEFAULT_SURVEY_PUBLISHING_DURATION)


class SurveyStatus:
    DRAFT = 1
    PUBLISHED = 2
    EXPIRED = 3

    ICONS = {
        PUBLISHED: 'fas fa-check',
        EXPIRED: 'far fa-calendar',
        DRAFT: 'fas fa-pencil-alt'
    }

    LABELS = {
        DRAFT: _('Draft'),
        PUBLISHED: _('Published'),
        EXPIRED: _('Expired'),
    }

    CHOICES = tuple(LABELS.items())


class Survey(models.Model):
    ALL_IN_ONE_PAGE = 0
    BY_QUESTION = 1
    BY_CATEGORY = 2

    DISPLAY_METHOD_CHOICES = [
        (BY_QUESTION, _("By question")),
        (BY_CATEGORY, _("By category")),
        (ALL_IN_ONE_PAGE, _("All in one page")),
    ]

    name = models.CharField(_("Name"), max_length=400)
    description = models.TextField(_("Description"))
    need_logged_user = models.BooleanField(_("Only authenticated users can see it and answer it"))
    editable_answers = models.BooleanField(_("Users can edit their answers afterwards"), default=True)
    display_method = models.SmallIntegerField(
        _("Display method"), choices=DISPLAY_METHOD_CHOICES, default=ALL_IN_ONE_PAGE
    )
    template = models.CharField(_("Template"), max_length=255, null=True, blank=True)
    expire_date = models.DateField(_("Survey will not be visible after this date"), blank=True, null=False,
                                   default=in_duration_day)
    redirect_url = models.URLField(_("Redirect URL"), blank=True)
    # non-user updatable fields
    tenant_id = models.PositiveIntegerField(_('tenant_id'), blank=True, null=True)
    created_by_user = models.PositiveIntegerField(_('user id'), blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        _('status'),
        choices=SurveyStatus.CHOICES,
        default=SurveyStatus.DRAFT,
        db_index=True
    )
    create_date = models.DateTimeField(_('Create date'), auto_now_add=True)
    update_date = models.DateTimeField(_('Update date'), default=datetime.now)

    class Meta:
        verbose_name = _("survey")
        verbose_name_plural = _("surveys")

    def __str__(self):
        return str(self.name)

    @property
    def safe_name(self):
        return self.name.replace(" ", "_").encode("utf-8").decode("ISO-8859-1")

    def latest_answer_date(self):
        """Return the latest answer date.

        Return None is there is no response."""
        min_ = None
        for response in self.responses.all():
            if min_ is None or min_ < response.updated:
                min_ = response.updated
        return min_

    def get_absolute_url(self):
        return reverse("survey-detail", kwargs={"id": self.pk})

    def non_empty_categories(self):
        return [x for x in list(self.categories.order_by("order", "id")) if x.questions.count() > 0]

    def is_all_in_one_page(self):
        return self.display_method == self.ALL_IN_ONE_PAGE

    def is_expired(self):
        if not self.expire_date:
            return True
        return datetime.now().date() > self.expire_date

    def get_all_questions(self):
        return self.questions.all()
