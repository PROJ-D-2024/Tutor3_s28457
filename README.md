🛠️ Thesis Project: Data Cleaning and Standardization

📄 Project Purpose

The purpose of this project is to clean and standardize a dataset in preparation for the analysis and modeling required for my future thesis project. This involves selecting a relevant dataset, performing data cleaning (handling missing values, removing duplicates, addressing outliers), and standardizing the data to ensure consistency. The goal is to create a reproducible data preprocessing workflow.

🚀 Technologies Used

MongoDB: Used as the primary database for storing and managing the dataset.

Python: Used for scripting and executing data cleaning and preprocessing tasks.

MongoDB Compass: Used for connecting to MongoDB, exploring, and managing data.

Git and GitHub: Used for version control to ensure reproducibility and collaboration.

📊 System Architecture

This project follows a structured workflow for data loading, cleaning, and model training. The components and their interactions are shown in the architecture diagram.

How to Understand and Navigate the Architecture

  Data Source:
  
    sample_customer_data.csv: The initial dataset in CSV format.



  Data Loading:
  
    database_connection.py:
    
      Loads the CSV data into MongoDB (thesis_project database, sample_data collection).



  Data Cleaning:
  
    MongoDBDataCleaner.py:
    
      Cleans and standardizes the data by limiting age values, capping purchase amounts, and filling missing values.

  
  
  Model Training:
  
    load_cleaned_data.py:
    
      Processes the cleaned data, trains machine learning models (Logistic Regression, Random Forest, SVM), and evaluates their performance.


  Model Results:

    Model Performance Results:
    
      Outputs evaluation metrics like Accuracy, Precision, Recall, and F1 Score.
  
  
  Version Control:
  
    Git & GitHub:
    
      Use Git for version control and GitHub for collaboration.
