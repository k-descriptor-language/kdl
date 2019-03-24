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

connection  : node ARROW node ;

node_settings: node COLON json ;
