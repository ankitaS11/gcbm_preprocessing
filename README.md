This script follows the pseudocode from Andrew's design to update GCBM configs: https://hackmd.io/@aornugent/B1RluG69c.

## Execution

### End-Point

* Endpoints supported: `/gcbm/upload`
* Categories supported: `disturbances, classifiers, miscellaneous`

```bash
# This uploads a classifier, disturbance and a miscellaneous file
curl -F disturbances="@disturbances/disturbances_2011_moja.tiff" -F classifiers="@classifiers/Classifier1_moja.tiff" http://localhost:8080/gcbm/upload

# Try skipping disturbance file, and it will still work :)
```

**Expected Output:**

```bash
{
  "error": "Missing files for categories: ['config_files', 'input'], they are required for the simulation to run"
}
```

The outputs for classifier file and disturbance file will be stored in "templates/config/" folder.

### GCBM Pre-Processing

Run: `python3 gcbm.py` and a folder will be generated with the output config files (JSON) for all the categories.

Script:

```bash
pip install -r requirements.txt
python3 gcbm.py
cat templates/config/disturbances_2011_moja.json
cat templates/config/Classifier1_moja.json
```

Please see the `main` function in the `gcbm.py` file for more info. A payload is manually added, which checks if it has year and then the `has_year` key is set to `True`

## Validation

In order to make sure that the generated configs are correct, I've written a script `compare_jsons.py`. Pass the original folder first and the new folder second if you want (else the default paths are used).

```bash
>>> python3 compare_jsons.py compare templates/config/

Note: using compare for original JSONs and templates/config for new JSONs folders.
Failures: 0/11
Success: 11/11
```
