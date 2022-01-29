import logging
from datetime import datetime, timedelta, timezone
from mimetypes import guess_type
from pathlib import Path
from typing import Iterable, Tuple
from urllib.parse import urlencode, urlparse, urlunparse

import markdown
from mkdocs.structure.pages import Page
from mkdocs.utils import get_build_timestamp


logger = logging.getLogger("mkdocs.mkdocs_atom_plugin")


class Util:

    def to_string_with_tz(self, dt):
        tz = timezone(timedelta(hours=+9), 'JST')
        dt = dt.replace(tzinfo=tz)
        return dt.strftime('%Y-%m-%dT%H:%M:%S%z')


    def get_build_date(self):
        return self.to_string_with_tz(datetime.fromtimestamp(get_build_timestamp()))


    def get_file_date(self, page: Page, meta_date: str, meta_datetime_format: str) -> int:
        if page.meta.get(meta_date):
            ret = self.get_date_from_meta(meta_date_value = page.meta.get(meta_date), meta_datetime_format = meta_datetime_format)

        if ret is not None:
            return self.to_string_with_tz(ret)
        else:
            logging.warning(f"[atom-plugin] Date could not be retrieved for page: {page.file.abs_src_path}.")
            return self.get_build_date()


    def get_date_from_meta(self, meta_date_value: str, meta_datetime_format: str) -> float:
        try:
            if isinstance(meta_date_value, str):
                return datetime.strptime(meta_date_value, meta_datetime_format)
            else:
                logging.warning("[atom-plugin] Incompatible date type.")
        except ValueError as err:
            logging.warning(f"[atom-plugin] Incompatible date found. Trace: {err}")
        except Exception as err:
            logging.warning(f"[atom-plugin] Unable to retrieve date. Trace: {err}")

        return None


    def get_abstract(self, page: Page, chars_count: int = 160) -> str:
        if chars_count < 0:
            chars_count = None

        if page.markdown:
            if chars_count is None or len(page.markdown) < chars_count:
                return markdown.markdown(page.markdown[:chars_count], output_format = "html5")
            else:
                return markdown.markdown(f"{page.markdown[: chars_count - 3]}...", output_format = "html5")
        else:
            return None
