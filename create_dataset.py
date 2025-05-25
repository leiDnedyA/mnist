import os
import sys
import numpy as np
from draw import get_drawn_image

script_directory = os.path.dirname(os.path.realpath(__file__))
image_filename = sys.argv[2] if len(sys.argv) >= 3 else "images.npy"
label_filename = sys.argv[3] if len(sys.argv) >= 4 else "labels.txt"
image_filepath = os.path.join(script_directory, image_filename)
label_filepath = os.path.join(script_directory, label_filename)

images = []
labels = []

if os.path.exists(image_filepath) and os.path.exists(label_filepath):
    print("Loading image and label data...")
    loaded_images = np.load(image_filepath)
    images = list(loaded_images)
    with open(label_filepath, 'r') as f:
        labels = f.read().split('\n')

total_count = 100
canceled = False

digit_count = 10

print("Controls:")
print("\t<esc> Save work and quit")
print("\t<space> Save current digit and continue")
print("\t<q> Reset canvas")

try:
    for i in range(len(images) // digit_count, total_count // digit_count):
        for n in range(len(images) % digit_count, digit_count):
            print(f'({i * digit_count + n} / {digit_count * total_count}) Char: {n}')
            img = get_drawn_image(f'Write "{n}"!')
            if img is None:
                canceled = True
                print("Finished due to escape key! Saving labeled data")
                break
            images.append(img)
            labels.append(n)
        if canceled:
            break
except KeyboardInterrupt:
    print('Cancelling due to KeyboardInterrupt!')
    exit(1)

print(f'Saving images to {image_filepath}')
images = np.vstack(images)
np.save(image_filepath, images)

print(f'Saving labels to {label_filepath}')
with open(label_filepath, 'w') as f:
    for i in range(len(labels)):
        f.write(str(labels[i]))
        if i != len(labels) - 1:
            f.write("\n")
