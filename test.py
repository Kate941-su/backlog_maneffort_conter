from backlog_api import BacklogApi
from pprint import pprint
import datetime_converter
import datetime
import secret
import json
from csv_maker import CsvMaker

def makeEntity(issueName, date, start, end, productionTime, person):
    datetimeConverter = datetime_converter.DateTimeConverter()
    strDate = datetimeConverter.deConvertDate(date)
    strStart = datetimeConverter.deConvertTime(start)
    strEnd = datetimeConverter.deConvertTime(end)
    return [issueName, strDate, strStart, strEnd, str(productionTime), person]
    
def main():
    payload = {
        'apiKey' : secret.API_KEY,
        'count' : 100
    }
    projectID = 292193    
    backlogApi = BacklogApi(payload, projectID)

def read_json_test():
    with open('params.json') as f:
        di = json.load(f)
    print(di['issue_name'])        
    print(di['name_dict'])
    print(di['start_date'])        
    print(di['end_date'])
    
def csv_test():
    payload = {
        'apiKey' : secret.API_KEY,
    }
    with open('params.json') as f:
        params = json.load(f)

    datetimeConverter = datetime_converter.DateTimeConverter()
    
    # get params from JSON in local
    projectID = params['project_id']
    issueName = params['issue_name']
    nameDict = params['name_dict']
    startDate = datetimeConverter.convertDate(params['start_date'])
    endDate = datetimeConverter.convertDate(params['end_date'])
    outputPath = params['output_path']

    # initialise parameters
    productTimetotal = 0
    notifiyIssueList = []
    start = 1
    issueCountForShow = start
    entities = []
    entities.append([
        "Backlogキー + 項目名",
        "日付",
        "開始",
        "終了",
        "作業時間（分）",
        "作業者",
        "備考（摘要項目で伝えきれないと判断した場合は記入してください）"
        ])

    # set up API and issue list
    backlogApi = BacklogApi(payload, projectID = projectID)
    issueTotal = backlogApi.getIssueCountInProject()
    issueList = [(issueName + '-' + str(issueID)) for issueID in range(start, issueTotal)]
    # TODO get multipul task comment per single API
    for issueID in issueList:
        isNeedBlankRow = False
        bufferList = []
        issueData = backlogApi.getIssue(issueID)
        issueTitle = f'{issueID} {backlogApi.getIssueTitle(issueData)}'
        comments = backlogApi.getComments(issueID)  
        oldestCommentDate = startDate
        for comment in comments:
            content = comment['content']
            if (content):
                productDataList = backlogApi.extractProductdata(content)
                for productData in productDataList:
                    date = datetimeConverter.convertDate(productData[0])
                    start = datetimeConverter.convertTime(productData[1])
                    end = datetimeConverter.convertTime(productData[2])
                    timeDelta = datetimeConverter.getTimeDuration(end, start)                
                    commentUser = nameDict[backlogApi.getCommentUser(comment)]
                    entity = makeEntity(issueTitle, date, start, end, timeDelta, commentUser)
                    if (entity and date >= startDate and date <= endDate):
                        isNeedBlankRow = True
                        bufferList.append(entity)
                        productTimetotal += timeDelta
                    oldestCommentDate = date        
        # if oldest comment date (get maximum 100) date up to target month, Notify
        if ( len(comments) >= 100 and oldestCommentDate > startDate):
            notifiyIssueList.append(issueID)
        # Sort by date
        bufferList.sort(key = lambda x: x[1])
        for buffer in bufferList:
            entities.append(buffer)
        if (isNeedBlankRow):
            entities.append([])
        print(f'{issueCountForShow} done!')
        issueCountForShow += 1
    # Output total product time
    entities.append(['','','','',productTimetotal, '予算'])
    pprint(f'You should check this issue yourself below 👇. Because It has posibility to miss out some issue production time')
    pprint(notifiyIssueList)
    csvMaker = CsvMaker()
    csvMaker.makeCSV(outputPath, entities)
    
def unitIssueTest():
    payload = {
        'apiKey' : secret.API_KEY,
    }
    backlogApi = BacklogApi(payload, projectID = '292193')
    issueID = 'TMD_SHARE-173'
    issueData = backlogApi.getIssue(issueID)
    issueStatus = backlogApi.getIssueStatus(issueData)
    if issueStatus != '完了':
        issueTitle = issueID + backlogApi.getIssueTitle(issueData)
        comments = backlogApi.getComments(issueID)
        datetimeConverter = datetime_converter.DateTimeConverter()
        thisMonth = datetime.date(2023, 9, 1)                
        entities = []
        for comment in comments:
            lastUpdate = datetimeConverter.convertDateFromJson(comment['updated'])
            content = comment['content']
            if (lastUpdate >= thisMonth):
                if (content):
                    productDataList = backlogApi.extractProductdata(content)
                    for productData in productDataList:
                        date = datetimeConverter.convertDate(productData[0])
                        start = datetimeConverter.convertTime(productData[1])
                        end = datetimeConverter.convertTime(productData[2])
                        timeDelta = datetimeConverter.getTimeDuration(end, start)                
                        commentUser = nameConvertDict[backlogApi.getCommentUser(comment)]  
                        entities.append(makeEntity(issueTitle, date, start, end, timeDelta, commentUser))
            else:
                print('No comment is updated in this month')
    else:
        print('task is finished')
def test():
    payload = {
        'apiKey' : secret.API_KEY,
    }
    issueID = 'TMD_SHARE-248'
    backlogApi = BacklogApi(payload, projectID = 292193)    
    issueData = backlogApi.getIssue(issueID)
    ###### Test ########
    pprint('-----------ISSUE STATUS TEST--------------')    

    # test : You can get status of issue
    issueStatus = backlogApi.getIssueStatus(issueData)
    pprint('issue status : ' + issueStatus)

    pprint('-----------SUMMARY TEST--------------')        
    # test : You can get issue title    
    title = issueID + ' ' + issueData['summary']
    pprint(title)

    pprint('-----------COMMENT TEST--------------')
    # test : You can get comments
    comments = backlogApi.getComments(issueID)
    backlogApi.testShowCommentCount(comments)
    datetimeConverter = datetime_converter.DateTimeConverter()
    for comment in comments:
        content = comment['content']
        if (content):
            # test : You can extract product data by comment
            productDataList = backlogApi.extractProductdata(content)
            commentUser = backlogApi.getCommentUser(comment)
            for productData in productDataList:
                # test : You can extract productData                
                pprint(productData)
                
                # test : You can compare date
                date = datetimeConverter.convertDate(productData[0])
                thisMonth = datetime.date(2023, 9, 1)
                
                if (date >= thisMonth):
                    # test : You can get time delta
                    start = datetimeConverter.convertTime(productData[1])
                    end = datetimeConverter.convertTime(productData[2])
                    timeDelta = datetimeConverter.getTimeDuration(end, start)                
                    pprint('time delta : ' + str(timeDelta))                
                    
                    # test : You can extract user by comment
                    pprint('commnet user : ' + commentUser)   
                    pprint('entity : ' + str(makeEntity(
                        title, date, start, end, timeDelta, commentUser
                    )))

if __name__ == '__main__':
    # main()
    # test()
    csv_test()
    # unitIssueTest()
    # read_json_test()