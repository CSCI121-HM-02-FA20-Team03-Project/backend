from infer_model import InferModel
from PIL import Image
import torch
import numpy as np

im = InferModel()
path = '18_em_12_0.bmp'
img_open = Image.open(path).convert('L')
x_t = torch.from_numpy(np.array(img_open)).type(torch.FloatTensor)
prediction = im.infer(x_t)
print(prediction)
print(prediction)