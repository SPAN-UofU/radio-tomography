all:
	@read -p "How many sensors? " n; \
	cd software/listener-node; make clean; make; \
	cd ../../software/rf-node; make clean; \
	cd ../../tools; python rf_compiler.py $$n;

clean:
	cd software/listener-node; make clean; \
	cd ../../software/rf-node; make clean; \
