class ProgressBar():

    def __init__(self, totalTask: int):
        self.totalTask = totalTask
        self.outputPoint = 0
        self.outputProgressPointCount = 20
    
    def showProgress(self, progress: int):
        progressPercentage = progress / self.totalTask
        progressUnit = int(progressPercentage * 20)
        if (self.outputPoint != progressUnit):
            print(f'{int(progressPercentage * 100)}% done')
            self.outputPoint = progressUnit