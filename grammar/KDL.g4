/*
 * KDL
 */

grammar KDL;
import JSON;

WS          : [ \t\n]+ -> skip ;

ARROW       : '-->' ;

NODEPREFIX  : 'n' ;

COLON       : ':' ;

node_id     : NUMBER ;

port_id     : NUMBER ;

port        : COLON port_id ;

node        : '(' NODEPREFIX node_id port? ')' ;

source_node   : node ;

destination_node  : node ;

node_settings: node COLON json ;

connection  : source_node ARROW destination_node ;

