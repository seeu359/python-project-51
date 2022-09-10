import requests_mock
from page_loader import page_loader
import pathlib
import tempfile
import os
from page_loader import downloaders
from page_loader import file_handling as fh
from page_loader import link_handling as lh


TEST_LINK = 'http://test.com'
PATH_TO_FIXTURES = 'tests/fixtures'


def test_get_link_data():
    with requests_mock.Mocker() as mock:
        mock.get(TEST_LINK, text='mock_test')
        result = downloaders.get_link_data(TEST_LINK)
        assert result == 'mock_test'


def test_get_format_path(_result_format_link):
    result = 'ru-hexlet-io-projects-51-members-24681'
    assert result == _result_format_link


def fake_image_parser(*args):
    with open(os.path.join(PATH_TO_FIXTURES,
                           'picture_from_html.png'), 'rb') as pic:
        picture = pic.read()
    return picture


def fake_image_recorder(path, data):
    with open(path, 'wb') as img:
        img.write(data)


def test_download_data(open_hexlet_courses):
    with tempfile.TemporaryDirectory() as tmp:
        test_data = open_hexlet_courses
        downloaders.get_local_resources(test_data, tmp, TEST_LINK,
                                        data_parser=fake_image_parser,
                                        data_recorder=fake_image_recorder)
        for i in os.listdir(tmp):
            path = pathlib.Path(tmp, i)
            assert len(os.listdir(tmp)) == 1
            assert os.path.exists(path) is True


def test_make_dir():
    with tempfile.TemporaryDirectory() as tmp:
        converted_link = lh.get_format_link(TEST_LINK)
        path = fh.make_dir(converted_link, tmp)
        assert len(os.listdir(tmp)) == 1
        assert os.path.isdir(path) is True


def test_link_change(open_unmodified_html, open_hexlet_courses):
    fixture_before_change = open_unmodified_html
    test_data = open_hexlet_courses
    with tempfile.TemporaryDirectory() as tmp:
        modified_html = downloaders.get_local_resources(
            test_data, tmp, TEST_LINK,
            data_parser=fake_image_parser,
            data_recorder=fake_image_recorder
        )
        assert modified_html != fixture_before_change
