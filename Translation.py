import lk_track
import math
import ConfigParser
import random


class Translation():

    """docstring for Translation"""

    def __init__(self, headingChangeRad, track=lk_track.TrackLK):
        # super(Translation, self).__init__(headingChangeRad, track)
        self.s = math.sin(headingChangeRad)
        self.c = math.cos(headingChangeRad)
        self.trackedFeatures = track.GetTrackFeatures()
        self.m_TranslationIncrements = []
        self.m_GroundFeatures = []
        self.m_ScratchPadUsedGroundFeatures = []
        self.m_UsedGroundFeatures = []
        self.m_CurrentLocationChange = ()

        cf = ConfigParser.ConfigParser()
        cf.read("VO.conf")
        self.ground = int(cf.get("Boundary", "groundregiontop"))

    def run(self, headingChangeRad, track):
        self.PopulateRotationCorrectedTranslationIncrements(track, headingChangeRad)
        self.DeterminMostLikelyTranslationVector()

    def PopulateRotationCorrectedTranslationIncrements(self, track, headingChangeRad):
        self.s = math.sin(headingChangeRad)
        self.c = math.cos(headingChangeRad)
        self.m_TranslationIncrements = []
        trackedF = track
        featuresNum = len(trackedF.GetTrackFeatures())
        for i in xrange(featuresNum):
            try:
                feature = trackedF.GetTrackFeatures()[i]
            except IndexError:
                continue
            if len(feature) < 2:
                continue
            if not(feature[-1][1] > self.ground and feature[0][1] > self.ground):
                continue
            rotationCorrectedEndPoint = self.RemoveRotationEffect(feature[-1])
            translationIncrement = (feature[0][0] - rotationCorrectedEndPoint[0],
                                    feature[0][1] - rotationCorrectedEndPoint[1])
            self.m_TranslationIncrements.append(translationIncrement)
            self.m_GroundFeatures.append(feature)

    def DeterminMostLikelyTranslationVector(self):
        maxVotes = 0
        maxPicks = 40
        mostLikelyTranslation = (0, 0)

        if len(self.m_TranslationIncrements) < maxPicks:
            randomPicksCount = len(self.m_TranslationIncrements)
        else:
            randomPicksCount = maxPicks

        for i in xrange(randomPicksCount):
            self.m_ScratchPadUsedGroundFeatures = []
            index = int(math.floor(random.uniform(0, len(self.m_TranslationIncrements))))
            translationVector = self.m_TranslationIncrements[index]
            netX = 0
            netY = 0
            votes = 0
            for j in xrange(len(self.m_TranslationIncrements)):
                if i == j:
                    continue
                dx = self.m_TranslationIncrements[j][0] - translationVector[0]
                dy = self.m_TranslationIncrements[j][1] - translationVector[1]
                if (dx * dx + dy * dy) < 0.5:
                    votes = votes + 1
                    self.m_ScratchPadUsedGroundFeatures.append(self.m_GroundFeatures[j])
            if votes > maxVotes:
                maxVotes = votes
                mostLikelyTranslation = (translationVector[0] + netX / votes,
                                         translationVector[1] + netY / votes)
                temp = self.m_UsedGroundFeatures
                self.m_UsedGroundFeatures = self.m_ScratchPadUsedGroundFeatures
                self.m_ScratchPadUsedGroundFeatures = temp

        self.m_CurrentLocationChange = mostLikelyTranslation

    def RemoveRotationEffect(self, point):
        afterRemoveRotationEffect = (self.c * point[0] - self.s * point[1],
                                     self.s * point[0] + self.c * point[1])
        return(afterRemoveRotationEffect)

    def GetCurrentLocationChange(self):
        return(self.m_CurrentLocationChange)
