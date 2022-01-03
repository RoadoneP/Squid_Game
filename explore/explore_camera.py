import cv2
import numpy as np
import keyboard

def restart():
    while True:
        if keyboard.read_key() == "p":
            break


cap = cv2.VideoCapture(0)

sub = cv2.createBackgroundSubtractorKNN(history=1, dist2Threshold=5000, detectShadows=False)

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break
    pts = np.array([[0,460],[250,0],[390,0],[640,460]])
    rect = cv2.boundingRect(pts)
    x,y,w,h = rect
    croped = img[y:y+h, x:x+w].copy()

    ## (2) make mask
    pts = pts - pts.min(axis=0)

    mask = np.zeros(croped.shape[:2], np.uint8)
    cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

    ## (3) do bit-op
    dst = cv2.bitwise_and(croped, croped, mask=mask)

    mask = sub.apply(dst)
    # print(f"mask_max1: {np.unique(mask)}")
    # mask = np.expand_dims(mask, axis=2).repeat(3, axis=2)
    # mask = img * mask
    # print(f"mask_max2: {np.unique(mask)}")
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    cv2.imshow('mask', dst)
    cv2.imshow('image', mask)
    if cv2.waitKey(1) == ord('q'):
        break