class Student():
    def __init__(self, id) -> None:
        self.id = id
        self.cohort = None
        self.predictedScore = None
        self.actualScore = None
        self.rawPredict = None
        self.top5Courses = []
    
    def getID(self):
        return self.id
    
    def getCohort(self):
        return self.cohort
    
    def getTop5(self):
        return self.top5Courses
    
    def setCohort(self, cohort):
        self.cohort = cohort

    def setRawPredict(self, score):
        self.rawPredict = score
    
    def getRawPredict(self):
        return self.rawPredict
    
    def setPredictedScore(self, score):
        self.predictedScore = score
    
    def setActualScore(self, score):
        self.actualScore = score
    
    def getPredictedScore(self):
        return self.predictedScore
    
    def getActualScore(self):
        return self.actualScore
    
    def passPrediction(self):
        if self.predictedScore == 1:
            return True
        else:
            return False
    
    def passActual(self):
        if self.actualScore == 1:
            return True
        else:
            return False