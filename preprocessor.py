import re
import pandas as pd
def preprocess(data):
    #extract date and time
    def date_time(s):
        pattern = '\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s'
        result = re.match(pattern,s)
        if  result:
            return True
        return False

    #extract contacts
    def find_contact(s):
        s = s.split(":")
        if len(s)==2:
            return True
        else:
            return False
    

    #extract message
    def getMessage(line):
        splitline = line.split(" - ")
        datetime = splitline[0]
        date, time = datetime.split(', ')
        message = " ".join(splitline[1:])

        if find_contact(message):
            splitmessage = message.split(": ")
            author = splitmessage[0]
            message = splitmessage[1]
        else:
            author = None
        return date, time, author, message
    
    data = []
    conversation = "WhatsApp Chat with Sec-A UNOFFICIAL.txt"
    with open(conversation, encoding="utf-8") as fp:
        fp.readline()
        messageBuffer = []
        date, time, author = None, None, None
        while True:
            line = fp.readline()
            if not line:
                break
            line = line.strip()
            if date_time(line):
                if len(messageBuffer)>0:
                    data.append([date, time, author , " ".join(messageBuffer)])
                    messageBuffer.clear()
                    date, time, author, message = getMessage(line)
                    messageBuffer.append(message)
                else:
                    messageBuffer.append(line)

    
    df = pd.DataFrame(data, columns=["Date", "Time", "Contact", "Message"])
    df['Date']=pd.to_datetime(df["Date"])
    df["Month"]=df["Date"].dt.month_name()
    df["Year"]=df["Date"].dt.year
    df["Day_name"]=df["Date"].dt.day_name()
    
    return df