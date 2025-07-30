import pyarrow as pa
import pyarrow.flight as fl
import os
import requests
import pandas
import json
from dotenv import load_dotenv

load_dotenv()
req = requests.Session()
auth_session = os.environ.get("AUTH_SESSION", None)
if (auth_session): 
    print("Setting session from AUTH_SESSION")
    req.cookies.update({"id": auth_session})

def sample(pipeline_id, host=None, auth_session=None, genuine=10000, fraud=1000, from_days=180, to_days=30):
    """Returns a data sample for machine learning."""
    if host is None:
        host = os.environ.get("UI_HOST", None)
    if host is None:
        raise Exception(
            "The FraudAverse UI server host must be either passed as the `host` argument or set in the `UI_HOST` environment variable."
        )
    if (auth_session): 
        req.cookies.update({"id": auth_session})
    query = "{}"
    response = req.get(
        host + "/investigation/extern_api/sample/" + pipeline_id + f"/query/{query}/genuine/{genuine}/fraud/{fraud}"
    )
    json_data = json.loads(response.text)
    data = pandas.json_normalize(json_data)
    data_genuine = data.iloc[:, data.columns != "Fraud"]
    data_fraud = data["Fraud"].astype("int")
    
    return data_genuine, data_fraud


def get_categories(pd_dataframe: pandas.DataFrame):
    """Extracts all categories from pandas dataframe into single json."""
    categories = json.loads("{}")
    for frame in pd_dataframe:
        if pd_dataframe[frame].dtype == "category":
            cats = pandas.DataFrame({frame: pd_dataframe[frame].cat.categories})
            pd_dataframe[frame]
            categories[frame] = json.loads(cats.to_json())[frame]
    return categories
    

def persist(pipeline_id, compute_id, model_name, model, categories = "", host=None, auth_session=None):
    """ Persists a model in a scoring compute referenced by a pipeline and compute id
        Parameters
        ----------
        pipeline_id : str
            The pipeline id of the pipeline that should get modified. 
            The id is displayed in the url of the ui: `pipeline/{pipeline_id}/`
        compute_id : str
            The existing scoring compute that will receive the new model.
            The id is displayed in the url of the ui: `compute/{compute_id}/`
        model_name : str
            File name that should be displayed
        model : str
            The model as string in xgboost json format
        categories : str
            (optional) A json string of all categories that were used during training in following format
            {"attr1": { "0": "val_1", "1": "val_2"}, "attr2": { "0": "a", "b": "c"} }
    """
    
    if host is None:
        host = os.environ.get("UI_HOST", None)
    if host is None:
        raise Exception(
            "The FraudAverse UI server host must be either passed as the `host` argument or set in the `UI_HOST` environment variable."
        )
    if (auth_session): 
        req.cookies.update({"id": auth_session})

    try:
        response = req.put(
            host + "/processing/pipeline/" + pipeline_id + "/compute/" + compute_id + "/",
            json={"name": model_name, "model": model, "categories": categories},
        )
        response.raise_for_status()  # Raises an HTTPError if the status code is 4xx, 5xx
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")

    return response.text