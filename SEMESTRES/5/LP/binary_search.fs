\ Definindo o array v = [ 2 2 ... 7 ]
create v 2 , 2 , 4 , 6 , 7 ,

\ Coloca v[i] no topo do stack
: v@ ( i -- v[i] )  
  cells v + @ ; 

\ Busca binária: 
\ ret == menor índice i \in [lo, hi] tal que v[i] >= x
: foo ( x lo hi -- res )
    begin 2dup < 
    while
    2dup + 2 /
    dup v@ 4 pick >=
        if swap drop
        else 1 + rot drop swap
        then 
    repeat 
    rot 2drop 
    ;

\ Exemplo de uso: primeiro elemento >= 3 em v[0]...v[4]
\ 3 0 4 foo 
