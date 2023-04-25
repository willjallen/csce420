# DPLL Solver
This program is a DPLL solver implementation for propositional logic. It takes a CNF (conjunctive normal form) file as input and determines whether the given knowledge base (KB) is satisfiable or not. If it is satisfiable, the program outputs the satisfying model and lists the true propositions.

## Usage
To compile the program, use a C++ compiler supporting at least the C++14 standard:

```
g++ -std=c++14 -o dpll dpll.cpp
```

Run the compiled program with the following command:

```
./dpll <filename> <literal>* [+UCH]
```

- `<filename>`: The input CNF file containing the knowledge base.
- `<literal>*`: (Optional) A list of extra literals to be added to the knowledge base as unit clauses.
- `+UCH`: (Optional) Use the unit clause heuristic to optimize the search.