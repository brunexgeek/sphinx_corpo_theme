from sphinx.environment.adapters.toctree import TocTree
import sphinx.addnodes
from .toc import TreeGenerator
from .template import TemplateSelector
import os
import re
import json
from sphinx.util import logging
from sphinx.util.console import colorize
import time
from datetime import datetime
from .blogposts import setup as blogposts_setup

logger = logging.getLogger(__name__)

CORPO_HAS_TOC = '_corpo__has_toc'
CORPO_TOC_PRUNING = 'toc_pruning'

H1_REGEX = re.compile(r'<h1[^>]*>.*?</h1>', flags=re.DOTALL)
mapper = None

class Clock:

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_value, traceback):
        end = time.time()
        logger.info(f'{end} {colorize('blue',self.name)} took {'{:.6f}'.format(end - self.start)} seconds')

def remove_first_h1(html):
    match = H1_REGEX.search(html)
    if match:
        removed = match.group(0)
        cleaned = H1_REGEX.sub('', html, count=1)
        return removed, cleaned
    else:
        return "", html

def extract_title(context):
    context['corpo_title'], context['corpo_body'] = remove_first_h1(context.get('body', ''))

def custom_toc_generation(app, pagename, templatename, context, doctree):
    if pagename in ['genindex']:
        return

    extract_title(context)
    current_url = pagename
    uid = 1

    # compute the TOC tree
    with Clock('toctree.get_toctree_for'):
        toctree = TocTree(app.env)
        raw_toc = toctree.get_toctree_for(pagename, app.builder, False)
        # TODO store the result from the first execution to reuse on other calls

    # generate a custom TOC tree
    with Clock('TreeGenerator'):
        prune = template.get_config(app, CORPO_TOC_PRUNING, False, bool)
        gen = TreeGenerator(pagename, app.config.master_doc, raw_toc, prune)
        context['corpo_toc_map'] = gen.get_global_toc()
        if doctree and not doctree.get(CORPO_HAS_TOC, False):
            context['corpo_local_toc_map'] = gen.get_local_toc()
        elif app.config.html_theme_options.get('show_child_topics', False):
            logger.warning(f"ignoring local TOC for '{pagename}' because document has visible TOC")
        pageentry = gen.get_pageentry()
        context['corpo_parent'] = pageentry['parent'] if pageentry and 'parent' in pageentry else None
        context['corpo_root'] = gen.get_root()

def custom_template_selection(app, pagename, templatename, context, doctree):
    context['corpo_template'] = templatename
    selected = None

    # check if we should override the template based on 'template_overrides'
    if mapper:
        selected = mapper.select(pagename)
        if selected:
            context['corpo_template'] = selected

    # check if we should override the template based on 'template' metadata
    if context and 'meta' in context and context['meta'] and 'template' in context['meta']:
        name = context['meta']['template'].strip()
        if not name.endswith('.html'):
            raise ApplicationError("Templates must use extension '.html'")
        if name.find('/') >= 0:
            raise ApplicationError("Invalid character in template name")
        context['corpo_template'] = selected = name

    if selected:
        logger.info(f"Changing {colorize('darkgreen', pagename)} template to {colorize('darkgreen', selected)}")
    return selected

def custom_doctree_inspection(app, doctree):
    it = doctree.findall(sphinx.addnodes.toctree)
    doctree[CORPO_HAS_TOC] = False
    for node in it:
        if 'hidden' in node and not bool(node['hidden']):
            doctree[CORPO_HAS_TOC] = True
            break

def custom_metadata_processing(app, doctree, docname):
    metadata = app.env.metadata.get(docname, {})
    value = metadata.get("last_updated", None)

    if value and app.config.html_last_updated_fmt:
        try:
            parsed_date = datetime.fromisoformat(value)
            formatted_date = parsed_date.strftime(app.config.html_last_updated_fmt)
            metadata["last_updated"] = formatted_date
        except ValueError:
            del metadata["last_updated"]
            logger.warning(f"{colorize('darkgreen',docname)} has invalid ISO-8601 date: {value}")
    else:
        metadata["last_updated"] = None


def setup(app):
    # add Sphinx message catalog for translations; it seems Sphinx expects the catalog name to be 'sphinx'
    locale_dir = os.path.join(os.path.dirname(__file__), 'locales')
    app.add_message_catalog('sphinx', locale_dir)
    # register the theme
    theme_path = os.path.abspath(os.path.dirname(__file__))
    app.add_html_theme('sphinx_corpo_theme', theme_path)

    app.connect('doctree-read', custom_doctree_inspection)

    # TODO Change implementation to generate local TOC using TOC tree from the document itself;
    # we can scan all toctrees in the document and generate a local TOC using the first level of
    # each of them. (Note: actually, it's easier the way we do now)

    # TODO whenever we have only one page in the top level (e.g., because we're using 'template_overrides')
    # we probably could eliminate this page from TCO and use its children instead; this way we use this
    # page as masterdoc for that particular group of pages (by template).

    app.connect('html-page-context', custom_toc_generation)

    global mapper
    mapper = TemplateSelector(app)
    app.connect('html-page-context', custom_template_selection)

    app.connect("doctree-resolved", custom_metadata_processing)

    blogposts_setup(app)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': False,
    }
