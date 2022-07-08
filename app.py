import json
import os
from flask import Flask
from flask import request
from flask_restful import Api
from flask_cors import CORS
from enum import Enum

from gcbm import GCBMSimulation

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:8080/"])
api = Api(app)


class REQUIRED(Enum):
    YES = 1
    NO = 0


categories = {
    "disturbances": REQUIRED.NO,
    "classifiers": REQUIRED.YES,
    "miscellaneous": REQUIRED.YES,
    "config_files": REQUIRED.YES,
    "input": REQUIRED.YES
}


@app.route("/gcbm/upload", methods=["POST"])
def gcbm_upload():
    title = request.form.get('title') or 'simulation'
    title = ''.join(c for c in title if c.isalnum())

    project_dir = f"{title}"
    if not os.path.exists(f"{os.getcwd()}/input/{project_dir}"):
        os.makedirs(f"{os.getcwd()}/input/{project_dir}")

    def fix_path(path):
        return os.path.basename(path.replace("\\", "/"))

    gcbm = GCBMSimulation()

    errored_categories = []
    for category, req in categories.items():
        if category in request.files:
            for file in request.files.getlist(category):
                gcbm.add_file(category + "/" + file.filename)
        elif req == REQUIRED.YES:
            errored_categories.append(category)
    
    if len(errored_categories) != 0:
        return {"error": f"Missing files for categories: {errored_categories}, they are required for the simulation to run"}, 400

    # if "config_files" in request.files:
    #     for file in request.files.getlist("config_files"):
    #         if file.filename == "provider_config.json":
    #             provider_config = json.load(file)
    #             provider_config["Providers"]["SQLite"]["path"] = fix_path(provider_config["Providers"]["SQLite"]["path"])
    #             layers = []
    #             for layer in provider_config["Providers"]["RasterTiled"]["layers"]:
    #                 layer["layer_path"] = fix_path(layer["layer_path"])
    #                 layers.append(layer)
    #             provider_config["Providers"]["RasterTiled"]["layers"] = layers
    #             with open(f"{os.getcwd()}/input/{project_dir}/provider_config.json", "w") as pcf:
    #                 json.dump(provider_config, pcf)
    #         elif file.filename == "modules_output.json":
    #             modules_output = json.load(file)
    #             modules_output["Modules"]["CBMAggregatorSQLiteWriter"]["settings"]["databasename"] = "output/gcbm_output.db"
    #             modules_output["Modules"]["WriteVariableGeotiff"]["settings"]["output_path"] = "output"
    #             with open(f"{os.getcwd()}/input/{project_dir}/modules_output.json", "w+") as mof:
    #                 json.dump(modules_output, mof)
    #         else:
    #             file.save(f"{os.getcwd()}/input/{project_dir}/{file.filename}")
    # else:
    #     return {"error": "missing configuration file"}, 400

    # if "input" in request.files:
    #     for file in request.files.getlist("input"):
    #         file.save(f"{os.getcwd()}/input/{project_dir}/{file.filename}")
    # else:
    #     return {"error": "missing input"}, 400

    # if "db" in request.files:
    #     for file in request.files.getlist("db"):
    #         file.save(f"{os.getcwd()}/input/{project_dir}/{file.filename}")
    # else:
    #     return {"error": "missing db"}, 400

    return {"data": "All files uploaded successfully."}, 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
