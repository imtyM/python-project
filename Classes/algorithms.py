import os
import itertools as it
from collections import Counter

KNOWN_CELLS_LAB = ['ef39', 'f4b2', 'da36', 'ea75', '35fd', '51a6', '51a5', 'd9dd', 'ef61', '4de6', 'bbd2', '471a', '403a', '4de7', '4de5', '4db5', 'cbb7', '46f2', 'e77f', '46df', '46dd', '51a7', '4db3', '4648', '3a68', 'cbb9', '4dc8', 'ccf7']
class algorithms:

    def __init__(self, DBinstance, primary_string="primary_print."):
        self.db = DBinstance
        self.primaryString = primary_string

    def processQuery(self, inputData, deviationStep = 0.25):
        doc_count = 0
        cursor = None
        deviation = 0
        found_locations = []



        cells = self._getCellsList(inputData)
        cell_permutations = self._getPermutations(cells)
        print('CELL PERMUTATIONS ', cell_permutations)

        while doc_count == 0 and deviation < 10 : 
            
            for cellList in cell_permutations:
                print('CURRENT CELL LIST: ', cellList)

                query = self._buildQuery(cellList, inputData, deviation)
                cursor = self.db.findByQuery(query)
                doc_count = cursor.count()

                if doc_count > 0:
                    # if we get a really strong match, break and accept it. 
                    if len(cellList) > 3 and deviation < 4:
                        print('BREAKING with deviation of ', deviation)
                        print('Location of ', cursor.next()["location"]) 
                        break
                    for doc in cursor:
                        found_locations.append(doc["location"])

            deviation += deviationStep

        print('found locations ', found_locations)
        print('most common location: ', self._mostCommon( found_locations ))
        # self._processResults(doc_count, deviation, cursor)

    def _mostCommon(self, locs):
        if len(locs) > 0:
            el = Counter(locs)
            return el.most_common(1)[0][0]
        return "none"

    def _getPermutations(self, cells):
        permutations = []
        permutations.append(cells)
        
        if len(cells) > 6 :
            for cellList in it.combinations(cells, 6):
                permutations.append(list( cellList ))

        if len(cells) > 5 :
            for cellList in it.combinations(cells, 5):
                permutations.append(list( cellList ))

        if len(cells) > 4 :
            for cellList in it.combinations(cells, 4):
                permutations.append(list( cellList ))

        if len(cells) > 3:
            for cellList in it.combinations(cells, 3):
                permutations.append(list( cellList ))

        return permutations
        

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
        return query


    
    def debugProcess(self, inputData):
        print('Processing Location\n\n')

        self.processQuery(inputData)

        print('\n\n\nDone processing location\n\n\n')





        
        