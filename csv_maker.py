import csv
import mock_data
from pathlib import Path

class CsvMaker():

    def __init__(self, label= 'TMD_SHARE_202309'):
        self.label = label

    def makeCSV(self, dstPath, entities):
        Path(dstPath).parent.mkdir(parents=True, exist_ok=True)
        with open(dstPath, 'w', newline='') as csvFile:
            csvWriter = csv.writer(csvFile)
            for entity in entities:
                csvWriter.writerow(entity)

    def testMakeCSV(self):
        with open('./csv/' + self.label + '_' + '.csv', 'w') as csvFile:
            csvWriter = csv.writer(csvFile)
            for entity in mock_data.mockedEntity:
                csvWriter.writerow(entity)
