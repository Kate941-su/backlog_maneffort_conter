import requests
from pprint import pprint
import re
import secret

class BacklogApi():
    def __init__(self, payload, projectID):
        self.payload = payload
        self.projectID = projectID
        
    # 課題の総数を取得する
    def getIssueCountInProject(self):
        response = requests.get(f'{secret.API_HOST_URL}' + 'v2/issues/count?projectId[]={self.projectID}', self.payload)        
        print()
        if response.status_code == 200:
            return response.json()['count']
        else:
            assert False, "BAD RESPONSE"
            return 0
        
    # 課題の情報を取得する
    def getIssue(self, issueID):
        response = requests.get(f'{secret.API_HOST_URL}' + 'v2/issues/{issueID}', self.payload)        
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    # retType : [String]
    def getComments(self, issueID):
        response = requests.get(f'{secret.API_HOST_URL}' + 'v2/issues/{issueID}/comments?count=100', self.payload)
        if response.status_code == 200:
            return response.json()
        else:
            print("ISSHUE NOT FOUND")
            return {}

        
    # 課題のステータスを取得する
    def getIssueStatus(self, issueData):
        if issueData:
            status = issueData['status']['name']
            return status
        else:
            assert False, "BAD RESPONSE"
            return ''
        
    # 課題のステータスをセットする
    def setIssueStatus(self, issueID, status):
       try:
           requests.put(f'{secret.API_HOST_URL}' + 'v2/issues/{issueID}',
                        status,headers= {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'Authorization': self.payload['apiKey']
                        })
       except:
           print('bad response')
        
    # 課題のタイトルを取得する
    def getIssueTitle(self, issueData):
        if issueData:
            status = issueData['summary']
            return status
        else:
            assert False, "BAD RESPONSE"
            return ''
        
    # コメントしたユーザーを取得する
    def getCommentUser(self, comment):
        return comment['createdUser']['name']
        
    # test: コメントから実施データを取得する
    # retType : [
    #   [日付, 開始時刻, 終了時刻],[]・・・   
    # ]
    def extractProductdata(self, comment):
        productList = []
        datePattern = r'\d{4}/\d{2}/\d{2}'
        timePattern = r'\d{1,2}:\d{2}'
        dates = re.findall(datePattern, comment)
        times = re.findall(timePattern, comment)
        for i in range(len(dates)):
            try:
                productList.append([dates[i], times[i * 2], times[i * 2 + 1]])
            except:
                pass
        return productList
        
    ######## test #########
    # test : コメントを取得する        
    def testGetComments(self, issueID):
        response = requests.get(f'{secret.API_HOST_URL}' + 'v2/issues/{issueID}/comments', self.payload)
        if response.status_code == 200:
            comments = response.json()
            for comment in comments:
                print('comment auther : ' + str(comment['createdUser']['name']))
                print('comment content : ' + str(comment['content']))
        else:
            print("BAD RESPONSE : " + str(response.status_code))
                    
    def testShowCommentCount(self, commentList):
        print('comment count : ' + str(len(commentList)))
    # 課題のステータスを取得する
    def getStatusID(self, issueData):
        if issueData:
            status = issueData['status']['id']
            return status
        else:
            assert False, "BAD RESPONSE"
            return ''
    ##### deplicated ###### 
    def getAllUser(self):
        response = requests.get(f'{secret.API_HOST_URL}' + 'v2/users', self.payload)
        if response.status_code == 200:
            users = response.json()
            for user in users:
                pprint(user['name'])
        else:
            print("BAD RESPONSE : " + str(response.status_code))


