# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.models import Image
from wagtail.wagtailsearch import index


class BlogPostPage(Page):
    """Structure for blog articles."""
    post_date = models.DateTimeField()
    post_body = StreamField([
        ('text', blocks.RichTextBlock(icon='edit')),
        ('image', ImageChooserBlock(icon='image')),
    ])
    primary_visual = models.ForeignKey(Image, help_text=ugettext_lazy('Can be shown on overview pages or in feeds.'),
                                       null=True, blank=True, on_delete=models.SET_NULL)

    search_fields = Page.search_fields + (
        index.SearchField('post_body'),
        index.SearchField('post_date'),
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('post_body'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('post_date'),
    ]

    def __init__(self, *args, **kwargs):
        super(BlogPostPage, self).__init__(*args, **kwargs)

        # Prefill post date so that it is set automatically upon creation but can still be overridden by the user
        if self.post_date is None:
            self.post_date = timezone.now()
