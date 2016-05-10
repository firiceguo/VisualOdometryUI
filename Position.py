import math
import Translation
import Rotation
import lk_track
from PyQt4 import QtCore


class Position(QtCore.QThread):
    """docstring for Position"""

    _signalPosition = QtCore.pyqtSignal()

    def __init__(self, track=lk_track.TrackLK):
        super(Position, self).__init__(track)
        self.rotation = Rotation.Rotation(track)
        self.translation = Translation.Translation(self.rotation.GetRad(), track)

        self.rotationSum = 0
        self.pathLen = 0
        self.location = [0, 0]
        self.trackP = track
        self.heading = 0

        self.flag = 1
        self.timer = QtCore.QTimer(QtCore.QThread())

    def run(self):
        while self.flag:
            print(self.heading)
            # self.trackP._signal.connect(self.CalculatePosition)
            self.CalculatePosition()
            self._signalPosition.emit()

    def CalculatePosition(self):
        self.rotation.run(self.trackP)
        self.translation.run(self.rotation.GetRad(), self.trackP)

        self.heading += self.rotation.GetRad() / 2
        cosHeading = math.cos(self.heading)
        sinHeading = math.sin(self.heading)
        locationChangeRobot = self.translation.GetCurrentLocationChange()
        deltaXGlobal = locationChangeRobot[0] * cosHeading - locationChangeRobot[1] * sinHeading
        deltaYGlobal = locationChangeRobot[0] * sinHeading + locationChangeRobot[1] * cosHeading

        self.pathLen += math.sqrt(deltaXGlobal * deltaXGlobal + deltaYGlobal * deltaYGlobal)
        self.location = [self.location[0] + deltaXGlobal, self.location[1] + deltaYGlobal]
        self.heading += self.rotation.GetRad() / 2

    def GetDistance(self):
        return(math.sqrt(self.location[0] * self.location[0] + self.location[1] * self.location[1]))

    def GetPathLen(self):
        return(self.pathLen)

    def GetHeading(self):
        return(math.degrees(self.heading))

    def GetLocation(self):
        return(self.location)
