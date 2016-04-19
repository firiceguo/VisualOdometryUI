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
        self.translation = Translation.Translation(self.rotation.GetRad(track), track)

        self.rotationSum = 0
        self.pathLen = 0
        self.currentLocation = (0, 0)
        self.trackP = track

        self.flag = 1
        self.timer = QtCore.QTimer(QtCore.QThread())

    def run(self):
        while self.flag:
            # self.trackP._signal.connect(self.CalculatePosition)
            self.CalculatePosition()
            self._signalPosition.emit()

    def CalculatePosition(self):
        self.rotation.run(self.trackP)
        self.translation.run(self.trackP)

        locationChange_x = self.translation.GetCurrentLocationChange()[0]
        locationChange_y = self.translation.GetCurrentLocationChange()[1]

        self.rotationSum = self.rotationSum + self.rotation.GetRotationIncrements(self.trackP)
        self.pathLen = self.pathLen + math.sqrt(locationChange_x * locationChange_x + locationChange_y * locationChange_y)
        self.currentLocation = (self.currentLocation[0] + locationChange_x,
                                self.currentLocation[1] + locationChange_y)

    def GetDistance(self):
        return(math.sqrt(self.currentLocation[0] * self.currentLocation[0] + self.currentLocation[1] * self.currentLocation[1]))

    def GetPathLen(self):
        return(self.pathLen)

    def GetHeading(self):
        return(math.degrees(self.rotationSum))

    def GetLocation(self):
        return(self.currentLocation)
