# leetcodeContestSolutionExtractor
Solution to extract code of previous leetcode weekly contests. 

# Available Features

- Scrape 
- filter
- Create Solution file

# How to Run 

### What you need
    python3 

### Commads
	python extractLeetcodeContest.py
	
	mv finalData.json pythonFilter/
	
    python pythonFilter/pythonFilter.json
	
## output:

- 4 files named python_{0..4}.py 
- containing all python solution written by top 20-30 python leetcoders

# TODO
	
- rate limiting for each request. 

- Allow user to pass contest ID and number of pages to be scraped as arguments

- combine all feature
    - load user subs
    - code generator
    - python filter
    - file solution creater in single file
	
- Will make process as simple as 
		python extractContest.py contestID=w256 pages=3
		
- Make code modular so that more filters can be added
	
- Biweekly contest support
	
- leetcode china support



