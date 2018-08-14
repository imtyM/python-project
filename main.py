from Classes.serialClass import serialClass
from Classes.mongoDB import mongoDB

mongo = mongoDB()
mongo.insertOne({
    "imprint" : "this space is for an object of imprints",
     "location": "this space is for an object of locations"
     })
mongo.debug_loop()
