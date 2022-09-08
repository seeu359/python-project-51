import pytest
from page_loader import page_loader


@pytest.fixture()
def _result_format_link():
    link = 'https://ru.hexlet.io/projects/51/members/24681'
    return page_loader.get_format_link(link)


@pytest.fixture()
def _fixture_hexlet_courses():
    with open('tests/fixtures/hexlet-courses-fixture') as _fixture:
        fixture = _fixture.read()
    return fixture



