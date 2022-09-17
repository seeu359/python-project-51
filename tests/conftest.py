import os
import pytest
import requests
from bs4 import BeautifulSoup
from page_loader.downloaders import Downloaders
import requests_mock
import tempfile
import pathlib

PATH = 'tests/fixtures'
TEST_LINK = 'http://test.com'
TEST_PATH = os.getcwd()


def read_picture(path):
    with open(path, 'rb') as f:
        file = f.read()
    return file


def read_text_data(path):
    with open(path) as f:
        file = f.read()
    return file


@pytest.fixture()
def get_link_data_fixture():
    with requests_mock.Mocker() as mock:
        data = read_text_data(os.path.join(PATH, 'fixture_for_img.html'))
        mock.get(TEST_LINK, text='test')
        test_obj = Downloaders(TEST_LINK, TEST_PATH, data)
        return test_obj.get_text_data(TEST_LINK)


@pytest.fixture()
def resources_lst_fixture():
    data = read_text_data(os.path.join(PATH, 'fixture_for_img.html'))
    test_obj = Downloaders(TEST_LINK, os.getcwd(), data)
    return test_obj.get_resources_lst(test_obj.tags['img'])


@pytest.fixture()
def read_html_fixture():
    path = os.path.join(PATH, 'fixture_page.html')
    return read_text_data(path)


@pytest.fixture()
def test_bs_object():
    path = os.path.join(PATH, 'fixture_page.html')
    file = read_text_data(path)
    pars_file = BeautifulSoup(file, 'html.parser')
    find_img = pars_file.find_all('img', {'src': True})
    return file, find_img


@pytest.fixture()
def css_fixture():
    path = os.path.join(PATH, 'fixture_css_stylesheet.css')
    return read_text_data(path)


@pytest.fixture()
def fixture_for_checker():
    tag = 'img'
    res_path = '/test/path.svg'
    webpage_link = TEST_LINK
    return tag, res_path, webpage_link