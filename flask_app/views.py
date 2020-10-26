from flask_app import app
import torch
from torch.nn import Softmax
import numpy as np
from preprocessImage import *
from model import *

with open("./sample_cifar10_base64/image0.txt") as f:
    base64string = f.read()

@app.route('/')
def recognizeImage():

	base64string = request.get_json(force=True)['base64']
    image = get_image(base64string)

    if image.shape[1:] != (3,32,32):
        return jsonify( error = "only RGB image 32x32 accepted", message = "failure!" )

    model = get_model()

    output_tensor = model(image)
    output_tensor = Softmax(dim=1)(output_tensor)
    prob_pred_tensor, pred_tensor = torch.max(output_tensor, 1)

    output = np.squeeze(output_tensor.detach().numpy()) 

    prob_pred = np.squeeze(prob_pred_tensor.detach().numpy()) 

    pred = np.squeeze(pred_tensor.detach().numpy()) 

    classes = ['airplane', 'automobile', 'bird', 'cat', 'deer','dog', 'frog', 'horse', 'ship', 'truck']

    pred_dict = {'predicted_class' : str(classes[pred]),
                 'prob_predicted_class' : str(prob_pred)}

    for i,prob in enumerate(output):
        pred_dict[classes[i]] = str(prob)

    print({'prediction' : pred_dict, 'message' : "success!" })
    return {'prediction' : pred_dict, 'message' : "success!" }