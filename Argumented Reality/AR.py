import cv2
import numpy as np
import math
from OBJ import *

MIN_MATCHES = 109
def ar():   
    homograph = None
    cap = cv2.VideoCapture(1)  
    model = cv2.imread("Pattern1.jpg",0)
    cameraPara = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]])
    # ORB keypoint detector
    orb = cv2.ORB_create()              
    bfMatcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  
    kp_model, des_model = orb.detectAndCompute(model, None) 
    obj = OBJ("Pirate Ship.obj",swapyz=True)
    i = 0
    while True:
        i = i+1
        ret, frame = cap.read()
        if not ret:
            return 
        grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kp_frame, des_frame = orb.detectAndCompute(grey_frame, None)
        matches = bfMatcher.match(des_model, des_frame)
        matches = sorted(matches, key=lambda x: x.distance)
        if len(matches) > MIN_MATCHES:
            if i % 5==0 or i < 20:
                src_pts = np.float32([kp_model[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
                dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches]).reshape(-1,1,2)
                homograph, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,14)
                h, w = model.shape
                pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, homograph) 
    
            if homograph is not None:
                
            #frame = cv2.polylines(frame, [np.int32(block)], True, 255, 3, cv2.LINE_AA) 
            #draw the mathch points
            #frame = cv2.drawMatches(model, kp_model, frame, kp_frame,matches[:MIN_MATCHES], 0, flags=2)
            #if homograph is not None:
                projection = getProjectionMatrix(cameraPara,homograph)
                frame = objImage(frame,obj,projection,model)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1)== ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return 


def getProjectionMatrix(cameraPara,homograph):
    homograph = homograph * (-1)
    translation = np.dot(np.linalg.inv(cameraPara), homograph)
    firstCol = translation[:,0]
    secondCol = translation[:,1]
    thirdCol = translation[:,2]
    l = math.sqrt(np.linalg.norm(firstCol, 2) * np.linalg.norm(secondCol, 2))
    firstEst = firstCol/l
    secondEst = secondCol/l
    diagonal = firstEst + secondEst
    planeVec = np.cross(firstEst,secondEst)
    helperVec = np.cross(diagonal,planeVec)
    firstEst = np.dot(diagonal / np.linalg.norm(diagonal, 2) + helperVec / np.linalg.norm(diagonal, 2), 1 / math.sqrt(2))
    secondEst =np.dot(diagonal / np.linalg.norm(diagonal, 2) - helperVec / np.linalg.norm(diagonal, 2), 1 / math.sqrt(2))
    thirdEst = np.cross(firstEst,secondEst)
    projection = np.stack((firstEst,secondEst,thirdEst,thirdCol/l)).T
    return np.dot(cameraPara,projection)

def objImage(image,obj,projection,model):
    vertices = obj.vertices
    height,width = model.shape
    scale = np.eye(3) * 130
    for face in obj.faces:
        verticesF = face[0]
        points = np.array([vertices[vertex - 1] for vertex in verticesF])
        points = np.dot(points,scale)
        #center the object
        points = np.array([[p[0] + width/2, p[1] + height/2, p[2]] for p in points])
        #points = np.array([p[2] - 20 for p in points])
        dst = cv2.perspectiveTransform(points.reshape(-1, 1, 3), projection)
        objPoints = np.int32(dst)
        cv2.fillConvexPoly(image,objPoints,(244, 176, 66))
    return image

if __name__ == "__main__":   
    ar()