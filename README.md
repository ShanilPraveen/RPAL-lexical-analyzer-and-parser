# RPAL Interpreter

An interpreter for the RPAL (Right-reference Pedagogic Algorithmic Language) developed in Python. This project was completed as part of the CS3513 course at the University of Moratuwa by Group Cyclone_01 (Intake 22). It includes a custom lexer, parser, abstract syntax tree (AST) builder, tree standardizer (ST), and an interpreter based on tree-walking and CSE principles.

---

## 📌 Features

- Manual Lexical Analyzer using Python regex (no lex/yacc)
- Recursive Descent Parser
- Abstract Syntax Tree (AST) Construction
- AST → Standardized Tree (ST) Transformation
- Tree-Walking Interpreter simulating a Control Stack Environment (CSE) Machine
- Support for built-in RPAL constructs (e.g., `let`, `where`, `lambda`, `gamma`)
- Command-line interface for AST, ST, and execution

---

## 🧠 Project Structure

```
RPAL-lexical-analyzer-and-parser/
├── Lexer.py            # Lexical analyzer: tokenizes RPAL source code
├── parser.py           # Builds AST using recursive descent parsing
├── nodes.py            # AST/ST node definitions and standardization logic
├── environment.py      # Variable/function scope management and built-in functions
├── data_types.py       # Custom types for tuples, truth values, and nil
├── myrpal.py           # Entry point for execution, AST/ST visualization
├── testcode.rpal       # Sample RPAL program for testing
├── tests/              # Unit tests for components
├── Makefile            # Commands for building, running, and cleaning
├── .gitignore          # Git version control exclusions
└── Inputs/             # (Optional) Folder for storing test RPAL programs
```

---

## 🚀 How to Run

### 🛠 Prerequisites

- Python 3.8+ installed on your machine
- `pip` package manager

### 📥 Setup

```bash
# Clone this repository
git clone https://github.com/ShanilPraveen/RPAL-lexical-analyzer-and-parser.git
cd RPAL-lexical-analyzer-and-parser
```

### ▶️ Running the Interpreter

```bash
# Run the interpreter on a sample file
python myrpal.py testcode.rpal
```

### 📤 View AST

```bash
python myrpal.py -ast testcode.rpal
```

### 📤 View Standardized Tree

```bash
python myrpal.py -st testcode.rpal
```

### ✅ Run Tests

```bash
python -m pytest tests/
```

---

## 🧩 Language Design

- **Lexical Analysis**: Regex-based tokenizer that produces a list of tokens.
- **Parsing**: Recursive descent parsing for building a nested tree structure from tokens.
- **AST → ST Conversion**: Complex syntax constructs are standardized into canonical lambda-calculus-style structures.
- **Interpretation**: Each node in the ST interprets itself recursively, maintaining its own environment and closures.

---

## 🧑‍💻 Authors

- **Dasun W.A.T.** – 220094K  
- **Diwakar J.S.P.** – 220144P  

Department of Computer Science & Engineering  
University of Moratuwa

