import cv2
import numpy as np
MIN_MATCHES = 10
def ar():
    cap = cv2.imread("scene.jpg",0) 
    model = cv2.imread("Pattern1.jpg",0)
    # ORB keypoint detector
    orb = cv2.ORB_create()              
    bfMatcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  
    kp_model, des_model = orb.detectAndCompute(model, None) 
    kp_frame, des_frame = orb.detectAndCompute(cap, None)
    matches = bfMatcher.match(des_model, des_frame)
    matches = sorted(matches, key=lambda x: x.distance)
    src_pts = np.float32([kp_model[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    # compute Homography
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    if len(matches) > MIN_MATCHES:
            h, w = model.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            # project corners into frame
            dst = cv2.perspectiveTransform(pts, M)  
            # connect them with lines
            img2 = cv2.polylines(cap, [np.int32(dst)], True, 100, 3, cv2.LINE_AA)
            #cap = cv2.drawMatches(model, kp_model, cap, kp_frame,matches[:MIN_MATCHES], 0, flags=2)
            cv2.imshow('frame', cap)
    cv2.waitKey(0)
    return 0
ar()