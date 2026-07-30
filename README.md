# Serverless API Data Lake Pipeline 🚀

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Apache Parquet](https://img.shields.io/badge/Apache%20Parquet-white?style=for-the-badge&logo=apacheparquet&logoColor=blue)

An end-to-end serverless Data Engineering pipeline that ingests relational data from a REST API, transforms and compresses it into Parquet format, and catalogs it for analytical SQL querying in an S3 Data Lake. 

## 🏗️ Architecture

```text
[ Rick & Morty REST API ] 
         │
         ▼ (HTTP Requests + Rate Limit Handling)
[ AWS Glue (Python Shell Engine) ]
         │
         ▼ (Transformation: Flatten JSON, Extract Keys, Parquet Encoding)
[ Amazon S3 (Data Lake) ]
         │
         ▼ (Schema Discovery)
[ AWS Glue Crawler & Data Catalog ]
         │
         ▼ (Standard SQL)
[ Amazon Athena (Query Engine) ]

Key Features
Resilient API Ingestion: Implements exponential backoff and polite sleep intervals to bypass HTTP 429 Too Many Requests API rate limits.

Complex Data Flattening: Uses pandas to normalize deeply nested JSON payloads into flat relational columns.

Schema Evolution & Validation: Enforces explicit columnar types using pyarrow to prevent Data Lake corruption.

Cost-Optimized Storage: Converts standard JSON payloads into highly compressed Apache Parquet format, heavily reducing Amazon Athena query scan costs.

Automated Data Cataloging: Utilizes AWS Glue Crawlers to dynamically discover S3 data partitions and update the Glue Data Catalog.

🛠️ Tech Stack
Language: Python 3.9

Libraries: pandas, awswrangler, requests, pyarrow

Cloud Provider: Amazon Web Services (AWS)

Compute: AWS Glue (Python Shell, 0.0625 DPU)

Storage: Amazon S3

Analytics Engine: Amazon Athena

📂 Repository Structure
├── scripts/
│   └── rick_and_morty_etl.py    # Main AWS Glue Python Script
├── query_examples/
│   └── athena_queries.sql       # Sample SQL queries for analytics
├── README.md                    # Project Documentation

Setup & Deployment
1. AWS IAM Configuration
Create an IAM Role (AWSGlue-RickAndMorty-Role) with a custom policy to grant Glue permissions to execute multi-part S3 uploads and run crawlers:
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:AbortMultipartUpload",
                "s3:ListMultipartUploadParts"
            ],
            "Resource": "arn:aws:s3:::your-bucket-name/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:ListBucketMultipartUploads"
            ],
            "Resource": "arn:aws:s3:::your-bucket-name"
        }
    ]
}

2. Deploy the ETL Job
Upload the python script to your S3 bucket.

In the AWS Glue Console, create a new Python Shell job.

Attach the IAM role created in Step 1.

Run the job to extract the API data and write the Parquet files to s3://your-bucket-name/rick_and_morty/.

3. Catalog the Data
Navigate to AWS Glue Crawlers.

Add three explicit data sources:

s3://your-bucket-name/rick_and_morty/characters/

s3://your-bucket-name/rick_and_morty/locations/

s3://your-bucket-name/rick_and_morty/episodes/

Point the crawler to a new target database (e.g., rick_and_morty_db) and execute it.

📊 Analytics Usage (Amazon Athena)
Once the crawler completes, you can immediately query your structured data Lake in Amazon Athena.

