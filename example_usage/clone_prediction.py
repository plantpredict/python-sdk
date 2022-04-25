"""This file contains the code for "Clone a prediction." in the "Example Usage" section of the documentation located
at https://plantpredict-python.readthedocs.io."""

import plantpredict
from plantpredict.enumerations import TranspositionModelEnum

# authenticate using API credentials
api = plantpredict.Api(
    client_id="insert client_id here",
    client_secret="insert client_secret here"
)

# instantiate the prediction you wish to clone, specifying its ID and project ID (visible in the URL of that prediction
# in a web browser '.../projects/{project_id}/prediction/{id}/').
project_id = 13161   # CHANGE TO YOUR PROJECT ID
prediction_id = 147813   # CHANGE TO YOUR PREDICTION ID
prediction_to_clone = api.prediction(id=prediction_id, project_id=project_id)

# clone prediction (within the same project)
new_prediction_id = prediction_to_clone.clone(new_prediction_name='Cloned Prediction')

# update transposition model of new prediction
new_prediction = api.prediction(id=new_prediction_id, project_id=project_id)
new_prediction.get()
new_prediction.transposition_model = TranspositionModelEnum.HAY
new_prediction.update()
