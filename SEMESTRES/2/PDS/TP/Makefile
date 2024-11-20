TESTS = ./tests
SRC = ./src

all: clean
	g++ main.cpp ${SRC}/search_system.cpp
	clear
	./a.out

clean:
	clear

test: clean
	g++ ${TESTS}/utils_tests.cpp
	./a.out
	g++ ${TESTS}/search_system_tests.cpp ${SRC}/search_system.cpp
	./a.out