import plantpredict

# authenticate using API credentials
api = plantpredict.Api(
    client_id="insert client_id here",
    client_secret="insert client_secret here"
)

# instantiate a local Module object
moduleRequest = api.module()

file_name = "FS-6455-P CdTe October2020_v687.PAN"
file_path = "python-sdk\\example_usage\\FS-6480-P CdTe January2022_v7211.PAN"
new_moduleId = moduleRequest.upload_pan_file(file_name, file_path)
print(new_moduleId)
