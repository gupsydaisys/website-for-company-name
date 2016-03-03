# Website-Name

To random sample 25 companies and to get each computed website mapping (if one exists) and whether or not it's correct, type:

  `python run.py`

You'll need to have previously installed:
- urllib
- json
- urlparse 
- pyenchant
(just check the imports in all three files)

Obvious problems:
  - only grabbing top 4 entries for google search, should be doing top 10 probably
  - add better words to dictionary of trivial vocab

Once you have training data...
- for each website output, say how confident I am about it to being a match
- figure out the optimal value for the amount of characters left when you remove company words from the domain
- figure out how to threshold choosing all words in the company name
