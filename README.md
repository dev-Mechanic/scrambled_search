# Scrambled Word Search
Count how many of the words from a dictionary appear as substrings in a long string of characters either in their original form or in their scrambled form. The scrambled form of the dictionary word must adhere to the following rule: the first and last letter must be maintained while the middle characters can be reorganised.

## Inputs

- Dictionary File : a dictionary file, where each line comprises one dictionary word from which you can create your dictionary. E.g. “and”, “bath”, etc, but note the dictionary words do not need to be real words.

- Input File : an input file that contains a list of long strings, each on a newline, that you will need to use to search for your dictionary words. E.g. “btahand”

## How to run ?

### Docker
- Build docker 
`docker build -t scramble_search:20230423 . `

- Run docker
`docker run --rm -v $(pwd)/dictionary.txt:/opt/dictionary.txt -v $(pwd)/input.txt:/opt/input.txt scramble_search`
where path to dictionary and input file can be provided from the working directory.
-- Dictionary File : -v $(pwd)/dictionary.txt:/opt/dictionary.txt
-- Input File : -v $(pwd)/input.txt:/opt/input.txt

- See help
`docker run --rm scramble_search --h`

### Local
Ensure you have python installed. Python version >= 3
- python 
`python3 scramble_search.py --dictionary dictionary.txt --input input.txt`


## Cases Validated

### Valid Input
Following log will be generated for a valid dictionary and input file.
```
INFO:scrambled-search:Starting process for scrambled search
INFO:scrambled-search:Dictionary loaded with 5 words.
INFO:scrambled-search:Sum of all lengths of all words in dict =  27 chars.
INFO:scrambled-search:Input file loaded with 3 lines.
INFO:scrambled-search:Case  #1:4
INFO:scrambled-search:Case  #2:2
INFO:scrambled-search:Case  #3:3
INFO:scrambled-search:Completed process for scrambled search, took time 0.0028040409088134766s
```

### Empty file
Following warning log will be generated if any of the required files (dictionary, input) are empty.
```
INFO:scrambled-search:Starting process for scrambled search
INFO:scrambled-search:Dictionary loaded with 0 words.
WARNING:scrambled-search:No words found in dictionary
INFO:scrambled-search:Input file loaded with 0 lines.
WARNING:scrambled-search:No lines found in input file to search
INFO:scrambled-search:Completed process for scrambled search, took time 3.0994415283203125e-06s
```

### Missing file
Following log will be generated if any of the required files (dictionary, input) are missing.
```
INFO:scrambled-search:Starting process for scrambled search
ERROR:scrambled-search:Dictionary file not found at test-data/missingfile/dictionary.txt
Process stopped due to one or more errors.
```

## Dictionary over limit
Following log will be generated if the sum of lengths of all words in the dictionary exceed 105.
```
python3 scramble_search.py --dictionary test-data/largedict/dictionary.txt --input input.txt 
INFO:scrambled-search:Starting process for scrambled search
INFO:scrambled-search:Dictionary loaded with 25 words.
INFO:scrambled-search:Sum of all lengths of all words in dict =  139 chars.
WARNING:scrambled-search:Dictionary size exceeds allowed size of 105. Sum of lengths of all words in the dictionary should not exceed 105.
ERROR:scrambled-search:Dictionary file not found at test-data/largedict/dictionary.txt
```