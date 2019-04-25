Future Enhancements
===================

Over the course of development we have identified additional areas 
of opportunities for improvement with KDLC and kdlc, which were outside 
of the scope of the initial set of requirements.

1. Wrapped Metanodes
--------------------

The existing implementation of KDL and kdlc supports metanodes, but 
does not support wrapped metanodes.  Metanodes serve as a utility for
cleaning up workflows through node organization.  Alternatively, wrapped
metanodes provide a means for encapsulating complete functionality.

KNIME delves deeper into the details in the following article.

`Metanodes for Reusability: A short story of metanodes, wrapped metanodes, and metanode templates. <https://www.knime.com/blog/wrapped-metanodes-and-metanode-templates-in-knime-analytics-platform>`_

2. Bundling Data in knwf Archives
---------------------------------

KNIME offers the ability to introduce relative links to local workflow 
data within a user's KNIME workspace with the knime:// denotation prefixed 
to the relative location.  Subsequently, KNIME bundles this data within KNIME
archives when exporting a workflow.  When converting a knwf archive to KDL, 
the produced knwf archive does not contain this bundled data and a user will 
have to manually link to the path of the data.
