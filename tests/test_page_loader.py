import requests_mock
from page_loader import page_loader
import pathlib
import tempfile
import os


def test_get_link_data():
    with requests_mock.Mocker() as mock:
        test_link = 'http://test.com'
        mock.get(test_link, text='mock_test')
        result = page_loader.get_link_data(test_link)
        assert result == 'mock_test'


def test_get_format_path(_result_format_path):
    result = 'var/tmp/ru-hexlet-io-projects-51-members-24681.html'
    assert result == _result_format_path


def test_download(_fixture_hexlet_courses):
    with tempfile.TemporaryDirectory() as tmp:
        with requests_mock.Mocker() as mock:
            test_link = 'http://test.com'
            path = pathlib.Path(tmp, 'test-com.html')
            mock.get(test_link, text=_fixture_hexlet_courses)
            page_loader.download(test_link, tmp)
        with open(path) as test_f:
            test_file = test_f.read()
        assert os.path.isfile(path) is True
        assert test_file == _fixture_hexlet_courses
