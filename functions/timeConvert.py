from datetime import timedelta

def timeConvert(originalTime): #converts UTC to GMT+8
    newTime = str((originalTime + timedelta(hours=8)).strftime("%d %B %Y, %I:%M:%S%p"))
    return newTime