import re
from datetime import datetime
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date type
    
    # Define a function to parse dates with fallback
    def parse_date(date_str):
        try:
            # Try parsing with the four-digit year format
            return datetime.strptime(date_str.strip(" - "), "%d/%m/%Y, %H:%M")
        except ValueError:
            try:
                # Fallback to two-digit year format
                 datetime.strptime(date_str.strip(" - "), "%d/%m/%y, %H:%M")
            except ValueError:
                # Return NaT for invalid formats
                return pd.NaT

    # Apply the date parsing function
    df['message_date'] = df['message_date'].apply(parse_date)

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

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
