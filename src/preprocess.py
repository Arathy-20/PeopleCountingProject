import cv2

img=cv2.imread("dataset/ShanghaiTech/part_A/train_data/images/IMG_1.jpg")
print("original shape", img.shape)
img=cv2.resize(img, (224,224))
print("resized shape:",img.shape)

img=img/255.0
print("min pixel:", img.min())
print("max pixel:", img.max())