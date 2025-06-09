PYTHON = python

# Default target: runs the RPAL processor with the specified file
run:
	$(PYTHON) myrpal.py $(file)

# prints the AST
ast:
	$(PYTHON) myrpal.py -ast $(file)

# prints the ST
st:
	$(PYTHON) myrpal.py -st $(file)

# Run all tests
test:
	$(PYTHON) -m pytest tests/     

# cleans up the generated files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +

