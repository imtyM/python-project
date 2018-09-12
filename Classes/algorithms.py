
class algorithms:

    def __init__(self, DBinstance, primary_string="primary_print."):
        self.db = DBinstance
        self.primaryString = primary_string

    def processQuery(self, inputData, deviationStep = 0.1):
        doc_count = 0
        cursor = None
        deviation = 0

        while doc_count == 0 and deviation < 15 : 
            cursor = self.db.queryOnDeviation(inputData, deviation, self.primaryString)
            doc_count = cursor.count()
            deviation += deviationStep

        if doc_count == 0:
            print('No Docs found...\nWith a deviation of : ', deviation)
        else:
            print('Estimated location as : ', cursor.next()["location"], 'count of :', doc_count, 'with deviation of : ', deviation)


    
    def debugProcess(self, inputData):
        print('Processing Location\n\n')

        self.processQuery(inputData)

        print('\n\n\nDone processing location\n\n\n')





        
        