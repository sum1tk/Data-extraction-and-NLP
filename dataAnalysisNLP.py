import pandas as pd
import re 
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import string 

#storing the Input file as a pandas Dataframe
df=pd.read_excel('Input.xlsx')

#sentiment analysis
def sentimentScore(text,positive,negative):
    positiveS=0
    negativeS=0
    wordCount=0
    for i in nltk.word_tokenize(text):
        if i.isalpha():
            wordCount+=1      
        if i.lower() in positive:
            positiveS+=1
        elif i.lower() in negative:
            negativeS+=1
        
    
    polarity=(positiveS - negativeS)/(positiveS + negativeS + 0.000001)
    subjectivity=(positiveS + negativeS)/(wordCount + 0.000001)
    sentiment=[positiveS,negativeS,polarity,subjectivity,wordCount]
    return sentiment



#Making a list containing all stop words
fileNames=['StopWords_Auditor','StopWords_DatesandNumbers','StopWords_Generic','StopWords_GenericLong','StopWords_Geographic','StopWords_Names']
stop_words=' '
#iterating over stop words file names and adding words to our variable
for fileName in fileNames:
    with open(f'StopWords\{fileName}.txt', encoding = 'utf-8') as f1:
        stop_words+= f1.read()

#out of loop because different encoding 
with open('StopWords\StopWords_Currencies.txt', encoding = "ansi") as f2:
    stop_words += f2.read()

#standardising the case of stop_words and then splitting the string
stopWords=stop_words.lower().split()

#getting negavtive and positive words and storing them in a list ensuring they dont belong to stop words
with open('MasterDictionary\\negative-words.txt', 'r') as file:
    negative_unclean=file.read().split()
negative=[word.lower() for word in negative_unclean if word.lower() not in stopWords]
with open('MasterDictionary\positive-words.txt', 'r') as file:
    positive_unclean=file.read().split()
positive=[word.lower() for word in positive_unclean if word.lower() not in stopWords]


#adding columns to Dataframe and storing it in 'fnames'
fnames = df.assign(positive_score=0, negative_score=0, polarity_score=0, subjectivity_score=0, avg_sentence_length=0, percentage_of_complex_words=0, fog_index=0, avg_number_of_words_per_sentence=0, complex_word_count=0, word_count=0, syllable_per_word=0, personal_pronouns=0, avg_word_length=0)

#iterating over the data frame 'fnames'
for index, row in fnames.iterrows():
    file=open(f'{fnames.at[index, "URL_ID"]}.txt',encoding='utf-8')
    uncleantxt=file.read()
   
    #avg_number_of_words_per_sentence 
    wordCount = len(re.findall("[a-zA-Z-]+", uncleantxt))  #finding all words and counting them  
    sentences = sent_tokenize(uncleantxt)                  #making a list of sentences
    sentenceCount = len(sentences)                         #finding the number of sentces
    
    if sentenceCount>0:
        fnames.at[index, "avg_number_of_words_per_sentence"]=wordCount/sentenceCount  #calculating Average Sentence length
        fnames.at[index, "avg_sentence_length"]=wordCount/sentenceCount
    
    

    #pronoun counter
    pronounRegex = re.compile(r'\b(I|we|my|ours|(?-i:us))\b',re.I)              #regex to find personal pronouns excluding country US
    fnames.at[index, "personal_pronouns"] = len(pronounRegex.findall(uncleantxt))

    #syllable and complex word counting
    syllableCount=0
    complexWordcount=0
    characterCount=0
    for word in nltk.word_tokenize(uncleantxt):
        syllableComplexCount=0

        #counting vowels to count syllables using regex (deducting the count of expection cases)
        syllableCount+=len(re.findall(r'[aeiouy]',word.lower()))-len(re.findall(r'^[a-z]+[es|ed]$', word.lower()))
        syllableComplexCount+=len(re.findall(r'[aeiouy]',word.lower()))-len(re.findall(r'^[a-z]+[es|ed]$', word.lower()))
        
        #counting complex words by checking that syllable count is greater than 2
        if syllableComplexCount>2:
            complexWordcount+=1
        
        #loop for character count
        for i in range(len(word)):
                if word[i].isalpha():
                    characterCount += 1
    #computing and assigning complex word count
    fnames.at[index, "complex_word_count"]=complexWordcount


    #percentage of complex number,syllable per word,fog index
    if wordCount>0:
        #computing and assigning complex number percentage
        complexNoPerc=(complexWordcount/wordCount)*100                      
        fnames.at[index, "percentage_of_complex_words"]=complexNoPerc 

        #computing and assigning syllable per word      
        fnames.at[index, "syllable_per_word"]=syllableCount/wordCount   

        #computing and assigning fog index
        fnames.at[index, "fog_index"]=0.4 * ((wordCount/sentenceCount) + complexNoPerc) 

        #computing and assigning average word length
        fnames.at[index, "avg_word_length"]=characterCount/wordCount

    #cleaned word count

    #using nltk stopword and making a set of punctuations too
    stopWordsNLTK = set(stopwords.words('english'))
    punctuation = set(string.punctuation)

    #tokenizing the text
    wordsU=nltk.word_tokenize(uncleantxt)
    #cleaning stop words and punctuatiion
    words=[word for word in wordsU if word not in stopWordsNLTK and word not in punctuation]

    #cleaning for sentimental analysis
    uncleantxt = uncleantxt.split()
    resultwords  = [word for word in uncleantxt if word.lower() not in stopWords]
    resultwords= ' '.join(resultwords)

    #using the user-defined function to compute the variables
    sentiment=sentimentScore(resultwords,positive,negative)
    #assigning values from the function corresponding cells
    fnames.at[index, 'positive_score'] = sentiment[0]
    fnames.at[index, 'negative_score'] = sentiment[1]
    fnames.at[index, 'polarity_score'] = sentiment[2]
    fnames.at[index, 'subjectivity_score'] = sentiment[3]
    fnames.at[index, 'word_count'] = sentiment[4]

#creating Output from our Dataframe fnames
fnames.to_excel('Output Structure.xlsx', index = False, header=['URL_ID','URL','POSITIVE SCORE','NEGATIVE SCORE','POLARITY SCORE','SUBJECTIVITY SCORE','AVG SENTENCE LENGTH','PERCENTAGE OF COMPLEX WORDS','FOG INDEX','AVG NUMBER OF WORDS PER SENTENCE','COMPLEX WORD COUNT','WORD COUNT','SYLLABLE PER WORD','PERSONAL PRONOUNS','AVG WORD LENGTH'])