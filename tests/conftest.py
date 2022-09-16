import os
import pytest
import requests
from bs4 import BeautifulSoup
from page_loader.downloaders import Downloaders
import requests_mock

PATH = 'tests/fixtures'
TEST_LINK = 'http://test.com'
TEST_PATH = os.getcwd()


def read_html_data(path):
    with open(path) as f:
        file = f.read()
    return file


@pytest.fixture()
def get_link_data_fixture():
    with requests_mock.Mocker() as mock:
        data = read_html_data(os.path.join(PATH, 'fixture_for_img.html'))
        mock.get(TEST_LINK, text='test')
        test_obj = Downloaders(TEST_LINK, TEST_PATH, data)
        return test_obj.get_text_data(TEST_LINK)


@pytest.fixture()
def resources_lst_fixture():
    data = read_html_data(os.path.join(PATH, 'fixture_for_img.html'))
    test_obj = Downloaders(TEST_LINK, os.getcwd(), data)
    return test_obj.get_resources_lst(test_obj.tags['img'])
