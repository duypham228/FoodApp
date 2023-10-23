import session_manager
from functools import wraps
import json

# class test():
#     def __init__(self, session_manager):
#         self.session_manager = session_manager

#     def print(self):
#         print(session_manager.sessions)
    
#     def create_session(self, username):
#         session_manager.create_session(username)
    

# test1 = test(session_manager)
# test2 = test(session_manager)

# test1.create_session("test1")
# test2.create_session("test2")

# test1.print()
# dict1 = {"a": "b", "c": "d", "e": ""}
# if dict1["e"] is not None:
#     print("True")
# else:
#     print("False")
def get_value_from_yaml(yaml_content, key):
    lines = yaml_content.splitlines()
    value = None
    key_found = False

    for line in lines:
        if key in line:
            key_found = True
        elif key_found:
            value = line.strip()
            break

    return value

# Read the YAML content from your config file
with open("config.yml", "r") as config_file:
    yaml_content = config_file.read()

# Specify the key you want to extract (e.g., "tamubatch_path")
key = "tamubatch_path"

# Get the value associated with the key in the specified environment (e.g., "production")
tamubatch_path = get_value_from_yaml(yaml_content, f"{key}:")

print(f"{key}: {tamubatch_path}")
