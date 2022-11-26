from datetime import timedelta

def timeConvertShort(originalTime): #converts UTC to GMT+8
    newTime = str((originalTime + timedelta(hours=8)).strftime("%d/%m/%y, %H:%M:%S"))
    return newTime