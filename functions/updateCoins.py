from functions.sql_start import SQLObject

def updateCoins(id, amount):
    sql = 'UPDATE userDB SET coins = LEAST(coins + %s, 2147483647) WHERE userId = %s'
    val = (amount, id)
    SQLObject.execute(sql, val)
    SQLObject.commit()