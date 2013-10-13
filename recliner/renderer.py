from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import io

from docutils.core import publish_parts
from docutils.writers.html4css1 import HTMLTranslator, Writer
from docutils.utils import SystemMessage

import bleach

from . import six


__all__ = ["render", "clean", "htmlize"]


ALLOWED_TAGS = [
    # Bleach Defaults
    "a", "abbr", "acronym", "b", "blockquote", "code", "em", "i", "li", "ol",
    "strong", "ul",

    # Recliner Additions
    "br", "cite", "col", "colgroup", "dd", "div", "dl", "dt", "h1", "h2", "h3",
    "h4", "h5", "h6", "img", "p", "pre", "span", "table", "tbody", "td", "th",
    "thead", "tr", "tt",
]

ALLOWED_ATTRIBUTES = {
    # Bleach Defaults
    "a": ["href", "title"],
    "abbr": ["title"],
    "acronym": ["title"],
}

ALLOWED_ATTRIBUTES.update({
    # Recliner Additions
    "img": ["src"],
    "span": ["class"],
})

ALLOWED_STYLES = []


class HTML(six.text_type):

    raw = None
    rendered = False


def render(raw):
    settings = {
        # Cloaking email addresses provides a small amount of additional
        #   privacy protection for email addresses inside of a chunk of ReST.
        "cloak_email_addresses": True,

        # Prevent a lone top level heading from being promoted to document
        #   title, and thus second level headings from being promoted to top
        #   level.
        "doctitle_xform": True,

        # Set our initial header level
        "initial_header_level": 2,

        # Prevent local files from being included into the rendered output.
        #   This is a security concern because people can insert files
        #   that are part of the system, such as /etc/passwd.
        "file_insertion_enabled": False,

        # Halt rendering and throw an exception if there was any errors or
        #   warnings from docutils.
        "halt_level": 2,

        # Output math blocks as LaTeX that can be interpreted by MathJax for
        #   a prettier display of Math formulas.
        "math_output": "MathJax",

        # Disable raw html as enabling it is a security risk, we do not want
        #   people to be able to include any old HTML in the final output.
        "raw_enabled": False,

        # Disable all system messages from being reported.
        "report_level": 5,

        # Use typographic quotes, and transform --, ---, and ... into their
        #   typographic counterparts.
        "smart_quotes": True,

        # Strip all comments from the rendered output.
        "strip_comments": True,

        # Use the short form of syntax highlighting so that the generated
        #   Pygments CSS can be used to style the output.
        "syntax_highlight": "short",

        # Use a io.StringIO as the warning stream to prevent warnings from
        #   being printed to sys.stderr.
        "warning_stream": io.StringIO(),
    }

    writer = Writer()
    writer.translator_class = HTMLTranslator

    try:
        parts = publish_parts(raw,
                    writer=writer,
                    settings_overrides=settings,
                )
    except SystemMessage as exc:
        raise ValueError(exc.message)

    rendered = parts.get("html_body")

    if rendered is None:
        raise ValueError("There was no rendered value")

    return rendered


def clean(html):
    def nofollow(attrs, new=False):
        if attrs["href"].startswith("mailto:"):
            return attrs
        attrs["rel"] = "nofollow"
        return attrs

    # Clean the output using Bleach
    cleaned = bleach.clean(html,
                tags=ALLOWED_TAGS,
                attributes=ALLOWED_ATTRIBUTES,
                styles=ALLOWED_STYLES,
            )

    # Bleach Linkify makes it easy to modify links, however, we will not be
    #   using it to create additional links.
    cleaned = bleach.linkify(cleaned,
                callbacks=[
                    lambda attrs, new: attrs if not new else None,
                    nofollow,
                ],
                skip_pre=True,
                parse_email=False,
            )

    return cleaned


def htmlize(text):
    # Try to render the text, or use the text itself
    try:
        html = render(text)
        rendered = True
    except ValueError:
        html = text
        rendered = False

    # Clean the (possibly) rendered text
    cleaned = clean(html)

    cleaned = HTML(cleaned)
    cleaned.raw = text
    cleaned.rendered = rendered

    return cleaned
