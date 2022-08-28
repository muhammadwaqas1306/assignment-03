# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 15:40:37 2022

@author: Asim
"""

#importing libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import re
import nltk
import spacy
import string
from collections import Counter
import streamlit as st

def main():
    st.title("Spam and Non-spam Messages Analysis")
#reading files
    df=pd.read_csv("SMS_data.csv")


#lower case
    df["Message_body"] = df["Message_body"].str.lower()

#removal of punctuation
    PUNCT_TO_REMOVE = string.punctuation

    def remove_punctuation(text):
        """custom function to remove the punctuation"""
        return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

    df["Message_body"] = df["Message_body"].apply(lambda text: remove_punctuation(text))

#removal of numbers
    def remove_numbers(text):
        url_pattern = re.compile(r'[0-9]+')
        return url_pattern.sub('', text)

    df["Message_body"] = df["Message_body"].apply(lambda text: remove_numbers(text))

#removal of special characters
    def remove_special_characters(text):
        url_pattern = re.compile(r'[@_!#$%^&*()<>?/\|}{~:£]')
        return url_pattern.sub('', text)

    df["Message_body"] = df["Message_body"].apply(lambda text: remove_special_characters(text))

#removal of URLs
    def remove_urls(text):
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        return url_pattern.sub(r'', text)

    df["Message_body"] = df["Message_body"].apply(lambda text: remove_urls(text))

#lemmatization
    nltk.download('omw-1.4')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    from nltk.corpus import wordnet
    from nltk.stem import WordNetLemmatizer
    
    lemmatizer = WordNetLemmatizer()
    wordnet_map = {"N":wordnet.NOUN, "V":wordnet.VERB, "J":wordnet.ADJ, "R":wordnet.ADV}
    def lemmatize_words(text):
        pos_tagged_text = nltk.pos_tag(text.split())
        return " ".join([lemmatizer.lemmatize(word, wordnet_map.get(pos[0], wordnet.NOUN)) for word, pos in pos_tagged_text])
    df["Message_body"] = df["Message_body"].apply(lambda text: lemmatize_words(text))

#removal of stopwords (stopwords might not be helping in extracting common word so i am removing them because these words are very very common 
#so i am removing them
    nltk.download("stopwords")
    from nltk.corpus import stopwords
    ", ".join(stopwords.words('english'))

    STOPWORDS = set(stopwords.words('english'))
    def remove_stopwords(text):
        """custom function to remove the stopwords"""
        return " ".join([word for word in str(text).split() if word not in STOPWORDS])

    df["Message_body_without_stopwords"] = df["Message_body"].apply(lambda text: remove_stopwords(text))

#word counts
    def Word_Count(data_frame_col,counter_obj):
        for text in data_frame_col.values:
            for word in text.split():
                counter_obj[word] += 1
        return counter_obj

    cnt_words_dict_spam=Word_Count(df.query('Label=="Spam"')['Message_body_without_stopwords'],Counter())

    cnt_words_dict_nonspam=Word_Count(df.query('Label=="Non-Spam"')['Message_body_without_stopwords'],Counter())

#visualization of spam messages text analysis
    
    graphspam=pd.DataFrame(cnt_words_dict_spam.most_common(15),columns=['Word','Count'])
    graphspam=graphspam.sort_values('Count', ascending=1)
    

#visualization of non-spam messages text analysis
    
    graph_nonspam=pd.DataFrame(cnt_words_dict_nonspam.most_common(15),columns=['Word','Count'])
    graph_nonspam=graph_nonspam.sort_values('Count', ascending=1)
    
    label= st.selectbox('LABEL', df['Label'].unique())
    button=st.button('show results')
    
    if button :
        subset=df[df["Label"]== "Spam"]
        st.subheader("common keywords in spam SMS")
        fig=px.bar(graphspam,x='Count',y='Word', orientation='h')
        st.write(fig)
    else:
        subset=df[df["Label"]=="Non-Spam"]
        st.subheader("common keywords in Non-spam SMS")
        fig=px.bar(graph_nonspam,x='Count',y='Word', orientation='h')
        st.write(fig)
    
#  plotting of second graph is working fine in code but i am unable to display figure in streamlit
 #   df_by_date=df.groupby(["Date_Received"])
 #   no_of_messages_count=df_by_date['S. No.'].count()
 #   no_of_messages_count.plot()
 
    
    
if __name__=="__main__":
    main()
