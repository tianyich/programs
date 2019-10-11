import cv2
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
    if len(matches) > MIN_MATCHES:
            #draw the mathch points
            cap = cv2.drawMatches(model, kp_model, cap, kp_frame,
                                matches[:MIN_MATCHES], 0, flags=2)
    cv2.imshow('frame', cap)
    cv2.waitKey(0)
    return 0
ar()