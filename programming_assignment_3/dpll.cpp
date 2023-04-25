#include <fstream>
#include <vector>
#include <iostream>
#include <algorithm>
#include <sstream>
#include <unordered_map>
#include <string>
#include <iterator>
#include <cstring>
#include <cassert>


/**
 * Given a KB with sentence (A v B) ^ (B v ~C)  
 * Then NamedSymbols: [("A", 1), ("B", 2), ("C", 3)]
 * Symbols: [1, 2, 3]
 * A clause would be: [1, 2]
 * All of the clauses would be ClauseSet: [[1,2], [2, -3]] 
 * A model is an assignment (paired index wise(+1) to the symbols)
 * [0, 1, -1] means A is unassigned, B is true, C is false
 *  ^  ^  ^
 *  1  2  3
 */


typedef std::vector<std::pair<std::string, int>> NamedSymbols;
typedef std::vector<int> Symbols;
typedef std::vector<int> Clause;
typedef std::vector<std::vector<int>> ClauseSet;
typedef std::vector<int> Model;


struct KB{
    Symbols symbols;
    NamedSymbols namedSymbols;
    ClauseSet clauses;
};

/**
 * @brief Utility function to remove an element from a vector
 * 
 * @param vec 
 * @param valueToRemove 
 */
void removeItem(std::vector<int>& vec, int valueToRemove) {
    auto newEnd = std::remove(vec.begin(), vec.end(), valueToRemove);
    vec.erase(newEnd, vec.end());
}

/**
 * @brief Get the value of a symbol, given a model
 * 
 * @param symbol 
 * @param model 
 * @return true 
 * @return false 
 */
int getModelValue(const int symbol, const Model& model){
    int val = model[abs(symbol) - 1];
    
    if(val == 0) return 0;
    
    return symbol < 0 ? -val : val;
}

/**
 * @brief Evaluate the truthyness of a clause, given a model 
 * 
 * @param clause 
 * @param model 
 * @return int 
 */
int evaluateClause(const Clause& clause, const Model& model){
    int result = -1;
    for(const auto symbol : clause){
        int modelValue = getModelValue(symbol, model);
        
        if(modelValue == 0) return 0;
        if(modelValue == 1) return 1;

    }
    return result;
}


/**
 * @brief This function finds a clause which, according to the model, has exactly one undecided value 
 * and the rest of the values are unsatisied. In the case that no unit clause is found, an empty clause is returned.
 * 
 * @param clauses 
 * @param model 
 * @return Clause 
 */
Clause findUnitClause(const ClauseSet& clauses, const Model& model){
    Clause unitClause;
    for(const auto& clause : clauses){
        int undecidedValues = 0;
        bool hasSatisfiedValue = false;
        for(const auto symbol : clause){
            int modelValue = getModelValue(symbol, model);
            
            if(modelValue == 0) undecidedValues++;
            if(modelValue == 1) hasSatisfiedValue = true;
        }

        if(undecidedValues == 1 && !hasSatisfiedValue){
            unitClause = clause;
        }
    }

    return unitClause;
}
/**
 * @brief Given a unit clause, find which particular symbol is undecided and which value for this symbol would make the clause true
 * 
 * @param unitClause 
 * @param model 
 * @return std::pair<int, int> undecidedSymbol, necessaryValue
 */
std::pair<int, int> getUnitClauseSymbolAndValue(const Clause& unitClause, const Model& model){
    int undecidedSymbol;
    int necessaryValue;
    for(const auto symbol : unitClause){
        if(getModelValue(symbol, model) == 0){
            undecidedSymbol = symbol;
            necessaryValue = (symbol < 0 ? -1 : 1);
            break;
        }
    }

    return std::pair<int,int>(undecidedSymbol, necessaryValue);
}

/**
 * @brief Print the state of the model using named symbols 
 * 
 * @param namedSymbols 
 * @param model 
 */
void printModel(const NamedSymbols& namedSymbols, const Model& model){
    std::cout << "model: {";
    for (size_t i = 0; i < namedSymbols.size(); i++) {
        std::cout << "'" << namedSymbols[i].first << "': " << model[i];
        if (i != namedSymbols.size() - 1) {
            std::cout << ", ";
        }
    }
    std::cout << "}" << std::endl;
}

// Global vars
int dpllCalls = 0;
Model solutionModel;

bool runDPLL(ClauseSet clauses, Symbols symbols, NamedSymbols namedSymbols, Model model, bool useUnitClauseHeuristic){
    dpllCalls++;
    printModel(namedSymbols, model);
    // If some clause in clauses is false in model then return false
    // If every clause in clauses is true in model, then return true
    bool allTrue = true;
    for(const auto& clause : clauses){
        int result = evaluateClause(clause, model);
        if(result == -1){
            std::cout << "Backtracking" << std::endl;
            return false;
        }else if(result == 0){
            allTrue = false;
        }
    }

    if(allTrue){
        solutionModel = model;
        return true;
    }

    // **NOT IMPLEMENTING**
    // P, value <- Find-pure-symbol(symbols, clauses, model)
    // if P is non-null then return DPLL(clauses, symbols - P, model union {P=value})

    if(useUnitClauseHeuristic){
        // P, value <- Find-unit-clause(clauses, model)

        // Find a unit clause
        Clause unitClause = findUnitClause(clauses, model);

        // Check that is is nonempty
        if(unitClause.size() == 0) goto beach;

        // Find which symbol is unknown, and which value would make it true
        auto result = getUnitClauseSymbolAndValue(unitClause, model);
        int undecidedSymbol = result.first;
        int necessaryValue = result.second;

        // symbols - P
        removeItem(symbols, abs(undecidedSymbol));

        // model union {P=value}
        model[abs(undecidedSymbol) - 1] = necessaryValue;

        std::cout << "UCH: Assigning " << namedSymbols[abs(undecidedSymbol)-1].first << " value " << necessaryValue << std::endl;

        return runDPLL(clauses, symbols, namedSymbols, model, useUnitClauseHeuristic);
        
    }

    beach:
    
    // P <- First(symbols); rest <- rest(symbols)
    int firstSymbol = symbols[0];
    removeItem(symbols, firstSymbol);
    
    model[abs(firstSymbol) - 1] = 1;
    std::cout << "Choice-point: Assigning " << namedSymbols[abs(firstSymbol)-1].first << " value T" << std::endl;
    bool resultOne = runDPLL(clauses, symbols, namedSymbols, model, useUnitClauseHeuristic);

    model[abs(firstSymbol) - 1] = -1;
    std::cout << "Choice-point: Assigning " << namedSymbols[abs(firstSymbol)-1].first << " value F" << std::endl;
    bool resultTwo = runDPLL(clauses, symbols, namedSymbols, model, useUnitClauseHeuristic);

    return resultOne || resultTwo;
}


/**
 * @brief DPLL algorithm 
 * 
 * @param clauses 
 * @param symbols 
 * @param useUnitClauseHeuristic 
 * @return true KB is satisfiable 
 * @return false KB is unsatisfiable
 */
bool DPLL(ClauseSet clauses, Symbols symbols, NamedSymbols namedSymbols, bool useUnitClauseHeuristic){
    // Initialize model to all symbols undecided
    Model model(symbols.size(), 0);
    return runDPLL(clauses, symbols, namedSymbols, model, useUnitClauseHeuristic);
}

/**
 * @brief Consumes a token from the input cnf and converts it to a symbol and a named symbol
 * 
 * @param token 
 * @param namedSymbols 
 * @param symbols 
 * @param clause 
 */
void readSymbol(std::string token, NamedSymbols &namedSymbols, Symbols &symbols, Clause &clause) {
    int symbolValue;
    bool negated = false;

    if (token[0] == '-') {
        negated = true;
        token = token.substr(1);
    }

    auto it = std::find_if(namedSymbols.begin(), namedSymbols.end(),
                           [&](const std::pair<std::string, int> &elem) { return elem.first == token; });

    if (it != namedSymbols.end()) {
        symbolValue = it->second;
    } else {
        int newSymbol = namedSymbols.size() + 1;
        namedSymbols.push_back({token, newSymbol});
        symbols.push_back(newSymbol);
        symbolValue = newSymbol;
    }

    if (negated) {
        symbolValue = -symbolValue;
    }

    clause.push_back(symbolValue);
}

/**
 * @brief Parse the knowledge base from a given CNF file
 * 
 * @param filename 
 * @return KB 
 */
KB parseKB(const std::string &filename) {
    NamedSymbols namedSymbols;
    Symbols symbols;
    ClauseSet clauses;

    std::ifstream inFile(filename);
    std::string line;
    while (std::getline(inFile, line)) {
        // Remove comments
        line = line.substr(0, line.find('#'));

        // Ignore empty lines
        if (line.empty()) continue;

        // Split the line into tokens
        std::istringstream iss(line);
        std::vector<std::string> tokens{std::istream_iterator<std::string>{iss}, std::istream_iterator<std::string>{}};

        // Convert tokens to symbols and build a clause
        Clause clause;
        for (const auto &token : tokens) {
            readSymbol(token, namedSymbols, symbols, clause);
        }

        // Add clause to the KB, unless it is empty
        if(clause.size() != 0) clauses.push_back(clause);
    }

    return {symbols, namedSymbols, clauses};
}



struct CommandLineArgs {
    std::string filename;
    std::vector<std::string> extraLiterals;
    bool useUnitClauseHeuristic;
};

CommandLineArgs processCommandLineArgs(int argc, const char **argv) {
    CommandLineArgs args;
    args.useUnitClauseHeuristic = false;

    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <filename> <literal>* [+UCH]" << std::endl;
        exit(1);
    }

    args.filename = argv[1];

    for (int i = 2; i < argc; ++i) {
        if (strcmp(argv[i], "+UCH") == 0) {
            args.useUnitClauseHeuristic = true;
        } else {
            args.extraLiterals.push_back(argv[i]);
        }
    }

    return args;
}


int main(int argc, const char **argv) {
    CommandLineArgs args = processCommandLineArgs(argc, argv);

    KB kb = parseKB(args.filename);

    // Add extra literals as unit clauses
    for (const auto &literal : args.extraLiterals) {
        Clause unitClause;
        readSymbol(literal, kb.namedSymbols, kb.symbols, unitClause);
        kb.clauses.push_back(unitClause);
    }

    std::cout << "command: DPLL " << args.filename << " ";
     
    for (const auto &literal : args.extraLiterals) {
        std::cout << literal << " ";
    }
    std::cout << (args.useUnitClauseHeuristic ? "+UCH" : "") << std::endl;

    Model initialModel(kb.symbols.size(), 0);
    std::cout << "model: {";
    for (size_t i = 0; i < kb.namedSymbols.size(); i++) {
        std::cout << "'" << kb.namedSymbols[i].first << "': " << initialModel[i];
        if (i != kb.namedSymbols.size() - 1) {
            std::cout << ", ";
        }
    }
    std::cout << "}" << std::endl;

    bool satisfiable = DPLL(kb.clauses, kb.symbols, kb.namedSymbols, args.useUnitClauseHeuristic);

    std::cout << "The input KB is " << (satisfiable ? "satisfiable" : "unsatisfiable") << std::endl;

    // Print the final model
    if (satisfiable) {
        std::cout << "solution (model):" << std::endl;
        for (const auto &namedSymbol : kb.namedSymbols) {
            std::cout << namedSymbol.first << ": " << getModelValue(namedSymbol.second, solutionModel) << std::endl;
        }

        std::cout << "just the Satisfied (true) propositions:" << std::endl;
        for (const auto &namedSymbol : kb.namedSymbols) {
            if (getModelValue(namedSymbol.second, solutionModel) == 1) {
                std::cout << namedSymbol.first << " ";
            }
        }
        std::cout << std::endl;
    }

    std::cout << "total DPLL calls: " << dpllCalls << std::endl;
    std::cout << "UCH=" << (args.useUnitClauseHeuristic ? "True" : "False") << std::endl;

    return 0;
}
