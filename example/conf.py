from __future__ import annotations

import os
import re
from typing import TYPE_CHECKING

coverage_statistics_to_report = coverage_statistics_to_stdout = True
exclude_patterns = ['_build']

project = 'Astronomy Guide'
copyright = '2025, Astronomy Guys'
language = 'en'
release = version = "1.0.0"
show_authors = True
nitpicky = True
show_warning_types = True

html_theme = 'sphinx_corpo_theme'
modindex_common_prefix = ['sphinx.']
html_static_path = ['_static']
html_copy_source = False
html_last_updated_fmt = '%Y-%m-%d'

html_baseurl = 'http://localhost:8000/'
html_theme_options = {
    'template_overrides' : {
        'blog/' : 'blog.html',
    },
    'show_child_topics': True,
    'show_parent_topic': True,
    'toc_extra_links': [
        {
            'title': 'Astronomy in Wikipedia',
            'url': 'https://en.wikipedia.org/wiki/Astronomy'
        },
        {
            'title': 'NASA website',
            'url': 'https://www.nasa.gov/'
        }
    ],
    'footer_statement' : """This example documentation uses some content from Wikipedia. Wikipedia is hosted by the Wikimedia Foundation, a non-profit organization that also hosts a range of other projects. Text is available under the Creative Commons Attribution-ShareAlike 4.0 License; additional terms may apply.""",
    'show_menu_bar': True,
    'menu_bar_items': [
        {'title': 'Documentation', 'docname': 'docs/index'},
        {'title': 'Blog', 'docname': 'blog/index'}
    ],
}

gettext_compact = False

def setup(app: Sphinx) -> None:
    pass

