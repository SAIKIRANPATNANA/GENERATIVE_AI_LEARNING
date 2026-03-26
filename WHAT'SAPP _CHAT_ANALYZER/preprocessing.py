import pandas as pd
import warnings as warn 
import re
from aider import get_response
warn.filterwarnings("ignore")

def preprocess1(data):
    if((data.count('am')>10 and data.count('pm')>10) or (data.count('AM')>10 and data.count('PM')>10)):
        pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APMapm]{2}\s-\s' #12 hr pattern
    else:
        pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s" #24 hr 
    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({'user_message':messages, 'message_date':dates})
    for i in range(len(df)):
        if('<This Message Was Edited>' in df.loc[i]['user_message']):
            df.at[i,'user_message'] = df.loc[i]['user_message'].replace('<This Message Was Edited>','')
        if('\n' in df.loc[i]['user_message']):
            df.at[i,'user_message'] = df.loc[i]['user_message'].replace("\n",'')
        if(':' not in df.loc[i]['user_message'] or  '<Media omitted>' in df.loc[i]['user_message'] or  'null' in df.loc[i]['user_message'] or 'http' in df.loc[i]['user_message'] or 'This message was deleted' in df.loc[i]['user_message']):
            df = df.drop(i)
    df = df.reset_index(drop=True)
    users = []
    messages = [] 
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1: ]:
            users.append(entry[1])
            messages.append(entry[2])
    df = df.reset_index(drop=True)
    if(len(df)<len(users)):
        users = users[:len(df)]
        messages = messages[:len(df)]
    else: 
        df = df[:len(users)]
    df['users'] = users 
    df['messages'] = messages
    df  = df.drop('user_message',axis=1)
    person1 = df.users.unique()[0]
    person2 = df.users.unique()[1]
    for i in range(len(df)):
        if df.loc[i]['users'] == person1:
            df.at[i,'users'] = 'person1'
        elif df.loc[i]['users'] == person2:
            df.at[i,'users'] = 'person2'
    chat = []
    for i in range(len(df)):
        chat.append(df.loc[i]['users']+' :   '+df.loc[i]['messages'])
    return person1,person2,chat

def preprocess2(data):
    if((data.count('am')>10 and data.count('pm')>10) or (data.count('AM')>10 and data.count('PM')>10)):
        pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APMapm]{2}\s-\s' #12 hr pattern
        if (data.count('am')>10 and data.count('pm')>10):
            format = '%d/%m/%Y, %I:%M %p - '
        else: 
            format = '%m/%d/%y, %I:%M %p - '

    else:
        pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s" #24 hr 
        format='%m/%d/%y, %H:%M - '
    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({'user_message':messages, 'message_date':dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format=format)
    df.rename(columns={'message_date':'date'}, inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    for i in range(len(df)):
        if('<This Message Was Edited>' in df.loc[i]['user_message']):
            df.at[i,'user_message'] = df.loc[i]['user_message'].replace('<This Message Was Edited>','')
        if('\n' in df.loc[i]['user_message']):
            df.at[i,'user_message'] = df.loc[i]['user_message'].replace("\n",'')
        if('null' in df.loc[i]['user_message']):
            df = df.drop(i)
    df = df.reset_index(drop=True)
    users = []
    messages = [] 
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1: ]:
            users.append(entry[1])
            messages.append(entry[2])
    if(len(df)<len(users)):
        users = users[:len(df)]
        messages = messages[:len(df)]
    else: 
        df = df[:len(users)]
    df['users'] = users 
    df['messages'] = messages
    df = df.drop('user_message',axis=1)
    return df