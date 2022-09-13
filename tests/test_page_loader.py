import requests_mock
import pathlib
import tempfile
import os
from page_loader import downloaders


TEST_LINK = 'http://test.com'
PATH_TO_FIXTURES = 'tests/fixtures'


def fake_parser(*args):
    with open(os.path.join(PATH_TO_FIXTURES,
                           'fixture_css_stylesheet.css')) as css:
        css_style = css.read()
    return css_style


def fake_image_parser(*args):
    with open(os.path.join(PATH_TO_FIXTURES,
                           'picture_from_html.png'), 'rb') as pic:
        picture = pic.read()
    return picture


def fake_image_recorder(path, data):
    with open(path, 'wb') as img:
        img.write(data)


def fake_recorder(path, data):
    with open(path, 'w') as file:
        file.write(data)


def test_get_link_data():
    with requests_mock.Mocker() as mock:
        mock.get(TEST_LINK, text='mock_test')
        result = downloaders.get_link_data(TEST_LINK)
        assert result == 'mock_test'


def test_get_format_path(_result_format_link):
    result = 'ru-hexlet-io-projects-51-members-24681'
    assert result == _result_format_link


def test_download_images(image_fixture):
    with tempfile.TemporaryDirectory() as tmp:
        test_data, file_name = image_fixture
        downloaders.get_image(test_data, tmp, TEST_LINK,
                              data_parser=fake_image_parser,
                              data_recorder=fake_image_recorder)
        for i in os.listdir(tmp):
            _, extension = os.path.splitext(i)
            new_file = pathlib.Path(tmp, i)
            old_file = pathlib.Path(tmp, file_name)
            assert extension == '.png'
            assert len(os.listdir(tmp)) == 1
            assert os.path.exists(old_file) is False
            assert os.path.exists(new_file) is True


def test_download_links(links_fixture):
    with tempfile.TemporaryDirectory() as tmp:
        test_data, links_list = links_fixture
        first_file, second_file = links_list
        downloaders.get_links(test_data, tmp, TEST_LINK,
                              data_parser=fake_parser,
                              data_recorder=fake_recorder)
        old_file1 = pathlib.Path(tmp, first_file)
        old_file2 = pathlib.Path(tmp, second_file)
        new_file1 = pathlib.Path(tmp, 'test-com-application.css')
        new_file2 = pathlib.Path(tmp, 'test-com-courses.html')
        assert len(os.listdir(tmp)) == 2
        assert os.path.exists(old_file1) is False
        assert os.path.exists(old_file2) is False
        assert os.path.exists(new_file1) is True
        assert os.path.exists(new_file2) is True


def test_download_script(script_fixture):
    with tempfile.TemporaryDirectory() as tmp:
        test_data = script_fixture
        downloaders.get_script(test_data, tmp, TEST_LINK,
                               data_parser=fake_parser,
                               data_recorder=fake_recorder)
        new_file = pathlib.Path(tmp, 'test-com-packs-js-runtime.js')
        assert len(os.listdir(tmp)) == 1
        assert os.path.exists(new_file) is True
