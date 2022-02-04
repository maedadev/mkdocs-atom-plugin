from typing import NamedTuple


class Author(NamedTuple):
    email: str = None
    name: str = None


class Entry(NamedTuple):
    author: Author = None
    description: str = None
    id: str = None
    link: str = None
    published: str = None
    title: str = None
    updated: str = None
