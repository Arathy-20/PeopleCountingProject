import cv2
import numpy as np

IMG_SIZE = (224, 224)


def preprocess_image(pil_image):

    img_rgb = pil_image.convert("RGB")

    img_np = np.array(
        img_rgb,
        dtype=np.uint8
    )

    img_resized = cv2.resize(
        img_np,
        IMG_SIZE,
        interpolation=cv2.INTER_AREA
    )

    img_norm = img_resized.astype(
        np.float32
    ) / 255.0

    return np.expand_dims(
        img_norm,
        axis=0
    )