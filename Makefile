



clean :
	rm -rf tests/data/tmp
	mkdir tests/data/tmp
	autopep8 -r -i --ignore=E501,E116 .

test : clean
	pytest -v

	
