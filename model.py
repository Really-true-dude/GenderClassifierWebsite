import torch
from torch import nn
import torchvision
from torchvision import transforms


device = "cuda" if torch.cuda.is_available() else "cpu"
class_names = ["Female", "Male"]
weights_path = "modelWeights/ManVsFemale.pth"

transform = transforms.Compose([
   transforms.Resize(size=(224,224))
])

# Overriding the API to not get an error
from torchvision.models._api import WeightsEnum
from torch.hub import load_state_dict_from_url
def get_state_dict(self, *args, **kwargs):
    kwargs.pop("check_hash")
    return load_state_dict_from_url(self.url, *args, **kwargs)
WeightsEnum.get_state_dict = get_state_dict

weights = torchvision.models.EfficientNet_B0_Weights.DEFAULT # .DEFAULT = best available weights
ClassifierModel = torchvision.models.efficientnet_b0(weights=weights).to(device)

## Freezing the model parameters
for param in ClassifierModel.features.parameters():
  param.requires_grad = False

# Changing classifier layer
ClassifierModel.classifier = nn.Sequential(
    nn.Dropout(p = 0.2, inplace = True),
    nn.Linear(in_features = 1280, out_features=len(class_names), bias = True)
).to(device)

# Load weights
ClassifierModel.load_state_dict(torch.load(weights_path, map_location=torch.device(device)))