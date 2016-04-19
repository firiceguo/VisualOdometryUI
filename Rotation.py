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
        self.RotationIncrements = [0]

    def run(self, track):
        for i in xrange(track.GetTrackNum()):
            previousFeatureLocation = track.GetTrackFeatures()[i][0]
            currentFeatureLocation = track.GetTrackFeatures()[i][-1]
            if currentFeatureLocation[1] > self.sky:
                previousAngularPlacement = math.atan2(
                    np.float32(previousFeatureLocation[0]).item() - float(self.cx), float(self.fx))
                currentAngularPlacement = math.atan2(
                    np.float32(currentFeatureLocation[0]).item() - float(self.cx), float(self.fx))
                rotationIncrement = currentAngularPlacement - previousAngularPlacement
                self.RotationIncrements.append(rotationIncrement)

    def GetRotationIncrements(self, track):
        self.RotationIncrements.sort()
        return(math.degrees(self.RotationIncrements[len(self.RotationIncrements) // 2]))

    def GetRad(self, track):
        self.RotationIncrements.sort()
        return(self.RotationIncrements[len(self.RotationIncrements) // 2])
