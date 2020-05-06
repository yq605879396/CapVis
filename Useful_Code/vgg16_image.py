from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import image, img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.backend import clear_session

import numpy as np
import os

model = VGG16()
#model._make_predict_function()

def get_vector(img_path):
    img = image.load_img(img_path, target_size=(224,224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    result = model.predict(x)
    result[result<1e-4] = 0
    return result.flatten()

count = 0
relative_path = 'photo'
for directory, subdir, files in os.walk(relative_path):
    for file in files:
        if file.startswith('test'):
            count += 1
result = []
for i in range(count):
    path = relative_path + os.sep + 'test' + str(i+1) + '.jpg'
    result.append(get_vector(path))
result = np.array(result)

np.savetxt('photo/test_photo_vec', result)