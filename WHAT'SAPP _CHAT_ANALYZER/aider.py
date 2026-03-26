from urlextract import URLExtract
from collections import Counter
from wordcloud import WordCloud
from datetime import datetime
import string
import emoji
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
from stop_words import get_stop_words
import pathlib
import textwrap
import os
from dotenv import load_dotenv
from IPython.display import display
from IPython.display import Markdown
import google.generativeai as genai



load_dotenv()
genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))

stopwords = get_stop_words('en')
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F700-\U0001F77F"  # alchemical symbols
                           u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                           u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                           u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                           u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                           u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                           u"\U00002702-\U000027B0"  # Dingbats
                           u"\U000024C2-\U0001F251"  
                           "]+", flags=re.UNICODE)



def fetch_chat_stats(df):
    emoji = [emoji_pattern.findall(msg) for msg in df['messages']]
    emojis = []
    messages = []
    for moj in emoji:
        if(len(moj)>=1):
            li = []
            for i in range(len(moj)):
                for obj in moj[i]:
                    li.append(obj)
            moj = li
        emojis.extend(moj)  
    emojis = [emoji for emoji in emojis if emoji != '️']
    num_messages = len(df)
    words = [word for msg in df['messages'] for word in msg.split() if msg != '<Media omitted>\n' and word not in emojis and word not in string.punctuation]
    word_counts = Counter(words)
    word_counts = dict(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))
    num_words = len(words)
    num_media = len(df[df['messages']=='<Media omitted>'])
    num_emojis = len(emojis)
    emoji_counts = Counter(emojis)
    emoji_counts = dict(sorted(emoji_counts.items(), key=lambda item: item[1], reverse=True))
    extractor = URLExtract()
    num_urls = len([extractor.find_urls(msg) for msg in  list(df['messages']) if len(extractor.find_urls(msg))!=0])
    messages = [msg for msg in df['messages'] if '<Media omitted>' not in msg and 'This message was deleted' not in msg]
    return num_messages,num_words,num_media,num_urls,num_emojis,messages,emojis

def fetch_wordcloud(messages):
    text = ' '.join(messages)
    wordcloud = WordCloud(width=300, height=300, background_color='white', stopwords=set(stopwords)).generate(text)
    plt.figure(figsize=(8, 8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plotpath = "trash/word_cloud.png"
    plt.savefig(plotpath)
    plt.close()
    return plotpath

def fetch_activechatter(df):
    data = df['users'].value_counts()
    data = dict(data.head())
    users = list(data.keys())
    message_counts = list(data.values())
    colors = sns.color_palette("hls", len(users))
    plt.figure(figsize=(10, 6))
    sns.barplot(x=users, y=message_counts, palette=colors)
    plt.xlabel('Chatters')
    plt.ylabel('Number of Messages')
    plt.title('Number of Messages by User')
    plt.tight_layout()
    plotpath = "trash/most_active_users.png"
    plt.savefig(plotpath)
    plt.close()
    return plotpath

def fetch_topchatwords(df,emojis):
    words = [word for msg in df['messages'] for word in msg.split() if '<Media omitted>' not in msg and word not in emojis and word not in string.punctuation]
    word_counts = Counter(words)
    word_counts = dict(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))
    data = {'chat_words': word_counts.keys(), 'word_frequency':word_counts.values()}
    chat_words = list(word_counts.keys())
    word_frequency = list(word_counts.values())
    colors = sns.color_palette("hls", 25)
    plt.figure(figsize=(7, 6))
    sns.barplot(x=word_frequency[:25], y=chat_words[:25], palette=colors)
    plt.xlabel('frequency')
    plt.ylabel('words')
    plt.title('chat word frequency')
    plt.tight_layout()
    plotpath = "trash/chatwordfrequency.png"
    plt.savefig(plotpath)
    plt.close()
    return plotpath

def fetch_topchatemojis(emojis):
    emoji_counts = Counter(emojis)
    emoji_counts = dict(sorted(emoji_counts.items(), key=lambda item: item[1], reverse=True))
    data = {'chat_emojis': emoji_counts.keys(), 'emoji_frequency':emoji_counts.values()}
    chat_emojis = list(emoji_counts.keys())
    emoji_frequency = list(emoji_counts.values())
    if(len(data)<25):
        df = pd.DataFrame(data)
    else:
        df = (pd.DataFrame(data))[:25]
    colors = sns.color_palette("hls", 25)
    plt.figure(figsize=(7, 6))
    sns.barplot(x=emoji_frequency[:25], y=chat_emojis[:25], palette=colors)
    plt.xlabel('frequency')
    plt.ylabel('emojis')
    plt.title('chat emoji frequency')
    plt.tight_layout()
    plotpath = "trash/chat_emoji_frequency.png"
    plt.savefig(plotpath)
    plt.close()
    return df,plotpath

def fetch_chatactivitybymonth(df):
    month_order = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]    
    df = df.groupby(['month']).count()['messages'].reset_index()
    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)
    message_counts = list(df['messages'])
    months = list(df['month'])
    colors = sns.color_palette("hls", len(months))
    plt.figure(figsize=(10, 6))
    sns.barplot(x=months, y=message_counts, palette=colors)
    plt.xlabel('Month')
    plt.ylabel('Number of Messages')
    plt.title('Number of Messages by Month')
    plt.tight_layout()
    plotpath = "trash/messages_by_month.png"
    plt.savefig(plotpath)
    plt.close()
    return plotpath

def fetch_chatactivitybyday(df):
    df['day'] = df['date'].dt.day_name()
    df = df.groupby(['day']).count()['messages'].reset_index()
    message_counts = list(df['messages'])
    days = list(df['day'])
    colors = sns.color_palette("hls", len(days))
    plt.figure(figsize=(10, 6))
    sns.barplot(x=days, y=message_counts, palette=colors)
    plt.xlabel('Day')
    plt.ylabel('Number of Messages')
    plt.title('Number of Messages by Day')
    plt.tight_layout()
    plotpath = "trash/messages_by_day.png"
    plt.savefig(plotpath)
    plt.close()
    return plotpath

def get_response(person1,person2,chat):
    prompt = f"""I am providing a whatsapp conversation between person1 and person2. Predict the relationship between them based on their chat and analyze the characters of both individuals. Provide your analysis in the following format:

relationship: 
    2 to 3 points
character of person1:
    3 to 4 points
character of person2:
    3 to 4 points
sentiment analysis:
    3 to 4 points
summary:
    3 to 4 points

The chat goes like this: {chat}.Please ensure that your output follows this format consistently.Be very certain in maintaining the subheaders in the format provided and don't use anything(not even trailing space after colon) otherthan those words(relationship:, character of person1:, character of person2:, sentiment analysis:, summary:) in subheaders and even maintain the lower case of subheaders. Ignore any harmful content in the chat.
"""
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt,stream=True)
    response.resolve()
    li = response.text.split('\n')
    # li = ['Relationship:', '- Friends who have broken up recently.', '- They still have feelings for each other, but are trying to move on.', '', 'Character of A:', '- Emotional and impulsive: Expresses intense emotions throughout the conversation.', '- Determined to move on from the relationship: Repeatedly says "bye" and tries to cut off communication.', '- Has difficulty controlling their emotions: Uses strong language, like "vey" and "illa" to express anger and frustration.', '- Tries to maintain a friendly relationship: Uses terms of endearment, like "jyo baby" and "my baby", even after the breakup.', '', 'Character of B:', '- Tries to remain calm and rational: Often responds with short, simple answers or emojis.', '- Willing to work on the relationship: Suggests meeting up or communicating to resolve their issues.', '- Feels hurt and confused by the breakup: Asks "Em sambandham ledhu" (What is our relationship now?) and "Endhuku baby ala antav" (Why are you calling me baby?).', '- Tries to maintain a friendly relationship: Also uses terms of endearment, like "naanna" and "prashu baabu", even after the breakup.', '', 'Sentiment Analysis:', '- Mostly negative: The conversation is filled with expressions of anger, sadness, and hurt.', '- Some positive moments: There are a few brief instances of positivity, such as when they reminisce about happy memories.', '', 'Summary:', '- A and B are friends who have recently broken up, and they are both struggling to deal with the emotional fallout. They still have feelings for each other, but they are trying to move on. The conversation is filled with expressions of anger, sadness, and hurt, but there are also a few brief instances of positivity. Overall, the sentiment of the conversation is mostly negative.']
    print(li)
    rel = li[1:li.index('character of person1:')-1]
    a = li[li.index('character of person1:')+1:li.index('character of person2:')-1]
    b = li[li.index('character of person2:')+1:li.index('sentiment analysis:')-1]
    aoc = li[li.index('sentiment analysis:')+1:li.index('summary:')-1]
    soc = li[li.index('summary:')+1:]
    req = [rel,a,b,aoc,soc]
    person_1 = ''
    for i in person1:
        if i.isalpha():
            person_1 += i
    person_2 = ''
    for i in person2:
        if i.isalpha():
            person_2 += i
    for i in range(len(req)):
        for j in range(len(req[i])):
            req[i][j] = req[i][j].replace('person1',person_1)
            req[i][j] = req[i][j].replace('person2',person_2)
    return req[0],req[1],req[2],req[3],req[4]






