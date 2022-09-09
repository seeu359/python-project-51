import os
import pytest
from page_loader import link_handling as lh
from bs4 import BeautifulSoup

PATH = 'tests/fixtures'


@pytest.fixture()
def _result_format_link():
    link = 'https://ru.hexlet.io/projects/51/members/24681'
    return lh.get_format_link(link)


@pytest.fixture()
def open_hexlet_courses():
    with open(os.path.join(PATH, 'hexlet-courses-fixture.html')) as _fixture:
        fixture = _fixture.read()
    return fixture


@pytest.fixture()
def open_picture():
    with open(os.path.join(PATH, 'picture_from_html.png'), 'rb') as _fixture:
        fixture = _fixture.read()
    return fixture


@pytest.fixture()
def open_unmodified_html():
    with open(os.path.join(PATH, 'hexlet-courses-fixture.html')) as _fixture:
        fixture = _fixture.read()
    pars_html = BeautifulSoup(fixture, 'html.parser').prettify()
    return pars_html

