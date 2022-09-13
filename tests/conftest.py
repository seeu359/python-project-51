import os
import pytest
from page_loader import link_handling as lh
from bs4 import BeautifulSoup

PATH = 'tests/fixtures'


def get_path(filename):
    return os.path.join(PATH, filename)


@pytest.fixture()
def _result_format_link():
    link = 'https://ru.hexlet.io/projects/51/members/24681'
    return lh.get_format_link(link)


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


@pytest.fixture()
def image_fixture():
    with open(get_path('fixture_for_img.html')) as _fixture:
        fixture = _fixture.read()
    pars_html = BeautifulSoup(fixture, 'html.parser')
    images = pars_html.find_all('img', {'src': True})
    image_name = str()
    for img in images:
        image_name += img['src']
    return pars_html, image_name


@pytest.fixture()
def links_fixture():
    with open(get_path('fixture_for_link.html')) as _fixture:
        fixture = _fixture.read()
    pars_html = BeautifulSoup(fixture, 'html.parser')
    link_list = pars_html.find_all('link', {'href': True})
    link_name = list()
    for link in link_list:
        link_name.append(link['href'])
    return pars_html, link_name


@pytest.fixture()
def script_fixture():
    with open(get_path('fixture_for_script.html')) as _fixture:
        fixture = _fixture.read()
    pars_html = BeautifulSoup(fixture, 'html.parser')
    return pars_html
