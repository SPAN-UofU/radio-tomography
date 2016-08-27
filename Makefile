all:
	@while [ -z "$$n" ]; do \
		read -r -p "How many sensors? " n; \
		done;\
	cd tools; python rf_compiler.py $$n; \
	cd ../software/listener-node; make clean; make; 

clean:
	cd software/listener-node; make clean; \
	cd ../../software/rf-node; make clean;
