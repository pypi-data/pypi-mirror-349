import sys
sys.path.append("../")

from fraudaverse import fraudaverse
import xgboost as xgb
import pandas as pd
import numpy as np
import json
from dotenv import load_dotenv
import os.path

env_ui = "../../.env"
if os.path.isfile(env_ui):
    print("Reading env from '" + env_ui + "'")
    # We need to read 'API_COOKIE' for authentication
    load_dotenv(dotenv_path=env_ui)
    

def test_persist():
    # create sample model from data and upload/persist to FA
    
    types = [ "ATM", "POS",  "Ecom", "P2P", "SWIFT"]
    countries = [ "de", "nl",  "us", "fr", "es"]
    training = pd.DataFrame({ 
        "Amount": [ 112.09,  928.33, 3000.00, 1500.00, 4500.00,   48.50,  100.00,  455.85, 1100.00,12090.00,    8.79,  400.00,  220.40,  200.00,  112.09,  338.50,  255.30, 1400.00,  850.00,  400.00],
        "Type":   [  "POS",  "Ecom",   "P2P",   "ATM", "SWIFT",   "POS",  "Ecom",   "P2P",   "ATM", "SWIFT",   "POS",  "Ecom",   "P2P",   "ATM", "SWIFT",   "POS",  "Ecom",   "P2P",   "ATM", "SWIFT"],
        "Country":[  "de",   "nl",     "us",    "de",  "fr",      "nl",   "es",     "fr",    "de",  "es",      "us",   "de",     "nl",    "fr",  "es",      "de",   "fr",     "us",    "nl",  "fr"],
    })
    fraud = pd.DataFrame({ 
        "Fraud": [       0,       1,       0,       1,       0,       0,       0,       0,       1,       0,       0,       1,       0,       0,       0,       0,       0,       0,       0,       0]
    })
    training["Type"] = training["Type"].astype("category")
    training["Type"] = training["Type"].cat.set_categories(types)
    training["Country"] = training["Country"].astype("category")
    training["Country"] = training["Country"].cat.set_categories(countries)

    dtrain = xgb.DMatrix(training, label=fraud, enable_categorical=True)  
    param = {'booster': 'gbtree', 'objective': 'binary:logistic'}
    model = xgb.train(param, dtrain, 25, evals = [(dtrain, 'train')], early_stopping_rounds=5)

    # exporting categories here:

    all_categories = fraudaverse.get_categories(training)

    category_str = json.dumps(all_categories)
    model_str = model.save_raw("json").decode("utf-8")

    fraudaverse.persist(host="http://127.0.0.1:8080", 
                        pipeline_id="66226bf2c6b8580b7d374da3", 
                        compute_id="66227f948057a3cf49b71f7e", 
                        model_name="Scoring model", 
                        model=model_str, 
                        categories=category_str,
                        auth_session=os.environ['AUTH_SESSION']
    )
    print("Upload finished. Check UI or DB for changes.")

def test_sample():
   print(fraudaverse.sample(host="http://127.0.0.1:8080", pipeline_id="66226bf2c6b8580b7d374da3", auth_session=os.environ['AUTH_SESSION']))

if __name__ == '__main__':
    test_persist()
    test_sample()