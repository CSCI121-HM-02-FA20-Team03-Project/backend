from infer_model import InferModel
from preprocess import Preprocess
from PIL import Image
import torch
import numpy as np

im = InferModel()
path = 'download3.jpg'

originalImage = cv2.imread(path, cv2.IMREAD_UNCHANGED)

resizedImage = Preprocess.resizeImage(originalImage)
convertedImage = Preprocess.invertImageColor(resizedImage)[1]

# img_open = Image.open(path).convert('L')
# print(np.array(img_open))

x_t = torch.from_numpy(np.array(convertedImage)).type(torch.FloatTensor)
print(x_t)
print(len(x_t))
# for i in x_t:
#     print(i)
prediction = im.infer(x_t)
print(prediction)