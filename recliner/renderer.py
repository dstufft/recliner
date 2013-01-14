from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import io

from docutils.core import publish_parts
from docutils.writers.html4css1 import HTMLTranslator, Writer
from docutils.utils import SystemMessage


__all__ = ["render"]


def render(raw):
    settings = {
        # Cloaking email addresses provides a small amount of additional
        #   privacy protection for email addresses inside of a chunk of ReST.
        "cloak_email_addresses": True,

        # Prevent a lone top level heading from being promoted to document
        #   title, and thus second level headings from being promoted to top
        #   level.
        "doctitle_xform": False,

        # Prevent local files from being included into the rendered output.
        #   This is a security concern because people can insert files
        #   that are part of the system, such as /etc/passwd.
        "file_insertion_enabled": False,

        # Halt rendering and throw an exception if there was any errors or
        #   warnings from docutils.
        "halt_level": 0,

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

    return parts.get("html_body", "")
