import pytest
import requests_mock
import pathlib
import tempfile
import os
from page_loader.downloaders import Downloaders
import requests


TEST_PATH = os.getcwd()
TEST_LINK = 'http://test.com'
PATH = 'tests/fixtures'


def read_picture(path):
    with open(path, 'rb') as f:
        file = f.read()
    return file


def read_html_data(path):
    with open(path) as f:
        file = f.read()
    return file


def test_get_link_data(get_link_data_fixture):
    assert get_link_data_fixture == 'test'


@pytest.mark.parametrize('file, input_value, expected',
                         [('fixture_for_img.html', 'img', 1),
                          ('fixture_for_link.html', 'link', 2),
                          ('fixture_for_script.html', 'script', 2)]
                         )
def test_resource_lst(file, input_value, expected):
    test_data = read_html_data(os.path.join(PATH, file))
    test_obj = Downloaders(TEST_LINK, os.getcwd(), test_data)
    assert len(test_obj.get_resources_lst(
        test_obj.tags[input_value])) == expected
