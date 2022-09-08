import os.path
import pytest
from page_loader import page_loader
from bs4 import BeautifulSoup


@pytest.fixture()
def _result_format_link():
    link = 'https://ru.hexlet.io/projects/51/members/24681'
    return page_loader.get_format_link(link)


@pytest.fixture()
def open_hexlet_courses():
    with open('tests/fixtures/hexlet-courses-fixture.html') as _fixture:
        fixture = _fixture.read()
    return fixture


@pytest.fixture()
def open_picture():
    with open('tests/fixtures/picture_from_html.png', 'rb') as _fixture:
        fixture = _fixture.read()
    return fixture


@pytest.fixture()
def open_unmodified_html():
    with open('tests/fixtures/hexlet-courses-fixture.html') as _fixture:
        fixture = _fixture.read()
    pars_html = BeautifulSoup(fixture, 'html.parser').prettify()
    return pars_html
