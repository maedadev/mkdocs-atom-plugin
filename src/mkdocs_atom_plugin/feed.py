from typing import NamedTuple


class Author(NamedTuple):
    email: str = None
    name: str = None


class Category(NamedTuple):
    term: str = None
    label: str = None


class Entry(NamedTuple):
    authors: list = []
    categories: list = []
    description: str = None
    id: str = None
    link: str = None
    published: str = None
    title: str = None
    updated: str = None
