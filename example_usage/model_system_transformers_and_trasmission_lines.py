"""This file contains the code for "Model System-Level of Power Plant (Transformer, Transmission, etc.)" in the
"Example Usage" section of the documentation located at https://plantpredict-python.readthedocs.io."""

import plantpredict

# authenticate using API credentials
api = plantpredict.Api(
    username="insert username here",
    password="insert password here",
    client_id="insert client_id here",
    client_secret="insert client_secret here"
)

# This can be done upon initial creation of a prediction from
# scratch (see the example for `Create Project and Prediction from scratch.`_), but for the sake of example, we will
# consider the case of updating an existing power plant.

# instantiate a power plant, specifying its project ID and prediction ID (visible in the URL of that prediction in a
# web browser '.../projects/{project_id}/prediction/{id}').
project_id = 13161   # CHANGE TO YOUR PROJECT ID
prediction_id = 147813   # CHANGE TO YOUR PREDICTION ID
powerplant = api.powerplant(project_id=project_id, prediction_id=prediction_id)

# Retrieve its attributes
powerplant.get()

# Set the system availability_loss on the powerplant object in units [%]
powerplant.availability_loss = 1.7

# Set the plant output (LGIA) limit in units [MWac]
powerplant.lgia_limitation = 0.8

# add transformers and transmission lines, specifying the ordinal (1-indexed) such that they are in the desired order
# (where 1 is closest to the output of the plant)
powerplant.add_transformer(rating=0.6, high_side_voltage=600, no_load_loss=1.1, full_load_loss=1.7, ordinal=1)
powerplant.add_transmission_line(length=3, resistance=0.1, number_of_conductors_per_phase=1, ordinal=2)

# call the update method on the instance of PowerPlant to persist these changes to PlantPredict
powerplant.update()
