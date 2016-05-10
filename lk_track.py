#!/usr/bin/env python

'''
Lucas-Kanade tracker
====================

Lucas-Kanade sparse optical flow demo. Uses goodFeaturesToTrack
for track initialization and back-tracking for match verification
between frames.

Usage
-----
lk_track.py [<video_source>]


Keys
----
ESC - exit
'''

# Python 2/3 compatibility
from __future__ import print_function

from PyQt4 import QtCore
import numpy as np
import cv2
import video
from common import draw_str
import ConfigParser

lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 0.005))

feature_params = dict(maxCorners=1000,
                      qualityLevel=0.01,
                      minDistance=10,
                      blockSize=20)

global sec
sec = 0


class TrackLK(QtCore.QThread):
    _signal = QtCore.pyqtSignal()

    def __init__(self):
        super(TrackLK, self).__init__()
        self.track_len = 5
        self.detect_interval = 5
        self.tracks = []
        self.cam = video.create_capture(0)
        self.frame_idx = 0
        self.timer = QtCore.QTimer(QtCore.QThread())
        self.flag = 1
        self.w = 0
        self.h = 0

    def run(self):
        while self.flag:
            self.fps, frame = self.cam.read()
            self.h, self.w = frame.shape[:2]
            frame = self.undistort(frame)
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.vis = frame.copy()

            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
                d = abs(p0 - p0r).reshape(-1, 2).max(-1)
                good = d < 1
                new_tracks = []
                for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                    if not good_flag:
                        continue
                    tr.append((x, y))
                    if len(tr) > self.track_len:
                        del tr[0]
                    new_tracks.append(tr)
                    cv2.circle(self.vis, (x, y), 2, (0, 255, 0), -1)
                self.tracks = new_tracks
                cv2.polylines(self.vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))
                draw_str(self.vis, (20, 20), 'track count: %d' % len(self.tracks))

            if self.frame_idx % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x, y), 5, 0, -1)
                p = cv2.goodFeaturesToTrack(frame_gray, mask=mask, **feature_params)
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        self.tracks.append([(x, y)])

            self.frame_idx += 1
            self.prev_gray = frame_gray
            # cv2.imshow('lk_track', self.vis)

            # ch = 0xFF & cv2.waitKey(1)
            # if ch == 27:
            #     self._signal.emit(ch)

            self._signal.emit()

    def stop(self):
        self.flag = 0

    def GetTrackNum(self):
        return(len(self.tracks))

    def GetFrame(self):
        return(self.vis)

    def undistort(self, frame):
        cf = ConfigParser.ConfigParser()
        cf.read("VO.conf")
        cx = np.float32(cf.get("CameraParameters", "cx"))
        cy = np.float32(cf.get("CameraParameters", "cy"))
        fx = np.float32(cf.get("CameraParameters", "fx"))
        fy = np.float32(cf.get("CameraParameters", "fy"))
        k1 = np.float32(cf.get("CameraParameters", "k1"))
        k2 = np.float32(cf.get("CameraParameters", "k2"))
        k3 = np.float32(cf.get("CameraParameters", "k3"))
        p1 = np.float32(cf.get("CameraParameters", "p1"))
        p2 = np.float32(cf.get("CameraParameters", "p2"))
        camera_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
        dist_coefs = np.array([k1, k2, p1, p2, k3])
        h = self.h
        w = self.w
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w, h), 1, (w, h))
        dst = cv2.undistort(frame, camera_matrix, dist_coefs, None, newcameramtx)
        return(dst)

    def GetTrackFeatures(self):
        return(self.tracks)

# if __name__ == '__main__':
#     import sys
#     try:
#         video_src = sys.argv[1]
#     except:
#         video_src = 0
#     print(__doc__)
#     TrackLK().run()
#     cv2.destroyAllWindows()
