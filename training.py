import pandas as pd
import os
import shutil

import warnings
warnings.filterwarnings("ignore")

from deltalake import DeltaTable
from deltalake.writer import write_deltalake

df = pd.read_csv('./loan.csv')

DELTA_LAKE_TABLE = "loans.delta"
if os.path.exists(DELTA_LAKE_TABLE):
    shutil.rmtree(DELTA_LAKE_TABLE, ignore_errors=False, onerror=None)
write_deltalake(DELTA_LAKE_TABLE, df, overwrite_schema=True)
dt = DeltaTable(DELTA_LAKE_TABLE)
print(dt.version())

# Remove columns which missing values > 70%
df_1 = df.dropna(axis=1, thresh=int(0.70*len(df)))

print(
    'The number of columns has reduced from {} to {} columns by removing columns with 70% missing values'.
    format(len(df.columns), len(df_1.columns))
)

selected_loan_status = ['Fully Paid', 'Charged Off', 'Default']
df_2 = df_1[df_1.loan_status.isin(selected_loan_status)]
df_2.loan_status = df_2.loan_status.replace({'Fully Paid' : 'Good Loan'})
df_2.loan_status = df_2.loan_status.replace({'Charged Off' : 'Bad Loan'})
df_2.loan_status = df_2.loan_status.replace({'Default' : 'Bad Loan'})

print(
    'The number of rows has been reduced from {:,.0f} to {:,.0f} by filtering the data with the correlated loan status'.
    format(len(df_1), len(df_2))     
)

write_deltalake(DELTA_LAKE_TABLE, df_2, mode='overwrite', overwrite_schema=True)
dt = DeltaTable(DELTA_LAKE_TABLE)
print(dt.version())


dt.load_version(0)
df_3 = dt.to_pandas()

print(len(df_3.columns))
print(len(df_3))

dt.load_version(1)
df_2 = dt.to_pandas()
print(len(df_2.columns))
print(len(df_2))


df_3 = df_2[[
    'loan_status', 'term','int_rate',
    'installment','grade', 'annual_inc',
    'verification_status','dti'  # These features are just initial guess, you can try to choose any other combination
]]
df_3.head()

# Find missing values in the chosen columns
df_null = pd.DataFrame({'Count': df_3.isnull().sum(), 'Percent': round(100*df_3.isnull().sum()/len(df_3),2)})
df_null[df_null['Count'] != 0]

# Dropping rows with null values
df_clean = df_3.dropna(axis = 0)

print('Number of dropped rows: {} rows'.format(len(df_3)-len(df_clean)))


df_4 = df_2
# The next step is to transform categorical target variable into integer
df_clean.loan_status = df_clean.loan_status.replace({'Good Loan' : 1})
df_clean.loan_status = df_clean.loan_status.replace({'Bad Loan' : 0})
df_clean.loan_status.unique()

df_4.loan_status = df_4.loan_status.replace({'Good Loan' : 1})
df_4.loan_status = df_4.loan_status.replace({'Bad Loan' : 0})

df_4.columns.to_series().groupby(df_clean.dtypes).groups

# First, dropping categorical features (object type) which have too many options available
df_4 = df_4.drop(['emp_title', 'sub_grade', 'issue_d', 'last_pymnt_d', 'last_credit_pull_d', 'hardship_flag', 'debt_settlement_flag'], axis=1, errors='ignore')

# Second, to filter numerical features, we can use .corr() function to select only features with high correlation to the target variable
df_4.corr()['loan_status']

df_clean = df_4[[
    'loan_status', # target variable
    # features (object):
    'term', 'grade','home_ownership', 'verification_status', 'pymnt_plan', 'purpose', 
    'initial_list_status', 'application_type', 'int_rate',
    # features (int/float):
    'total_pymnt', 'total_pymnt_inv', 'total_rec_prncp', 'recoveries',                   
    'collection_recovery_fee', 'last_pymnt_amnt'
]]

df_null = pd.DataFrame({'Count': df_clean.isnull().sum(), 'Percent': round(100*df_clean.isnull().sum()/len(df_clean),2)})
df_null[df_null['Count'] != 0] 

from sklearn.preprocessing import LabelEncoder
label = LabelEncoder()

print(df_clean)
df_clean['term'] = label.fit_transform(df_clean['term'])
df_clean['grade'] = label.fit_transform(df_clean['grade'])
# df_clean['emp_length'] = label.fit_transform(df_clean['emp_length'])
df_clean['home_ownership'] = label.fit_transform(df_clean['home_ownership'])
df_clean['verification_status'] = label.fit_transform(df_clean['verification_status'])
df_clean['pymnt_plan'] = label.fit_transform(df_clean['pymnt_plan'])
df_clean['purpose'] = label.fit_transform(df_clean['purpose'])
df_clean['initial_list_status'] = label.fit_transform(df_clean['initial_list_status'])
df_clean['application_type'] = label.fit_transform(df_clean['application_type'])
df_clean['int_rate'] = label.fit_transform(df_clean['int_rate'])
df_clean['total_pymnt'] = label.fit_transform(df_clean['total_pymnt'])
df_clean['total_pymnt_inv'] = label.fit_transform(df_clean['total_pymnt_inv'])
df_clean['total_rec_prncp'] = label.fit_transform(df_clean['total_rec_prncp'])
df_clean['recoveries']= label.fit_transform(df_clean['recoveries'])
df_clean['collection_recovery_fee']= label.fit_transform(df_clean['collection_recovery_fee'])
df_clean['last_pymnt_amnt']= label.fit_transform(df_clean['last_pymnt_amnt'])

df_clean.head()

x = df_clean.drop(['loan_status'], axis=1)
y = df_clean['loan_status']

x.head()

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import numpy as np 
import matplotlib.pyplot as plt


coltrans = ColumnTransformer(
    [('one_hot_encoder', OneHotEncoder(categories='auto'), [0,1,2,3,4,5,6,7,8])],        
    remainder = 'passthrough'                               
)                                                         

#x = np.array(coltrans.fit_transform(x))

from sklearn.model_selection import train_test_split
xtr, xts, ytr, yts = train_test_split(
    x,
    y,
    test_size = .2,
)

from sklearn.ensemble import RandomForestClassifier
import time

start = time.time()

model = RandomForestClassifier()
model.fit(xtr, ytr)

stop = time.time()
duration = stop-start
print('The training took {:.2f} seconds.'.format(duration))

print(round(model.score(xts, yts) * 100, 2), '%')
y_pred = model.predict(xts)

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(yts, y_pred)

from sklearn.metrics import ConfusionMatrixDisplay
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                               display_labels=model.classes_)
disp.plot()
plt.show()
plt.savefig('cm.png')


pd.crosstab(yts, y_pred, rownames=['Actual'], colnames=['Predicted'], margins=True)

from sklearn.metrics import classification_report

target_names = ['Bad Loan', 'Good Loan']
print(classification_report(yts, model.predict(xts), target_names=target_names))

import sklearn.metrics as metrics

# calculate the fpr and tpr for all thresholds of the classification
probs = model.predict_proba(xts)
preds = probs[:,1]

fpr, tpr, threshold = metrics.roc_curve(yts, y_pred)
roc_auc = metrics.auc(fpr, tpr)

# Plotting the ROC curve
plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
plt.savefig('roc.png')

import pickle
pickle.dump(model, open("model.pkl", 'wb'))

loaded_model = pickle.load(open("model.pkl", 'rb'))
print(round(loaded_model.score(xts, yts) * 100, 2), '%')

