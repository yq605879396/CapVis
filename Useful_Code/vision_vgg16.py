import torch
from torchvision import datasets, transforms as T
import torchvision.models as models
from torch.autograd import Variable

from PIL import Image

import numpy as np

vgg16 = models.vgg16(pretrained=True)
vgg16.eval()

transform = T.Compose([T.Resize(256), T.CenterCrop(224), T.ToTensor(), T.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225])])

img = Image.open('photo/test8.jpg')
img = transform(img)
img = img.unsqueeze(0)
img = Variable(img)

result = vgg16(img).detach().numpy().flatten()

print(result)
print(result.sum())