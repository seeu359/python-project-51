import requests_mock
from page_loader import page_loader
import pathlib
import tempfile
import os


TEST_LINK = 'http://test.com'


def test_get_link_data():
    with requests_mock.Mocker() as mock:
        mock.get(TEST_LINK, text='mock_test')
        result = page_loader.get_link_data(TEST_LINK)
        assert result == 'mock_test'


def test_get_format_path(_result_format_link):
    result = 'ru-hexlet-io-projects-51-members-24681'
    assert result == _result_format_link


def test_download_page(_fixture_hexlet_courses):
    with tempfile.TemporaryDirectory() as tmp:
        with requests_mock.Mocker() as mock:
            path = pathlib.Path(tmp, 'test-com.html')
            mock.get(TEST_LINK, text=_fixture_hexlet_courses)
            page_loader.download(TEST_LINK, tmp)
        with open(path) as test_f:
            test_file = test_f.read()

        assert os.path.isfile(path) is True
        assert test_file == _fixture_hexlet_courses


def test_download_picture(_download_pic, _fixture_picture):
    assert _download_pic == _fixture_picture

