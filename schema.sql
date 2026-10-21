-- Schema recreated from the uploaded Phase 2 connector.py
-- Updated USAGE_INFO.Usage_ID to AUTO_INCREMENT for Phase 3 registration.
-- Run against the selected MySQL database (e.g., defaultdb).

CREATE TABLE IF NOT EXISTS ORGANIZATION (
    Organization_ID INT NOT NULL PRIMARY KEY,
    Name VARCHAR(500) NOT NULL,
    Organization_Type VARCHAR(255),
    Description TEXT,
    Contact_Info VARCHAR(500)
);

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
);

CREATE TABLE IF NOT EXISTS RESOURCES (
    Resource_ID INT NOT NULL PRIMARY KEY,
    Name TEXT,
    Format VARCHAR(100),
    URL TEXT NOT NULL,
    Resource_Type VARCHAR(255),
    Dataset_ID INT NOT NULL,
    FOREIGN KEY (Dataset_ID) REFERENCES DATASET(Dataset_ID)
);

CREATE TABLE IF NOT EXISTS USERS (
    Email VARCHAR(255) NOT NULL PRIMARY KEY,
    Username VARCHAR(100) NOT NULL,
    Gender VARCHAR(50),
    Age INT,
    Birth_date DATE,
    Country VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS TAGS (
    Tag_Name VARCHAR(255) NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS DATASETTAG (
    Dataset_ID INT NOT NULL,
    Tag_Name VARCHAR(255) NOT NULL,
    PRIMARY KEY (Dataset_ID, Tag_Name),
    FOREIGN KEY (Dataset_ID) REFERENCES DATASET(Dataset_ID),
    FOREIGN KEY (Tag_Name) REFERENCES TAGS(Tag_Name)
);

CREATE TABLE IF NOT EXISTS USAGE_INFO (
    Usage_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Project_Name VARCHAR(255) NOT NULL,
    Project_Category VARCHAR(100) NOT NULL,
    User_Email VARCHAR(255) NOT NULL,
    Dataset_ID INT NOT NULL,
    FOREIGN KEY (User_Email) REFERENCES USERS(Email),
    FOREIGN KEY (Dataset_ID) REFERENCES DATASET(Dataset_ID)
);
