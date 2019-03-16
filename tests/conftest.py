import pytest
import kdlc
from shutil import rmtree
import os

# from .context import kdlc

test_generated_dir = os.path.dirname(__file__) + "/generated/"


@pytest.fixture(scope="session")
def my_setup(request):
    print("\nDoing setup")

    def fin():
        print("\nDoing teardown")

        if os.path.exists(test_generated_dir):
            rmtree(test_generated_dir)

        kdlc.TMP_INPUT_DIR.cleanup()
        kdlc.TMP_OUTPUT_DIR.cleanup()

    request.addfinalizer(fin)
