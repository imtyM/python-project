import pymongo

KNOWN_CELLS_LAB = ['ef39', 'f4b2', 'da36', 'ea75', '35fd', '51a6', '51a5', 'd9dd', 'ef61', '4de6', 'bbd2', '471a', '403a', '4de7', '4de5', '4db5', 'cbb7', '46f2', 'e77f', '46df', '46dd', '51a7', '4db3', '4648', '3a68', 'cbb9', '4dc8', 'ccf7']

class mongoDB:
    
    def __init__(self, collection,dataBase='projectDB', host='localhost', port=27017):
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
    
    def findAll(self):
        return self.collection.find()
    
    def updateFingerprint(self, data):
        query = {"location" : data["location"]}
        # update history
        for sample in data["fingerprint_set"]:
            push_string = "fingerprint_set." + sample 
            update = {
                "$push" : {
                    push_string:{
                        "$each": data["fingerprint_set"][sample],
                        "$slice" : -500
                    }
                }
            }
            updateOneResult = self.collection.update_one(query, update, upsert=True)
        # update primary_print            
        for sample in data["primary_print"]:
            push_string = "primary_print." + sample 
            update = {
                "$set" : { 
                    push_string: data["primary_print"][sample]
                }
            }
            updateOneResult = self.collection.update_one(query, update, upsert=True)
        return updateOneResult
   
    def findByRegex(self, regex):
       query = {
           "location" : {"$regex": regex}
       }
       findResult = self.collection.find(query)
       return findResult
    
    def findByQuery(self, query):
        return self.collection.find(query)

    def queryOnDeviation(self, input_data, deviation, fieldString="primary_print."):
        query = dict()
        primaryString = fieldString
        for cell in input_data:
            if cell in KNOWN_CELLS_LAB:
                query[primaryString + cell] = {"$gt" : input_data[cell] - deviation, "$lte": input_data[cell] + deviation}
        
        print('Built query : \n', query, '\n')

        return self.findByQuery(query)
        

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
                print('Printing all collections in DB: ' + self.collectionName)
                
                self.dataBase.list_collection_names()

            else:
                print(cmd + 'Please enter a valid command.')

            print('\n+++++\n') 
            
        print('Broke from loop, goodbye.')

     