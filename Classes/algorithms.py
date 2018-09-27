
import os

class algorithms:

    def __init__(self, DBinstance, primary_string="primary_print."):
        self.db = DBinstance
        self.primaryString = primary_string

    def processQuery(self, inputData, deviationStep = 0.1):
        doc_count = 0
        cursor = None
        deviation = 0

        while doc_count == 0 and deviation < 30 : 
            cursor = self.db.queryOnDeviation(inputData, deviation, self.primaryString)
            doc_count = cursor.count()
            deviation += deviationStep

        if doc_count == 0:
            print('No Docs found...\nWith a deviation of : ', deviation)
        else:
            locale = cursor.next()["location"]
            print('Estimated location as : ', locale, 'count of :', doc_count, 'with deviation of : ', deviation)
            os.system('spd-say '+ locale)


    
    def debugProcess(self, inputData):
        print('Processing Location\n\n')

        self.processQuery(inputData)

        print('\n\n\nDone processing location\n\n\n')





        
        