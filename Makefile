TEST_CMD = python3 -m doctest
CHECKSTYLE_CMD = flake8
AUTO_PEP = autopep8

all: compile pep8 checkstyle 

compile:
	@echo "Nothing to compile for Python"

checkstyle:
	$(CHECKSTYLE_CMD) BondMarket/*.py
	$(CHECKSTYLE_CMD) BondMarket/app/*.py
	$(CHECKSTYLE_CMD) BondMarket/gui/*.py
	$(CHECKSTYLE_CMD) BondMarket/gui/menues/*.py

pep8:
	$(AUTO_PEP) -i --max-line-length 80 BondMarket/*.py
	$(AUTO_PEP) -i --max-line-length 80 BondMarket/app/*.py
	$(AUTO_PEP) -i --max-line-length 80 BondMarket/gui/*.py
	$(AUTO_PEP) -i --max-line-length 80 BondMarket/gui/menues/*.py 

clean:
	rm -f *.pyc
	rm -rf __pycache__
