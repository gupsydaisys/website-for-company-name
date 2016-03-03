# Website-Name

Currently if your run convert.py, it outputs a company name with a website domain name that it believes is the official company website

You'll need to have previously installed:
- urllib
- json
- urlparse 
- pyenchant

Once you have training data...
- for each website output, say how confident I am about it to being a match
- figure out the optimal value for the amount of characters left when you remove company words from the domain
- figure out how to threshold choosing all words in the company name
