Future Enhancements
===================

Over the course of development we have identified additional areas 
of opportunities for improvement with KDLC and kdlc, which were outside 
of the scope of the initial set of requirements.

1. Retain Node Descriptions
---------------------------

Within the KNIME GUI, nodes have a free text label underneath themselves, 
which can assist users with organization and management of their workflows.  
Retaining this description and exposing it within KDL can provide an improved 
user experience for individuals authoring and editing workflows with KDL.

2. Bundling Data in knwf Archives
---------------------------------

KNIME offers the ability to introduce relative links to local workflow 
data within a user's KNIME workspace with the knime:// denotation prefixed 
to the relative location.  Subsequently, KNIME bundles this data within KNIME
archives when exporting a workflow.  When converting a knwf archive to KDL, 
the produced knwf archive does not contain this bundled data and a user will 
have to manually link to the path of the data.

3. Merging Workflows
--------------------

KDL presents opportunities for improved automation and development of workflows.  
The ability to merge two workflows into a single workflow presents itself as a 
time saving feature, which could remove a previously tedious process.
