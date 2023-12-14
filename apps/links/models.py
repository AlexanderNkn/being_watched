from django.db import models
from django.utils.translation import gettext_lazy as _


class VisitedLink(models.Model):
    visited_at = models.DateTimeField(
        verbose_name=_('Visited at'),
        db_index=True,
    )
    link = models.URLField(
        verbose_name=_('Visited link'),
    )
    domain = models.URLField(
        verbose_name=_('Visited domain'),
    )
