import re
from nltk.corpus import stopwords
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder as LE
from nltk.stem import WordNetLemmatizer
import nltk
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
import csv
labelencoder=LabelEncoder()

def cleanse(file):
    job_desc=[]
    labels=[]
    stemmer=WordNetLemmatizer()
    
    f=open(file,'r',encoding='cp437')
    reader = csv.reader(f)
    for desc,label in reader:
        #stop words
        stopLex=set(stopwords.words('english')) 
        #remover special characters
        text=re.sub(r'\W',' ',desc)
        label=re.sub(r'\n','',label)
        
        #lowercase
        text=re.sub('[^a-z]',' ',text.lower()) 
        
         # remove all single characters
        text = re.sub(r'\s+[a-zA-Z]\s+', ' ',text)
    
        # Remove single characters from the start
        text= re.sub(r'\^[a-zA-Z]\s+', ' ',text) 
        
        # Substituting multiple spaces with single space
        text= re.sub(r'\s+', ' ', text, flags=re.I)
        
        # Removing prefixed 'b'
        text = re.sub(r'^b\s+', '',text)        
        text = text.split()
        text  = [word for word in text if word not in stopLex]
        # Lemmatization
        text = [stemmer.lemmatize(word) for word in text]
        text = ' '.join(text)

        job_desc.append(text) 
        labels.append(label)
    f.close()
    return job_desc,labels
def test_cleanse(file):
    job_desc=[]
    data=[]
    stemmer=WordNetLemmatizer()
    
    f=open(file,'r',encoding='cp437')
    for line in f:
        desc=line
        stopLex=set(stopwords.words('english')) 
        #remover special characters
        text=re.sub(r'\W',' ',desc)
        
        #lowercase
        text=re.sub('[^a-z]',' ',text.lower()) 
        
         # remove all single characters
        text = re.sub(r'\s+[a-zA-Z]\s+', ' ',text)
    
        # Remove single characters from the start
        text= re.sub(r'\^[a-zA-Z]\s+', ' ',text) 
        
        # Substituting multiple spaces with single space
        text= re.sub(r'\s+', ' ', text, flags=re.I)
        
        # Removing prefixed 'b'
        text = re.sub(r'^b\s+', '',text)
        text = text.split()
        text  = [word for word in text if word not in stopLex]
    
        # Lemmatization
        text = [stemmer.lemmatize(word) for word in text]
        text = ' '.join(text)
        
        job_desc.append(text) 
        data.append(line)
        
    f.close()
    return job_desc,data

#Build a counter based on the training dataset
desc_train,labels_train=cleanse('trainingset.csv')
desc_test,data_test=test_cleanse('testingset.csv')
#desc_train,labels_train=cleanse('data_train.csv')
#desc_test,data_test=test_cleanse('data_test.csv')
labels_train=labelencoder.fit_transform(labels_train)
counter = CountVectorizer()
counter.fit(desc_train)

#count the number of times each term appears in a document and transform each doc into a count vector
counts_train = counter.transform(desc_train)#transform the training data
counts_test = counter.transform(desc_test)#transform the testing data

#train classifier
rfc=RandomForestClassifier()
rfc.fit(counts_train,labels_train)

#Predicting and giving file as output
pred_rfc=rfc.predict(counts_test)
pred_test=labelencoder.inverse_transform(pred_rfc)
fw=open('predict1.csv','w')
writer=csv.writer(fw,delimiter=',')
zipped_set=zip(desc_test,pred_test)
for row in zipped_set:
    writer.writerow(row)
fw.close()




