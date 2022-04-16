
# coding: utf-8

# In[ ]:


###Before running code
#1.make sure your python installed nltk, requests,beautifulsoup4 (type the following code inside terminal)
#pip install -U nltk
#pip install -U requests
#pip install -U beautifulsoup4

#2.make sure you have "query_result.csv" (which contains column "uname" and "url") inside directory. If no, please do the following
#Go to Gdrive -->RMBI4980 --> Kickstarter --> new --> "Kickstarter code.sql"; run it inside MySQL/Sequel Pro
#Type query: select id,uname,name,url from top100; run it and export as "query_result.csv"

###Instruction
#This coding is used to process sentiment analysis of all selected Kickstarter products:
#-->Loop all URL of the product
#--> Crawl comment data 
#--> Save in temp csv called "ListOfComments1.csv"
#--> Process sentiment analysis (taking average for comments made by each backer; taking average for all comments for each product)
#--> Save all result in csv called "CommentsAnalysis1.csv"

#Remark: there is the function called randomSleep which is used to try avoiding to be blocked by the website


# In[14]:


###List of importing
#For function "make_soup", "crawl_comment"
import requests
from bs4 import BeautifulSoup

#For function "rawdata", Comment_write_csv", "SentimentAnalysis", "Analysis_write_csv", "Analysis_append_csv"
import csv

#For function "SentimentAnalysis"
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#For function "rawdata"
from collections import defaultdict

#For function "randomSleep"
import time, random

#For function "RemoveTempCsv"
import os

#For function "Comment_write_csv"
import pandas as pd


# In[15]:


def rawdata():
    columns = defaultdict(list) # each value in each column is appended to a list

    with open('query_result.csv',encoding="latin-1") as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value 
                columns[k].append(v) # append the value into the appropriate list
                                     # based on column name k

    return(columns['uname'],columns['url'])


# In[16]:


def make_soup(url):

    page = requests.get(url)

    return BeautifulSoup(page.text, 'html.parser')


# In[17]:


def randomSleep():
        sleeptime =  random.randint(2, 5)
        time.sleep(sleeptime)


# In[18]:


def RemoveTempCsv():
    if os.path.exists('ListOfComments1.csv'):
        os.remove('ListOfComments1.csv')


# In[19]:


def Comment_open_csv():
    with open("ListOfComments1.csv","w") as csv_file:
        pass


# In[20]:


def Comment_write_csv(name,data): #input list of commenters' name and list of comment content
    file_name = "ListOfComments1.csv"
    
    # pandas can convert a list of lists to a dataframe.
    # each list is a row thus after constructing the dataframe
    # transpose is applied to get to the user's desired output. 
    df = pd.DataFrame([name,data])
    df = df.transpose() 
    
    # write the data to the specified csv file
    # without adding the index of the dataframe to the output 
    # and without adding a header to the output. 
    df.to_csv(file_name, index=False, header=None)


# In[21]:


def crawl_comment(KickstarterURL):  #Input: product's page in Kickstarter Web
    try:
        ###Collect creator bio page of the product
        soup=make_soup(KickstarterURL+'/creator_bio')
        ###Try avoiding to be blocked, with a random short wait
        randomSleep()
        
        ###For testing
        #print(soup) 
        #print(soup.status_code) 
        #print(soup.prettify()) #show all coding in the web page
        
        ###Used later to check if the comment is made by creator
        MainDesignerName=""
        RangeOfDesignerDetail = soup.find('div',class_="creator-bio-details col col-4 pt3 pb3 pb10-sm")
        MDN = RangeOfDesignerDetail.find('span',class_="identity_name")
        
        if MDN:
            MainDesignerName = MDN.get_text()
            MainDesignerName = MainDesignerName.replace('\n','')

          
            
            
            
        ###Collect comment page of the product
        soup=make_soup(KickstarterURL+'/comments')
        
        ###Try avoiding to be blocked, with a random short wait
        randomSleep()
        
        ###For testing
        #print(soup) 
        #print(soup.status_code) 
        #print(soup.prettify()) #show all coding in the web page
        
        ###Find the area of comment in the webpage
        RangeOfComment = soup.find('ol',class_="comments")
        
        listName=["Commenter"]
        data=["Comment"] #List of comments ready to be put into csv file
        
        if RangeOfComment==None:
            Comment_write_csv(listName,data)
            return 0
            
        #print(RangeOfComment) #show all coding in the whole area of comments if necessary
        
        ###For normalizing score of multiple comments from same backer
        ListOfNames=RangeOfComment.findAll('a',class_="author green-dark") 

        for name in range(len(ListOfNames)):
            name = ListOfNames[name].get_text()
            
            if name != MainDesignerName:
                listName.append(name) #collect all backers' name
                #listName.append(''.join(name.findAll(text=True))) #collect all commenters' name
    
        ###Collect comment content
        ListOfCommenters=RangeOfComment.findAll('div',class_="main clearfix pl3 ml3")
        
        ### Pull all text from the comments
        x = 1
        NoOfCommentFromCreator = 0
        
        # Get each comment by looping all commenters
        for commenter in range(len(ListOfCommenters)):
            CommenterName = ListOfCommenters[commenter].find('a',class_="author green-dark").get_text()

            if CommenterName != MainDesignerName: #if commenter is backer, then do sentiment analysis
                print ("Comment" + str(x) + ": ")
                print()

                #Print each sentence in one line & combine into a complete sentence & store into "data" variable
                Comment = ListOfCommenters[commenter].findAll("p")
                NumberOfSentence = len(Comment)

                WholeSentence = []

                for sentence in range(NumberOfSentence): #print all comments

                    print ("".join((Comment[sentence].get_text())), sep='', end='\n') #show all comments
                    WholeSentence.append((Comment[sentence].get_text()))

                WholeSentence = ''.join(WholeSentence)

                data.append(WholeSentence)
                print()
                x += 1
            if CommenterName == MainDesignerName:
                NoOfCommentFromCreator += 1
        
        ###For testing
        #print(data) #List of all comments
        
        ###Write to CSV
        Comment_write_csv(listName,data)
        
        return(NoOfCommentFromCreator)
        
    except Exception as e:
        print(e)

#Tutorial: https://www.dataquest.io/blog/web-scraping-tutorial-python/

#crawl_comment("https://www.kickstarter.com/projects/1218200025/naked-0") #testing


# In[22]:


def Analysis_write_csv():
    with open("CommentsAnalysis1.csv","w") as csv_file:
        writer = csv.writer(csv_file,delimiter=',')
        writer.writerow(["Product Name","Total number of comments (backer only)","Number of Negative Comment","Number of Neutral Comment","Number of Positive Comment","% of Negative Comment","% of Neutral Comment","% of Positive Comment","Overall Score","Number of creator comment"])


# In[23]:


def Analysis_append_csv(data,NoOfCreatorComment):
    with open("CommentsAnalysis1.csv","a") as csv_file:
        if data:
            if NoOfCreatorComment:
                data.append(NoOfCreatorComment)

            else:
                data.append(0)
                
            writer = csv.writer(csv_file)
            writer.writerow(data)   


# In[24]:


def SentimentAnalysis(ProductName,csvFile):
    try:
        with open(csvFile,'r') as f:
        #for sentence in f:
           # ListOfReview.append(sentence)
            reader=csv.reader(f)
            ListOfReview = list(reader)
            ListOfReview = [l[1] for l in ListOfReview] #second column
            ListOfReview = ListOfReview[1:] #ignore the first one which is the header
            
        ###For testing
        #print(ListOfReview) #List containing all comments

        #For sentence in ListOfReview:
        #    print(sentence) #Show each comment

        ###Sentiment analysis using NLTK
        print()
        print("------------------Sentiment Analysis------------------")
        sid = SentimentIntensityAnalyzer()
        ListOfPolarity = []
        ListOfRate = []
        x=1

        #Looping all comments
        for sentence in ListOfReview:
            print("Comment"+ str(x) + ": " + sentence)
            print()

            ss = sid.polarity_scores(sentence)

            for k in ss:
                print('{0}: {1} '.format(k, ss[k]), end='')
                print()
            print()
            
            #if ss['compound']: 
            ListOfPolarity.append(ss['compound'])

            x+=1
        
        df = pd.read_csv(csvFile)
        df['polarity'] = ListOfPolarity
        df.to_csv(csvFile, index=False)

        #Calcuating average polarity for each commenter
        df1=df.groupby('Commenter')['polarity'].mean()

        #Adjust the data and update the csv file
        df2=df1.reset_index()[['Commenter', 'polarity']].to_csv('ListOfComments1.csv', index=False)

        df = pd.read_csv(csvFile)
        ListOfPolarity = df['polarity'].tolist()
        
        #Calculate the average polarity of each product
        if len(ListOfPolarity) >= 1:
            PolarityMean = df['polarity'].mean()
        else:
            PolarityMean = 0
        
        #Count the number of different types of comment for a product
        for polarity in ListOfPolarity:
            if polarity < 0:
                ListOfRate.append("neg")
            elif polarity == 0:
                ListOfRate.append("neu")
            else:
                ListOfRate.append("pos")
        
        NoOfComments = len(ListOfRate)

        data = [ProductName]

        if NoOfComments != 0:
            NoOfNeg = ListOfRate.count("neg")
            NoOfNeu = ListOfRate.count("neu")
            NoOfPos = ListOfRate.count("pos")
            RatioNeg = ListOfRate.count("neg")/len(ListOfRate)
            RatioNeu = ListOfRate.count("neu")/len(ListOfRate)
            RatioPos = ListOfRate.count("pos")/len(ListOfRate)

            data.append(NoOfComments)
            data.append(NoOfNeg)
            data.append(NoOfNeu)
            data.append(NoOfPos)
            data.append('%.2f'%RatioNeg)
            data.append('%.2f'%RatioNeu)
            data.append('%.2f'%RatioPos)
            data.append(PolarityMean)

        if NoOfComments == 0:
            NoOfNeg = 0
            NoOfNeu = 0
            NoOfPos = 0
            RatioNeg = 0
            RatioNeu = 0
            RatioPos = 0

            data.append(NoOfComments)
            data.append(NoOfNeg)
            data.append(NoOfNeu)
            data.append(NoOfPos)
            data.append('%.2f'%RatioNeg)
            data.append('%.2f'%RatioNeu)
            data.append('%.2f'%RatioPos)
            data.append(PolarityMean)

        print()
        print("------------------Summary------------------")
        print('{:30}'.format("List of Rating:"), ListOfRate)
        print('{:30}'.format("Total number of comments:"), len(ListOfRate))
        print('{:30}'.format("Number of negative comments: "), NoOfNeg, "(", '{:.1%}'.format(RatioNeg), ")")
        print('{:30}'.format("Number of neutral comments: "), NoOfNeu, "(", '{:.1%}'.format(RatioNeu), ")")
        print('{:30}'.format("Number of positive comments: "), NoOfPos, "(", '{:.1%}'.format(RatioPos), ")")
        print('{:30}'.format("Overall score of product:"), PolarityMean)
        print()

        return data #for next step: appending the data into csv file
    
    except Exception as e:
        print(e)

#SentimentAnalysis("ProductName","ListOfComments1.csv") #for testing


# In[ ]:


def main():
    
    ListOfProductName = rawdata()[0]
    ListOfKickstarterURL = rawdata()[1]
    
    Analysis_write_csv() #create a csv file storing result of sentiment analysis
    
    RemoveTempCsv() #Delete the temp csv if it exists (in case it uses back the existing temp file for further process)
    
    x = 0
    
    for KickstarterURL in ListOfKickstarterURL:
        
        ProductName = ListOfProductName[x] #Take the corresponding product name

        Comment_open_csv() #Create a new temp csv 
        
        NoOfCreatorComment = crawl_comment(KickstarterURL)
        Analysis_append_csv(SentimentAnalysis(ProductName,'ListOfComments1.csv'),NoOfCreatorComment) #append analysis result into csv file
        
        RemoveTempCsv() #Delete the old temp csv
        
        x +=1 #Loop all selected product
        
        #Steps of core function:
        #Function: crawl_comment(KickstarterURL)
        #1. Crawl comment from website
        #2. Put them into "ListOfComments1.csv" file: function "Comment_write_csv(data)"
        #3. Return the number of comment from creator --> Stored in NofCreatorComment
        
        #Function: Analysis_append_csv
        #1. Process sentiment analysis using previous csv file "ListOfComments1.csv"
        #2. Put analysis result into "CommentsAnalysis1.csv" file
        
main()


# In[ ]:


def SentimentAnalysis(ProductName,csvFile):
    try:
        with open(csvFile,'r') as f:
            reader=csv.reader(f)
            ListOfReview = list(reader)
            ListOfReview = [l[1] for l in ListOfReview] #second column
            ListOfReview = ListOfReview[1:] #ignore the first one which is the header

        ###Sentiment analysis using NLTK
        sid = SentimentIntensityAnalyzer()
        ListOfPolarity = []

        #Looping all comments
        for sentence in ListOfReview:

            ss = sid.polarity_scores(sentence)

            ListOfPolarity.append(ss['compound'])
        
        df = pd.read_csv(csvFile)
        df['polarity'] = ListOfPolarity
        df.to_csv(csvFile, index=False)

        #Calcuating average polarity for each commenter
        df1=df.groupby('Commenter')['polarity'].mean()

        #Adjust the data and update the csv file
        df2=df1.reset_index()[['Commenter', 'polarity']].to_csv('ListOfComments1.csv', index=False)

        df = pd.read_csv(csvFile)
        ListOfPolarity = df['polarity'].tolist()
        
        #Calculate the average polarity of each product
        if len(ListOfPolarity) >= 1:
            PolarityMean = df['polarity'].mean()
        else:
            PolarityMean = 0
        
        ListOfRate = []
        
        #Count the number of different types of comment for a product
        for polarity in ListOfPolarity:
            if polarity < 0:
                ListOfRate.append("neg")
            elif polarity == 0:
                ListOfRate.append("neu")
            else:
                ListOfRate.append("pos")
        
        NoOfComments = len(ListOfRate)

        data = [ProductName]

        if NoOfComments != 0:
            NoOfNeg = ListOfRate.count("neg")
            NoOfNeu = ListOfRate.count("neu")
            NoOfPos = ListOfRate.count("pos")
            RatioNeg = ListOfRate.count("neg")/len(ListOfRate)
            RatioNeu = ListOfRate.count("neu")/len(ListOfRate)
            RatioPos = ListOfRate.count("pos")/len(ListOfRate)

            data.append(NoOfComments)
            data.append(NoOfNeg)
            data.append(NoOfNeu)
            data.append(NoOfPos)
            data.append('%.2f'%RatioNeg)
            data.append('%.2f'%RatioNeu)
            data.append('%.2f'%RatioPos)
            data.append(PolarityMean)

        if NoOfComments == 0:
            NoOfNeg = 0
            NoOfNeu = 0
            NoOfPos = 0
            RatioNeg = 0
            RatioNeu = 0
            RatioPos = 0

            data.append(NoOfComments)
            data.append(NoOfNeg)
            data.append(NoOfNeu)
            data.append(NoOfPos)
            data.append('%.2f'%RatioNeg)
            data.append('%.2f'%RatioNeu)
            data.append('%.2f'%RatioPos)
            data.append(PolarityMean)

        print()
        print("------------------Summary------------------")
        print('{:30}'.format("List of Rating:"), ListOfRate)
        print('{:30}'.format("Total number of comments:"), len(ListOfRate))
        print('{:30}'.format("Number of negative comments: "), NoOfNeg, "(", '{:.1%}'.format(RatioNeg), ")")
        print('{:30}'.format("Number of neutral comments: "), NoOfNeu, "(", '{:.1%}'.format(RatioNeu), ")")
        print('{:30}'.format("Number of positive comments: "), NoOfPos, "(", '{:.1%}'.format(RatioPos), ")")
        print('{:30}'.format("Overall score of product:"), PolarityMean)
        print()

        return data #for next step: appending the data into csv file
    
    except Exception as e:
        print(e)

#SentimentAnalysis("ProductName","ListOfComments1.csv") #for testing

