import os
import itertools as it
from collections import Counter

KNOWN_CELLS_LAB = ['ef39', 'f4b2', 'da36', 'ea75', '35fd', '51a6', '51a5', 'd9dd', 'ef61', '4de6', 'bbd2', '471a', '403a', '4de7', '4de5', '4db5', 'cbb7', '46f2', 'e77f', '46df', '46dd', '51a7', '4db3', '4648', '3a68', 'cbb9', '4dc8', 'ccf7']
KNOWN_CELLS_REAL = ['02c8', 'f566', 'f57a', 'f567', 'f565', '46df', 'e77e', 'da4b', 'e77f', 'da49', 'f4b2', 'f58d', '46dd', 'f21d', 'ef39', 'ef61', 'e77d', 'd9ab', 'da36', 'd9dd', 'f579', 'ef63']
class algorithms:

    def __init__(self, DBinstance, primary_string="primary_print."):
        self.db = DBinstance
        self.primaryString = primary_string

    def processQuery(self, inputData, deviationStep = 0.25):
        doc_count = 0
        cursor = None
        deviation = 0
        found_locations = []
        break_location = None

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
                        break_location = cursor.next()["location"] 
                        break
                    for doc in cursor:
                        found_locations.append(doc["location"])

            deviation += deviationStep
        loc_len = len(found_locations)
        common = self._mostCommon(found_locations)
        print('found locations ', found_locations)
        print('most common location: ', common)
        return self._processResults(loc_len,doc_count, deviation, common, break_location)

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
            if cell in KNOWN_CELLS_REAL:
                cells.append(cell)
        return cells


    def _processResults(self,loc_len, doc_count, deviation, common, break_location):
        if doc_count == 0 and loc_len == 0:
            print('No Docs found...\nWith a deviation of : ', deviation)
        else:
            if break_location is not None:
                print('Estimated break location as : ', break_location, 'count of :', doc_count, 'with deviation of : ', deviation)
                os.system('spd-say '+ break_location)
                return break_location
            else:
                print('Estimated common location as : ', common, 'count of :', doc_count, 'with deviation of : ', deviation)
                os.system('spd-say '+ common)
                return common
                
    
    def _buildQuery(self, cells, input_data, deviation, fieldString="primary_print."):
        query = dict()
        primaryString = self.primaryString
        for cell in cells:
            query[primaryString + cell] = {"$gt" : input_data[cell] - deviation, "$lte": input_data[cell] + deviation}
        return query


    
    def debugProcess(self, inputData):
        print('Processing Location\n\n')

        return self.processQuery(inputData)

        print('\n\n\nDone processing location\n\n\n')





        
        