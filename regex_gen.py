import re
from mock_data import testExtractText

class RegexGen():
    datePattern = r'\d{4}/\d{2}/\d{2}'
    timePattern = r'\d{1,2}:\d{2}'
    testText =  testExtractText
    def testExtract(self):
        dates = re.findall(self.datePattern, self.testText)
        times = re.findall(self.timePattern, self.testText)
        for i in range(len(dates)):
            print(f'日付: {dates[i]}, 開始時間: {times[i*2]}, 終了時間: {times[i*2 + 1]}')
            
regexGen = RegexGen()
regexGen.testExtract()