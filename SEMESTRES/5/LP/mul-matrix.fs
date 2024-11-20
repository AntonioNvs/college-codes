1048576 CONSTANT buffer-size  
CREATE buffer buffer-size allot  

CREATE vector_a buffer-size ALLOT
CREATE vector_b buffer-size ALLOT
CREATE vector_c buffer-size ALLOT


VARIABLE index
VARIABLE fileid  
VARIABLE ior  

: read-file
   r/o open-file throw fileid ! 
  buffer buffer-size fileid @ read-file drop
  dup ior ! 
  drop
;

: close-file ( -- )
  fileid @ close-file throw
;

: reading-file-process ( -- )
  read-file
  close-file
;

: pow ( base exponent -- result )
  1 swap 0 ?DO
    over *
  LOOP
  nip 
;

: sqrt ( n -- f )
    s>f fsqrt f>s
;

VARIABLE buffer-index

VARIABLE pos

CREATE aux-num buffer-size ALLOT
VARIABLE aux-index
VARIABLE len-num
VARIABLE num

: transform-to-vector_a ( -- )
  0 index !
  0 buffer-index !
  BEGIN
    buffer-index @ ior @ <
  WHILE
    buffer buffer-index @ + C@ 48 - 0>= buffer buffer-index @ + C@ 48 - -3 = OR
    IF 
      0 aux-index !
      1 pos !

      BEGIN
        buffer-index @ ior @ <
        buffer buffer-index @ + C@ 48 - 0>=
        buffer buffer-index @ + C@ 48 - -3 =
        OR
        AND
      WHILE
        buffer buffer-index @ + C@ 48 - dup dup
        
        -3 = IF -1 pos ! ELSE
          aux-num aux-index @ CELLS + ! 
          aux-index @ 1 +  aux-index !
        THEN
        buffer-index @ 1 + buffer-index !
      REPEAT 

      0 num !
      aux-index @ 1 - aux-index !
      aux-index @ len-num !
      
      BEGIN
        aux-index @ 0>=
      WHILE
        num @ aux-num aux-index @ CELLS + @ 10 len-num @ aux-index @ - pow * + num !
        aux-index @ 1 - aux-index !
      REPEAT
      
      num @ pos @ * vector_a index @ CELLS + ! index @ 1 + index ! 
    THEN
    
    buffer-index @ 1 + buffer-index !
  REPEAT
;

: transform-to-vector_b ( -- )
   0 index !
  0 buffer-index !
  BEGIN
    buffer-index @ ior @ <
  WHILE
    buffer buffer-index @ + C@ 48 - 0>= buffer buffer-index @ + C@ 48 - -3 = OR
    IF 
      0 aux-index !
      1 pos !

      BEGIN
        buffer-index @ ior @ <
        buffer buffer-index @ + C@ 48 - 0>=
        buffer buffer-index @ + C@ 48 - -3 =
        OR
        AND
      WHILE
        buffer buffer-index @ + C@ 48 - dup dup
        
        -3 = IF -1 pos ! ELSE
          aux-num aux-index @ CELLS + ! 
          aux-index @ 1 +  aux-index !
        THEN
        buffer-index @ 1 + buffer-index !
      REPEAT 

      0 num !
      aux-index @ 1 - aux-index !
      aux-index @ len-num !
      
      BEGIN
        aux-index @ 0>=
      WHILE
        num @ aux-num aux-index @ CELLS + @ 10 len-num @ aux-index @ - pow * + num !
        aux-index @ 1 - aux-index !
      REPEAT
      
      num @ pos @ * vector_b index @ CELLS + ! index @ 1 + index ! 
    THEN
    
    buffer-index @ 1 + buffer-index !
  REPEAT
;

: print
  CELLS OVER + SWAP
  DO I @ . 1 CELLS +LOOP 

  CR
;

VARIABLE fileA
VARIABLE fileB
VARIABLE fileC
VARIABLE fileAlength
VARIABLE fileBlength
VARIABLE fileClength

: read-arg ( -- )
  next-arg 2dup
  fileA swap move
  fileAlength !
  drop

  next-arg 2dup
  fileB swap move
  fileBlength !
  drop

  next-arg 2dup
  fileC swap move
  fileClength !
  drop
;

read-arg

fileA fileAlength @
reading-file-process
transform-to-vector_a 

fileB fileBlength @
reading-file-process
transform-to-vector_b 

index @ sqrt CONSTANT SIZE

\ vector_a index @ print
\ vector_b index @ print

VARIABLE idx
VARIABLE jdx
VARIABLE kdx
VARIABLE sum
: matrix_mul 
   SIZE 0 DO 
      I idx ! 
      SIZE 0 DO  
         I jdx !
         0 sum !
         SIZE 0 DO 
            I kdx !
            vector_a kdx @ idx @ SIZE * + CELLS + @ vector_b jdx @ kdx @ SIZE * + CELLS + @ * sum +!
         1 +LOOP 
         sum @ vector_c jdx @ idx @ SIZE * + CELLS + !
      1 +LOOP
   1 +LOOP ;


matrix_mul

: print_final_matrix ( cell-count -- ) 0 
   DO vector_c I CELLS + @ . I 1 + SIZE MOD 0= IF CR THEN LOOP
;

\ index @ print_final_matrix

CREATE word 1 ALLOT

: write-array-to-file ( -- )
  w/o create-file throw fileid !

  SIZE 0 do
    I idx ! 
    SIZE 0 do
      I jdx !
      vector_c jdx @ idx @ SIZE * + CELLS + @

      dup 0< IF
        45 word 0 + !
        word 1 fileid @ write-file throw
        abs
      THEN

      0 <# #S #>
      fileid @ write-file throw
      
      32 word 0 + !
      word 1 fileid @ write-file throw
    LOOP
    10 word 0 + !
    word 1 fileid @ write-file throw
  LOOP

  close-file
;

fileC fileClength @
write-array-to-file