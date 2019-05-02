/*
 * KDL
 */

grammar KDL;
import JSON;

WS          : [ \t\n\r]+ -> skip ;

ARROW       : '-->' ;

VARIABLE_ARROW: '~~>' ;

NODEPREFIX  : 'n' ;

COLON       : ':' ;

COMMA       : ',' ;

DOT         : '.' ;

CONNECTION_TAG : '"connections"';

META_IN_TAG : '"meta_in_ports"' ;

META_OUT_TAG : '"meta_out_ports"' ;

META_IN : 'META_IN' ;

META_OUT: 'META_OUT' ;

node_id     : NUMBER (DOT NUMBER)* ;

port_id     : NUMBER ;

port        : COLON port_id ;

node        : '(' NODEPREFIX node_id port? ')' ;

node_settings: node COLON json ;

source_node   : node ;

destination_node  : node ;

connection  : source_node ARROW destination_node ;

var_connection : source_node VARIABLE_ARROW destination_node ;

meta_in_node : '(' META_IN port ')' ;

meta_out_node : '(' META_OUT port ')' ;

meta_connection: meta_in_node ARROW destination_node
    | source_node ARROW meta_out_node
    | meta_in_node ARROW meta_out_node ;

meta_var_connection: meta_in_node VARIABLE_ARROW destination_node
    | source_node VARIABLE_ARROW meta_out_node
    | meta_in_node VARIABLE_ARROW meta_out_node ;

meta_in_ports: META_IN_TAG COLON json ;

meta_out_ports: META_OUT_TAG COLON json ;

meta_settings: node COLON '{' STRING COLON STRING ','
	                          STRING COLON STRING ','
	                          CONNECTION_TAG COLON '{'
	                          (connection | var_connection | meta_connection | meta_var_connection)
	                          (COMMA (connection | var_connection | meta_connection| meta_var_connection))*
	                          '}' COMMA
	                          meta_in_ports COMMA
	                          meta_out_ports
	                      '}';

node_list: (node_settings | meta_settings)
                    (COMMA (node_settings | meta_settings))* ;

nodes       : 'Nodes {' node_list? '}' ;

global_variables: '"variables": ' json COMMA? ;

workflow_connections: CONNECTION_TAG COLON '{'
                           (connection|var_connection)
                            (COMMA (connection|var_connection))*
                       '}' ;

workflow: 'Workflow {' global_variables?
                       workflow_connections?
                    '}' ;
