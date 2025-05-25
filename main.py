import os
from keras.datasets import mnist
from keras import models
from keras import layers
from keras.utils import to_categorical
from draw import get_drawn_image

network = None

NETWORK_FILENAME = 'model.keras'

if not os.path.exists(NETWORK_FILENAME):
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

    network = models.Sequential()
    layer_count = 3
    for _ in range(layer_count):
        network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28, )))
    network.add(layers.Dense(10, activation='softmax'))
    network.compile(optimizer='rmsprop',
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])

    def preprocess(images):
        return images.reshape((60000, 28*28)).astype('float32') / 255

    train_images = train_images.reshape((60000, 28*28)).astype('float32') / 255
    test_images = test_images.reshape((10000, 28*28)).astype('float32') / 255

    print(test_images)

    train_labels = to_categorical(train_labels)
    test_labels = to_categorical(test_labels)

    network.fit(train_images, train_labels, epochs=5, batch_size=128)

    test_loss, test_acc = network.evaluate(test_images, test_labels)
    print(f"Test loss: {test_loss}\nTest accuracy: {test_acc * 100} %")

    network.save(NETWORK_FILENAME)
else:
    network = models.load_model(NETWORK_FILENAME)

user_image = get_drawn_image()

result = network(user_image)[0]

curr_max = -1.0
guess = -1
for i in range(len(result)):
    n = float(result[i])
    if n > curr_max:
        curr_max = max(curr_max, n)
        guess = i

print(f'You wrote {guess}')
