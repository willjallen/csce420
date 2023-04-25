# Makefile

# Compiler
CC = g++

# Compiler flags
CFLAGS = -std=c++11 -Wall -Wextra -pedantic

# Source files
SRC = dpll.cpp

# Object files
OBJ = $(SRC:.cpp=.o)

# Executable
EXEC = dpll

# Default target
all: $(EXEC)

# Linking object files
$(EXEC): $(OBJ)
	$(CC) $(OBJ) -o $(EXEC)

# Compiling source files
%.o: %.cpp
	$(CC) $(CFLAGS) -c $< -o $@

# Clean
clean:
	rm -f $(OBJ) $(EXEC)