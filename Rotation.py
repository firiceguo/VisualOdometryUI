import ConfigParser
import lk_track
import math


class Rotation():
    """Calculate Rotation"""

    def __init__(self, track=lk_track.TrackLK):
        super(Rotation, self).__init__()
        cf = ConfigParser.ConfigParser()
        cf.read("VO.conf")
        self.cx = cf.get("CameraParameters", "cx")
        self.fx = cf.get("CameraParameters", "fx")
        self.sky = cf.get("Boundary", "skyregionbottom")
        self.RotationIncrements = []

    def run(self, track):
        for i in xrange(track.GetTrackNum):
            previousFeatureLocation = track.GetTrackFeatures()[i, 0]
            currentFeatureLocation = track.GetTrackFeatures()[i, -1]
            if currentFeatureLocation[1] < self.sky:
                previousAngularPlacement = math.atan2(previousFeatureLocation[0] - self.cx, self.fx)
                currentAngularPlacement = math.atan2(currentFeatureLocation[0] - self.cx, self.fx)
                rotationIncrement = currentAngularPlacement - previousAngularPlacement
                self.RotationIncrements.append(rotationIncrement)

    def GetRotationIncrements(self):
        return(self.RotationIncrements)
