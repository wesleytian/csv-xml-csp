# CSV-XML-PARSER

This is Python script that turns a csv file into a xml file that can work with AIspace's Consistency Based CSP Solver. http://www.aispace.org/downloads.shtml

A sample CSV file needs to be in this format.

Number of Variables n,,,...,
Variable 1’s Name,Varaible 1’s Domain Size,Value 1,Value 2,...,Value k1,,,...,
Variable 2’s Name,Varaible 2’s Domain Size,Value 1,Value 2,...,Value k2,,,...,
...
Variable n’s Name,Varaible n’s Domain Size,Value 1,Value 2,...,Value kn,,,...,
Number of All Different Constraints m,,,...,
Variable Name 1,Variable Name 2,...,Variable Name j1,,,...,
Variable Name 1,Variable Name 2,...,Variable Name j2,,,...,
...
￼ ￼ ￼ ￼ ￼ ￼
2 
Variable Name 1,Variable Name 2,...,Variable Name jm,,,...,
Number of Conjunctive Normal Form Clauses p,,,...,
Clause 1’s Literal 1,Clause 1’s Literal 2,...,Clause 1’s Literal i1,,,...,
Clause 2’s Literal 1,Clause 2’s Literal 2,...,Clause 2’s Literal i2,,,...,
...
Clause p’s Literal 1,Clause p’s Literal 2,...,Clause p’s Literal ip,,,...,

It can then be converted into a XML file with tags such as <VARIABLENAME> </VARIABLENAME>
and <TABLE> </TABLE> which can be uploaded to the CSP solver to find a solution.

There is a sample csv file that includes simple CSV files that can be converted then solved.

# Instructions

Note: a empty output.xml is given in the repo., so you can skip some of the steps

# NOTE
Remember to clear the output.xml before running a new csv file

## MACINTOSH
### IF DO NOT HAVE OUTPUT.XML
Open terminal in folder
Type 
: chmod +x makemac.sh
: ./makemac.sh

### IF USING INCLUDED OUTPUT.XML
#### CHANGE FILE NAME
Open parser.py
in the 7th and 8th line, change the filename to the filename that you want to run the parser on.

## RUN
python3 parser.py


## WINDOWS

### IF DO NOT HAVE OUTPUT.XML
Open prompt
: make.bat
(run the make.bat file)
OR just create a file named output.xml

### IF USING INCLUDED OUTPUT.XML
#### CHANGE FILE NAME
Then Open parser.py
in the 7th and 8th line, change the filename to the filename that you want to run the parser on.

## RUN
: python3 parser.py
(not sure if that’s how you run it on windows)

