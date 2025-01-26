import re
from datetime import datetime
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s?\d{1,2}:\d{2}(?:\s?[APap][Mm])?\s?-\s?'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    #Cleaning extra spaces and new line character
    dates  = [date.replace('\u202f', ' ') for date in dates]
    messages = [message.strip() for message in messages]

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date type
    
    # Define a function to parse dates with fallback
    def parse_date(date_str):
        date_str = date_str.strip(" - ")
        for fmt in ("%d/%m/%Y, %H:%M", "%d/%m/%Y, %I:%M %p", "%d/%m/%y, %H:%M", "%d/%m/%y, %I:%M %p"):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return pd.NaT  # Return NaT if no format matches

    # Apply the date parsing function
    df['message_date'] = df['message_date'].apply(parse_date)

    # Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Split the user-message data into separate user and message columns
    users = []
    messages = []

    for message in df['user_message']:
        if ": " in message:
            user, actual_message = message.split(": ", 1)  # Split into two parts
            users.append(user)
            messages.append(actual_message)
        else:
            users.append("Group Notification")
            messages.append(message)

    # Add the user and message columns to the dataframe
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract year, month, day, hour, and minute from the 'date' column
    df['online_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year.astype(str).replace(',', '')
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
