#!/usr/bin/env python
# coding: utf-8

# ## Wordle Web Scraper

# In[1]:


#uses Beautiful Soup
get_ipython().system('pip install beautifulsoup4')
get_ipython().system('pip install pyenchant')


# In[2]:


#import all necessary libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import re
import enchant
from heapq import nlargest
import itertools


# In[3]:


html_text = requests.get('https://progameguides.com/wordle/all-wordle-answers-in-2022-updated-daily/').text


# In[4]:


soup = BeautifulSoup(html_text, "lxml")
#print(soup.prettify())


# In[5]:


siblings = soup.find_all('strong',text =re.compile(" - #" ))
#print(siblings)


# In[6]:


dirtyWordsDF = pd.DataFrame(columns = ['answers'])
for sibling in soup.find_all('strong',text =re.compile(" - #" )):
    for word in sibling.parent.next_siblings:
        dirtyWordsDF = dirtyWordsDF.append({'answers':str(word.encode('utf-8'))}, ignore_index = True)
        
dirtyWordsDF.to_csv('test_words')


# In[7]:


cleanWordsDF = pd.DataFrame(columns = ['answers'])
for word in dirtyWordsDF['answers']:
    word = word[-11:]
    word = word[:-6]
    cleanWordsDF = cleanWordsDF.append({'answers':str(word)}, ignore_index = True)
cleanWordsDF.to_csv('words')


# In[8]:


d = enchant.Dict("en_US")
for word in cleanWordsDF['answers']:
    if word == "":
        cleanWordsDF['answers']=cleanWordsDF[cleanWordsDF.answers != word]
    elif not isinstance(word, str):
        cleanWordsDF['answers']=cleanWordsDF[cleanWordsDF.answers != word]
    elif d.check(word) == False:
        cleanWordsDF['answers']=cleanWordsDF[cleanWordsDF.answers != word]
        
cleanWordsDF.to_csv('words')


# In[9]:


cleanWordsDF = cleanWordsDF.dropna()
cleanWordsDF = cleanWordsDF.drop_duplicates()


# In[10]:


lettersDict = {}

for word in cleanWordsDF['answers']:
    for letter in word:
        if letter not in lettersDict:
            lettersDict[letter] = 1
        else:
            lettersDict[letter]+=1


# In[11]:


n=1
while(int(n) < 5 or int(n) > 10):
    n = int(input("Select a value for n (5<=n<=10): "))
bestNLetters = nlargest(n, lettersDict, key = lettersDict.get)
bestNLetters


# In[12]:


bestLetterCombos = itertools.permutations(bestNLetters, 5)

perms = [''.join(p) for p in itertools.permutations(bestNLetters, 5)]


# In[13]:


BestWordsDF = pd.DataFrame(columns = ['Best_Init_Guesses'])
for perm in perms:
    if d.check(perm) == True:
        BestWordsDF = BestWordsDF.append({'Best_Init_Guesses':perm}, ignore_index = True)


# In[14]:


BestWordsDF.to_csv("Best Initial Guesses for Wordle")


# In[15]:


pd.set_option('display.max_rows', None)
BestWordsDF.head(5)


# In[16]:


from wordcloud import WordCloud


# In[17]:


words = BestWordsDF['Best_Init_Guesses'].values


# In[18]:


print(words)


# In[20]:


wordcloud2 = WordCloud().generate(' '.join(BestWordsDF['Best_Init_Guesses']))

plt.imshow(wordcloud2)
plt.axis("off")
plt.show()


# In[21]:


wordcloud2.to_file('WordleCloud.png')


# In[ ]:




