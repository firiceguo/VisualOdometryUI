import ConfigParser
import lk_track
import math
import numpy as np


class Rotation():
    """Calculate Rotation"""

    def __init__(self, track=lk_track.TrackLK):
        # Rotation.__init__(self, track)
        cf = ConfigParser.ConfigParser()
        cf.read("VO.conf")
        self.cx = cf.get("CameraParameters", "cx")
        self.fx = cf.get("CameraParameters", "fx")
        self.sky = int(cf.get("Boundary", "skyregionbottom"))
        self.RotationIncrements = []
        self.m_HeadingChange = 0

    def run(self, track):
        trackedF = track
        featuresNum = len(trackedF.GetTrackFeatures())
        self.RotationIncrements = []
        for i in xrange(featuresNum):
            try:
                previousFeatureLocation = trackedF.GetTrackFeatures()[i][0]
                currentFeatureLocation = trackedF.GetTrackFeatures()[i][-1]
            except IndexError:
                continue
            if currentFeatureLocation[1] < self.sky:
                previousAngularPlacement = math.atan2(
                    np.float32(previousFeatureLocation[0]).item() - float(self.cx), float(self.fx))
                currentAngularPlacement = math.atan2(
                    np.float32(currentFeatureLocation[0]).item() - float(self.cx), float(self.fx))
                rotationIncrement = currentAngularPlacement - previousAngularPlacement
                self.RotationIncrements.append(rotationIncrement)
        if len(self.RotationIncrements) > 0:
            meanRotationIncrement = self.GetRotationIncrements()
            self.m_HeadingChange = meanRotationIncrement

    def GetRotationIncrements(self):
        self.RotationIncrements.sort()
        return(math.degrees(self.RotationIncrements[len(self.RotationIncrements) // 2]))
        # return(math.degrees(np.mean(self.RotationIncrements)))
        # self.RotationIncrements.sort()
        # middle = self.RotationIncrements[len(self.RotationIncrements) // 2]
        # mean = np.mean(self.RotationIncrements)
        # return(math.degrees((middle + mean) / 2))

    def GetRad(self):
        return(math.radians(self.m_HeadingChange))
