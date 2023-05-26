import pandas as pd
import numpy as np
import math
import sqlalchemy
import pymssql
import pyodbc
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

#####CLEANING#######

# make sure to rename dataset
raw_df = pd.read_csv('C:/Users/Drexel/Documents/datafolder/raw_data_10_23_22.csv', header = 1)  

raw_df.head()

raw_df.columns

#Grab only columns that course grades and Exam Scores, drop gpa columns
filter = [col for col in raw_df if not col.startswith(('Term', 'Cum','Unnamed'))]

filtered_df = raw_df[filter]

#drop p/f classes
dropped_df = filtered_df.drop(columns=filtered_df.columns[(filtered_df == 'P').any()])

dropped_df.head()

# Letter Grade to Numerical Grade Defined by Salus's Optometry Program
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

mapped_df = dropped_df.replace(grade_dict)

mapped_df.head()

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
 
a = datetime.datetime.now()
final_df = final_df.assign(created_at=a)

conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=EDREXEI\EI;Database=testjawn;"                  "uid=Drexel;pwd=$4hEs@7F")

df = pd.read_sql_query('SELECT * FROM [testjawn].[dbo].[test_table1]', conn)

connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=EDREXEI\EI;Database=testjawn;uid=Drexel;pwd=$4hEs@7F"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

engine = create_engine(connection_url)

final_df.to_sql('training_data', engine, if_exists='append',index= False)

print(final_df)

##### LOGISTIC MODEL ######


log_df = final_df

log_df['Pass/Fail'] = np.where(log_df['Part I'] >= 300, 1, 0)

log_df

X = log_df.drop(['Part I', 'Pass/Fail', 'created_at'], axis= 1)
y = log_df['Pass/Fail']

feature_names = X.iloc[:, 1:].columns

#X = X.values
#y = y.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=44)

X_train = X_train.iloc[:, 1:]
IDfortest = X_test.iloc[:, 0:1]
X_test = X_test.iloc[:,1:]

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

pipe = make_pipeline(StandardScaler(), LogisticRegression())

pipe.fit(X_train, y_train)

pipe.score(X_test, y_test)

sc = StandardScaler()

X_train_scaled = sc.fit_transform(X_train)

X_test_scaled = sc.transform(X_test)

X_train_scaled

logreg = LogisticRegression()
logreg.fit(X_train_scaled, y_train)

y_pred = logreg.predict(X_test_scaled)
y_pred_prob = logreg.predict_proba(X_test_scaled)

pass_chance_array = []
for x in y_pred_prob:
    value = "%.7f" % x[1]
    pass_chance_array.append(value)


# print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, y_pred)
print(confusion_matrix)

y_test

y_pred

actualvspredict = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})

logresults = pd.merge(IDfortest, actualvspredict, left_index=True, right_index=True)

logresults['Probability'] = pass_chance_array

a = datetime.datetime.now()
logresults = logresults.assign(created_at=a)
print(logresults)

logresults.to_sql('model_results', engine, if_exists='append',index= False)

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

#FEATURE IMPORTANCE
w0 = logreg.intercept_[0]

w0

w = logreg.coef_[0]

feature_importance = pd.DataFrame(feature_names, columns = ["feature"])
feature_importance["importance"] = pow(math.e, w)
feature_importance = feature_importance.sort_values(by = ["importance"], ascending=False)

a = datetime.datetime.now()
feature_importance = feature_importance.assign(created_at=a)
print(feature_importance)

feature_importance.to_sql('feature_importance', engine, if_exists='append',index= False)
