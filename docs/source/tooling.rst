Tooling
=======

The development team established a handful of supporting development tools and scripts, 
which can be found within the scripts folder. ::

   ❯ tree scripts
   scripts
   ├── build-docs.sh
   ├── e2e.sh
   ├── format.sh
   ├── generate-parser.sh
   ├── perf-test.py
   └── quality-check.sh

Before executing any of the scripts download the development dependencies by 
executing the following command. ::

   pip install -e '.[dev]'

build-docs.sh
-------------

In order to construct the documentation you are reading now, the team has utilized 
sphinx for generating this static website.  It takes the rst files as defined within 
``docs/source`` of the project's root directory as input to generate the static 
assets.  You can learn about at `http://www.sphinx-doc.org <http://www.sphinx-doc.org>`_.

To build the documentation for viewing locally, then execute ``scripts/build-docs.sh`` 
from the root directory of the project.

To view the generated documentation, then open ``docs/build/html/index.html`` from the 
root directory into a web browser.

e2e.sh
----------------

The end-to-end script provides a deterministic test for validating the 
kdlc application by compiling kdl and decompiling knwf archives.

To run the script, firstly install ``kdlc`` by following the kdlc 
`installation instructions <kdlc.html>`_.  Then execute ``scripts/e2e.sh`` 
from the root directory of the project.

format.sh
---------

The format shell script runs an opinionated code formatter across the project called 
black.  More information about black can be found at 
`https://github.com/ambv/black <https://github.com/ambv/black>`_.

To run the code formatter, then execute ``scripts/format.sh`` from the root directory 
of the project.

generate-parser.sh
------------------

To support the parsing of KDL, the team elected to utilize ANTLR (ANother Tool for 
Language Recognition).  The generate parser shell script executes ANTLR against our 
defined grammar files within grammar folder found within the root of the project.  

Before executing the shell script, you must install ANTLR first in the matching location 
found within the shell script.  The installation instructions for ANTLR can be found at 
`https://www.antlr.org/ <https://www.antlr.org/>`_.  At the time of writing this 
documentation, ANTLR is on version 4.7.2 and our shell script expects you to place the 
jar within the ``/usr/local/lib`` directory.

To run the generate parser shell script after installing ANTLR, then execute 
``scripts/generate-parser.sh`` from the root directory of the project.

perf-test.py
------------

To performance test ``kdlc`` with load, the performance test script constructs a KDL 
document with a string of node connections, then compiles the document to a knwf archive 
and subsequently decompiles the archive to a KDL document while capturing time metrics.  The 
script helps identify performance degradation as a result of implementation decisions.

To run the script, firstly install ``kdlc`` by following the kdlc 
`installation instructions <kdlc.html>`_.  
Then run ``python3 scripts/perf-test.py`` to run with 2 nodes by default or provide an 
argument to run with a desired amount of nodes, such as 
``python3 scripts/perf-test.py 10``.

quality-check.sh
----------------

The quality check runs a suite of tooling to insure the quality of our deliverable. 
This particular script gets run within our continuous integration pipeline on code 
deliveries.

It runs the following tooling and will exit on failure.

* `black <https://github.com/ambv/black>`_ for code formatting
* `flake8 <http://flake8.pycqa.org>`_ for style guide enforcement
* `mypy <http://mypy-lang.org/>`_ for static type checking
* `pytest <https://docs.pytest.org>`_ for test execution
* `sphinx <http://www.sphinx-doc.org>`_ for validating documentation compilation

To run the quality check script, then execute ``scripts/quality-check.sh`` from the 
root directory of the project.
