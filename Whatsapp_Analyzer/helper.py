import re
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji
import matplotlib.pyplot as plt


# Helper function to read stopwords
def read_stopwords():
    try:
        with open('stop_hinglish.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        print("Error: The 'stop_hinglish.txt' file is missing.")
        return ""


# Function to fetch statistics
def fetch_stats(user_name, df):
    if user_name != "Overall":
        df = df[df['user'] == user_name]

    # Fetching total number of messages
    no_of_messages = df.shape[0]

    # Fetching total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Fetching total number of media files
    no_of_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    # Fetching number of links shared
    links = []
    # Regular expression for matching URLs
    url_pattern = r'https?://(?:www\.)?[\w-]+\.[a-z]+(?:/[\w\-./?%&=]*)?'

    for message in df['message']:
        urls = re.findall(url_pattern, message)
        links.extend(urls)

    return no_of_messages, len(words), no_of_media_messages, len(links)


# Function to get most active users
def most_active_users(df):

    x = df['user'].value_counts().head()
    per_df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns = {'user':'Name','count':'Message Count'})

    return x, per_df


# Function to create the word cloud
def create_wordcloud(username, df):
    stop_words = read_stopwords()

    if username != 'Overall':
        df = df[df['user'] == username]

    # Filtering out group notifications and media omitted messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        words = [word for word in message.lower().split() if word not in stop_words]
        return " ".join(words)

    # Applying stop word removal
    temp['filtered_message'] = temp['message'].apply(remove_stop_words)

    # Generating word cloud
    wc = WordCloud(width=800, height=400, min_font_size=8, background_color='white')
    df_wc = wc.generate(temp['filtered_message'].str.cat(sep=' '))
    return df_wc


# Function to get top 20 most common words
def most_common_words(username, df):
    stop_words = read_stopwords()

    if username != 'Overall':
        df = df[df['user'] == username]

    # Filtering  out group notifications and media omitted messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    common_word_df = pd.DataFrame(Counter(words).most_common(20), columns=["Word", "Frequency"])
    return common_word_df


# Function to count emojis
def emoji_count(username, df):
    if username != 'Overall':
        df = df[df['user'] == username]

    # Extract emojis from messages
    emojis = [c for message in df['message'] for c in message if emoji.is_emoji(c)]
    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=["Emoji", "Count"])
    return emoji_df


# Function to create a monthly timeline
def monthly_timeline(username, df):
    if username != 'Overall':
        df = df[df['user'] == username]

    # Group by year, month_num, and month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    # Combine month and year into a single column
    timeline['time'] = timeline.apply(lambda x: f"{x['month']}-{x['year']}", axis=1)

    return timeline


def daily_timeline(username, df):
    # Filter data for the selected user
    if username != 'Overall':
        df = df[df['user'] == username]

    # Group messages by date
    dailytimeline = df.groupby('online_date').count()['message'].reset_index()

    return dailytimeline

def week_activity(username, df):
    if username != 'Overall':
        df = df[df['user'] == username]

    return df['day_name'].value_counts().reset_index().rename(columns = {'day_name':'Day','count':'No. of Messages'})

def month_activity(username, df):

    if username != 'Overall':
        df = df[df['user'] == username]

    return df['month'].value_counts().reset_index().rename(columns = {'month':'Month','count':'No. of Messages'})
    