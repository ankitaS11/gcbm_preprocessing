This script follows the pseudocode from Andrew's design to update GCBM configs: https://hackmd.io/@aornugent/B1RluG69c.

## Execution

### End-Point

* Endpoints supported: `/gcbm/upload`
* Categories supported: `disturbances`

```bash
curl -F disturbances="@disturbances/disturbances_2011_moja.tiff" -F title="run4" http://localhost:8080/gcbm/upload
```

**Expected Output:**

```bash
{
  "error": "Missing files for categories: ['classifiers', 'miscellaneous', 'config_files', 'input'], they are required for the simulation to run"
}
```

### GCBM Pre-Processing

Run: `python3 gcbm.py disturbances/disturbances_2011_moja.tiff` and a folder will be generated with the output config file (JSON)

Script:

```bash
pip install -r requirements.txt
python3 gcbm.py disturbances/disturbances_2011_moja.tiff
cat templates/config/disturbances_2011_moja.json
```

Please see the `main` function in the `gcbm.py` file for more info. A payload is manually added, which checks if it has year and then the `has_year` key is set to `True`

## TODOs

There are a lot of in-line TODOs, this is the first draft to see how we can implement this the most pythonic way.
