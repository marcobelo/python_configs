cmd_clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf *.log
