from urlextract import URLExtract
extractor = URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(seleted_user,df):
    
    if seleted_user != 'Overall':
        df = df[df['Contact'] == seleted_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['Message']:
        words.extend(message.split())

    # fetch the total number of media messages
    num_media_message = df[df["Message"] =='<Media omitted>'].shape[0]

    # fetch the total number of links 
    links=[]
    for message in df["Message"]:
        links.extend(extractor.find_urls(message))


    return num_messages , len(words), num_media_message, len(links)


def fetch_most_busy_users(df):
    x = df['Contact'].value_counts().head()
    df = round((df['Contact'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns = ({"index":'Name',"Contact":"Percent"}))
    return x, df
   
def word_cloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]
    
    wc = WordCloud(width=500, height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df["Message"].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]

    words = []
    for message in df["Message"]:
        words.extend(message.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]
    emojis = []
    for message in  df['Message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]
    monthly_timeline = df.groupby(["Month","Year"]).count()["Message"].reset_index()
    time = []
    for i in range(monthly_timeline.shape[0]):
        time.append(monthly_timeline['Month'][i] + "-" + str(monthly_timeline['Year'][i]))

    monthly_timeline['Time'] = time
    return monthly_timeline


def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]
    daily_timeline = df.groupby(["Date"]).count()["Message"].reset_index()
    
    return daily_timeline


def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]
    return df["Day_name"].value_counts()


def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]
    return df["Month"].value_counts()

