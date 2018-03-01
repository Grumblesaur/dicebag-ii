all: backup clean

clean:
	rm -rf parser.out __pycache__ parsetab.py *.pyc
	rm -rf rules/__pycache__
	rm -rf ply/__pycache__
backup:
	cp state/dice state/dice.bak
	cp state/turns state/turns.bak
restore:
	mv state/dice.bak state/dice
	mv state/turns.bak state/turns
