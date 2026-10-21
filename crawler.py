import os
import json
import requests

# Create output directory
os.makedirs("output", exist_ok=True)
datasets = []
rowsperpage = 20


'''
First part:
for page in range(100):
    url = f"https://catalog.data.gov/api/3/action/package_search?rows={rowsperpage}&start={page * rowsperpage}"
    res = requests.get(url)
    data = res.json()

    results = data["result"]["results"]
    datasets.extend(results)

with open("output/dataset_test.json", "w") as f:
    json.dump(datasets, f, indent=4)

print("Total datasets:", len(datasets))
'''
'''
Second part:
with open("output/dataset_test.json", "r") as f:
    raw_datasets = json.load(f)

organizations = []
datasets_table = []
resources_table = []
tags_table = []
datasettag_table = []

org_map = {}
dataset_id = 1
resource_id = 1

for dataset in raw_datasets:
    org = dataset.get("organization") or {}
    org_id = org.get("id")

    if org_id and org_id not in org_map:
        org_map[org_id] = len(org_map) + 1
        organizations.append({
            "Organization_ID": org_map[org_id],
            "Name": org.get("title") or org.get("name"),
            "Description": org.get("description"),
            "Organization_Type": org.get("type"),
            "Contact_Info": dataset.get("maintainer_email") or dataset.get("maintainer")
        })
    current_org_id = org_map.get(org_id)

    datasets_table.append({
        "Dataset_ID": dataset_id,
        "Title": dataset.get("title"),
        "Description": dataset.get("notes"),
        "Access_level": "private" if dataset.get("private") else "public",
        "License": dataset.get("license_title") or dataset.get("license_id"),
        "Metadata_Created_Date": (dataset.get ("metadata_created") or "")[:10],
        "Metadata_Updated_Date": (dataset.get("metadata_modified") or "")[:10],
        "Identifier": dataset.get("id"),
        "Category": None,
        "Publisher": org.get("title") or dataset.get("author"),
        "Homepage_URL": dataset.get("url"),
        "Organization_ID": current_org_id
    })


    for resource in dataset.get("resources", []):
        resources_table.append({
            "Resource_ID": resource_id,
            "Name": resource.get("name"),
            "Format": resource.get("format"),
            "URL": resource.get("url"),
            "Resource_Type": resource.get("resource_type"),
            "Dataset_ID": dataset_id
        })
        resource_id += 1


    for tag in dataset.get("tags", []):
        tag_name = tag.get("display_name") or tag.get("name")
        if tag_name:
            tags_table.append({"Tag_Name": tag_name})
            datasettag_table.append({
                "Dataset_ID": dataset_id,
                "Tag_Name": tag_name
            })

    dataset_id += 1


with open("output/organizations.json", "w") as f:
    json.dump(organizations, f, indent=4)

with open("output/datasets_table.json", "w") as f:
    json.dump(datasets_table, f, indent=4)

with open("output/resources_table.json", "w") as f:
    json.dump(resources_table, f, indent=4)

with open("output/tags_table.json", "w") as f:
    json.dump(tags_table, f, indent=4)

with open("output/datasettag_table.json", "w") as f:
    json.dump(datasettag_table, f, indent=4)

print("Organizations:", len(organizations))
print("Datasets:", len(datasets_table))
print("Resources:", len(resources_table))
print("Tags:", len(tags_table))
print("DatasetTag:", len(datasettag_table))
'''