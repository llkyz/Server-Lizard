from .sql_start import sqlCursor, sqlDb

def updateCoins(id, amount):
    sql = 'UPDATE userDB SET coins = LEAST(coins + %s, 2147483647) WHERE userId = %s'
    val = (amount, id)
    sqlCursor.execute(sql, val)
    sqlDb.commit()