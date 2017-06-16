import pyglet
from pyglet.gl import *
from alarm_manager import AlarmManager

WHITE = (255, 255, 255, 255)
PINK = (200, 0, 100, 255)
DPINK = (99, 75, 101, 255)

class SettingsDisplay:
    def __init__(self):
        self.batchUI = pyglet.graphics.Batch()
        self.bgOff = pyglet.image.load('data/img/bgoff.png')
        self.bgOn = pyglet.image.load('data/img/bgon.png')
        self.bg = self.bgOff
        self.inc = Icon('data/img/inc.png', x=394, y=145, batch=self.batchUI)
        self.dec = Icon('data/img/dec.png', x=394, y=70, batch=self.batchUI)
        self.done = Icon('data/img/done.png', x=402, y=15, batch=self.batchUI)
        self.off = Icon('data/img/off.png', x=405, y=240, batch=self.batchUI)
        self.on = Icon('data/img/on.png', x=405, y=240, batch=self.batchUI, visible=False)

        self.hour = 1
        self.min = 0
        self.am = True
        self.selectedTime = None
        self.selectedDays = {'sun':False, 'mon':False, 'tue':False,
            'wed':False, 'thur':False, 'fri':False}
        self.alarmSched = AlarmManager(self.hour, self.min, self.am, self.selectedDays)

        self.hourLabel = pyglet.text.Label(str(self.hour), font_name='Cat Font',
            font_size=85, x=50-27, y=210, color=WHITE, width=120, height=100,
            multiline=True, align='right', batch=self.batchUI)
        self.minLabel = pyglet.text.Label("{:02}".format(self.min), font_name='Cat Font',
            font_size=85, x=195-27, y=210, color=WHITE, width=130, height=100,
            batch=self.batchUI)
        self.amLabel = pyglet.text.Label('AM', font_name='Cat Font', font_size=25, x=315,
            y=235, color=WHITE, width=50, height=50, batch=self.batchUI)
        self.colon = pyglet.text.Label(':', font_name='Cat Font', font_size=85,
            x=165-27, y=215, color=WHITE, batch=self.batchUI)
        self.dayLabels = {
            'sun': pyglet.text.Label('S', font_name='Cat Font', font_size=35, x=58,
                y=150, color=DPINK, width=40, height=50, batch=self.batchUI),
            'mon': pyglet.text.Label('M', font_name='Cat Font', font_size=35, x=94,
                y=150, color=DPINK, width=40, height=50, batch=self.batchUI),
            'tue': pyglet.text.Label('T', font_name='Cat Font', font_size=35, x=139,
                y=150, color=DPINK, width=40, height=50, batch=self.batchUI),
            'wed': pyglet.text.Label('W', font_name='Cat Font', font_size=35, x=174,
                y=150, color=DPINK, width=40, height=50, batch=self.batchUI),
            'thur': pyglet.text.Label('T', font_name='Cat Font', font_size=35, x=234,
                y=150, color=DPINK, width=40, height=50, batch=self.batchUI),
            'fri': pyglet.text.Label('F', font_name='Cat Font', font_size=35, x=271,
                y=150, color=DPINK, width=40, height=50, batch=self.batchUI),
            'sat': pyglet.text.Label('S', font_name='Cat Font', font_size=35, x=308,
                y=150, color=DPINK, width=40, height=50, batch=self.batchUI)}
        self.banner = pyglet.text.Label('Alarm set for 12 hours\nand 1 minutes from now',
            font_name='Helvetica', font_size=15, x=10, y=56, color=WHITE, width=375,
            multiline=True, align='center')

        def off_func():
            self.alarmSched.on = True
            self.bg = self.bgOn
            def f(dt):
                self.off.visible = False
                self.on.visible = True
            pyglet.clock.schedule_once(f, 0.21)

        def on_func():
            self.alarmSched.on = False
            self.bg = self.bgOff
            def f(dt):
                self.off.visible = True
                self.on.visible = False
            pyglet.clock.schedule_once(f, 0.21)

        def inc_func():
            if self.selectedTime == self.hourLabel:
                self.hour = 1 if self.hour == 12 else self.hour+1
                self.hourLabel.text = str(self.hour)
            elif self.selectedTime == self.minLabel:
                self.min = 0 if self.min == 50 else self.min+10
                self.minLabel.text = "{:02}".format(self.min)

        def dec_func():
            if self.selectedTime == self.hourLabel:
                self.hour = 12 if self.hour == 1 else self.hour-1
                self.hourLabel.text = str(self.hour)
            elif self.selectedTime == self.minLabel:
                self.min = 50 if self.min == 0 else self.min-10
                self.minLabel.text = "{:02}".format(self.min)

        def done_func():
            return True

        self.icons = {self.off:off_func, self.on:on_func, self.inc:inc_func, self.dec:dec_func, self.done:done_func}
        self.alarmSched.writeConfig()

    def readConfig():
        with open('alarm.config', 'r') as f:
            data = f.read().split(':')
            days = data[-1].split(',')


    def isPressed(self, icon, x, y):
        x2 = icon.x
        y2 = icon.y
        w = icon.width
        h = icon.height
        if x >= x2 and y >= y2 and x <= x2+w and y <= y2+h:
            return True
        return False

    def setSelectedTime(self, label):
        if self.selectedTime:
            self.selectedTime.color = WHITE
        label.color = PINK
        self.selectedTime = label

    def selectDay(self, label):
        pass

    def press(self, x, y):
        if x > 390:
            for i in self.icons:
                if i.visible and self.isPressed(i, x, y):
                    i.act()
                    return self.icons[i]()
        elif y > 190:
            if self.isPressed(self.hourLabel, x, y):
                self.setSelectedTime(self.hourLabel)
            elif self.isPressed(self.minLabel, x, y):
                self.setSelectedTime(self.minLabel)
            elif self.isPressed(self.amLabel, x, y):
                self.am = not self.am
                self.amLabel.text = 'AM' if self.am else 'PM'
        else:
            for d, l in self.dayLabels.iteritems():
                if self.isPressed(l, x, y):
                    if l.color == DPINK: # not selected
                        self.selectedDays[l.text] = True
                        l.color = PINK
                    else: # selected
                        self.selectedDays[l.text] = False
                        l.color = DPINK
                    print(self.selectedDays)

    def draw(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.bg.blit(0, 0)
        self.batchUI.draw()
        if self.on.visible:
            self.banner.draw()


class Icon(pyglet.sprite.Sprite):
    def __init__(self, path, x, y, batch=None, visible=True):
        pyglet.sprite.Sprite.__init__(self, pyglet.image.load(path), x, y, batch=batch)
        self.visible = visible
        self.waiting = False # avoid double click abuse

    def act(self):
        if self.waiting:
            return
        self.waiting = True
        self.x -= self.width/6
        self.y -= self.height/6
        self.scale = 1.25
        pyglet.clock.schedule_once(self.restoreScale, 0.2)

    def restoreScale(self, dt=0):
        self.waiting = False
        self.scale = 1.0
        self.x += self.width/6
        self.y += self.height/6
