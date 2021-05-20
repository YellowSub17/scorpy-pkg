

test :
	pytest -v tests/


clean :
	rm -rf tests/data/tmp
	mkdir tests/data/tmp
	rm -rf tests/__pycache__/
	autopep8 -r -i --ignore=E501,E116 .


	
