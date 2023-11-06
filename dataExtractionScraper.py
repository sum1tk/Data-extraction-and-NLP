from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import pandas as pd

#reading the Input file
url_dataset = pd.read_excel('Input.xlsx') 
#accesssing the URL column   
URLs = list(url_dataset.iloc[:,1])                  

#iterating over the URLs
for i,URL in enumerate(URLs):
    try:
        soup = BeautifulSoup(urlopen(URL), 'html.parser')  #parser
        URLtitle = str(url_dataset.iloc[i,0])                      
        URLtxt = soup.title.string + " "                    #variable to hold article content and title 
        
        for x in soup.article.find_all("p"):               #finding article content and storing it
            URLtxt += x.text
        file = open(f'{URLtitle}.txt',"a",encoding='utf-8') #writing data to files
        file.write(URLtxt)
        file.close()
    except HTTPError as e:
        with open(f'{str(url_dataset.iloc[i,0])}.txt', 'w', encoding='utf-8') as file:
            pass 
        print(f"Error accessing URL: {URL}")
        print(f"HTTP Error {e.code}: {e.reason}")
        
        continue
#114:URLs 114:scraped 2:HTTP Error 404
