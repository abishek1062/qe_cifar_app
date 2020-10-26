from flask_app import app
from flask_app.preprocessImage import *
from flask_app.model import *
import torch
from torch.nn import Softmax
import numpy as np
from flask import request, jsonify


@app.route('/',methods=['GET','POST'])
def recognizeImage():
    try:
        base64string = request.get_json(force=True)['base64']
    except:
        return jsonify(error = "payload does not have base64", message = 'failure!')

    try:
        image = get_image(base64string)
    except:
        return jsonify(error = 'improper base64 encoding', message = "failure!")

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

    return jsonify(prediction = pred_dict, message = "success!" )