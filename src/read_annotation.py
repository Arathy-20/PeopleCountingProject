from scipy.io import loadmat

mat = loadmat(
    "dataset/ShanghaiTech/part_A/train_data/ground-truth/GT_IMG_1.mat"
)

print(mat["image_info"])