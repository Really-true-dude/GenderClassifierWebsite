import torch
import torchvision
from typing import List, Dict
from model import ClassifierModel, device, class_names


def PredictOnImage(model: torch.nn.Module,
                   image_path: str,
                   class_names: List[str] = None,
                   transform: torchvision.transforms = None,
                   device = device) -> Dict[str, float]:
    print("Classifying image..")
    # load image
    target_image = torchvision.io.read_image(str(image_path)).type(torch.float32)
    target_image /= 255

    # transform if necessary
    if transform:
        target_image = transform(target_image)
        
    model.to(device)

    # making predictions
    model.eval()
    results = {}
    with torch.inference_mode():
        target_image = target_image.unsqueeze(dim=0)
        target_image_logits = model(target_image.to(device))

        target_image_pred_prob = torch.softmax(target_image_logits, dim=1)
        target_image_pred_prob = torch.squeeze(target_image_pred_prob)

        for i, prediction in enumerate(target_image_pred_prob):
            temp = {class_names[i]: prediction.item()}
            results.update(temp)

    print(results) # printing for debugging
    return results



