"""This file contains the code for "Set a prediction's monthly factors (albedo, soiling loss, spectral loss)" in the "Example Usage" section of the
documentation located at https://plantpredict-python.readthedocs.io."""

import plantpredict
from plantpredict.enumerations import SoilingModelTypeEnum, SpectralShiftModelEnum


# authenticate using API credentials
api = plantpredict.Api(
    username="insert username here",
    password="insert password here",
    client_id="insert client_id here",
    client_secret="insert client_secret here"
)

# this can be done upon initial creation of a prediction, but for the sake of example, we will consider the case of
# updating an existing prediction.

# instantiate the prediction of interest using the :py:class:`~plantpredict.prediction.Prediction` class, specifying
# its ID and project ID (visible in the URL of that prediction in a web browser
# `.../projects/{project_id}/prediction/{id}/`).
project_id = 13161  # CHANGE TO YOUR PROJECT ID
prediction_id = 147813  # CHANGE TO YOUR PREDICTION ID
prediction = api.prediction(id=prediction_id, project_id=project_id)

# retrieve the prediction's attributes
prediction.get()

# this example assumes that the user wants to specify all 3 available monthly factors, and enforce that the prediction
# use monthly soiling loss and spectral loss averages. however, a user can choose just to specify albedo, or albedo and
# soiling loss, or albedo and spectral shift.

# set the `monthly_factors` as such, where albedo is in units `[decimal]`, soiling loss in `[%]`, and spectral loss in
# `[%]`. for soiling loss and spectral loss, a negative number indicates a gain. the values below should be replaced
# with those obtained from measurements/assumptions for your project
prediction.monthly_factors = [
    {"month": 1, "month_name": "Jan", "albedo": 0.4, "soiling_loss": 0.40, "spectral_shift": 0.958},
    {"month": 2, "month_name": "Feb", "albedo": 0.3, "soiling_loss": 0.24, "spectral_shift": 2.48},
    {"month": 3, "month_name": "Mar", "albedo": 0.2, "soiling_loss": 0.76, "spectral_shift": 3.58},
    {"month": 4, "month_name": "Apr", "albedo": 0.2, "soiling_loss": 0.88, "spectral_shift": 3.48},
    {"month": 5, "month_name": "May", "albedo": 0.2, "soiling_loss": 0.81, "spectral_shift": 2.58},
    {"month": 6, "month_name": "Jun", "albedo": 0.2, "soiling_loss": 1.01, "spectral_shift": 1.94},
    {"month": 7, "month_name": "Jul", "albedo": 0.2, "soiling_loss": 1.21, "spectral_shift": 3.7},
    {"month": 8, "month_name": "Aug", "albedo": 0.2, "soiling_loss": 0.99, "spectral_shift": 4.57},
    {"month": 9, "month_name": "Sep", "albedo": 0.2, "soiling_loss": 1.34, "spectral_shift": 6.39},
    {"month": 10, "month_name": "Oct", "albedo": 0.2, "soiling_loss": 0.54, "spectral_shift": 4.16},
    {"month": 11, "month_name": "Nov", "albedo": 0.3, "soiling_loss": 0.52, "spectral_shift": 0.758},
    {"month": 12, "month_name": "Dec", "albedo": 0.4, "soiling_loss": 0.33, "spectral_shift": 0.886}
]

# in order to enforce that the prediction use monthly average values (rather than soiling time series from a weather
# file, for instance), the `soiling_model` and `spectral_shift_model` must be set with the following code (assuming
# that both soiling loss and spectral shift loss are specified in `monthly factors`)
prediction.soiling_model = SoilingModelTypeEnum.CONSTANT_MONTHLY
prediction.spectral_shift_model = SpectralShiftModelEnum.MONTHLY_OVERRIDE

# call the update method on the instance of Prediction to persist these changes to PlantPredict
prediction.update()
