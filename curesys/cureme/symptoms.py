import joblib
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, classification_report, precision_score, roc_curve
# import plot_confusion_matrix
from sklearn.metrics import RocCurveDisplay
import seaborn as sns
from sklearn.utils import shuffle
# from pandas_profiling import ProfileReport
from sklearn.linear_model import LogisticRegression, Perceptron, RidgeClassifier, SGDClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.ensemble import BaggingClassifier, AdaBoostClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

df = pd.read_csv(r'D:\notebook\notebook\dataset.csv')
df = shuffle(df, random_state=42)
df.head()
# print(df.head())

for col in df.columns:

    df[col] = df[col].str.replace('_', ' ')
# print(df.head())
# print(df.describe())

# Check for null and NaN values

null_checker = df.apply(lambda x: sum(x.isnull())).to_frame(name="count")
# print(null_checker)

plt.figure(figsize=(10, 5))
plt.plot(null_checker.index, null_checker['count'])
plt.xticks(null_checker.index, rotation=45, horizontalalignment='right')
plt.title('Before removing Null values')
plt.xlabel('column names')
plt.margins(0.1)
# plt.show() ####################
# Remove the trailing space from the symptom columns
# print(df.head())
cols = df.columns
# print(cols)
data = df[cols].values.flatten()
# print("dataSWKEJFGHWE", data)
s = pd.Series(data)
# print(s)
s = s.str.strip()
# if there were any unwanted spaces before or after a symptom name, they would be removed
# creates a two-dimensional array with rows and columns
s = s.values.reshape(df.shape)
# print(s)
# df that contains the cleaned data from the NumPy array s. The column names of df will match those of the original DataFrame
df = pd.DataFrame(s, columns=df.columns)
# print(df.head())
# trailing whitespaces have been removed in the new df
df = df.fillna(0)
# print(df.head())
# filled na values with '0'
# SYMPTOMS SEVERITY WITH RANKS
df1 = pd.read_csv(r'D:\notebook\notebook\Symptom-severity.csv')
df1['Symptom'] = df1['Symptom'].str.replace("_", " ")
# print(df1.head())
# get list of symptoms which are unique
# print(df1['Symptom'].unique())
# print("df valuesssssss" ,df.values)
vals = df.values  # extracts vals from values of df
symptoms = df1["Symptom"].unique()
# identifies vals matching with symptoms in df1 and assigns the severity rank to them
for i in range(len(symptoms)):
    vals[vals == symptoms[i]] = df1[df1['Symptom']
                                    == symptoms[i]]['weight'].values[0]


d = pd.DataFrame(vals, columns=cols)

d = d.replace('dischromic  patches', 0)
d = d.replace('spotting  urination', 0)
df = d.replace('foul smell of urine', 0)
# print(df.head(10))

null_checker = df.apply(lambda x: sum(x.isnull())).to_frame(name='count')
# print(null_checker)

##
plt.figure(figsize=(10, 5))
plt.plot(null_checker.index, null_checker['count'])
plt.xticks(null_checker.index, rotation=45, horizontalalignment='right')
plt.title('After removing Null values')
plt.xlabel('column names')
plt.margins(0.01)
# plt.show()

# print("no of symptoms used in total to identity the diseases", len(df1['Symptom'].unique()))
# print("no of diseases to be identified", len(df['Disease'].unique()))

# print(df)
data = df.iloc[:, 1:].values
# print(data)
labels = df['Disease'].values
# ALLOTTING TRAINING AND TESTING DATA TO x_train, x_test, y_train, y_test
# 80 PERCENT FOR TRAINING AND 20 FOR TESTING
# USING train_test_split
x_train, x_test, y_train, y_test = train_test_split(
    data, labels, train_size=0.8, random_state=42)
# print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
##
tree = DecisionTreeClassifier(criterion='gini', random_state=42, max_depth=13)
tree.fit(x_train, y_train)
# make preds
preds = tree.predict(x_test)
# print(preds)
##
conf_mat = confusion_matrix(y_test, preds)
# print(conf_mat)
# plt.figure(figsize=(8, 6))
# plt.imshow(conf_mat, interpolation='nearest', cmap=plt.cm.Blues)
# plt.title('Confusion Matrix')
# plt.colorbar()

# classes = ['Negative', 'Positive']  # Define class labels
# tick_marks = range(len(classes))
# plt.xticks(tick_marks, classes)
# plt.yticks(tick_marks, classes)

# for i in range(len(classes)):
#     for j in range(len(classes)):
#         plt.text(j, i, str(conf_mat[i][j]), horizontalalignment='center', verticalalignment='center')

# plt.xlabel('Predicted Label')
# plt.ylabel('Actual Label')
# plt.show()
##
df_cm = pd.DataFrame(conf_mat, index=df['Disease'].unique(),
                     columns=df['Disease'].unique())

# print('F1-score% =', f1_score(y_test, preds, average='macro')*100, '|', 'Accuracy% = ', accuracy_score(y_test, preds)*100)
sns.heatmap(df_cm)
# Random Forest classifier using k-fold cross-validation
kfold = KFold(n_splits=10, shuffle=True, random_state=42)
DS_train = cross_val_score(tree, x_train, y_train,
                           cv=kfold, scoring='accuracy')
pd.DataFrame(DS_train, columns=['Scores'])
# print("Mean Accuracy: %.3f%%, Standard Deviation: (%.2f%%)" % (DS_train.mean()*100.0, DS_train.std()*100.0))
kfold = KFold(n_splits=10, shuffle=True, random_state=42)
DS_test = cross_val_score(tree, x_test, y_test, cv=kfold, scoring='accuracy')
pd.DataFrame(DS_test, columns=['Scores'])
# print("Mean Accuracy: %.3f%%, Standard Deviation: (%.2f%%)" % (DS_test.mean()*100.0, DS_test.std()*100.0))
##
kfold = KFold(n_splits=10, shuffle=True, random_state=42)
DS_test = cross_val_score(tree, x_test, y_test, cv=kfold, scoring='accuracy')
pd.DataFrame(DS_test, columns=['Scores'])
# print("Mean Accuracy: %.3f%%, Standard Deviation: (%.2f%%)" % (DS_test.mean()*100.0, DS_test.std()*100.0))
##
rfc = RandomForestClassifier(random_state=42)
rnd_forest = RandomForestClassifier(
    random_state=42, max_features='sqrt', n_estimators=500, max_depth=13)
rnd_forest.fit(x_train, y_train)
preds = rnd_forest.predict(x_test)
print(x_test[0])
print(preds[0])
conf_mat = confusion_matrix(y_test, preds)
df_cm = pd.DataFrame(
    conf_mat, index=df['Disease'].unique(), columns=df['Disease'].unique())
# print('F1-score% =', f1_score(y_test, preds, average='macro')*100, '|', 'Accuracy% =', accuracy_score(y_test, preds)*100)
sns.heatmap(df_cm)
##
kfold = KFold(n_splits=10, shuffle=True, random_state=42)
rnd_forest_train = cross_val_score(
    rnd_forest, x_train, y_train, cv=kfold, scoring='accuracy')
pd.DataFrame(rnd_forest_train, columns=['Scores'])
# print("Mean Accuracy: %.3f%%, Standard Deviation: (%.2f%%)" % (rnd_forest_train.mean()*100.0, rnd_forest_train.std()*100.0))
##
kfold = KFold(n_splits=10, shuffle=True, random_state=42)
rnd_forest_test = cross_val_score(
    rnd_forest, x_test, y_test, cv=kfold, scoring='accuracy')
pd.DataFrame(rnd_forest_test, columns=['Scores'])
# print("Mean Accuracy: %.3f%%, Standard Deviation: (%.2f%%)" % (rnd_forest_test.mean()*100.0, rnd_forest_test.std()*100.0))
##
discrp = pd.read_csv(
    r'D:\notebook\notebook\symptom_Description.csv') 
ektra7at = pd.read_csv(
    r'D:\notebook\notebook\symptom_precaution.csv')

# # save
# joblib.dump(rfc, r'C:\Users\91707\Desktop\notebook\random_forest.joblib')
# loaded_rf = joblib.load(
#     r'C:\Users\91707\Desktop\notebook\random_forest.joblib')
# ##


def predd(model, *symptoms):
    # Assuming df1 is your DataFrame with Symptom and weight columns
    a = np.array(df1["Symptom"])
    b = np.array(df1["weight"])

    # Convert symptoms to numeric values using the mapping logic
    numeric_symptoms = [symptom if symptom not in a else b[np.where(
        a == symptom)][0] for symptom in symptoms]

    psy = [numeric_symptoms]

    # Make a prediction
    prediction = model.predict(psy)
    
    # Disease Description
    disp = discrp[discrp['Disease'] == prediction[0]].values[0][1]

    # Precautionary measures
    precautions = ektra7at[ektra7at['Disease'] ==
                           prediction[0]].iloc[:, 1:].values.tolist()

    # Recommended Doctor
    recommended_doctor = ""

    # Conditional recommendations based on predicted disease
    if prediction[0] == 'Impetigo':
        recommended_doctor = "Dermatologist - Dr. Smith"
    elif prediction[0] == 'Malaria':
        recommended_doctor = "Infectious Disease Specialist - Dr. Johnson"
    elif prediction[0] == 'Typhoid':
        recommended_doctor = "Gastroenterologist - Dr. Williams"
    elif prediction[0] == 'Jaundice':
        recommended_doctor = "Hepatologist - Dr. Brown"
    elif prediction[0] == 'Hepatitis C':
        recommended_doctor = "Gastroenterologist - Dr. Wilson"

    # Constructing result with disease description, precautions, and doctor recommendation
    result = [
        # f"The Disease Name: {prediction[0]}",
        # f"The Disease Description: {disp}",
        "Recommended Things to do at home:"
    ]
    result.extend(precautions)
    # result.append(f"Probability of the Disease: {probability_percentage:.2f}%")
    result.append(f"Recommended Doctor: GASTROENTROLOGIST")

    return result


a = np.array(df1["Symptom"])
b = np.array(df1["weight"])
# Convert symptoms to numeric values using the mapping logic
numeric_symptoms = [symptom if symptom not in a else b[np.where(
    a == symptom)][0] for symptom in symptoms]

psy = [numeric_symptoms]

##
n_groups = 2
algorithms = ('Decision Tree', 'Random Forest')
train_accuracy = (DS_train.mean()*100.0,
                  rnd_forest_train.mean()*100.0,)
test_accuracy = (DS_test.mean()*100.0,
                 rnd_forest_test.mean()*100.0)
Standard_Deviation = (DS_test.std()*100.0,
                      rnd_forest_test.std()*100.0)
##
# create plot git commit -m "Initial commit of my project"
#https://github.com/kvzuifx/curatio-curing-
fig, ax = plt.subplots(figsize=(15, 10))
index = np.arange(n_groups)
bar_width = 0.3
opacity = 1
rects1 = plt.bar(index, train_accuracy, bar_width,
                 alpha=opacity, color='Cornflowerblue', label='Train')
rects2 = plt.bar(index + bar_width, test_accuracy, bar_width,
                 alpha=opacity, color='Teal', label='Test')
rects3 = plt.bar(index + bar_width, Standard_Deviation, bar_width,
                 alpha=opacity, color='red', label='Standard Deviation')
plt.xlabel('Algorithm')  # x axis label
plt.ylabel('Accuracy (%)')  # y axis label
plt.ylim(0, 115)
plt.title('Comparison of Algorithm Accuracies')  # plot title
plt.xticks(index + bar_width * 0.5, algorithms)  # x axis data labels
plt.legend(loc='upper right')  # show legend
for index, data in enumerate(train_accuracy):
    plt.text(x=index - 0.035, y=data + 1,
             s=round(data, 2), fontdict=dict(fontsize=8))
for index, data in enumerate(test_accuracy):
    plt.text(x=index + 0.25, y=data + 1,
             s=round(data, 2), fontdict=dict(fontsize=8))
for index, data in enumerate(Standard_Deviation):
    plt.text(x=index + 0.25, y=data + 1,
             s=round(data, 2), fontdict=dict(fontsize=8))
    ##
# plt.show()
sympList = df1["Symptom"].to_list()
# predd(rnd_forest,sympList[7],sympList[5],sympList[2],sympList[80],0,0,0,0,0,0,0,0,0,0,0,0,0)
num_symptoms = len(sympList)
# print("Number of symptoms:", num_symptoms)
# print(sympList)
# print(sympList[7])
# print("   break  ", sympList)
