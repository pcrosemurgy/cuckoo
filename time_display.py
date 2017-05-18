import pyglet
import datetime

class TimeDisplay:
    def __init__(self, winWidth, winHeight):
        pyglet.font.add_file('data/cat.ttf')
        catFont = pyglet.font.load('Cat Font')

#self.bannerText = None
        self.dateText = None
        self.timeText = None
        self.colon = pyglet.text.Label(':', font_name='Cat Font', font_size=125,
            y=winHeight/2, color=(200, 0, 100, 255),
            anchor_x='center', anchor_y='center')

        self.winWidth = winWidth
        self.winHeight = winHeight
        self._showColon = True
        self._bound1 = 0
        self._bound2 = 0
        self.date = ''
        self.hour = ''
        self.minute = ''
        self.update()

    def colonSwitch(self, dt=0):
        self._showColon = not self._showColon

    def update(self, dt=0):
        weekday, month, date, hour, minute = datetime.datetime.now().strftime("%A:%b:%d:%I:%M").split(":")
        hour = str(int(hour))

        if self.date != date: # update date text label
            self.dateText = pyglet.text.Label("{}, {} {}".format(weekday, month, date),
                font_name='Cat Font', font_size=18, x=self.winWidth/2,
                y=self.winHeight/2-120, color=(200, 0, 100, 255),
                anchor_x='center', anchor_y='center')
            self.date = date

        if self.hour != hour: # update hour colon bound
            self._bound1 = pyglet.text.Label(hour, font_name='Cat Font', font_size=125).content_width
            self.hour = hour

        if self.minute != minute: # update time text label
            self.timeText = pyglet.text.Label("{} {}".format(hour, minute),
                font_name='Cat Font', font_size=125, x=self.winWidth/2,
                y=self.winHeight/2, color=(200, 0, 100, 255),
                anchor_x='center', anchor_y='center')
            self._bound2 = pyglet.text.Label(minute, font_name='Cat Font', font_size=125).content_width
            self.colon.x = self.winWidth/2-(self._bound2-self._bound1)/2.0
            self.minute = minute

    def draw(self):
        self.timeText.draw()
        self.dateText.draw()
        if self._showColon:
            self.colon.draw()
