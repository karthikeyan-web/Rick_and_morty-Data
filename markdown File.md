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