import pymongo

class mongoDB:

    
    def __init__(self, host='localhost', port=27017, dataBase='projectDB', collection='fingerprints'):
        self.collectionName = collection
        self.dataBaseName = dataBase

        self.mongoClient = pymongo.MongoClient(host,port)
        self.dataBase = self.mongoClient[dataBase]
        self.collection = self.dataBase[collection]

    def changeCollection(self, collection):
        self.collectionName = collection
        self.collection = self.dataBase[collection]
    
    def changeDataBase(self, dataBase):
        self.dataBaseName = dataBase
        self.dataBase = self.mongoClient[dataBase]

    def insertOne(self, data):
        insertOneResult = self.collection.insert_one(data)
        return insertOneResult
   
    def insertOneInCollection(self, data, collection):
        insertOneResult = self.dataBase[collection].insert_one(data)
        return insertOneResult

    def insertMany(self, data):
        insertManyResult = self.collection.insert_many(data)
        return insertManyResult
    
    def insertManyInCollection(self, data, collection):
        insertManyResult = self.dataBase[collection].insert_many(data)
        return insertManyResult

    def debug_loop(self):
        print(r"""
                Begin Debug loop
        """)

        while 1:
            print(r"""
                Commands:
                    exit
                    readcollection
                    readdb
            """)

            cmd = input (">>")
            
            if cmd == 'exit' or cmd == 'eixt': 
                print('Exiting debug loop')
                break
            elif cmd == 'readcollection':
                print('Printing data in entire collection: ' + self.collectionName)
                for data in self.collection.find():
                    print(data)
            
        print('Broke from loop, goodbye.')

     