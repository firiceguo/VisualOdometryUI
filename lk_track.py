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

lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 0.005))

feature_params = dict(maxCorners=500,
                      qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)

global sec
sec = 0


class TrackLK(QtCore.QThread):
    _signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super(TrackLK, self).__init__()
        self.track_len = 10
        self.detect_interval = 5
        self.tracks = []
        self.cam = video.create_capture(0)
        self.frame_idx = 0
        self.timer = QtCore.QTimer(QtCore.QThread())
        self.flag = 1

    def run(self):
        while self.flag:
            ret, frame = self.cam.read()
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

            ch = 0xFF & cv2.waitKey(1)
            if ch == 27:
                self._signal.emit(ch)

            self._signal.emit(ch)

    def stop(self):
        print(0xFF & cv2.waitKey(1))
        self.flag = 0

    def GetFrame(self):
        return(self.vis)

    def GetTrackNum(self):
        return(len(self.tracks))

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
