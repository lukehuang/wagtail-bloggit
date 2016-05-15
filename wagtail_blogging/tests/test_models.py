# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from wagtail_blogging.models import BlogPostPage


class BlogPostPageTest(TestCase):
    """Tests for the BlogPostPage model."""
    def test_autofill_post_date(self):
        """The post date should be filled automatically upon construction of a model."""
        fixed_date = timezone.now()
        with freeze_time(fixed_date):
            post = BlogPostPage()
            assert post.post_date == fixed_date
