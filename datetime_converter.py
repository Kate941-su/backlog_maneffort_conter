from datetime import datetime
import mock_data

class DateTimeConverter():
    dateFormat = '%Y/%m/%d'
    timeFormat = '%H:%M'        
    
    # str -> datetime.date
    def convertDate(self, dateStr):
        return datetime.strptime(dateStr, self.dateFormat).date()
    
    # str -> datetime.time
    def convertTime(self, timeStr):
        return datetime.strptime(timeStr, self.timeFormat).time()
    
    # str(from json) -> datetime.date
    def convertDateFromJson(self, dateFormatFromJson):
        spritDate = dateFormatFromJson.split('T')
        spritDate = spritDate[0].split('-')
        date = f'{spritDate[0]}/{spritDate[1]}/{spritDate[2]}'
        return datetime.strptime(date, self.dateFormat).date()
    
    # datetime.date -> str
    def deConvertDate(self, date: datetime.date):
        return date.strftime(self.dateFormat)
    
   # datetime.time -> str
    def deConvertTime(self, time: datetime.time):
        return time.strftime(self.timeFormat)
    
    # TODO ERROR HANDLING
    def getTimeDuration(self, now: datetime.time, then: datetime.time, type = 'minutes'):
        startMinutes = then.hour * 60 + then.minute
        endMinutes =  now.hour * 60 + now.minute
        res = endMinutes - startMinutes
        if (res < 0) : # If working over the day, endminutes add +1 day minitus.
            res += 24 * 60
        return res
    
# test
def main():    
    datetimeConverter = DateTimeConverter()
    now = datetimeConverter.convert(mock_data.datetimeStr2)
    then = datetimeConverter.convert(mock_data.datetimeStr1)
    delta = datetimeConverter.getTimeDuration(now, then)
    print(delta)
    
if __name__ == '__main__':
    main()