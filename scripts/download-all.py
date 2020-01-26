#!/usr/bin/env python3
import os
from pathlib import Path
from functools import lru_cache
from typing import Sequence, TypeVar, Optional, Tuple

import requests
from lxml.html import fromstring, tostring
from lxml.cssselect import CSSSelector as Selector

T = TypeVar("T")


def get_first(to_iterate: Sequence[T], fallback: Optional[T] = None) -> Optional[T]:
    return next(iter(to_iterate), fallback)


def normalize_str(s: str) -> str:
    return s.casefold().strip()


@lru_cache(1)
def get_bearings():
    this_dir = Path(os.path.dirname(__file__)).absolute()
    repo_root = Path(this_dir, "..").absolute()
    return this_dir, repo_root


all_versions = [
    "2.6",
    "2.7",
    "3.0",
    "3.1",
    "3.2",
    "3.3",
    "3.4",
    "3.5",
    "3.6",
    "3.7",
    "3.8",
    "3.9",
]
n_versions = len(all_versions)


def make_download_page_url(version: str) -> str:
    return f"https://docs.python.org/{version}/download.html"


def get_download_page(version: str) -> str:
    url = make_download_page_url(version)
    response = requests.get(url)
    if not response.ok:
        response.raise_for_status()
    return response.text


@lru_cache(n_versions)
def make_download_page_cache_location(version: str):
    _, repo_root = get_bearings()
    return Path(repo_root, f".cache/downloads/{version}/download_page.html")


def cache_download_page(version: str, data: str) -> None:
    download_page_cache_location = make_download_page_cache_location(version)
    os.makedirs(os.path.dirname(download_page_cache_location), exist_ok=True)
    with open(download_page_cache_location, "w") as target:
        target.write(data)


def get_download_page_if_necessary(version: str) -> [str, str]:
    cache_location = make_download_page_cache_location(version)
    if not os.path.exists(cache_location):
        page = get_download_page(version)
        cache_download_page(version, page)
    with open(cache_location) as cached_file:
        return cached_file.read()


@lru_cache(n_versions)
def extract_download_link_table(page:str) -> 'lxml.etree.Elementree':
    dom = fromstring(page)
    select_table = Selector("table.docutils")
    tables = select_table(dom)
    assert (
        len(tables) == 1
    ), f"ambiguous number ({len(tables)}) of `table.docutils` in \n{tostring(html)}"
    return tables[0]


def extract_doc_url(page: str, query: str = "html") -> str:
    table = extract_download_link_table(page)
    for row in Selector("tr")(table):
        first = get_first(Selector("td:first-child")(row))
        if first is None:
            continue
        text = normalize_str(first.text)
        if query in text:
            (a_zip, a_br, *_) = Selector("a[href]")(row)
            return tuple(
                normalize_archive_download_url(a.attrib["href"].strip())
                for a in (a_zip, a_br)
            )
    raise Exception(f"{query} not found in {tostring(table).decode()}")


@lru_cache(100)
def ensure_dir_exists(path: str) -> None:
    if not dir_exists(path):
        os.makedirs(os.path.dirname(path))

def normalize_archive_download_url(url: str, version: str = "") -> str:
    if "//" in url:
        return url
    else:
        return f"https://docs.python.org/{version}/{url.rstrip('/')}"


def fs_cache(make_path: Callable[[str], str]):
    def decorator(f):
        path = make_path(version)
        def wrapped(version: str):

            if not os.path.exists(path):
                data = f(version)
                with open(path, 'w') as target:
                    target.write(data)
            else:
                with open()
    return decorator


if __name__ == "__main__":
    for version in all_versions:
        page = get_download_page_if_necessary(version)
        download_url_zip, download_url_br = extract_doc_url(page)
        print(normalize_archive_download_url(download_url_zip, version))

