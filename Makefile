all:
	cd software/listener-node; make clean; make; \
	cd ../../software/rf-node; make clean; \
	cd ../../tools; python rf_compiler.py 2;
