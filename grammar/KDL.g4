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

node_id     : NUMBER ;

port_id     : NUMBER ;

port        : COLON port_id ;

node        : '(' NODEPREFIX node_id port? ')' ;

node_settings: node COLON json ;

nodes       : 'Nodes {' node_settings (COMMA node_settings)* '}' ;

source_node   : node ;

destination_node  : node ;

connection  : source_node (ARROW|VARIABLE_ARROW) destination_node ;

global_variables: 'variables: ' json COMMA ;

workflow: 'Workflow {' global_variables? connection (COMMA connection)* '}' ;

