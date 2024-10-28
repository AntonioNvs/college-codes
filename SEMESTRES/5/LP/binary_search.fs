1048576 CONSTANT buffer-size  
CREATE buffer buffer-size allot  

CREATE v buffer-size ALLOT

VARIABLE index
VARIABLE fileid  
VARIABLE ior  
variable result

\ Adiciona os conteúdos do arquivo no buffer
: read-file
   r/o open-file throw fileid ! 
  buffer buffer-size fileid @ read-file drop
  dup ior ! 
  drop
  cr
;

: close-file ( -- )
  fileid @ close-file throw
;

\ Rotina de leitura de arquivo
: main ( -- )
  read-file
  close-file
;

: transform-to-vector ( -- )
  0 index !
  ior @ 0 DO 
    buffer I + C@ 48 - dup
    0>= IF v index @ CELLS + ! index @ 1 + index ! ELSE drop THEN
  LOOP
;

: print
  CELLS OVER + SWAP
  DO I @ . 1 CELLS +LOOP 

  CR
;

\ Coloca v[i] no topo do stack
: v@ ( i -- v[i] )  
  cells v + @
;


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
    v@ rot = 
    if .
    else ." -1 " drop
    then
;

\ Exemplo de uso: primeiro elemento >= 3 em v[0]...v[4]
\ 3 0 4 foo 

\ Retorna o valor em uma posição do vetor
: get-value ( -- n )
  result @
  cells
  v +
  @
;

: check-equal ( n1 n2 -- )
  =
  if
    cr ." TRUE " cr
  else
    cr ." FALSE " cr
  then ;

: sqrt ( n -- f )
    s>f fsqrt f>s
;

\ caminho do arquivo passado por linha de comando
variable input-file
1 arg input-file !

input-file @ main
transform-to-vector

index @ sqrt CONSTANT SIZE
index @ 1 - index !

\ inteiro a ser procurado passado por linha de comando
variable input-int
2 arg s>number drop input-int !

input-int @ 0 index @ foo result !

variable value
get-value value !

input-int @ value @ check-equal

bye