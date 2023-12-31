# -*- coding: utf-8 -*-
"""SpamClassifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xx0t-ZC8l-61hTtg9hNmbbFStns2e8YZ
"""

import os
import pandas as pd
import numpy as np 
from sklearn.datasets import load_files
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.draw.util import Label

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/gdrive')
# %cd /gdrive/My\ Drive

#!unzip -u "/gdrive/MyDrive/Assignment PRML/archive.zip" -d "/gdrive/MyDrive/Assignment PRML/spam.zip"

X, Y = [], []
dataset = load_files("/gdrive/MyDrive/Assignment PRML/spam.zip/enron1")

#emails are appended X_data
X_data= np.append(X, dataset.data)
#target are appended to Y_data
Y_data = np.append(Y, dataset.target)
no_of_datapoints = len(X_data)
X = X_data
Y = Y_data

#define labels for mail and target
df = pd.DataFrame(columns=['data', 'label'])
df['data'] = [data for data in X]
df['label'] = [label for label in Y]

#seperate mail and target column 
mail_X = df.drop(['label'], axis=1)
target_Y = df['label']

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def data_preprocessing(X):
  #make set of all words of email
  wordsSet = set()

  #store words of all mails in words list
  words = []
  for i in range(0, len(X)):
    # Clean data by removing all symbols except letters, replacing all gaps with spaces, removing 'b' in the beginning of each text, convert into lowercase
    para = re.sub(r'\\r\\n', ' ', str(mail_X['data'][i]))
    para = re.sub(r'^b\s+', '', para) 
    para = re.sub('[^a-zA-Z]', ' ', para)
    para = re.sub(r'\s+', ' ', para)
    para = para.lower()
    para = para.split() 

    # If the word is not in stopword, stem that word 
    para = [stemmer.stem(word) for word in para if word not in stopwords.words('english')]

    #add all words of mail[i] in set
    for word in para:
      wordsSet.add(word)
    para = ' '.join(para)
    
    # set_of_words.add(para)
    words.append(para)
  print(len(words))
  return words, wordsSet

words, wordsSet = data_preprocessing(mail_X)

# print(wordsSet)

#initialize dictionary to set all words in mails with 1 for spam and 1 for non spam as its count in respective mails
dictionary = {}
for i in wordsSet:
  dictionary[i] = [1,1]
print(dictionary)

#Update dictionary to store count of spam or non-spam for each word 
for i in range(len(words)):
  sentence = words[i]
  spam_non_spam = int(Y[i])
  wordsnew = list(sentence.split(" "))
  
  for i in wordsnew:
    dictionary[i][spam_non_spam] += 1
print(dictionary["subject"])
print(len(dictionary))

#count total words in spam and non spam mails
def count_spam_non_spam():
  no_of_spam = 0
  no_of_nonspam = 0
  for i in dictionary:
    no_of_nonspam += dictionary[i][0]
    no_of_spam += dictionary[i][1]
    
  print(no_of_spam)
  print(no_of_nonspam)
  return no_of_spam, no_of_nonspam

no_of_spam, no_of_nonspam = count_spam_non_spam()

#probability of non spam and spam emails
def compute_prob_spam_nonspam():
  prob_of_spam = no_of_spam / (no_of_spam + no_of_nonspam)
  prob_of_nonspam = no_of_nonspam / (no_of_spam + no_of_nonspam)
  print(prob_of_spam)
  print(prob_of_nonspam)
  return prob_of_spam, prob_of_nonspam

prob_of_spam, prob_of_nonspam = compute_prob_spam_nonspam()

def naiveBayes(X, dictionary):
  words, wordsSet = data_preprocessing(X, Y)

  #count total words in spam and non spam mails
  no_of_spam, no_of_nonspam = count_spam_non_spam()

  #probability of non spam and spam emails
  prob_of_spam, prob_of_nonspam = compute_prob_spam_nonspam()

  #calculate test probabilities by naive bayes
  test_prob_of_nonspam = prob_of_nonspam
  for word in words:
      if word in dictionary.keys():
          test_prob_of_nonspam *= (dictionary[word][0] / no_of_nonspam)

  test_prob_of_spam = prob_of_spam
  for word in words:
      if word in dictionary.keys():
          test_prob_of_spam *= (dictionary[word][1] / no_of_spam)

  test_Y = 0
  #if probability of spam is greater than nonspam return 1 
  if(test_prob_of_nonspam < test_prob_of_spam):
      test_Y = 1
  if(test_Y == 0):
      print("0")
  else:
      print("1")

#To test on test data run the algorithm with dictionary created from train data
X, Y = [], []
#load testing data
for t in sorted(os.listdir("test")):
  with open (os.path.join("test",t),'r') as file:
    Xtest = np.append(X, file)
    naiveBayes(Xtest,dictionary)

