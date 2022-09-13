from urllib.parse import urlparse
import furl
import re
import os


def domain_check(picture_link, web_page):
    picture_link_parse = urlparse(picture_link)
    web_page_parse = urlparse(web_page)
    if not picture_link_parse.scheme:
        return True
    else:
        return True if web_page_parse.netloc == picture_link_parse.netloc \
            else False


def make_source_link(page_link, picture_link):
    picture_link_pars = urlparse(picture_link)
    page_link_pars = urlparse(page_link)
    if picture_link_pars.scheme:
        return picture_link
    else:
        link_body = f'{page_link_pars.scheme}://{page_link_pars.netloc}'
        build_link = furl.furl(link_body).add(path=picture_link)
        return str(build_link)


def get_format_link(link):
    parse_link = urlparse(link)
    link_without_scheme = ''.join(parse_link[1:])
    template = re.findall(r'[\da-zA-Z-.]+\.[a-zAZ]+/[@\w/-]+\.\w+',
                          link_without_scheme)
    not_format_link = link_without_scheme[0:-1] if link.endswith('/') else \
        link_without_scheme

    if len(template) == 0:
        format_link = re.sub(r'[^a-zA-Z\d]', '-', not_format_link)
        return format_link
    link_body, _ = os.path.splitext(not_format_link)
    format_link = re.sub(r'[^a-zA-Z\d]', '-', link_body)
    return format_link
