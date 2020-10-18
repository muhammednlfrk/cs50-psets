# Library imports
from json import loads

# Load appsettings
with open("appsettings.secret.json", "r") as appsettings_file:
    appsettings_file_data = appsettings_file.read()
appsettings = loads(appsettings_file_data)
