import numpy as np
import matplotlib.pyplot as plt
from functions import head_tail_breaks
from PIL import Image

image_path = r"D:\Data\The Nature of Order\9-1.png"
output_path = r"D:\Data\The Nature of Order\9-1_ht.png"

# Load the image, convert to grayscale
try:
    with Image.open(image_path) as rgb_image:
        gray_image = np.array(rgb_image.convert("L"))
except IOError as e:
    raise IOError(f"Failed to open or process the image file: {image_path}") from e

# Apply head-tail breaks classification
ht_index, cuts = head_tail_breaks(gray_image, break_per=0.5)
print("Ht-index:%s, Cuts:%s" % (ht_index, cuts))

# Create the classified image
htimg = np.full(gray_image.shape, -1, dtype=np.uint8)
for i, threshold in enumerate(cuts):
    htimg[gray_image > threshold] = i + 1

# Display and save the result
plt.imshow(htimg, cmap="Spectral")
plt.show()
plt.imsave(output_path, htimg, cmap="Spectral")
