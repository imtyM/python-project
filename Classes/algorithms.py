import os

KNOWN_CELLS_LAB = ['ef39', 'f4b2', 'da36', 'ea75', '35fd', '51a6', '51a5', 'd9dd', 'ef61', '4de6', 'bbd2', '471a', '403a', '4de7', '4de5', '4db5', 'cbb7', '46f2', 'e77f', '46df', '46dd', '51a7', '4db3', '4648', '3a68', 'cbb9', '4dc8', 'ccf7']
class algorithms:

    def __init__(self, DBinstance, primary_string="primary_print."):
        self.db = DBinstance
        self.primaryString = primary_string

    def processQuery(self, inputData, deviationStep = 0.5):
        doc_count = 0
        cursor = None
        deviation = 0

        cells = self._getCellsList(inputData)

        while doc_count == 0 and deviation < 20 : 
            query = None
            cursor = None

            query = self._buildQuery(cells,inputData, deviation)
            cursor = self.db.findByQuery(query)


            doc_count = cursor.count()
            deviation += deviationStep

        self._processResults(doc_count, deviation, cursor)

    def _getCellsList(self, inputData):
        cells = []
        for cell in inputData:
            if cell in KNOWN_CELLS_LAB:
                cells.append(cell)
        return cells


    def _processResults(self, doc_count, deviation, cursor):
        if doc_count == 0:
            print('No Docs found...\nWith a deviation of : ', deviation)
        else:
            locale = cursor.next()["location"]
            print('Estimated location as : ', locale, 'count of :', doc_count, 'with deviation of : ', deviation)
            os.system('spd-say '+ locale)
    
    def _buildQuery(self, cells, input_data, deviation, fieldString="primary_print."):
        query = dict()
        primaryString = self.primaryString
        for cell in cells:
            query[primaryString + cell] = {"$gt" : input_data[cell] - deviation, "$lte": input_data[cell] + deviation}
        
        print('Built query : \n', query, '\n')

        return query


    
    def debugProcess(self, inputData):
        print('Processing Location\n\n')

        self.processQuery(inputData)

        print('\n\n\nDone processing location\n\n\n')





        
        