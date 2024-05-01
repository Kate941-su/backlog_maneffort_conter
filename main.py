from backlog_api import BacklogApi
from pprint import pprint
import datetime_converter
import secret
import json
from csv_maker import CsvMaker
from progress_bar import ProgressBar

def makeEntity(issueName, date, start, end, productionTime, person):
    datetimeConverter = datetime_converter.DateTimeConverter()
    strDate = datetimeConverter.deConvertDate(date)
    strStart = datetimeConverter.deConvertTime(start)
    strEnd = datetimeConverter.deConvertTime(end)
    return [issueName, strDate, strStart, strEnd, str(productionTime), person]
    
def main():
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
    startFrom = int(params['start_from'])

    # initialise parameters
    productTimetotal = 0
    notifiyIssueList = []
    start = startFrom
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
    progressBar = ProgressBar(issueTotal)
    # TODO get multipul task comment per single API
    for issueID in issueList:
        print(issueID)
        isNeedBlankRow = False
        bufferList = []
        issueData = backlogApi.getIssue(issueID)
        if bool(issueData) != False:        
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
            # print(f'{issueCountForShow} done!')
        progressBar.showProgress(issueCountForShow)
        issueCountForShow += 1
    # Output total product time
    entities.append(['','','','',productTimetotal, '予算'])
    print('FINISHED!!')
    pprint(f'You should check this issue yourself below 👇. Because It has posibility to miss out some issue production time')
    if(notifiyIssueList):
        pprint(notifiyIssueList)
    else:
        print('None')
    csvMaker = CsvMaker()
    csvMaker.makeCSV(outputPath, entities)

if __name__ == '__main__':
    main()