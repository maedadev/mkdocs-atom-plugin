# MkDocs Atom Plugin

MkDocs Atom Plugin generates Atom feed.

This plugin is inspired by [MkDocs RSS Plugin](https://github.com/Guts/mkdocs-rss-plugin/).

## Usage

Minimal option:

```yaml
plugins:
  - atom
```

Full options:

```yaml
plugins:
  - atom:
      abstract_chars_count: 160
      datetime:
        format: "%Y-%m-%d %H:%M"
        timezone: "UTC"
      length: 20
```

Page options:

```yaml
author_email: [Email of author. Use authors for multiple authors]
author_name: [Name of author. Use authors for multiple authors]
authors:
  - email: [Email of author]
    name: [Name of author]
  - email: [Email of another author]
    name: [Name of another author]
category_label: [Label of category. Use categories for multiple categories]
category_term: [Term of category. Use categories for multiple categories]
categories:
  - label: [Label of category]
    term: [Term of category]
  - label: [Label of another category]
    term: [Term of another category]
title:  [Title for the page]
published: [Time when page is published for the first time. Format and Timezone are defined by options]
updated: [Time when page is updated. Format and Timezone are defined by options]
```
