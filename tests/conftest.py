import pytest
from page_loader import page_loader


@pytest.fixture()
def _result_format_path():
    path = 'https://ru.hexlet.io/projects/51/members/24681'
    save_path = 'var/tmp'
    return page_loader.get_format_path(path, save_path)


@pytest.fixture()
def _fixture_hexlet_courses():
    with open('tests/fixtures/ru-hexlet-io-courses') as _fixture:
        fixture = _fixture.read()
    return fixture



