import cv2

img = cv2.imread(
    "dataset/ShanghaiTech/part_A/train_data/images/IMG_1.jpg"
)

cv2.imshow("Image", img)

cv2.waitKey(0)
cv2.destroyAllWindows()