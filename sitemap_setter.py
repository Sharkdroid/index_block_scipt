import csv
import json
import requests
from typing import Dict, Any
from os import getenv
from sys import exit
from dotenv import load_dotenv
from warnings import warn

load_dotenv(".env")

if getenv("api_key") is not None:
    api_key = getenv("api_key")
else:
    raise EnvironmentError("api_key not present in environment file")


header = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {api_key}"

}

if getenv("cascade_site") == "apptest":
    base_url = "https://cascadeapptest.csi.edu:8443/api/v1"
    print("Using apptest")
elif getenv("cascade_site") == "prod":
    print("Using prod")
    base_url = "https://cascade.csi.edu:8443/api/v1"
else:
    raise EnvironmentError("'apptest' and 'prod' are the only valid inputs")

if getenv("csv_path") is not None:
    sitemap_csv_file = getenv("csv_path")
    # force type conversion for type hinting 
    sitemap_csv_file = str(sitemap_csv_file)
else:
    raise EnvironmentError("Please make sure csv_path is included in the .env")

if getenv("asset_type") is not None:
    asset_type = getenv("asset_type")
else:
    raise EnvironmentError("Make sure asset_type is specified.")

# extracts the actual asset fields
def strip_cascade_object(raw_response: Dict[str, Any]) -> Dict[str, Any]:
    return raw_response["asset"][asset_type]

# retrieves the location of the sitemap metadata then changes its value. 
def set_sitemap_if_exists(asset: Dict[str, Any]) -> Dict[str, Any]:
    # check if should be published
    if "shouldBePublished" in asset and asset["shouldBePublished"]:
        fields = asset["metadata"]["dynamicFields"]
        sitemap_field = [ field for field in fields if field['name'] == "sitemap" ]
        # check if sitemap exists
        if len(sitemap_field) > 0:
            field_value = sitemap_field[0]["fieldValues"][0]["value"]
            if field_value == 'No':
                sitemap_field[0]["fieldValues"][0]["value"] = 'Yes'
    else:
        print(f"{asset['path']} not set to publish")
    return asset
    

with requests.session() as session:
    with open(sitemap_csv_file, 'r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            try:
                # ignore header row
                if row == ['id','path','site','is_published','has_sitemap_meta','sitemap_value_current']:
                    continue
                (
                    _id, 
                    path,
                    site_name, 
                    is_published,
                    has_sitemap,
                    cur_sitemap_val
                ) = row
                resp = session.get(
                    f"{base_url}/read/{asset_type}/{_id}",
                    headers=header
                )
                data = resp.json()
                if not ("asset" in data and asset_type in data["asset"]):
                    warn(f"unable to parse the asset:{path} - cascade returned:{data}")
                    continue
                asset = strip_cascade_object(data)
                # if it contains metadata field
                if "metadata" in asset and "dynamicFields" in asset["metadata"]:
                    asset = set_sitemap_if_exists(asset)
                    payload = json.dumps({"asset":{asset_type : asset}})                      
                    edit_response = session.post(
                        f"{base_url}/edit",
                        headers=header,
                        data=payload
                    )
                    edit_status = edit_response.json()
                    if "success" in edit_status and not edit_status["success"]:
                        warn(f"{path} unsuccessful at updating. Return message:{edit_status["message"]}")
                    else:
                        print(f"successfully updated {path}")
            except requests.JSONDecodeError:
                print(f"Request did not return a valid JSON format. (Most likely a HTML response)")
            except requests.RequestException:
                print(f"Unable to get extract data from {path}. ")
            except ValueError:
                print(f"Please fix the row {path} it contains too many columns")
                exit(1)
