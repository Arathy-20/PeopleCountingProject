import os

image_folder = "dataset/ShanghaiTech/part_A/train_data/images"

images = os.listdir(image_folder)

print("Number of images:", len(images))
print("First 5 images:")

for img in images[:5]:
    print(img)