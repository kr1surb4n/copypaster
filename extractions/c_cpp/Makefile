parse:
	rm -fr html
	cp -fr html_backup html
	find html/ -name "*.html" | python parser.py
	find html/ -type f -name "*.html" -delete
	find html/ -type d -empty -delete
