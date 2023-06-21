from pony.orm import Database

db = Database()

db.bind(provider='postgres', user="postgres", password="root", host="localhost", database="license-managment")
