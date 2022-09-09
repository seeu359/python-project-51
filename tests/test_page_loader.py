import requests_mock
from page_loader import page_loader
import pathlib
import tempfile
import os
from page_loader import downloaders

TEST_LINK = 'http://test.com'
PATH = 'tests/fixtures'


def test_get_link_data():
    with requests_mock.Mocker() as mock:
        mock.get(TEST_LINK, text='mock_test')
        result = downloaders.get_link_data(TEST_LINK)
        assert result == 'mock_test'


def test_get_format_path(_result_format_link):
    result = 'ru-hexlet-io-projects-51-members-24681'
    assert result == _result_format_link


def fake_image_parser(args=None):
    with open(os.path.join(PATH, 'picture_from_html.png'), 'rb') as pic:
        picture = pic.read()
    return picture


def fake_image_recorder(path, data):
    with open(path, 'wb') as img:
        img.write(data)


def test_download_page(open_hexlet_courses):
    with tempfile.TemporaryDirectory() as tmp:
        with requests_mock.Mocker() as mock:
            path = pathlib.Path(tmp, 'test-com.html')
            mock.get(TEST_LINK, text=open_hexlet_courses)
            page_loader.download(TEST_LINK, tmp)
        with open(path) as test_f:
            test_file = test_f.read()

        assert os.path.isfile(path) is True
        assert test_file == open_hexlet_courses


def test_download_picture():
    with tempfile.TemporaryDirectory() as tmp:
        webpage_path = os.path.join(PATH, 'hexlet-courses-fixture.html')
        link = 'https://ru.hexlet.io/courses'
        downloaders.download_pictures(webpage_path, tmp, link,
                                      image_parser=fake_image_parser,
                                      image_recorder=fake_image_recorder)
        for i in os.listdir(tmp):
            path = pathlib.Path(tmp, i)
            print(i)
            assert len(os.listdir(tmp)) == 1
            assert os.path.exists(path) is True


def test_link_change(open_unmodified_html):
    fixture_before_change = open_unmodified_html
    with tempfile.TemporaryDirectory() as tmp:
        webpage_path = os.path.join(PATH, 'hexlet-courses-fixture.html')
        modified_html = downloaders.download_pictures(
            webpage_path, tmp, TEST_LINK,
            image_parser=fake_image_parser,
            image_recorder=fake_image_recorder)
        assert modified_html != fixture_before_change
