#---------------------------------------------------------------------
# Arquivo	: Makefile
# Conteúdo	: compilar o programa operation
# Autor		: Antônio Neves. (antonioneto@dcc.ufmg.br)
# Histórico	: 2023-03-28 - arquivo criado
#---------------------------------------------------------------------
# Opções	: make all - compila tudo
#		: make clean - remove objetos e executável
#---------------------------------------------------------------------

CC = gcc
SRC = src
OBJ = obj
INC = include
BIN = bin
OBJS = $(OBJ)/main.o $(OBJ)/circular_queue.o $(OBJ)/stack.o
HDRS = $(INC)/circular_queue.h $(INC)/stack.h 
CFLAGS = -Wall -c -g -I $(INC)

EXE = $(BIN)/main

all: run
run: $(EXE)
	$(EXE) 

$(BIN)/main: $(OBJS)
	$(CC) -o $(BIN)/main $(OBJS)

$(OBJ)/main.o: $(HDRS) $(SRC)/main.c
	$(CC) $(CFLAGS) -o $(OBJ)/main.o $(SRC)/main.c

$(OBJ)/circular_queue.o: $(HDRS) $(SRC)/circular_queue.c
	$(CC) $(CFLAGS) -o $(OBJ)/circular_queue.o $(SRC)/circular_queue.c

$(OBJ)/stack.o: $(HDRS) $(SRC)/stack.c
	$(CC) $(CFLAGS) -o $(OBJ)/stack.o $(SRC)/stack.c
	
clean:
	rm -f $(EXE) $(OBJS) gmon.out
