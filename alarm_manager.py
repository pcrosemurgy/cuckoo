import os
import json
import schedule

class AlarmManager:
    def __init__(self, alarmFunc):
        self.data = {'hour':1, 'min':0, 'am':True, 'days':[]}
        self.alarmFunc = alarmFunc
        if os.path.isfile('conf.json'):
            with open('conf.json', 'r') as f:
                self.data = json.load(f)
            self.scheduleJobs()

    def save(self, days, hour, minute, am):
        self.data['hour'] = hour
        self.data['min'] = minute
        self.data['am'] = am
        self.data['days'] = days
        with open('conf.json', 'w') as f:
            f.write(json.dumps(self.data))
        self.scheduleJobs()

    def scheduleJobs(self):
        print("HIT 1")
        for d in self.data['days']:
            if d == 'sun':
                schedule.every().sunday.do(self.alarmFunc)
            if d == 'mon':
                schedule.every().monday.do(self.alarmFunc)
            if d == 'tue':
                schedule.every().tuesday.do(self.alarmFunc)
            if d == 'wed':
                schedule.every().wednesday.do(self.alarmFunc)
            if d == 'thur':
                schedule.every().thursday.do(self.alarmFunc)
            if d == 'fri':
                schedule.every().friday.do(self.alarmFunc)
            if d == 'sat':
                schedule.every().saturay.do(self.alarmFunc)

    def cancelJobs(self):
        schedule.clear()

    def run(self):
        schedule.run_pending()

    def genBanner(self):
        pass
