from datetime import timedelta

def timeConvert(originalTime): #converts UTC to GMT+8
    newTime = originalTime + timedelta(hours=8)
    return newTime