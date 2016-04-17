#!/usr/bin/env python

'''
camera calibration for distorted images with chess board samples
reads distorted images, calculates the calibration and write undistorted images

usage:
    calibrate.py [--debug <output path>] [--square_size] [<image mask>]

default values:
    --debug:    ./output/
    --square_size: 1.0
    <image mask> defaults to ../data/left*.jpg
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2

# local modules
from common import splitfn

# built-in modules
import os
import ConfigParser


class CorrectCamera:
    def __init__(self):
        args, img_mask = getopt.getopt(sys.argv[1:], '', ['debug=', 'square_size='])
        args = dict(args)
        args.setdefault('--debug', './output/')
        args.setdefault('--square_size', 1.0)
        if not img_mask:
            img_mask = './data/left*.jpg'  # default
            self.img_names = glob(img_mask)
        else:
            pass
            # img_mask = img_mask[0]
            self.img_names = img_mask

        print(self.img_names)
        self.debug_dir = args.get('--debug')
        if not os.path.isdir(self.debug_dir):
            os.mkdir(self.debug_dir)
        square_size = float(args.get('--square_size'))

        self.pattern_size = (9, 6)
        self.pattern_points = np.zeros((np.prod(self.pattern_size), 3), np.float32)
        self.pattern_points[:, :2] = np.indices(self.pattern_size).T.reshape(-1, 2)
        self.pattern_points *= square_size

        self.h, self.w = 0, 0

        self.img_points = []
        self.img_names_undistort = []
        self.obj_points = []

    def run(self):
        for fn in self.img_names:
            print('processing %s... ' % fn, end='')
            img = cv2.imread(fn, 0)
            if img is None:
                print("Failed to load", fn)
                continue

            self.h, self.w = img.shape[:2]
            found, corners = cv2.findChessboardCorners(img, self.pattern_size)
            if found:
                term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
                cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)

            if self.debug_dir:
                vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                cv2.drawChessboardCorners(vis, self.pattern_size, corners, found)
                path, name, ext = splitfn(fn)
                outfile = self.debug_dir + name + '_chess.png'
                cv2.imwrite(outfile, vis)
                if found:
                    self.img_names_undistort.append(outfile)

            if not found:
                print('chessboard not found')
                continue

            self.img_points.append(corners.reshape(-1, 2))
            self.obj_points.append(self.pattern_points)

            print('ok')

        # calculate camera distortion
        rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(
            self.obj_points, self.img_points, (self.w, self.h), None, None)

        print(self.img_names_undistort)
        print("\nRMS:", rms)
        print("camera matrix:\n", camera_matrix)
        print("distortion coefficients: ", dist_coefs.ravel())

        return([self.img_names_undistort, camera_matrix, dist_coefs])


if __name__ == '__main__':
    import sys
    import getopt
    from glob import glob

    img_names_undistort, camera_matrix, dist_coefs = CorrectCamera().run()

    # undistort the image with the calibration
    print('')
    for img_found in img_names_undistort:
        img = cv2.imread(img_found)

        h, w = img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w, h), 1, (w, h))

        dst = cv2.undistort(img, camera_matrix, dist_coefs, None, newcameramtx)

        # crop and save the image
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]
        outfile = img_found + '_undistorted.png'
        print('Undistorted image written to: %s' % outfile)
        cv2.imwrite(outfile, dst)

    cf = ConfigParser.ConfigParser()
    cf.read("VO.conf")
    cf.set("CameraParameters", "cx", camera_matrix[0, 2])
    cf.set("CameraParameters", "cy", camera_matrix[1, 2])
    cf.set("CameraParameters", "fx", camera_matrix[0, 0])
    cf.set("CameraParameters", "fy", camera_matrix[1, 1])
    cf.set("CameraParameters", "k1", dist_coefs.ravel()[0])
    cf.set("CameraParameters", "k2", dist_coefs.ravel()[1])
    cf.set("CameraParameters", "k3", dist_coefs.ravel()[4])
    cf.set("CameraParameters", "p1", dist_coefs.ravel()[2])
    cf.set("CameraParameters", "p2", dist_coefs.ravel()[3])

    with open("VO.conf", "w+") as f:
        cf.write(f)

    cv2.destroyAllWindows()
