import re
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import string
import nltk
import warnings 
warnings.filterwarnings("ignore", category=DeprecationWarning)

train = pd.read_csv('https://raw.githubusercontent.com/dD2405/Twitter_Sentiment_Analysis/master/train.csv')
# train1 = pd.read_csv('https://raw.githubusercontent.com/hritikzutshi/SocialMediaSentimentAnalysis/master/djangotest/proj/Corona_NLP_train.csv',encoding='latin1')
input = pd.read_csv('/home/hertz/MyGit/djangotest/proj/input.csv', encoding = 'latin1')

# test = pd.read_csv('https://raw.githubusercontent.com/dD2405/Twitter_Sentiment_Analysis/master/test.csv')
# test1 = pd.read_csv('https://raw.githubusercontent.com/hritikzutshi/SocialMediaSentimentAnalysis/master/djangotest/proj/Corona_NLP_test.csv',encoding='latin1')

# train1.drop('TweetAt', inplace=True, axis=1)
# train1.drop('ScreenName', inplace=True, axis=1)
# train1.drop('Location', inplace=True, axis=1)

# test1.drop('TweetAt', inplace=True, axis=1)
# test1.drop('ScreenName', inplace=True, axis=1)
# test1.drop('Location', inplace=True, axis=1)

# train1['tweet'] = train1.OriginalTweet
# train1["tweet"] = train1["tweet"].astype(str)
# train1.drop('OriginalTweet', inplace=True, axis=1)


# test1['tweet'] = test1.OriginalTweet
# test1["tweet"] = test1["tweet"].astype(str)
# test1.drop('OriginalTweet', inplace=True, axis=1)


# def classes_def(x):
#     if x ==  "Extremely Positive":
#         return 1
#     elif x == "Extremely Negative":
#         return 0
#     elif x == "Negative":
#         return 0
#     elif x ==  "Positive":
#         return 1
#     else:
#         return 2
    

# train1['label']=train1['Sentiment'].apply(lambda x:classes_def(x))
# test1['label']=test1['Sentiment'].apply(lambda x:classes_def(x))

# train1.label.value_counts(normalize= True)

# train1.drop('Sentiment', inplace=True, axis=1)
# test1.drop('Sentiment', inplace=True, axis=1)

# train1 = train1.rename(columns={'UserName':'id'})
# test1 = test1.rename(columns={'UserName':'id'})

# train1=train1[['id','label','tweet']]
# test1=test1[['id','label','tweet']]

combine = train.append(input,ignore_index=True,sort=True)
#combine = input
combine.isnull().sum().sort_values(ascending=False)

def remove_pattern(text,pattern):    
    # re.findall() finds the pattern i.e @user and puts it in a list for further task
    r = re.findall(pattern,text)    
    # re.sub() removes @user from the sentences in the dataset
    for i in r:
        text = re.sub(i,"",text)    
    return text
    
def remove_urls(text):
    url_remove = re.compile(r'https?://\S+|www\.\S+')
    return url_remove.sub(r'', text)

def remove_html(text):
    html=re.compile(r'<.*?>')
    return html.sub(r'',text)    
#combine['tweet']=str(combine['tweet'])
combine['tweet'] = np.vectorize(remove_pattern)(combine['tweet'], "@[\w]*")

combine['tweet']=combine['tweet'].apply(lambda x:remove_html(x))

combine['tweet']=combine['tweet'].apply(lambda x:remove_urls(x))        

combine['tweet'] = combine['tweet'].str.replace("[^a-zA-Z#]", " ", regex=True)

combine['tweet'] = combine['tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))

tokenized_tweet = combine['tweet'].apply(lambda x: x.split())

from nltk import PorterStemmer

ps = PorterStemmer()

tokenized_tweet = tokenized_tweet.apply(lambda x: [ps.stem(i) for i in x])

tokenized_tweet.head()

for i in range(len(tokenized_tweet)):
    tokenized_tweet[i] = ' '.join(tokenized_tweet[i])

combine['tweet'] = tokenized_tweet

def clean_dataset(df):
    assert isinstance(df, pd.DataFrame)
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].astype(np.float64)


#combine = clean_dataset(combine)
np.nan_to_num(combine)

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf=TfidfVectorizer(sublinear_tf=True,stop_words='english')
tfidf_matrix=tfidf.fit_transform(combine['tweet'])

inputVec=TfidfVectorizer(sublinear_tf=True,stop_words='english')

#df_tfidf = pd.DataFrame(tfidf_matrix.todense())

#df_tfidf

tfidf_matrix1 = tfidf_matrix[:31962]
input_matrix = tfidf_matrix[31962:]


from sklearn.model_selection import train_test_split

x_train_tfidf,x_valid_tfidf,y_train_tfidf,y_valid_tfidf = train_test_split(tfidf_matrix1,train['label'],test_size=0.3,random_state=42)

from sklearn.linear_model import LogisticRegression

# Log_Reg = LogisticRegression(solver = 'liblinear', random_state = 42, max_iter=1000)

# Log_Reg.fit(x_train_tfidf,y_train_tfidf)

# pred = Log_Reg.predict(input_matrix)

from sklearn.svm import LinearSVC

lsvc = LinearSVC()

lsvc.fit(x_train_tfidf,y_train_tfidf)

pred = lsvc.predict(input_matrix)

input['label'] = pred
#submission = input[['id','label']]
print(input)

combine.to_csv('result.csv')

# compression_opts = dict(method='zip',
#                         archive_name='out.csv')  
# combine.to_csv('out.zip', index=False,
#           compression=compression_opts) 
# arr = [1,2,3,4,5]
# print(arr[2:])
# print(arr[:1])
