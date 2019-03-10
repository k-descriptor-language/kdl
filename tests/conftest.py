import pytest
from shutil import rmtree
from .context import kdlc


@pytest.fixture(scope="session")
def my_setup(request):
    print('\nDoing setup')

    def fin():
        print('\nDoing teardown')
        rmtree(f'{kdlc.INPUT_PATH}/TestWorkflow')
    request.addfinalizer(fin)
