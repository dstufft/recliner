import collections
import StringIO
import sys
import urlparse
import xmlrpclib

from docutils import io, readers
from docutils.core import publish_doctree, Publisher
from docutils.transforms import TransformError
from progress.bar import Bar

import recliner

##############################################################################
##### Copied from PyPI #######################################################
##############################################################################


def pypi_render(source):
    """
    Copied (and slightly adapted) from pypi.description_tools
    """
    ALLOWED_SCHEMES = '''file ftp gopher hdl http https imap mailto mms news
        nntp prospero rsync rtsp rtspu sftp shttp sip sips snews svn svn+ssh
        telnet wais irc'''.split()

    settings_overrides = {
        "raw_enabled": 0,  # no raw HTML code
        "file_insertion_enabled": 0,  # no file/URL access
        "halt_level": 2,  # at warnings or errors, raise an exception
        "report_level": 5,  # never report problems with the reST code
    }

    # capture publishing errors, they go to stderr
    old_stderr = sys.stderr
    sys.stderr = s = StringIO.StringIO()
    parts = None

    try:
        # Convert reStructuredText to HTML using Docutils.
        document = publish_doctree(source=source,
            settings_overrides=settings_overrides)

        for node in document.traverse():
            if node.tagname == '#text':
                continue
            if node.hasattr('refuri'):
                uri = node['refuri']
            elif node.hasattr('uri'):
                uri = node['uri']
            else:
                continue
            o = urlparse.urlparse(uri)
            if o.scheme not in ALLOWED_SCHEMES:
                raise TransformError('link scheme not allowed')

        # now turn the transformed document into HTML
        reader = readers.doctree.Reader(parser_name='null')
        pub = Publisher(reader, source=io.DocTreeInput(document),
            destination_class=io.StringOutput)
        pub.set_writer('html')
        pub.process_programmatic_settings(None, settings_overrides, None)
        pub.set_destination(None, None)
        pub.publish()
        parts = pub.writer.parts

    except:
        pass

    sys.stderr = old_stderr

    # original text if publishing errors occur
    if parts is None or len(s.getvalue()) > 0:
        return None
    else:
        return parts['body']


##############################################################################
##############################################################################
##############################################################################

client = xmlrpclib.Server("http://pypi.python.org/pypi")

counter = collections.Counter()

unexpected = []

packages = client.list_packages()

for package in Bar("Processing", max=len(packages)).iter(packages):
    for version in client.package_releases(package, True):
        release_data = client.release_data(package, version)

        description = release_data.get("description", "")

        if description is None:
            continue

        html = recliner.htmlize(description)
        pypi = pypi_render(description)

        counter["total"] += 1

        if html.rendered:
            counter["recliner"] += 1
        if pypi is not None:
            counter["pypi"] += 1

        if not html.rendered and pypi is not None:
            unexpected.append((package, version))


for key, count in counter.items():
    print key, "=>", count

if unexpected:
    print ""
    print "Recliner => No; PyPI => Yes"
    print "==========================="

    for package, version in unexpected:
        print "    ", package.encode("utf-8"), "=>", version.encode("utf8")
