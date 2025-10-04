from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective
from sphinx.util.osutil import relpath
from sphinx.util import logging
from .util import deduce_docname
from markupsafe import escape as markup_escape
from datetime import datetime
from gettext import gettext as __
from sphinx.util.console import colorize
import math
#from markupsafe import striptags  as jinja_striptags

logger = logging.getLogger(__name__)

class BlogPosts(SphinxDirective):
    has_content = True
    option_spec = {
        'page_size': int,
    }

    def run(self):
        node = BlogPostsNode()
        node['entries'] = self.content
        node['page_size'] = int(self.options.get('page_size', 8))
        if node['page_size'] < 1:
            node['page_size'] = 1
        return [node]

from docutils import nodes

class BlogPostsNode(nodes.General, nodes.Element):
    pass

# TODO add option to scan the index directory for blog posts

def _visit_custom_toc_node_html(self, node):
    env = self.builder.env

    self.body.append('<div class="blogposts">\n')
    count = 0
    pages = 0
    for entry in node['entries']:
        entry = entry.strip()
        if len(entry) == 0:
            continue
        docname = deduce_docname(entry, self.builder.current_docname)
        if docname and docname in env.found_docs:
            title = markup_escape(env.titles[docname].astext())
            url = self.builder.get_relative_uri(self.builder.current_docname, docname)
            metadata = env.metadata[docname]
            description = markup_escape(metadata['description']) if 'description' in metadata else ''

            try:
                last_updated = markup_escape(metadata['last_updated']) if 'last_updated' in metadata else None
                if last_updated:
                    temp = datetime.fromisoformat(last_updated)
                    format = self.config.html_last_updated_fmt
                    if not format:
                        format = '%Y-%m-%d'
                    last_updated = temp.strftime(format)
            except ValueError:
                last_updated = None
                logger.warning(f"{colorize('darkgreen',docname)} has invalid ISO-8601 date")

            if count == 0:
                pages += 1
                self.body.append(f'<div class="page" style="{ 'display:none' if pages > 1 else ''}" data-page="{pages}"><ul>\n')

            self.body.append(f'<li><a href="{url}"><div class="card"><h2 class="title">{title}</h2>\n')
            if last_updated:
                self.body.append(f'<p class="last-updated">{__('Last updated on ')} {last_updated}</p>')
            self.body.append(f'<p class="description">{description}</p></div></a></li>\n')

            count += 1
            if count >= node['page_size']:
                self.body.append('</ul></div>\n')
                count = 0
    if count > 0:
        self.body.append('</ul></div>\n')

    if pages > 1:
        self.body.append(f'<div class="navigation">')
        for i in range(1, pages + 1):
            self.body.append(f'<input class="{ 'selected' if i == 1 else ''}" data-page="{i}" type="button" value="{i}"/>')
        self.body.append(f'</div>')

    self.body.append('</div>\n')


def _depart_custom_toc_node_html(self, node):
    pass

def setup(app):
    app.add_node(BlogPostsNode,
                 html=(_visit_custom_toc_node_html, _depart_custom_toc_node_html))
    app.add_directive("blogposts", BlogPosts)
