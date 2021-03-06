wagtail-bloggit
================

**Update**: A GitHub user recommended that I check out [puput](https://github.com/APSL/puput), which already does most of the things I wanted to achieve with this project. Since I don't have any ambition to reinvent the wheel, I've decided to abandon this repository.

[![Build Status](https://travis-ci.org/pieterdd/wagtail-bloggit.svg?branch=master)](https://travis-ci.org/pieterdd/wagtail-bloggit)

[Wagtail](https://www.wagtail.io/) is a convenient way to build CMS-based sites on Django, but it lacks built-in support for WordPress-like blogging. This library aims to address that.

- A new type of page is added to the admin: blog posts.
- The `import_wordpress_posts` command will import exported WordPress content into a Wagtail site.

The `demosite` folder contains a boilerplate Wagtail instance. This instance is simply a dependency for the test suite and is excluded from install.
