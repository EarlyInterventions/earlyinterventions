import pandas as pd
import numpy as np
import math
import sqlalchemy
#import pymssql
#import pyodbc
import datetime 
import mysql
import mysql.connector
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

def addtime(df):
    a = datetime.datetime.now()
    timeadded_df = df.assign(created_at=a)

    return timeadded_df

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
    id_df = mapped_df.iloc[0:, 0:1]
    mapped_df.iloc[:, 1:].astype(float)
    float_df = mapped_df.iloc[:, 1:].astype(float)
    credit_hours_arr = float_df.iloc[0,0:-4].values
    part1_scores = float_df.iloc[:,-4:]
    float_df = float_df.iloc[:, 0:-4] * np.array(credit_hours_arr)
    final_df = pd.merge(id_df,float_df, how='left', right_index=True, left_index=True)
    final_df = pd.merge(final_df, part1_scores, how='right', right_index=True, left_index=True)
    final_df = final_df.iloc[1:]
    final_df = final_df.dropna(axis='columns')
    
    #add datetime to df
    a = datetime.datetime.now()
    final_df = final_df.assign(created_at=a)
    
    return final_df

def upload_df_to_db(df, table_name):
    connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=EDREXEI\EI;Database=testjawn;uid=Drexel;pwd=$4hEs@7F"
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

    engine = create_engine(connection_url)

    df.to_sql(table_name, engine, if_exists='append',index= False)

def get_feature_importance(fitted_model, model_features):
    w = fitted_model.coef_[0]
    feature_importance_df = pd.DataFrame(model_features, columns = ["features"])
    feature_importance_df["importance"] = pow(math.e, w)
    feature_importance_df = feature_importance_df.sort_values(by = ["importance"], ascending=False)
    feature_importance_df = addtime(feature_importance_df)
    upload_df_to_db(feature_importance_df, 'feature_importance')

#read data
cohort2022_df = read_data('C:/Users/Drexel/Documents/datafolder/Drexel Copy - ODT 2022.csv')

#read data
cohort2023_df = read_data('C:/Users/Drexel/Documents/datafolder/Drexel Copy - ODT 2023.csv')

#clean it
clean_cohort2022_df = clean_data(cohort2022_df)

#clean it
clean_cohort2023_df = clean_data(cohort2023_df)

#Convert grades
clean_cohort2022_df = convert_grades(clean_cohort2022_df)

#Convert grades
clean_cohort2023_df = convert_grades(clean_cohort2023_df)

#Create a boolean for whether they pass or fail in 2022
clean_cohort2022_df['Pass/Fail'] = np.where(clean_cohort2022_df['Part I'] >= 300, 1, 0)

#Set all features in 2022 cohort as X_train 
X_train = clean_cohort2022_df.drop(['Part I', 'Pass/Fail', 'created_at'], axis= 1)

#Set pass/fail as the y_train
y_train = clean_cohort2022_df['Pass/Fail']

#Create a boolean for whether they pass or fail in 2023
clean_cohort2023_df['Pass/Fail'] = np.where(clean_cohort2023_df['Part I'] >= 300, 1, 0)

#Set all features in 2023 cohort as X_test 
X_test = clean_cohort2023_df.drop(['Part I', 'Pass/Fail', 'created_at'], axis= 1)

#Set pass/fail as the y_test
y_test = clean_cohort2023_df['Pass/Fail']

#Drop the id column for X_train for model fitting
X_train = X_train.iloc[:, 1:]

#Create a df that contains only ids of X_test
IDfortest = X_test.iloc[:, 0:1]

#Drop the id column for X_test for model fitting
X_test = X_test.iloc[:,1:]

#Create a list of all the features
feature_names = X_test.columns

#THIS COLUMN I WILL DROP IN ORDER TO MAKE THINGS KINDA WORK !! 
X_train.columns.difference(X_test.columns).tolist()

#DROPPING THIS BECAUSE IT'S MISSING IN X_TEST
X_train = X_train.drop(['7710'], axis=1)

#RUN THE MODEL
sc = StandardScaler()

X_train_scaled = sc.fit_transform(X_train)
X_test_scaled = sc.transform(X_test)

logreg = LogisticRegression()
logreg.fit(X_train_scaled, y_train)

y_pred = logreg.predict(X_test_scaled)

#Get the probablity of the value being true
y_pred_prob = logreg.predict_proba(X_test_scaled)

#Convert the probablity to something readible 
pass_chance_array = []
for x in y_pred_prob:
    value = "%.7f" % x[1]
    pass_chance_array.append(value)

#Look at the confusion matrix
from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, y_pred)
print(confusion_matrix)

#Create a dataframe to see actual vs predicted
actualvspredict = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})

#Create a dataframe to see actual vs predicted
logresults = pd.merge(IDfortest, actualvspredict, left_index=True, right_index=True)

#Add the probability of getting a 1 
logresults['Probability'] = pass_chance_array

#
logresults = addtime(logresults)

print(logresults)   

upload_df_to_db(logresults, 'model_results')

#See our accuracy, recall, precision, and f1 score
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

#Run the get_feature_importance function
#get_feature_importance(logreg, feature_names)

w0 = logreg.intercept_[0]
w0
w = logreg.coef_[0]
feature_importance = pd.DataFrame(feature_names, columns = ["feature"])
feature_importance["importance"] = pow(math.e, w)
feature_importance = feature_importance.sort_values(by = ["importance"], ascending=False)
feature_importance = addtime(feature_importance)
print(feature_importance)
connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=EDREXEI\EI;Database=testjawn;uid=Drexel;pwd=$4hEs@7F"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)
feature_importance.to_sql('feature_importance', engine, if_exists='append',index= False)
