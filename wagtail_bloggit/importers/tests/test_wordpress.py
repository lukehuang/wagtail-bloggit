# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import os
from contextlib import contextmanager

from django.core.management import call_command
from django.test import TestCase
from wagtail.wagtailcore.models import Page

from wagtail_bloggit.importers.wordpress import WordPressImporter
from wagtail_bloggit.models import BlogPostPage


def compose_datafile_path(filename):
    """Returns absolute path to a test file in the data directory."""
    return os.path.join(os.path.dirname(__file__), 'data/{}'.format(filename))


class WordPressImporterCommandTest(TestCase):
    """Tests for the management command to import WordPress posts."""
    def test_bad_path(self):
        """Bad path shouldn't crash the command and shouldn't lead to new imports."""
        call_command('import_from_wordpress', '/random_nonexistent_file')

        # A blog page should have been added to the predefined pages (root and homepage), but no posts should have
        # been imported.
        assert Page.objects.count() == 3
        assert BlogPostPage.objects.count() == 0

    def test_existing_blog_parent(self):
        """Appending items to an existing parent post shouldn't lead to a new parent being created."""
        blog_parent = Page.objects.get(title='Root').add_child(title='The blog')
        call_command('import_from_wordpress', compose_datafile_path('wordpress_no_posts.xml'), parent_id=blog_parent.id)

        # No increase in the number of Pages expected!
        assert Page.objects.count() == 3

    def test_valid_file(self):
        """Test import with a valid non-empty file."""
        call_command('import_from_wordpress', compose_datafile_path('wordpress_rich_html_item.xml'))

        # A blog page should have been added to the predefined pages. There is one imported post that should show up in
        # the Page query as well as the BlogPostPage query.
        assert Page.objects.count() == 4
        assert Page.objects.filter(title='Blog').exists() is True

        # A post should have been imported
        assert BlogPostPage.objects.count() == 1
        assert BlogPostPage.objects.get().title == 'This is my test post'


class WordPressImporterTest(TestCase):
    """Tests for the WordPressImporter class."""
    @contextmanager
    def open_test_file(self, filename):
        """Context manager that opens a test file from the data directory."""
        with open(compose_datafile_path(filename)) as handle:
            yield handle

    def test_no_items(self):
        """Attempt to parse a file without any blog posts."""
        with self.open_test_file('wordpress_no_posts.xml') as handle:
            importer = WordPressImporter(handle)
            assert importer.get_posts() == []
            assert importer.total_detected() == 0
            assert importer.total_detected() == 0

    def test_rich_html_item(self):
        """Attempt to parse a file with one post containing various HTML tags."""
        with self.open_test_file('wordpress_rich_html_item.xml') as handle:
            importer = WordPressImporter(handle)

            posts = importer.get_posts()
            assert len(posts) == 1
            assert importer.total_detected() == 1
            assert importer.total_detected() == 1

            post = posts[0]
            assert post.title == 'This is my test post'
            assert '<p>Lorem ipsum dolor sit amet, consectetur adipiscing ëlit.' in post.post_body.raw_text
