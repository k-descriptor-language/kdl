KDLC
====

The kdlc application runs on Python 3.7.  The details below illustrate an 
installation procedure and how to utilize the application for working 
with KDL.

Installation Procedure
----------------------

1. Install Python 3.7 from `https://www.python.org/ <https://www.python.org/>`_
2. Install Git from `https://git-scm.com/ <https://git-scm.com/>`_
3. Open a terminal
4. Navigate to a working directory with ``cd``
5. Clone the kdlc project by executing ``git clone git@github.com:k-descriptor-language/kdl.git``
6. Navigate into the kdlc project space by executing ``cd kdl``
7. Install kdlc by executing ``python3 setup.py install``

User Guide
----------

The following sections demonstrate the various available operations with kdlc.

Help
++++

Execute ``kdlc --help`` within your terminal for an overview of available flags. ::

   ❯ kdlc --help
   Usage: kdlc [OPTIONS]

   Options:
     -o, --output TEXT            The output file, either .knwf or .kdl  [required]
     -i, --input PATH             The input file, either .knwf or .kdl  [required]
     -d, --debug                  Print debug logging to stdout
     -tp, --templates_path PATH   Path to a custom templates catalogue
     --help                       Show this message and exit.

Compile KDL to knwf Archive
+++++++++++++++++++++++++++

Execute kdlc with a KDL document as the input argument and define a filename for 
the output knwf archive. ::

   kdlc -i complex.kdl -o workflow.knwf

Compile KDL to knwf Archive with a custom templates path
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Execute kdlc with a KDL document as the input argument and define a filename for
the output knwf archive. ::

   kdlc -i complex.kdl -o workflow.knwf -tp PATH_TO_CUSTOM_TEMPLATE_LIBRARY

Decompile knwf Archive to KDL
+++++++++++++++++++++++++++++

Execute kdlc with a knwf archive as the input argument and define a filename for 
the output KDL document. ::

   kdlc -i complex.knwf -o workflow.kdl
