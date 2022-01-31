import io
import numpy as np    
from PIL import Image
import mxnet as mx
from mxnet.gluon.data.vision import transforms

class MLDriver():
    def __init__(self):
        # Download the labels for the ML model
        mx.test_utils.download('https://s3.amazonaws.com/onnx-model-zoo/synset.txt')
        with open('synset.txt', 'r') as f:
            self.labels = [l.rstrip() for l in f]

    def process_request_data(self, image_string):
        image = self.__get_numpy_arr_from_binary_image(image_string)

        preprocessed_image = self.__preprocess(image)

        return preprocessed_image

    def get_predictions(self, scores):
        scores = np.squeeze(scores)
        sorted_scores = np.argsort(scores)[::-1]

        predictions = ""
        for i in sorted_scores[0:3]:
            predictions += f"I am {str(scores[i])}% sure it is a {' '.join(self.labels[i].split(' ')[1:])}. "
        
        return predictions

    def __preprocess(self, img):
        img = mx.ndarray.array(img)

        transform_fn = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        
        img = transform_fn(img)
        img = img.expand_dims(axis=0)
        return img.asnumpy()
        
    def __get_numpy_arr_from_binary_image(self, image_string):
        img = Image.open(io.BytesIO(image_string))
        return np.asarray(img)

ml_driver = None

def initialize():
    global ml_driver

    ml_driver = MLDriver()

def get_instance():
    global ml_driver

    return ml_driver