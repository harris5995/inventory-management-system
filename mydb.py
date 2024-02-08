import mysql.connector
from decouple import config

# Replace 'DATABASE_PASSWORD' with the actual key in your .env file
password = config('DATABASE_PASSWORD')

dataBase = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd=password,
)

# Prepare a cursor object
cursorObject = dataBase.cursor()

# Create a database
cursorObject.execute("CREATE DATABASE IF NOT EXISTS warehouse_inventory")
print("All Done!")