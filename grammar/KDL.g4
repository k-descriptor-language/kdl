grammar KDL;

WS          : [ \t\n]+ -> skip ;

NUMBER      : '0' | [1-9] [0-9]* ;

ANY         : . ;

node        : '(n' NUMBER ')' ;

json        : '{' (.)*? '}' ;

node_settings : node ':' json ;
