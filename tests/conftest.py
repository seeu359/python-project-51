import pytest
from page_loader import page_loader
import tempfile
import os
import pathlib

TEST_LINK = 'http://test.com'

@pytest.fixture()
def _result_format_link():
    link = 'https://ru.hexlet.io/projects/51/members/24681'
    return page_loader.get_format_link(link)


@pytest.fixture()
def _fixture_hexlet_courses():
    with open('tests/fixtures/hexlet-courses-fixture.html') as _fixture:
        fixture = _fixture.read()
    return fixture


@pytest.fixture()
def _fixture_picture():
    with open('tests/fixtures/picture_from_html.png', 'rb') as _fixture:
        fixture = _fixture.read()
    return fixture

@pytest.fixture()
def _download_pic():
    with tempfile.TemporaryDirectory() as tmp:
        webpage_path = 'tests/fixtures/hexlet-courses-fixture.html'
        page_loader.download_pictures(webpage_path, tmp, TEST_LINK)
        for i in os.listdir(tmp):
            path = pathlib.Path(tmp, i)
            with open(path, 'rb') as test_pic:
                test_picture = test_pic.read()
                return test_picture
