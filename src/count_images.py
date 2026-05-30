import os

train_folder = "dataset/ShanghaiTech/part_A/train_data/images"
test_folder = "dataset/ShanghaiTech/part_A/test_data/images"

print("Train:", len(os.listdir(train_folder)))
print("Test :", len(os.listdir(test_folder)))