import pytest
from .context import kdlc


@pytest.fixture(scope="session")
def my_setup(request):
    print("\nDoing setup")

    def fin():
        print("\nDoing teardown")
        kdlc.TMP_INPUT_DIR.cleanup()
        kdlc.TMP_OUTPUT_DIR.cleanup()

    request.addfinalizer(fin)
