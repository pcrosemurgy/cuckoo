import os
import json
import schedule

class AlarmManager:
    def __init__(self):
        self.data = {'hour':1, 'min':0, 'am':True, 'days':[]}
        if os.path.isfile('conf.json'):
            with open('conf.json', 'r') as f:
                self.data = json.load(f)
            # TODO self.scheduleJobs

    def save(self, days, hour, minute, am):
        self.data['hour'] = hour
        self.data['min'] = minute
        self.data['am'] = am
        self.data['days'] = days
        with open('conf.json', 'w') as f:
            f.write(json.dumps(self.data))
            # TODO self.scheduleJobs

    def cancelJobs(self):
        # TODO schedule.clear('label')
        pass

    def scheduleJobs(self):
        pass

    def genBanner(self):
        pass
