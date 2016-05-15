# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import logging
import sys

from django.core.management import BaseCommand
from wagtail.wagtailcore.models import Page

from wagtail_bloggit.importers.wordpress import WordPressImporter

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Imports blog posts from a WordPress XML dump.'

    def add_arguments(self, parser):
        parser.add_argument('filename', help='Can be a local file path or an URL.')
        parser.add_argument('--parent_id', required=False, help='ID of parent page to attach imported posts to. If '
                                                                'omitted, a new page will be made.')

    def handle(self, *args, **options):
        if options['parent_id']:
            try:
                parent_page = Page.objects.get(id=options['parent_id'])
            except Page.DoesNotExist:
                logger.error('Parent page #{} not found.'.format(options['parent_id']))
                sys.exit(1)
        else:
            parent_page = Page.add_root(title='Blog')

        importer = WordPressImporter(options['filename'])
        for post in importer.generate_posts():
            parent_page.add_child(instance=post)
