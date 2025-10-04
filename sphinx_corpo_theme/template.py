from sphinx.errors import ApplicationError
from sphinx.util import logging
import re
from typing import Any, Type
from sphinx.util.console import colorize

logger = logging.getLogger(__name__)

THEME_CONF_CONTENT_MAPPING = 'template_overrides'

PATTERN = re.compile(r'^([\w-]+/)+$')

def get_config(app, name : str, value : Any, value_type : Type):
    if name in app.config.html_theme_options:
        temp = app.config.html_theme_options[name]
        if not isinstance(temp, value_type):
            raise ApplicationError("Configuration option '{name}' must be a value of type '{valuetype}'")
        return temp
    return value

class TemplateSelector:

    def __init__(self, app):
        self.mapping = get_config(app, THEME_CONF_CONTENT_MAPPING, {}, dict)
        if not self.mapping:
            return

        # validate mapping prefixes
        keys = list(self.mapping.keys())
        for i, prefix in enumerate(keys):
            if not self._is_valid_prefix(prefix):
                raise ApplicationError(f"invalid mapping prefix '{prefix}'")
            for j, other in enumerate(keys):
                if i != j and other.startswith(prefix):
                    raise ApplicationError(f"mapping prefix '{prefix}' is prefix of another mapping")
        # validate content type
        for item in self.mapping.keys():
            if not isinstance(item, str):
                raise ApplicationError(f"expected dict value but found {type(item)}")

    def _is_valid_prefix(self, value: str) -> bool:
        return value == '' or re.fullmatch(PATTERN, value) is not None

    def select(self, pagename) -> str | None:
        for prefix in self.mapping:
            if pagename.startswith(prefix):
                return self.mapping[prefix]
        return None


