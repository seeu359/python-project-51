import os
import pytest
from bs4 import BeautifulSoup
from page_loader.core.downloader import Downloader
import requests_mock
import tempfile
from page_loader.loader import make_request_by_url
PATH = 'tests/fixtures'
TEST_URL = 'http://test.com'
TEST_FILE_PATH = 'test/file/path.png'


def read_bytes_data(path):
    with open(path, 'rb') as f:
        file = f.read()
    return file


def read_text_data(path):
    with open(path) as f:
        file = f.read()
    return file


@pytest.fixture()
def get_url_data_fixture():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with requests_mock.Mocker() as mock:
            mock.get(TEST_URL, text='test')
            test_obj = Downloader(TEST_URL, tmp_dir, tmp_dir, tmp_dir,
                                  make_request_by_url(TEST_URL).text)
            return test_obj.get_text_data(TEST_URL)


@pytest.fixture()
def html_fixture():
    path = os.path.join(PATH, 'fixture_page.html')
    return read_text_data(path)


@pytest.fixture()
def html_fixture2():
    path = os.path.join(PATH, 'fixture_page2.html')
    return read_text_data(path)


@pytest.fixture()
def test_bs_object():
    path = os.path.join(PATH, 'fixture_page.html')
    file = read_text_data(path)
    pars_file = BeautifulSoup(file, 'html.parser')
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
