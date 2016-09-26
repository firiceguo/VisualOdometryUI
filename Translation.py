import math
import ConfigParser
import cv2
import numpy as np


class Translation():

    """Calculate Translation"""

    def __init__(self, headingChangeRad, track):
        self.t = math.tan(headingChangeRad / 2)
        self.trackedFeatures = track
        self.m_TranslationIncrements = []
        self.m_CurrentLocationChange = (0, 0)

        cf = ConfigParser.ConfigParser()
        cf.read("VO.conf")
        self.ground = int(cf.get("Boundary", "groundregiontop"))
        self.fx = np.float32(cf.get("CameraParameters", "fx"))

    def run(self, headingChangeRad, perspectiveMatrix, track, prevHeading, currHeading):
        self.PopulateRotationCorrectedTranslationIncrements(track, headingChangeRad, perspectiveMatrix)
        self.DeterminMostLikelyTranslationVector(headingChangeRad, prevHeading, currHeading)

    def PopulateRotationCorrectedTranslationIncrements(self, track, headingChangeRad, perspectiveMatrix):
        self.s = math.sin(headingChangeRad)
        self.c = math.cos(headingChangeRad)
        self.m_TranslationIncrements = []
        self.m_CurrentLocationChange = (0, 0)
        trackedF = track
        featuresNum = len(trackedF)
        point = [[], []]
        for i in xrange(featuresNum):
            try:
                feature = trackedF[i]
            except IndexError:
                continue
            if len(feature) < 2:
                continue
            if not(feature[-1][1] > self.ground and feature[0][1] > self.ground):
                continue

            rotationCorrectedEndPoint = self.RemoveRotationEffect(feature[-1])
            point[0] = self.PerspectiveTrans(rotationCorrectedEndPoint, perspectiveMatrix)
            point[1] = self.PerspectiveTrans(feature[0], perspectiveMatrix)
            translationIncrement = (point[1][0] - point[0][0],
                                    point[1][1] - point[0][1])
            if translationIncrement[0] * translationIncrement[1] > 2:
                self.m_TranslationIncrements.append(translationIncrement)

    def DeterminMostLikelyTranslationVector(self, headingChangeRad, prevHeading, currHeading):
        if len(self.m_TranslationIncrements) > 0:
            Heading = math.tan(math.pi / 2 - prevHeading)
            minn = math.tan(math.atan2(self.m_TranslationIncrements[0][1],
                                       self.m_TranslationIncrements[0][0])) - Heading
            num = 0
            for i in xrange(len(self.m_TranslationIncrements)):
                temp = math.tan(math.atan2(self.m_TranslationIncrements[i][1],
                                           self.m_TranslationIncrements[i][0])) - Heading
                if temp < minn:
                    minn = temp
                    num = i
            self.m_CurrentLocationChange = self.m_TranslationIncrements[num]

    def RemoveRotationEffect(self, point):
        afterRemoveRotationEffect = (point[0] - 2 * self.fx * self.t, point[1])
        return(afterRemoveRotationEffect)

    def GetCurrentLocationChange(self):
        return(self.m_CurrentLocationChange)

    def PerspectiveTrans(self, points, perspectiveMatrix):
        points = np.array(points, np.float32).reshape(-1, 1, 2)
        afterTrans = cv2.perspectiveTransform(points, perspectiveMatrix)
        return([afterTrans[0][0][0], afterTrans[0][0][1]])
