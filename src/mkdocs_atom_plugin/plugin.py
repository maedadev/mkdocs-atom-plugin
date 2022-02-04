import logging
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page

from . import __about__
from .feed import Entry
from .util import Util

FEED_FILENAME = "atom.xml"
TEMPLATE_FOLDER = Path(__file__).parent / "templates"
TEMPLATE_FILENAME = "atom.xml.jinja2"

logger = logging.getLogger("mkdocs.mkdocs_atom_plugin")


class AtomPlugin(BasePlugin):

    config_scheme = (
        ("abstract_chars_count", config_options.Type(int, default = 160)),
        ("datetime", config_options.Type(dict, default=None)),
        ("length", config_options.Type(int, default = 20)),
    )


    def __init__(self):
        self.util = Util()
        self.feed = {'generator_version': __about__.__version__}
        self.entries = []


    def on_config(self, config: config_options.Config) -> dict:
        self.feed['description'] = config.get("site_description", None)
        self.feed['entries'] = []
        self.feed['title'] = config.get("site_name", None)
        self.feed['updated'] = self.util.get_build_date()

        html_url = config.get("site_url", None)
        if html_url is not None:
            html_url = os.path.join(html_url, '') # add trailing slash
            self.feed['html_url'] = html_url
            self.feed["rss_url"] = html_url + FEED_FILENAME

        return config


    def on_page_content(self, html: str, page: Page, config: config_options.Config, files) -> str:
        if self.config.get('datetime') is not None:
            datetime_format = self.config.get('datetime').get('format', '%Y-%m-%d %H:%M')
            timezone_name = self.config.get('datetime').get('timezone', 'UTC')
        else:
            datetime_format = '%Y-%m-%d %H:%M'
            timezone_name = 'UTC'

        self.entries.append(
            Entry(
                authors = self.util.get_authors(page = page),
                categories = self.util.get_categories(page = page),
                description = self.util.get_abstract(page = page, chars_count = self.config.get("abstract_chars_count")),
                id = page.canonical_url,
                link = page.canonical_url,
                published = self.util.get_page_date(page = page, meta_date = 'published', datetime_format = datetime_format, timezone_name = timezone_name),
                title = page.title,
                updated = self.util.get_page_date(page = page, meta_date = 'updated', datetime_format = datetime_format, timezone_name = timezone_name, fallback = True),
            )
        )


    def on_post_build(self, config: config_options.Config) -> dict:
        length = self.config.get("length")
        feed_entries = sorted(self.entries, key = lambda entry: entry.updated, reverse = True)[:length]
        self.feed.get("entries").extend(feed_entries)

        env = Environment(
            autoescape = select_autoescape(["html", "xml"]),
            loader = FileSystemLoader(TEMPLATE_FOLDER),
        )

        template = env.get_template(TEMPLATE_FILENAME)

        out_path = Path(config.get("site_dir")) / FEED_FILENAME
        with out_path.open(mode = "w", encoding = "UTF8") as f:
            f.write(template.render(feed = self.feed))
