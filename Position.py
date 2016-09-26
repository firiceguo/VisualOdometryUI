import math
import Translation
import Rotation
import lk_track
from PyQt4 import QtCore
import numpy as np
import cv2
import matplotlib.pyplot as plt


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
        self.loc = []
        self.trackP = track
        self.heading = 0
        self.trans = 0.059

        self.flag = 1
        self.timer = QtCore.QTimer(QtCore.QThread())

    def run(self):
        perspectiveMatrix = self.GetPerspectiveMatrix()
        x = []
        y = []
        while self.flag:
            self.CalculatePosition(perspectiveMatrix)
            self._signalPosition.emit()
            if not self.trackP.fps:
                for i in xrange(len(self.loc)):
                    x.append(self.loc[i][0])
                    y.append(self.loc[i][1])
                plt.plot(x, y, 'o')
                plt.show()
                break

    def CalculatePosition(self, perspectiveMatrix):
        GoodFeatures = []
        GoodFeatures = self.DetermineGoodFeatures(self.trackP.GetTrackFeatures())
        self.rotation.run(GoodFeatures)

        prevHeading = self.heading
        self.heading += self.rotation.GetRad()
        currHeading = self.heading
        self.translation.run(self.rotation.GetRad(), perspectiveMatrix, GoodFeatures, prevHeading, currHeading)
        change = self.translation.GetCurrentLocationChange()
        self.location[0] += change[0]
        self.location[1] += change[1]
        self.pathLen += math.sqrt(change[0] * change[0] + change[1] * change[1])

    def SetZero(self):
        self.rotationSum = 0
        self.pathLen = 0
        self.location = [0, 0]
        self.heading = 0

    def GetDistance(self):
        ans = math.sqrt(self.location[0] * self.location[0] + self.location[1] * self.location[1]) * self.trans
        return(ans)

    def GetPathLen(self):
        ans = self.pathLen * self.trans
        return(ans)

    def GetHeading(self):
        return(math.degrees(self.heading))

    def GetLocation(self):
        ans = [self.location[0] * self.trans, - self.location[1] * self.trans]
        self.loc.append(ans)
        return(ans)

    def GetPerspectiveMatrix(self):
        img = cv2.imread("./data/perspectiveimg.jpg", 0)
        w = img.shape[1]
        h = img.shape[0]

        src = [[186, 361], [449, 361],
               [133, 466], [508, 466]]
        src = np.array(src, np.float32)
        dst = np.array([[w // 2 - 100, h - 200], [w // 2 + 100, h - 200],
                        [w // 2 - 100, h], [w // 2 + 100, h]], np.float32)
        ret = cv2.getPerspectiveTransform(src, dst)

        return(ret)

    def DetermineGoodFeatures(self, tracks):
        features = tracks
        GoodFeatures = []
        for i in xrange(len(features)):
            FeatureScore = 5
            for j in xrange(len(features[i]) - 1):
                if len(features[i]) < 5:
                    continue
                try:
                    PrevPoint = np.array(features[i][j])
                    CurrPoint = np.array(features[i][j + 1])
                except IndexError:
                    continue
                dis = np.linalg.norm(PrevPoint - CurrPoint)
                if dis > 15:
                    FeatureScore += 1
                else:
                    FeatureScore -= 1
            if FeatureScore < 6:
                GoodFeatures.append(features[i])
        return(GoodFeatures)
