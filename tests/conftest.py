import os
import pytest
from bs4 import BeautifulSoup
from page_loader.core.downloader import get_text_data
import requests_mock
from tests.test_page_loader import read_bytes_data, read_text_data

PATH = 'tests/fixtures'
TEST_URL = 'http://test.com'
TEST_FILE_PATH = 'test/file/path.png'



@pytest.fixture()
def get_url_data_fixture():
    with requests_mock.Mocker() as mock:
        mock.get(TEST_URL, text='test')
        return get_text_data(TEST_URL)


@pytest.fixture()
def html_fixture():
    path = os.path.join(PATH, 'fixture_page.html')
    return read_text_data(path)


@pytest.fixture()
def html_fixture2():
    path = os.path.join(PATH, 'fixture_page2.html')
    return read_text_data(path)


@pytest.fixture()
def test_bs_object(html_fixture):
    pars_file = BeautifulSoup(html_fixture, 'html.parser')
    img_resources_set = pars_file.find_all('img', {'src': True})
    link_resource_set = pars_file.find_all('link', {'href': True})
    script_resource_set = pars_file.find_all('script', {'src': True})
    return img_resources_set, link_resource_set, script_resource_set


@pytest.fixture()
def css_fixture():
    path = os.path.join(PATH, 'fixture_css_stylesheet.css')
    return read_bytes_data(path)


@pytest.fixture()
def fixture_for_checker():
    tag = 'img'
    res_path = '/test/path.svg'
    webpage_url = TEST_URL
    return tag, res_path, webpage_url
