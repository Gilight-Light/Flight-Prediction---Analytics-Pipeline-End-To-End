# Data Engineering Project: Flight Prediction - Analytics Pipeline End-To-End

## Describe

This project implements an **end-to-end data pipeline** for collecting, processing, and analyzing Flight data. The pipeline is designed to:
- **Download Dataset** Download dataset from kaggle and save in Docker Container
- **Extract** raw flight data from various sources (CSV, Database).
- **Transform** the data into a structured format.
- **Load** the processed data into a data warehouse for analysis.
- **Generate insights** for business intelligence using analytical tools.

## Target
The objective of this project is to create a **scalable and automated data pipeline** that:
- Integrates data from different sources.
- Processes the data in Batch-time.
- Loads data into a data warehouse.
- Provides clean, structured data for insightful analysis.

## Technologies and tools:
This project uses the following technologies and tools:
- **Programming Languages**: Python, SQL
- **Data Extraction**: API Kaggle (using 'curl' and `unzip`)
- **ETL Tools**: Apache Airflow for orchestration, Pandas for data transformation
- **Data Storage**: PostgresDB for raw data storage, BigQuery for data warehousing
- **Data Analysis**: Jupyter Notebooks, SQL for querying
- **Reporting & Visualization**: Streamlit, Matplotlib for data visualization
- **Version Control**: Git, GitHub

## Config

### Requirements systems
- Git
- BigQuery Account
- Docker

### Install systems
1. **Clone repository**:
   ```bash
   git clone https://github.com/yourusername/data-engineering-project.git
2. **Docker build Inmage**:
- cd End-To-End-Project-ETL

- docker build --tag projectetl

- docker compose up airflow-init

- docker compose up

