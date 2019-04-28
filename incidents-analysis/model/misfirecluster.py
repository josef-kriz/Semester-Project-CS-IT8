class MisfireCluster:
    def __init__(self, machineID, date, duration, count = 2):
        self.date = date
        self.machineID = machineID
        self.duration = duration
        self.count = count
    def addMisfire(self, date):
        self.count += 1
        if date < self.date:
            self.duration = self.date - date + self.duration
            self.date = date
        else:
            self.duration = self.duration if date < self.date + self.duration else date - self.date
    def __repr__(self):
        return 'MisfireCluster(' + str(self) + ')'
    def __str__(self):
        return str(self.machineID) + ', ' + str(self.date) + ', ' + str(self.duration) + ', ' + str(self.count)
    