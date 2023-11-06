Data Extraction and NLP(Sentiment Analysis,Readability etc.) Test Assignment
This repository contains the solution for the Data Extraction and NLP Test Assignment. The objective of this assignment is to extract textual data articles from a given URL and perform text analysis to compute various variables as explained in the provided documents.

the dataExtractionScraper.py file contains a web scraper that extracts data 
the dataAnalysisNLP.py file comntains code that does NLP 

In analysis we do:
      -Sentiment analysis - positive score,negative score and polarity,Subjectivity Score
      -Analysis of Readability	-Fog index
      -Average Number of Words Per Sentence	
      -Complex Word Count	
      -Word Count	
      -Syllable Count Per Word	
      -Personal Pronouns	
      -Average Word Length

Project Structure
Input.xlsx: Input file containing articles and their corresponding URLs.
StopWords: Folder containing stop words lists used for cleaning the text during sentimental analysis.
MasterDictionary: Folder containing the master dictionary of positive and negative words.
Text Analysis.docx: Document explaining the methodology adopted for text analysis.
output_structure.xlsx: Output data structure file specifying the format of the output.
requirements.txt: Python dependencies required to run the project.
dataExtractionScraper.py: Python script for data extraction from URLs using BeautifulSoup, Selenium, or Scrapy.
dataAnalysisNLP.py: Python script for performing textual analysis and computing variables based on the extracted data.
Getting Started
Prerequisites
Python 3.x installed on your system.
Required libraries and dependencies can be installed using the following command:

command:
pip install <libraryName>

Libraries required:numpy,pandas,nlptk,urlopen,beautifulsoup

Data Extraction
Place the articles and their corresponding URLs in the Input.xlsx file.

Run the dataExtractionScraper.py script to extract article texts from the provided URLs and save them as separate text files with URL_ID as the file name.

command:
python dataExtractionScraper.py
Extracted article texts will be saved in the output folder.

Text Analysis
Ensure the extracted articles are available in the output folder.

Run the dataAnalysisNLP.py script to perform textual analysis and compute the variables specified in the output data structure.

command:
python dataAnalysisNLP.py
The computed variables will be saved in the output folder in the format specified in the output_structure.xlsx file.

Output
The output folder will contain individual text files for each article with their corresponding computed variables as per the specified output data structure.

For any questions or issues, please contact me at sumitkothari900@gmaiil.com.
