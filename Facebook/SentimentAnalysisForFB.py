###List of importing
#For function "make_soup", "crawl_comment"
import requests
from bs4 import BeautifulSoup

#For function "rawdata", Comment_write_csv", "SentimentAnalysis", "Analysis_write_csv", "Analysis_append_csv"
import csv

#For function "SentimentAnalysis"
import nltk
#nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#For function "rawdata"
from collections import defaultdict

#For function "randomSleep"
import time, random

#For function "RemoveTempCsv"
import os

#For function "Comment_write_csv"
import pandas as pd





def rawdata():
    columns = defaultdict(list) # each value in each column is appended to a list
    ListOfComment = []
    with open('comment.csv',encoding="latin-1") as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            ListOfComment.append(row['ï»¿Comment'])

    return(ListOfComment)





def Analysis_write_csv():
    with open("FBCommentsAnalysis1.csv","w") as csv_file:
        writer = csv.writer(csv_file,delimiter=',')
        writer.writerow(["Comment","Overall Score"])





def Analysis_append_csv(data):
    with open("FBCommentsAnalysis.csv","a") as csv_file:             
            writer = csv.writer(csv_file,delimiter=',')
            for d in data:
                writer.writerow(d)   





def SentimentAnalysis(ListOfReview):
    try:
        ###Sentiment analysis using NLTK
        sid = SentimentIntensityAnalyzer()
        ListOfPolarity = []
        ListOfRate = []

        #Looping all comments
        for sentence in ListOfReview:

            ss = sid.polarity_scores(sentence)

            for k in ss:
                print('{0}: {1} '.format(k, ss[k]), end='')
                print()
            print()
            
            #if ss['compound']: 
            ListOfPolarity.append(ss['compound'])
        
        return ListOfPolarity
    except Exception as e:
        print(e)






def main():
    ListOfComment = rawdata()
    ListOfPolarity = SentimentAnalysis(ListOfComment)
    f = open("myfile.txt", "w")
    x=0
    for C in ListOfPolarity:
        f.write(str(C)+'\n')
        #f.write(ListOfComment[x]+","+str(C)+'\n')
        x+=1
    f.close()
    
    print(str(x+1))
main()

