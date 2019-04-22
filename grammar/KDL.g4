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

node_id     : NUMBER (DOT NUMBER)* ;

port_id     : NUMBER ;

port        : COLON port_id ;

node        : '(' NODEPREFIX node_id port? ')' ;

node_settings: node COLON json ;

meta_settings: node COLON '{' STRING COLON STRING ','
	                          STRING COLON STRING ','
	                          CONNECTION_TAG COLON '{'
	                          (connection | var_connection | meta_connection | meta_var_connection)
	                          (COMMA (connection | var_connection | meta_connection| meta_var_connection))*
	                          '}'
	                      '}';

nodes       : 'Nodes {' (node_settings | meta_settings)
                        (COMMA (node_settings | meta_settings))* '}' ;

source_node   : node ;

destination_node  : node ;

meta_in : 'META_IN' ;

meta_in_node : '(' meta_in port ')' ;

meta_out: 'META_OUT' ;

meta_out_node : '(' meta_out port ')' ;

connection  : source_node ARROW destination_node ;

var_connection : source_node VARIABLE_ARROW destination_node ;

meta_connection: meta_in_node ARROW destination_node
    | source_node ARROW meta_out_node ;

meta_var_connection: meta_in_node VARIABLE_ARROW destination_node
    | source_node VARIABLE_ARROW meta_out_node ;

global_variables: '"variables": ' json COMMA ;

workflow: 'Workflow {' global_variables?
                       CONNECTION_TAG COLON '{'
                           (connection|var_connection)
                            (COMMA (connection|var_connection))*
                       '}'
                    '}' ;
