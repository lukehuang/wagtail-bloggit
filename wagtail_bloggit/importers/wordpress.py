# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from time import mktime

import feedparser
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify

from wagtail_bloggit.models import BlogPostPage


class WordPressImporter(object):
    """Given a file-like object (URL, file, stream or string), attempts to convert this data into blog posts."""
    def __init__(self, url_file_stream_or_string):
        self.url_file_stream_or_string = url_file_stream_or_string
        self._exceptions = []
        self._total_imported = 0

    def get_posts(self):
        """
        Attempt to extract blog posts for the XML file one by one. Returns all posts at once. For the generator version,
        see `generate_posts`.
        :return List of successfully imported posts.
        :rtype BlogPostPage[]
        """
        return [post for post in self.generate_posts()]

    def generate_posts(self):
        """
        Generator that will attempt to extract blog posts from the XML file one by one.
        """
        self._exceptions = []
        self._total_imported = 0
        parse_dict = feedparser.parse(self.url_file_stream_or_string)

        for item in parse_dict['items']:
            try:
                post_body = ''
                if 'content' in item and len(item['content']) > 0:
                    post_body = item['content'][0].value

                post_date = timezone.now()
                if 'published_parsed' in item:
                    post_date = datetime.fromtimestamp(mktime(item['published_parsed']))

                post = BlogPostPage(
                    title=item['title'],
                    slug=item.get('wp_post_name', slugify(item['title'])),
                    post_date=post_date,
                    post_body=post_body,
                )
                self._total_imported += 1
                yield post
            except Exception as e:
                self._exceptions.append(e)

    def total_imported(self):
        """
        :returns: Total number of successfully parsed posts.
        """
        return self._total_imported

    def total_detected(self):
        """
        :returns: Total number of posts that were detected in the XML dump, including the failed imports.
        """
        return self._total_imported + len(self._exceptions)
