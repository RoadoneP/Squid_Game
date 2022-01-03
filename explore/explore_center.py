import numpy as np
import cv2

cap = cv2.VideoCapture(0)
sub = cv2.createBackgroundSubtractorKNN(history=1, dist2Threshold=5000, detectShadows=False)

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    mask = sub.apply(img)
    # print(f"mask_max1: {np.unique(mask)}")
    # mask = np.expand_dims(mask, axis=2).repeat(3, axis=2)
    # mask = img * mask
    # print(f"mask_max2: {np.unique(mask)}")
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # mask = cv2.dilate(mask, kernel, iterations=2)
    # mask의 값 0 or 255의 값을  0 or 1로 바꾸고 합치기
    cx, cy = np.where(mask == 255.)
    if len(cx) != 0:
        cx = np.round(np.mean(cx)).astype("int")
        cy = np.round(np.mean(cy)).astype("int")
        img = cv2.circle(img, (cy, cx), 10, (0, 255, 0), -1, cv2.LINE_AA)
        mask = cv2.circle(mask, (cy, cx), 10, (0, 255, 0), -1, cv2.LINE_AA)
    else:
        cx = 0
        cy = 0


    cv2.imshow('img', img)
    cv2.imshow('mask', mask)
    if cv2.waitKey(1) == ord('q'):
        break