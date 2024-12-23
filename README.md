# Data Engineering Project: Flight Prediction - Analytics Pipeline End-To-End

## 📌 Overview

Welcome to the Data Engineering Project! This project is designed to build an end-to-end data pipeline using cutting-edge technologies such as ETL, ELT, and Data Visualization. It uses modern tools and frameworks such as Apache Airflow, Docker, and Streamlit to build a scalable, efficient, and automated data pipeline.

### Key Features
- **Download Dataset**: Download dataset from Kaggle and save in Docker Container.
- **Extract**: Raw flight data from various sources (CSV, Database).
- **Transform**: The data into a structured format.
- **Load**: The processed data into a data warehouse for analysis.
- **Generate insights**: For business intelligence using analytical tools.

## Target
The objective of this project is to create a **scalable and automated data pipeline** that:
- Integrates data from different sources.
- Processes the data in batch-time.
- Loads data into a data warehouse.
- Provides clean, structured data for insightful analysis.

## 🛠️ Technologies and Tools
This project uses the following technologies and tools:
- **Programming Languages**: Python, SQL
- **Data Extraction**: API Kaggle (using `curl` and `unzip`)
- **ETL Tools**: Apache Airflow for orchestration, Pandas for data transformation
- **Data Storage**: PostgresDB for raw data storage, BigQuery for data warehousing
- **Data Analysis**: Jupyter Notebooks, SQL for querying
- **Reporting & Visualization**: Streamlit, Matplotlib for data visualization
- **Version Control**: Git, GitHub

## 📂 Project Structure
```
Flight Prediction - Analytics Pipeline End-To-End/
├── dags/
│   ├── sql/
│   │   ├── business_flight.sql
│   │   ├── economy_flight.sql
│   │   └── cleandata_flight.sql
│   ├── dag_download_dataset.py
│   ├── dag_ETL.py
│   └── dag_extract_dataset.py
├── .env
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
├── gradient_boosting_model.joblib
├── query.py
├── README.md
├── requirements.txt
└── streamlit_visual.py
```

## 📋 Prerequisites
- Git
- BigQuery Account
- Docker
- Streamlit Cloud

## ⚙️ Installation
Follow these steps to get the project up and running on your local machine:

1. **Clone repository**:
   Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/data-engineering-project.git
   ```

2. **Docker build image**:
   We use Docker for environment consistency. To build the Docker image, run the following command:
   ```bash
   cd End-To-End-Project-ETL
   docker build --tag projectetl .
   docker compose up airflow-init
   docker compose up
   ```

### Run your pipeline and visual
1. **Run DAG**:
   We use Apache Airflow to automate the ETL tasks. Run the following command to initialize Airflow.
   - Login to Airflow at [localhost:8080](http://localhost:8080/) with user: airflow - password: airflow
   ```bash
   Download_dataset_from_kaggle >> Extract_data_into_Postgres >> ETL_DATA
   ```

2. **Run Streamlit**:
   ```bash
   streamlit run streamlit_visual.py
   ```
   - Open Streamlit at [localhost:8501](http://localhost:8501/)

## 🚀 Usage
1. **Airflow UI**:
   To monitor the pipeline, navigate to the Airflow UI:
   - Open your browser and go to [http://localhost:8080](http://localhost:8080).
   - Use the default credentials (usually admin/admin).

2. **Streamlit Dashboard**:
   This will launch an interactive dashboard on [http://localhost:8501](http://localhost:8501).

### 🧑‍💻 Contributing
We welcome contributions! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit (`git commit -am 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a new Pull Request.

### 📚 Documentation
- [Airflow Documentation](https://airflow.apache.org/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)





