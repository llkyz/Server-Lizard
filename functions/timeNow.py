from datetime import datetime, timedelta

def timeNow(): #converts UTC to GMT+8
    return (datetime.utcnow() + timedelta(hours=8)).strftime("%d %B %Y, %I:%M:%S%p")