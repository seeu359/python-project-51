import pytest
import requests_mock
import pathlib
import tempfile
import requests
import os
from bs4 import BeautifulSoup
from page_loader.lib.exceptions import DirectoryCreationError, \
    MissingSchemaError, ResourceDownloadError, HttpRequestError
from page_loader.lib.downloader import _resources_validator, \
    _save_resources, _get_bytes_data, _check_image_extension, \
    _is_true_domain, _make_dir, _get_resources
from page_loader.lib.file_handling import save_data
from page_loader.lib.url_handling import PathHandler, build_resource_url, \
    check_url
from page_loader.loader import download
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
            image_data = _get_bytes_data(TEST_URL)
            path = pathlib.Path(tmp_dir, 'test.png')
            save_data(image_data, str(path), 'wb')
            image = read_bytes_data(path)
            assert image == requests.get(TEST_URL).content


#
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


def test_get_resources_set(html_fixture):
    soup = BeautifulSoup(html_fixture, 'html.parser')
    img, link, script = _get_resources(soup, TEST_URL3)
    assert len(img) == 1
    assert len(link) == 2
    assert len(script) == 1


@pytest.mark.parametrize('index, tag, attr, expected,',
                         [(0, 'img', 'src', 1),
                          (1, 'link', 'href', 2),
                          (2, 'script', 'src', 1),
                          ]
                         )
def test_is_true_domain(index, tag, attr, expected, test_bs_object):
    resource_set = test_bs_object[index]
    result_set = _resources_validator(resource_set, tag, attr, TEST_URL2)
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


def test_raise_download():
    with tempfile.TemporaryDirectory() as tmp:
        with pytest.raises(MissingSchemaError):
            download('url-without-scheme.ru', tmp)


def test_raise_file_worker():
    with tempfile.TemporaryDirectory() as tmp:
        path_to_save = os.path.join(tmp, 'test-file.txt')
        data = 'test-data'
        save_data(data, path_to_save, 'w')
        assert os.path.isfile(path_to_save)


@pytest.mark.parametrize('status_code',
                         [404,
                          500,
                          ]
                         )
def test_make_request_error404(status_code):
    with pytest.raises(ResourceDownloadError):
        with requests_mock.Mocker() as mock:
            mock.get(TEST_URL, text='test data', status_code=status_code)
            make_request(TEST_URL)


def test_make_request_timeout():
    with pytest.raises(HttpRequestError):
        with requests_mock.Mocker() as mock:
            mock.get(TEST_URL, exc=requests.exceptions.Timeout)
            make_request(TEST_URL)


@pytest.mark.parametrize('path',
                         ['/another_test_dir',
                          '',
                          ]
                         )
def test_make_dir_permission_error(path):
    with pytest.raises(DirectoryCreationError):
        with tempfile.TemporaryDirectory() as tmp:
            dir_without_rights = os.path.join(tmp, 'testdir')

            os.makedirs(name=dir_without_rights, mode=0o664)
            _make_dir(dir_without_rights + path)
