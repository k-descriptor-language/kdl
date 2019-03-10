import pytest
from shutil import rmtree
from contextlib import suppress
from .context import kdlc


@pytest.fixture(scope="session")
def my_setup(request):
    print('\nDoing setup')

    def fin():
        print('\nDoing teardown')
        with suppress(FileNotFoundError):
            rmtree(f'{kdlc.INPUT_PATH}')
            rmtree(f'{kdlc.OUTPUT_PATH}')
    request.addfinalizer(fin)
