import csv
import json
import random
import mysql.connector

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME", "projectdb")
)

cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS ORGANIZATION (
    Organization_ID INT NOT NULL PRIMARY KEY,
    Name VARCHAR(500) NOT NULL,
    Organization_Type VARCHAR(255),
    Description TEXT,
    Contact_Info VARCHAR(500)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS DATASET (
    Dataset_ID INT NOT NULL PRIMARY KEY,
    Title TEXT NOT NULL,
    Description TEXT,
    Access_level VARCHAR(50),
    License VARCHAR(500),
    Metadata_Created_Date DATE,
    Metadata_Updated_Date DATE,
    Identifier VARCHAR(500),
    Category TEXT,
    Publisher VARCHAR(500),
    Homepage_URL TEXT,
    Organization_ID INT,
    FOREIGN KEY (Organization_ID) REFERENCES ORGANIZATION(Organization_ID)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS RESOURCES (
    Resource_ID INT NOT NULL PRIMARY KEY,
    Name TEXT,
    Format VARCHAR(100),
    URL TEXT NOT NULL,
    Resource_Type VARCHAR(255),
    Dataset_ID INT NOT NULL,
    FOREIGN KEY (Dataset_ID) REFERENCES DATASET(Dataset_ID)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS USERS (
    Email VARCHAR(255) NOT NULL PRIMARY KEY,
    Username VARCHAR(100) NOT NULL,
    Gender VARCHAR(50),
    Age INT,
    Birth_date DATE,
    Country VARCHAR(100)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS TAGS (
    Tag_Name VARCHAR(255) NOT NULL PRIMARY KEY
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS DATASETTAG (
    Dataset_ID INT NOT NULL,
    Tag_Name VARCHAR(255) NOT NULL,
    PRIMARY KEY (Dataset_ID, Tag_Name),
    FOREIGN KEY (Dataset_ID) REFERENCES DATASET(Dataset_ID),
    FOREIGN KEY (Tag_Name) REFERENCES TAGS(Tag_Name)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS USAGE_INFO (
    Usage_ID INT NOT NULL PRIMARY KEY,
    Project_Name VARCHAR(255) NOT NULL,
    Project_Category VARCHAR(100) NOT NULL,
    User_Email VARCHAR(255) NOT NULL,
    Dataset_ID INT NOT NULL,
    FOREIGN KEY (User_Email) REFERENCES USERS(Email),
    FOREIGN KEY (Dataset_ID) REFERENCES DATASET(Dataset_ID)
)
""")


with open("Milestone 2 - Database/output/organizations.json", "r") as f:
    organizations = json.load(f)

with open("Milestone 2 - Database/output/datasets_table.json", "r") as f:
    datasets = json.load(f)

with open("Milestone 2 - Database/output/resources_table.json", "r") as f:
    resources = json.load(f)

with open("Milestone 2 - Database/output/tags_table.json", "r") as f:
    tags = json.load(f)

with open("Milestone 2 - Database/output/datasettag_table.json", "r") as f:
    datasettag = json.load(f)

for org in organizations:
    query = """
    INSERT IGNORE INTO ORGANIZATION
    (Organization_ID, Name, Organization_Type, Description, Contact_Info) VALUES (%s, %s, %s, %s, %s)
    """
    val = (
        org["Organization_ID"],
        org["Name"],
        org["Organization_Type"],
        org["Description"],
        org["Contact_Info"]
    )
    cur.execute(query, val)

for dataset in datasets:
    query = """
    INSERT IGNORE INTO DATASET
    (Dataset_ID, Title, Description, Access_level, License, Metadata_Created_Date, Metadata_Updated_Date, Identifier,Category, Publisher, Homepage_URL, Organization_ID)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    val = (
        dataset["Dataset_ID"],
        dataset["Title"],
        dataset["Description"],
        dataset["Access_level"],
        dataset["License"],
        dataset["Metadata_Created_Date"] or None,
        dataset["Metadata_Updated_Date"] or None,
        dataset["Identifier"],
        dataset["Category"],
        dataset["Publisher"],
        dataset["Homepage_URL"],
        dataset["Organization_ID"]
    )
    cur.execute(query, val)

for resource in resources:
    query = """
    INSERT IGNORE INTO RESOURCES
    (Resource_ID, Name, Format, URL, Resource_Type, Dataset_ID) VALUES (%s, %s, %s, %s, %s, %s)
    """
    val = (
        resource["Resource_ID"],
        resource["Name"],
        resource["Format"],
        resource["URL"],
        resource["Resource_Type"],
        resource["Dataset_ID"]
    )
    cur.execute(query, val)

for tag in tags:
    query = "INSERT IGNORE INTO TAGS (Tag_Name) VALUES (%s)"
    val = (tag["Tag_Name"],)
    cur.execute(query, val)

for dt in datasettag:
    query = "INSERT IGNORE INTO DATASETTAG (Dataset_ID, Tag_Name) VALUES (%s, %s)"
    val = (
        dt["Dataset_ID"],
        dt["Tag_Name"]
    )
    cur.execute(query, val)

conn.commit()

with open("users.csv", "r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        query = """
        INSERT IGNORE INTO USERS (Email, Username, Gender, Age, Birth_date, Country) VALUES (%s, %s, %s, %s, %s, %s)
        """
        val = (
            row["Email"],
            row["Username"],
            row["Gender"],
            int(row["Age"]) if row["Age"] else None,
            row["Birth_date"] if row["Birth_date"] else None,
            row["Country"]
        )
        cur.execute(query, val)

conn.commit()

cur.execute("SELECT Email FROM USERS")
users = [row[0] for row in cur.fetchall()]

cur.execute("SELECT Dataset_ID FROM DATASET")
datasets = [row[0] for row in cur.fetchall()]

project_names = [
    "Health Analysis",
    "Climate Study",
    "Traffic Dashboard",
    "Crime Report",
    "Population Insights",
    "Education Tracker",
    "Energy Forecast",
    "Housing Study",
    "Water Quality Analysis",
    "Agriculture Monitor"
]

project_categories = [
    "Health",
    "Environment",
    "Transportation",
    "Crime",
    "Population",
    "Education",
    "Energy",
    "Housing",
    "Water",
    "Agriculture"
]

for usage_id in range(1, 501):
    query = """
    INSERT IGNORE INTO USAGE_INFO
    (Usage_ID, Project_Name, Project_Category, User_Email, Dataset_ID) VALUES (%s, %s, %s, %s, %s)
    """
    val = (
        usage_id,
        random.choice(project_names),
        random.choice(project_categories),
        random.choice(users),
        random.choice(datasets)
    )
    cur.execute(query, val)

conn.commit()
cur.close()
conn.close()
