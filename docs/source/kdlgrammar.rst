KDL Grammar
===========

KDL serves as a textual representation of KNIME workflows.  The workflows consist of a variety 
of nodes with differing responsibilities, which connect with edges to form a graph.  This 
domain language provides the capability to modify and author workflows to run within KNIME.

Nodes
-----


Workflow
--------

A KDL workflow is defined by the connections between nodes in the following format,
where the node_id is a reference to the id of node definition within the ``Nodes {...}``
section above ::

   (<source_node_id>:<source_port>)-->(<dest_node_id>:<dest_port>)

All of the various connections are encapsulated within the ``"connections"`` section of a Workflow
wrapper object. For example the following denotes a simple workflow where the output
of node_1:port_1 is connected to the input of node_2:port_1, whose output is connected to
node_3:port_1 ::

   Workflow {
       "connections": {
           (n1:1)-->(n2:1),
           (n2:1)-->(n3:1)
       }
   }

This example is the representation of the above KDL within KNIME

.. figure:: images/Workflow1.png
   :align:  center

Nodes may have multiple inports and outports depending on the node's definition but this
is handled simply by updating the source/dest port in the connection definition. In the
following example, node_3 is a Joiner node which has multiple inports ::

   Workflow {
       "connections": {
           (n1:1)-->(n3:1),
           (n2:1)-->(n3:2),
           (n3:1)-->(n4:1)

       }
   }

This example is the representation of the above KDL within KNIME

.. figure:: images/Workflow2.png
   :align:  center

Workflow Variables
------------------


Global Variables
++++++++++++++++


Variable Connections
++++++++++++++++++++


used_variable and exposed_variable
++++++++++++++++++++++++++++++++++


Metanodes
---------


Parent/Child IDs
++++++++++++++++


Meta In/Out Ports
+++++++++++++++++


Connections
+++++++++++


Wrapped Metanodes
-----------------


WrappedInput/WrappedOut
+++++++++++++++++++++++


