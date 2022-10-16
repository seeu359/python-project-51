import os
import pytest
from bs4 import BeautifulSoup
from page_loader.core.downloaders import Downloaders
import requests_mock
import tempfile
from page_loader.core.dataclasses import DownloadInformation
from page_loader.loader import _make_request_by_link
PATH = 'tests/fixtures'
TEST_LINK = 'http://test.com'
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
def get_link_data_fixture():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with requests_mock.Mocker() as mock:
            test_main_obj = DownloadInformation(
                webpage_link=TEST_LINK, path_to_save_directory=tmp_dir,
                path_to_resources_directory=tmp_dir,
                path_to_main_html=tmp_dir)
            mock.get(TEST_LINK, text='test')
            test_obj = Downloaders(test_main_obj,
                                   _make_request_by_link(TEST_LINK))
            return test_obj.get_text_data(TEST_LINK)


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
    webpage_link = TEST_LINK
    return tag, res_path, webpage_link
