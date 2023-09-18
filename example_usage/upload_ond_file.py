import plantpredict

# authenticate using API credentials
api = plantpredict.Api(
    client_id="insert client_id here",
    client_secret="insert client_secret here"
)

# instantiate a local Inverter object
inverterRequest = api.inverter()

file_name = "Huawei_SUN2000-60KTL_M0_480V.OND"
file_path = "python-sdk\\example_usage\\Huawei_SUN2000-60KTL_M0_480V.OND"
new_inverter = inverterRequest.upload_ond_file(file_name, file_path)
print(new_inverter['id'])
