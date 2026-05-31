import os
import cv2
import numpy as np
from scipy.io import loadmat
x=[]
y=[]
image_folder ="dataset/ShanghaiTech/part_A/train_data/images"
images = os.listdir(image_folder)  
for image_name in images:
    image_path= os.path.join(image_folder, image_name)
    img=cv2.imread(image_path)
    img=cv2.resize(img,(224,224))
    img=img/225.0

    image_number = image_name.split("_")[1].split(".")[0]

    mat_path=(
        f"dataset/ShanghaiTech/part_A/train_data/"
        f"ground-truth/GT_IMG_{image_number}.mat"

    )

    mat = loadmat(mat_path)
    locations = mat["image_info"][0,0][0,0][0]
    count=len(locations)
    x.append(img)
    y.append(count)
print("images loaded", len(x))
print("counts loaded", len(y))
print("first count",y[0])

X=np.array(x)
Y=np.array(y)
print("X shape:", X.shape)
print("Y shape:", Y.shape)