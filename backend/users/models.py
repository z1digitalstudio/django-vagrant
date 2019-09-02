# -*- coding: utf-8 -*-
import os
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from users.managers import UserManager


def get_slug_for_session(instance):
    return instance.get_full_name() or 'Anonymous'


def upload_to_avatars(instance, filename):
    return os.path.join('avatars', str(instance.id), filename)


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    first_name = models.CharField(
        verbose_name=_('first name'),
        max_length=30,
    )

    last_name = models.CharField(
        verbose_name=_('last name'),
        max_length=30,
    )

    email = models.EmailField(
        verbose_name=_('email address'),
        null=True,
        unique=True
    )

    email_confirmed = models.BooleanField(
        verbose_name=_('email confirmed'),
        default=False,
    )

    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=True,
        help_text=_('Designates whether the user '
                    'can log into this admin site.')
    )

    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    )

    date_joined = models.DateTimeField(
        verbose_name=_('date joined'),
        default=timezone.now
    )

    location = models.CharField(
        verbose_name=_('location'),
        max_length=255,
        blank=True
    )

    company_name = models.CharField(
        verbose_name=_('company name'),
        max_length=255,
        blank=True
    )

    avatar = models.ImageField(
        verbose_name=_(u'avatar'),
        upload_to=upload_to_avatars,
        max_length=4000,
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    class Meta:
        verbose_name = _(u'User')
        verbose_name_plural = _(u'Users')
