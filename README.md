# Open Data Catalog ETL & Relational Database

A Python and MySQL data-engineering project that retrieves public datasets from the **Data.gov CKAN API**, transforms the nested API responses into normalized relational records, and loads the processed data into a MySQL database.

The project demonstrates API ingestion, ETL processing, relational database design, data normalization, and Python-to-MySQL integration.

## Features

- Retrieves public datasets from the Data.gov CKAN API
- Supports ingestion of up to **2,000 datasets** per run
- Extracts dataset, organization, resource, and tag information
- Converts nested JSON responses into relational-style records
- Stores processed data as intermediate JSON files
- Loads transformed records into MySQL using Python
- Models one-to-many and many-to-many relationships
- Imports additional user data from CSV
- Generates sample dataset-usage records
- Uses environment variables for database credentials

## ETL Pipeline

The project follows a simple Extract, Transform, Load workflow:

```text
Data.gov CKAN API
        |
        v
   Python Crawler
        |
        v
 Raw JSON Response
        |
        v
 Transformation
        |
        +--------------------+
        |                    |
        v                    v
 Organizations          Datasets
        |                    |
        +---------+----------+
                  |
           +------+------+
           |             |
           v             v
       Resources        Tags
                         |
                         v
                 Dataset-Tag Links
                  |
                  v
             MySQL Database
