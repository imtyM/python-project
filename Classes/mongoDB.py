import pymongo

class mongoDB:

    
    def __init__(self, host='localhost', port=27017, dataBase='projectDB', collection='fingerprints'):
        self.collectionName = collection
        self.dataBaseName = dataBase
        self.hostName = host

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
                    dbinfo
                    readcollection
                    readdb
            """)

            cmd = input (">>")
            print('\n+++++\n') 

            if cmd == 'exit' or cmd == 'eixt': 
                print('Exiting debug loop')
                break

            elif cmd == 'dbinfo':
                print('Current mongoDB object is linked to: ' + self.hostName)
                print('And is linked to the data base: ' + self.dataBaseName)
                print('And the dabase is currently pointing to collection: ' + self.collectionName)

            elif cmd == 'readcollection':
                print('Printing data in entire collection: ' + self.collectionName)
                for data in self.collection.find():
                    print(data)

            elif cmd == 'readdb':
                print('Printing all collections in DB: ' + self.dataBaseName)
                self.dataBase.list_collection_names()

            else:
                print(cmd + 'Please enter a valid command.')

            print('\n+++++\n') 
            
        print('Broke from loop, goodbye.')

     