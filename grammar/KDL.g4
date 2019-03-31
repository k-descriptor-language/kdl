/*
 * KDL
 */

grammar KDL;
import JSON;

WS          : [ \t\n]+ -> skip ;

ARROW       : '-->' ;

VARIABLE_ARROW: '~~>' ;

NODEPREFIX  : 'n' ;

COLON       : ':' ;

node_id     : NUMBER ;

port_id     : NUMBER ;

port        : COLON port_id ;

node        : '(' NODEPREFIX node_id port? ')' ;

node_settings: node COLON json ;

nodes       : 'Nodes {' node_settings+ '}' ;

source_node   : node ;

destination_node  : node ;

connection  : source_node (ARROW|VARIABLE_ARROW) destination_node ;

workflow: 'Workflow {' connection+ '}' ;

