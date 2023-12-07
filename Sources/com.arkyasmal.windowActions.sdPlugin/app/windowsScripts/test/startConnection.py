import subprocess
import json
import os
import pathlib

# Get the current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))
new_path = os.path.normpath(os.path.abspath(os.path.join(current_dir,r"..\..\..\dist\connection.exe" )))
new_path = pathlib.Path(new_path).as_posix()
register_event = json.dumps({})
new_args = ['--port', '8000', '-pluginUUID', "1234", '--registerEvent', register_event]
all_args = [new_path]
all_args.extend(new_args)
print(all_args)
subprocess.call(all_args)