import pandas as pd
import numpy as np
import math
import sqlalchemy
#import pymssql
#import pyodbc
import datetime 
#import mysql
#import mysql.connector
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

input = 'filepath'

def read_data(input_path):
    raw_df = pd.read_csv(input_path, header = 1)
    return raw_df

def clean_data(df):
    #Grabs whatever row contains part I
    part1column = [i for i in df if df[i].isin(['Part I']).any()][0]
    df = df.rename(columns={"Unnamed: 0": "ID", part1column: "Part I"})
    filter = [col for col in df if not col.startswith(('Term', 'Cum','Unnamed'))]
    filtered_df = df[filter]
    dropped_df = filtered_df.drop(columns=filtered_df.columns[(filtered_df == 'P').any()])
    dropped_df = dropped_df.replace('Part I',np.NaN)
    return dropped_df

def convert_grades(df):
    grade_dict = { 
              "A" : 4.0,
              "A-" : 3.7,
              "B+" : 3.30,
              "B" : 3.0,
              "B-" : 2.7,
              "C+" : 2.3,
              "C" : 2.0,
              "C-" : 1.7,
              "D+" : 1.3,
              "D" : 1.0,
              "D-" : 0.7,
              "F" : 0
    }
    
    mapped_df = df.replace(grade_dict)
    id_df = mapped_df.iloc[0:, 0:2]
    mapped_df.iloc[:, 1:].astype(float)
    float_df = mapped_df.iloc[:, 1:].astype(float)
    credit_hours_arr = float_df.iloc[0,1:-1].values
    part1_scores = float_df.iloc[:,-1:]
    float_df = float_df.iloc[:, 1:-1] * np.array(credit_hours_arr)
    final_df = pd.merge(id_df,float_df, how='left', right_index=True, left_index=True)
    final_df = pd.merge(final_df, part1_scores, how='right', right_index=True, left_index=True)
    final_df = final_df.iloc[1:]
    
    return final_df

def filter_dataframe(df, column_name, values):
    filtered_df = df[df[column_name].isin(values)]
    return filtered_df

def get_columns_with_no_nulls_and_values(df, column_name, values):
    # Filter dataframe where specific column is equal to the given value
    filtered_df = filter_dataframe(df, column_name, values)

    # Get columns with no nulls
    non_null_columns = filtered_df.columns[filtered_df.isnull().sum() == 0]

    # Get columns from the filtered dataframe
    result_columns = filtered_df.columns.intersection(non_null_columns)
    result_columns = [e for e in result_columns if e not in ('ID', 'Year', 'Part I', 'created_at')]

    return result_columns

def fit_model(X_train, y_train, X_test, y_test):
    
    logreg = LogisticRegression()
    logreg.fit(X_train, y_train)
    
    return logreg


def get_feature_importance(fitted_model, model_features):
    w = fitted_model.coef_[0]
    feature_importance_df = pd.DataFrame(model_features, columns = ["feature"])
    feature_importance_df["importance"] = pow(math.e, w)
    feature_importance_df = feature_importance_df.sort_values(by = ["importance"], ascending=False) 
    
    return feature_importance_df

def addtime(df):
    a = datetime.datetime.now()
    timeadded_df = df.assign(created_at=a)

    return timeadded_df

def upload_df_to_db(df, table_name):
    connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=EDREXEI\EI;Database=testjawn;uid=Drexel;pwd=$4hEs@7F"
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

    engine = create_engine(connection_url)

    df.to_sql(table_name, engine, if_exists='append',index= False)

def get_years(filepath):

    #read data
    #cohort_df = read_data('merged_data.csv')
    #cohort_df = read_data('C:/Users/Drexel/Documents/datafolder/merged_data_with_new_course.csv')
    cohort_df = read_data(filepath)

    #clean it
    clean_cohort_df = clean_data(cohort_df)

    clean_cohort_df = convert_grades(clean_cohort_df)


    unique_values_year = clean_cohort_df.loc[clean_cohort_df['Part I'].notnull(), 'Year'].unique().astype(int)

    ###Return this list back to the user
    unique_values_year = unique_values_year.tolist()

    return unique_values_year, clean_cohort_df

#Temporary using 2022 as selected year. Replace 2022 with the selected years. 
### This should be returned to users

def get_unique_values(clean_cohort_df, user_selected_years):
    #columns = get_columns_with_no_nulls_and_values(clean_cohort_df, 'Year', [2022])

    user_selected_years = [int(i) for i in user_selected_years]

    # print(user_selected_years)
    # print(type(user_selected_years))
    columns = get_columns_with_no_nulls_and_values(clean_cohort_df, 'Year', user_selected_years)

    return columns

#removed first col / temporary solution. hard coded 
### Change this to be an input 

def filter_training_dataframe(clean_cohort_df, unique_values_year, selected_courses):    
    # removed_1_col = ['7101-FA1', '7103-FA1', '7105-FA1', '7106-FA1', '7400-FA1', '7503-FA1', '7505-FA1', '7701-FA1', 
                    #  '8630-FA1', '7130-SP1', '7405-SP1', '7406-SP1', '7407-SP1', '7408-SP1', '7504-SP1', '7506-SP1', '7600-SP1', 
                    #  '8631-SP1', '7131-SU2', '7340-SU2', '7409-SU2', '7410-SU2', '7601-SU2', '8632-SU2', '7109-FA2', '7140-FA2', 
                    #  '7341-FA2', '7402-FA2', '7404-FA2', '7500-FA2', '7507-FA2', '7602-FA2', '8530-FA2', '8635-FA2', '7141-SP2', 
                    #  '7232-SP2', '7350-SP2', '7414-SP2', '7603-SP2', '8500-SP2', '8531-SP2', '7320-SU3', '7342-SU3', '7351-SU3', 
                    #  '7424-SU3', '8532-SU3', '7300-FA3', '7301-FA3', '7321-FA3', '7343-FA3', '8501-FA3', '8636-FA3', '7509-SP3']

    unique_values_year = [int(i) for i in unique_values_year]
    
    #Filter the dataframe with selected year
    new_filtered_df = filter_dataframe(clean_cohort_df, 'Year', unique_values_year)

    filtered_col_df = new_filtered_df.loc[:, new_filtered_df.columns.isin(selected_courses)]

    id_year_df = new_filtered_df.iloc[0:, 0:2]

    part1_scores = new_filtered_df.iloc[:,-1:]

    final_df = pd.merge(id_year_df,filtered_col_df, how='left', right_index=True, left_index=True)

    training_df = pd.merge(final_df, part1_scores, how='right', right_index=True, left_index=True)

    return training_df

def create_test_dataframe(clean_cohort_df, selected_courses):
    testing_data = clean_cohort_df[clean_cohort_df['Part I'].isna()]
    testing_id_year_df = testing_data.iloc[0:, 0:2]
    testing_filtered_col_df = testing_data.loc[:, testing_data.columns.isin(selected_courses)]
    testing_df = pd.merge(testing_id_year_df,testing_filtered_col_df, how='left', right_index=True, left_index=True)
    
    return testing_df

def create_model(training_df, testing_df):
    training_df['Pass/Fail'] = np.where(training_df['Part I'] >= 300, 1, 0)
    X_train = training_df.drop(['Part I', 'Pass/Fail', 'Year'], axis= 1)
    y_train = training_df['Pass/Fail']
    IDfortest = testing_df.iloc[:, 0:2]
    X_test = testing_df.drop(['Year'], axis= 1)
    X_train = X_train.iloc[:, 1:]
    ID_df = IDfortest.reset_index(drop=True)
    X_test = X_test.iloc[:,1:]
    feature_names = X_test.columns
    sc = StandardScaler()

    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    
    return X_train, y_train, X_test, ID_df, feature_names

def fit_model(X_train, y_train):
    
    logreg = LogisticRegression()
    fitted_model = logreg.fit(X_train, y_train)
    
    return fitted_model

def predict_results(fitted_model, X_test, ID_df):
    y_pred = fitted_model.predict(X_test)
    
    y_pred_prob = fitted_model.predict_proba(X_test)
    
    pass_chance_array = []
    for x in y_pred_prob:
        value = "%.7f" % x[1]
        pass_chance_array.append(value)
    
    actual_prob = pd.DataFrame({'Predicted': y_pred, 'Probability': pass_chance_array})
    
    logresults = pd.merge(ID_df, actual_prob, left_index=True, right_index=True)
    logresults = addtime(logresults)
    upload_df_to_db(logresults, 'model_results')
    return logresults

def get_feature_importance(fitted_model, feature_names):
    w = fitted_model.coef_[0]
    feature_importance_df = pd.DataFrame(feature_names, columns = ["course_name"])
    feature_importance_df["importance"] = pow(math.e, w)
    feature_importance_df = feature_importance_df.sort_values(by = ["importance"], ascending=False) 
    feature_importance_df = addtime(feature_importance_df)
    upload_df_to_db(feature_importance_df, 'feature_importance')
    return feature_importance_df