import sys
import numpy as np
from draw import get_drawn_image

images = []
labels = []

count = 100
canceled = False

try:
    for i in range(count // 10):
        for n in range(10):
            print(f'Write a {n}')
            img = get_drawn_image(f'Write "{n}"')
            if img is None:
                canceled = True
                print("Finished due to escape key! Saving labeled data")
                break
            images.append(img)
            labels.append(n)
        if canceled:
            break
except KeyboardInterrupt:
    print('Finished due to KeyboardInterrupt! Saving labeled data...')

image_filename = sys.argv[2] if len(sys.argv) >= 3 else "images.out"
label_filename = sys.argv[3] if len(sys.argv) >= 4 else "labels.out"
print(f'Saving images to {image_filename}')
images = np.vstack(images)
np.save(image_filename, images)

print(f'Saving labels to {label_filename}')
with open(label_filename, 'w') as f:
    for label in labels:
        f.write(f'{label}\n')
