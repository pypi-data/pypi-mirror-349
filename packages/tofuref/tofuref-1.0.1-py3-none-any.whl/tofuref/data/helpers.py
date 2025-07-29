import re
from typing import Tuple, Union, Dict, Any, Optional
import logging

import httpx
from async_lru import alru_cache
from yaml import safe_load
from yaml.scanner import ScannerError

from tofuref import __version__

LOGGER = logging.getLogger(__name__)


def header_markdown_split(contents: str) -> Tuple[dict, str]:
    """
    Most of the documentation files from the registry have a YAML "header"
    that we mostly (at the moment) don't care about. Either way we
    check for the header and if it's there, we split it.
    """
    header = {}
    if re.match(r"^---$", contents, re.MULTILINE):
        split_contents = re.split(r"^---$", contents, 3, re.MULTILINE)
        try:
            header = safe_load(split_contents[1])
        except ScannerError as _:
            header = {}
        markdown_content = split_contents[2]
    else:
        markdown_content = contents
    return header, markdown_content


@alru_cache(maxsize=64)
async def get_registry_api(
    endpoint: str, json: bool = True, log_widget: Optional[Any] = None
) -> Union[Dict[str, dict], str]:
    """
    Sends GET request to opentofu providers registry to a given endpoint
    and returns the response either as a JSON or as a string. It also "logs" the request.

    The function is cached because of tests. In practice, the cache will never get used.
    """
    uri = f"https://api.opentofu.org/registry/docs/providers/{endpoint}"
    LOGGER.debug("Starting async client")
    async with httpx.AsyncClient(
        headers={"User-Agent": f"tofuref v{__version__}"}
    ) as client:
        LOGGER.debug("Client started, sending request")
        try:
            r = await client.get(uri)
            LOGGER.debug("Request sent, response received")
        except Exception as e:
            LOGGER.error("Something went wrong", exc_info=e)
            if log_widget is not None:
                log_widget.write(f"Something went wrong: {e}")
            return ""

    if log_widget is not None:
        log_widget.write(f"GET [cyan]{endpoint}[/] [bold]{r.status_code}[/]")

    if json:
        return r.json()
    else:
        return r.text
