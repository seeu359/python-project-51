import pytest
import requests_mock
import pathlib
import tempfile
import requests
import os
from page_loader.lib.exceptions import DirectoryCreationError, \
    MissingSchemaError
from page_loader.lib.downloader import Downloader, _resources_validator, \
    _change_path_in_html, _save_resources, get_bytes_data, \
    _check_image_extension, _is_true_domain
from page_loader.lib.file_handling import FileWorker
from page_loader.lib.url_handling import PathHandler, build_resource_url, \
    check_url
from page_loader.loader import download, _make_dir
from page_loader.lib.dataclasses import RecordingData, ImgTag, ScriptTag, \
    LinkTag
from page_loader.loader import make_request

TEST_URL = 'http://test.com'
TEST_URL2 = 'https://ru.hexlet.io/courses'
TEST_URL3 = 'https://ru.hexlet.io'
PATH = 'tests/fixtures'


def read_bytes_data(path):
    with open(path, 'rb') as f:
        file = f.read()
    return file


def read_text_data(path):
    with open(path) as f:
        file = f.read()
    return file


def test_main_func(html_fixture2):
    with tempfile.TemporaryDirectory() as tmp:
        with requests_mock.Mocker() as mock:
            mock.get(TEST_URL, text=html_fixture2)
            path = download(TEST_URL, tmp)
            path_to_dir = os.path.join(tmp, 'test-com_files')
            print(os.listdir(tmp))
            assert os.path.exists(path)
            assert os.path.isfile(path)
            assert os.path.isdir(path_to_dir)


def test_get_url_data(get_url_data_fixture):
    assert get_url_data_fixture == 'test'


def test_get_image_data(html_fixture):
    with tempfile.TemporaryDirectory() as tmp_dir:
        with requests_mock.Mocker() as mock:
            content = read_bytes_data(os.path.join(PATH, 'image_fixture.png'))
            mock.get(TEST_URL, content=content)
            image_data = get_bytes_data(TEST_URL)
            path = pathlib.Path(tmp_dir, 'test.png')
            recording_data = RecordingData(data=image_data,
                                           path_to_save_data=str(path))
            file_worker = FileWorker(recording_data)
            file_worker.save_bytes_data()
            image = read_bytes_data(path)
            assert image == requests.get(TEST_URL).content


def test_change_path_in_html(test_bs_object):
    with tempfile.TemporaryDirectory() as tmp:
        img_result_set, _, _ = test_bs_object
        for img in img_result_set:
            old_path = img['src']
            new_path = _change_path_in_html(TEST_URL, img, 'src', tmp)
            assert old_path != new_path


@pytest.mark.parametrize('extension, reader, path',
                         [('.css', read_bytes_data,
                           os.path.join(PATH, 'fixture_css_stylesheet.css')),
                          ('.html', read_text_data,
                           os.path.join(PATH, 'fixture_page.html'))])
def test_record_resource(extension, reader, path):
    with tempfile.TemporaryDirectory() as tmp:
        fixture_data = reader(path)
        local_resource_path = 'test_path.ext'
        _save_resources(local_resource_path, fixture_data, tmp, extension)
        test_file = reader(os.path.join(tmp, local_resource_path))
        path_to_file = os.path.join(tmp, local_resource_path)
        assert os.path.isfile(path_to_file)
        assert test_file == fixture_data


@pytest.mark.parametrize('tag, expected',
                         [(ImgTag, 1),
                          (LinkTag, 2),
                          (ScriptTag, 1)]
                         )
def test_get_resources_set(tag, expected, html_fixture):
    with requests_mock.Mocker() as mock:
        with tempfile.TemporaryDirectory() as tmp_dir:
            mock.get(TEST_URL3, text=html_fixture)
            test_obj = Downloader(TEST_URL3, tmp_dir, tmp_dir, tmp_dir,
                                  make_request(TEST_URL3).text)
            assert len(test_obj.get_resources_set(tag)) == expected


@pytest.mark.parametrize('index, tag, expected,',
                         [(0, ImgTag, 1),
                          (1, LinkTag, 2),
                          (2, ScriptTag, 1)]
                         )
def test_is_true_domain(index, tag, expected, test_bs_object):
    resource_set = test_bs_object[index]
    result_set = _resources_validator(resource_set, tag, TEST_URL2)
    assert len(result_set) == expected


@pytest.mark.parametrize('url, expected',
                         [('test/file/path.png',
                           'folder_files/test-file-path.png'),
                          ('test/file/path',
                           'folder_files/test-file-path.html')]
                         )
def test_build_path_to_swap_in_html(url, expected):
    test_obj = PathHandler(url)
    folder = 'main/folder_files'
    assert test_obj.build_path_to_swap_in_html(folder) == expected


@pytest.mark.parametrize('url, file_path, expected',
                         [(TEST_URL, 'http://test.com/file/file2.png',
                           'http://test.com/file/file2.png'),
                          (TEST_URL, 'file/file2.png',
                           'http://test.com/file/file2.png')]
                         )
def test_build_url(url, file_path, expected):
    assert build_resource_url(url, file_path) == expected


def test_error_make_dir():
    with pytest.raises(DirectoryCreationError):
        _make_dir('test_path/test')


def test_error_missing_scheme():
    with pytest.raises(MissingSchemaError):
        check_url('test-url.com')


def test_error_file_not_found_error():
    with pytest.raises(DirectoryCreationError):
        _make_dir('/Users/a.cheremushkin/hello/test')


@pytest.mark.parametrize('path, expected',
                         [('test-file.jpg', True),
                          ('test-file2.html', False),
                          ('test-file3.css', False),
                          ('test-file4.png', True)
                          ])
def test_check_image_extension(path, expected):
    assert _check_image_extension(path) is expected


@pytest.mark.parametrize('resource_link, webpage_url, expected',
                         [('http://test.com/test/path.png', TEST_URL, True),
                          ('test.com/test/path.css', TEST_URL, True),
                          ('https://test-url3.com', TEST_URL2, False),
                          ])
def test_is_true_domain2(resource_link, webpage_url, expected):
    assert _is_true_domain(resource_link, webpage_url) is expected


def test_raise_dowload():
    with tempfile.TemporaryDirectory() as tmp:
        with pytest.raises(MissingSchemaError):
            download('url-without-scheme.ru', tmp)


def test_raise_file_worker():
    with tempfile.TemporaryDirectory() as tmp:
        path_to_save = os.path.join(tmp, 'test-file.txt')
        data = 'test-data'
        FileWorker(RecordingData(
            data=data,
            path_to_save_data=path_to_save)).save_text_data()
        assert os.path.isfile(path_to_save)
