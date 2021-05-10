

test : clean
	pytest -v


clean :
	rm -rf tests/data/tmp
	mkdir tests/data/tmp
	#autopep8 --select=E501,E741,E203,W503,E302,E228,E303,E127,E251,E226,W291,E231,E201,E202,E265,E222,E225,E116,E241,E261,E262,W391 .

	
