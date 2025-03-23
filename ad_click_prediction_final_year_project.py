# -*- coding: utf-8 -*-
"""Ad Click Prediction Final Year Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1D-q-oHQJDoKpm1fLm37Nd-UecxuNEn1y

# **Ad Click Prediction**

# **Goal of the Project**

Goal of the project is to find the accuracy of Model if a particular user is likely to click on particular ad or not based on his feature.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import io
from google.colab import files
uploaded = files.upload()
dataframe = pd.read_csv(io.StringIO(uploaded['advertising.csv'].decode('utf-8')))

dataframe

dataframe.info()

"""## **Are there any duplicate records present?**"""

dataframe.duplicated().sum()

"""As the value above is zero, there are no duplicates.

# Attribute Type Classification

## Determing the type of attributes in the given dataset
"""

numeric_columns = ['Daily Time Spent on Site', 'Age', 'Area Income', 'Daily Internet Usage' ]

categorical_columns = ['Gender', 'Clicked on Ad' ]

"""# Exploratory Data Analysis

## What age group does the dataset majorly consist of?
"""

plt.figure(figsize=(10,7))
sns.displot(data=dataframe, x='Age', bins=20, kde=True, edgecolor="k", linewidth=1)

"""Here, we can see that most of the internet users are having age in the range of 26 to 42 years."""

print('Age of the oldest person:', dataframe['Age'].max(), 'Years')
print('Age of the youngest person:', dataframe['Age'].min(), 'Years')
print('Average age in dataset:', dataframe['Age'].mean(), 'Years')

"""## What is the income distribution in different age groups?"""

sns.jointplot(x='Age', y='Area Income', color= "green", data= dataframe)

"""Here, we can see that mostly teenagers are higher earners with age group of 20-40 earning 50k-70k.

## Which age group is spending maximum time on the internet?
"""

sns.jointplot(x='Age', y='Daily Time Spent on Site', data= dataframe)

"""From the above plot its evident that the age group of 25-40 is most active on the internet.

## Which gender has clicked more on online ads?
"""

dataframe.groupby(['Gender','Clicked on Ad'])['Clicked on Ad'].count().unstack()

"""Based on above data we can see that a greater number of females have clicked on ads compared to male.

## **Maximum number of internet users belong to which country in the given dataset?**
"""

pd.crosstab(index=dataframe['Country'],columns='count').sort_values(['count'], ascending=False)

"""Based on the above data frame we can observe that maximum number of users are from France and Czech.

# What is the relationship between different features?
"""

sns.pairplot(dataframe, hue='Clicked on Ad')

"""# Data Cleaning"""

sns.heatmap(dataframe.isnull(), yticklabels=False)

"""As we see, we don't have any missing data

Considering the 'Advertisement Topic Line', we decided to drop it. In any case, if we need to extract any form of interesting data from it

As to 'City' and the 'Nation', we can supplant them by dummy variables with numerical features, Nonetheless, along these lines we got such a large number of new highlights.

Another methodology would be thinking about them as a **categorical** features and coding them in one numeric element, conversion into **categorical data type**

The numerical codes corresponding to each unique category in the categorical 'City' column. The codes are assigned based on the order in which the unique values appear in the column.

Changing 'Timestamp' into numerical value is more complicated. So, we can change ‘Timestamp’ to numbers or convert them to spaces of time/day and consider it to be categorical and afterwards we converted it into numerical values. And we selected the month and the hour from the timestamp as features
"""

dataframe['City Codes']= dataframe['City'].astype('category').cat.codes

dataframe['Country Codes'] = dataframe['Country'].astype('category').cat.codes

dataframe[['City Codes','Country Codes']].head(5)

dataframe['Month'] = dataframe['Timestamp'].apply(lambda x: x.split('-')[1])
dataframe['Hour'] = dataframe['Timestamp'].apply(lambda x: x.split(':')[0].split(' ')[1])

dataframe[['Month','Hour']].head(5)

"""# Data Model Implementation

Dropping
"""

X = dataframe.drop(labels=['Ad Topic Line','City','Country','Timestamp','Clicked on Ad'], axis=1)

Y = dataframe['Clicked on Ad']

"""**Splitting Dataset**"""

from sklearn.model_selection import train_test_split

X= pd.get_dummies(X)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state = 42)

"""**Implementing Naive Bayes Model**"""

from sklearn.naive_bayes import GaussianNB

nav_bayes_model = GaussianNB()

nav_bayes_model.fit(X_train, Y_train)

nav_bayes_pred = nav_bayes_model.predict(X_test)

"""**Implementing Decision Tree Model**"""

from sklearn.tree import DecisionTreeClassifier

dec_tree_model = DecisionTreeClassifier()

dec_tree_model.fit(X_train, Y_train)

dec_tree_pred = dec_tree_model.predict(X_test)

"""**Implementing K-Nearest Neighbours Model**"""

from sklearn.neighbors import KNeighborsClassifier

knn_model = KNeighborsClassifier()

knn_model.fit(X_train, Y_train)

knn_pred = knn_model.predict(X_test)

"""# **Confusion Matrix** for Finding the incorrect and correct predictions"""

from sklearn.metrics import confusion_matrix

cmn = confusion_matrix(Y_test, nav_bayes_pred)

cmd = confusion_matrix(Y_test, dec_tree_pred)

cmk = confusion_matrix(Y_test, knn_pred)

""" Assuming the class names are binary: 0 (Not Clicked), 1 (Clicked)"""

class_names = [0, 1]

"""# Plot confusion matrix for Navie Bayes"""

print(cmn)
sns.heatmap(cmn, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix - Naive Bayes')
plt.show()

"""# Plot confusion matrix for Decision Tree"""

print(cmd)
sns.heatmap(cmd, annot=True, fmt='d', cmap='Greens', xticklabels=class_names, yticklabels=class_names)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix - Decision Tree')
plt.show()

"""# Plot confusion matrix for KNN"""

print(cmk)
sns.heatmap(cmk, annot=True, fmt='d', cmap='Oranges', xticklabels=class_names, yticklabels=class_names)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix - KNN')
plt.show()

"""**Finding accuracy in each model**"""

from sklearn.metrics import accuracy_score

"""### Naive Bayes"""

nav_bayes_accuracy = accuracy_score(nav_bayes_pred, Y_test)
print(nav_bayes_accuracy*100)

"""## Decision Tree"""

dec_tree_accuracy = accuracy_score(dec_tree_pred, Y_test)
print(dec_tree_accuracy*100);

"""## KNN Model"""

knn_accuracy = accuracy_score(knn_pred, Y_test)
print(knn_accuracy*100);

"""##Compute **ROC curve** and **ROC area** for each model"""

from sklearn.metrics import precision_score, recall_score, roc_curve, roc_auc_score

nav_bayes_fpr, nav_bayes_tpr, _ = roc_curve(Y_test, nav_bayes_pred)
nav_bayes_auc = roc_auc_score(Y_test, nav_bayes_pred)

dec_tree_fpr, dec_tree_tpr, _ = roc_curve(Y_test, dec_tree_pred)
dec_tree_auc = roc_auc_score(Y_test, dec_tree_pred)

knn_fpr, knn_tpr, _ = roc_curve(Y_test, knn_pred)
knn_auc = roc_auc_score(Y_test, knn_pred)

plt.plot(nav_bayes_fpr, nav_bayes_tpr, label=f'Naive Bayes (AUC = {nav_bayes_auc:.2f})')
plt.plot(dec_tree_fpr, dec_tree_tpr, label=f'Decision Tree (AUC = {dec_tree_auc:.2f})')
plt.plot(knn_fpr, knn_tpr, label=f'KNN (AUC = {knn_auc:.2f})')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()

"""# Compute F1 score for each model"""

from sklearn.metrics import f1_score

nav_bayes_pred_labels = (nav_bayes_pred >= 0.5).astype(int)
dec_tree_pred_labels = (dec_tree_pred >= 0.5).astype(int)
knn_pred_labels = (knn_pred >= 0.5).astype(int)


nav_bayes_f1 = f1_score(Y_test, nav_bayes_pred_labels)
dec_tree_f1 = f1_score(Y_test, dec_tree_pred_labels)
knn_f1 = f1_score(Y_test, knn_pred_labels)

print("F1 Score for Naive Bayes:", nav_bayes_f1)
print("F1 Score for Decision Tree:", dec_tree_f1)
print("F1 Score for KNN:", knn_f1)

"""### Checking of overfitting of Dataset"""

from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB

"""Extract features and target variable"""

x = dataframe.drop('Clicked on Ad', axis=1)
y = dataframe['Clicked on Ad']

nb_model = GaussianNB()

"""# Perform cross-validation"""

X_encoded = pd.get_dummies(x)
scores = cross_val_score(nb_model, X_encoded, y, cv=5)  # Use 5-fold cross-validation
print("Mean CV Score:", scores.mean())

from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt

train_sizes, train_scores, test_scores = learning_curve(nb_model, X_encoded, y, cv=25, train_sizes=np.linspace(.1, 1.0, 5))

# Calculate mean and standard deviation of training and test scores
train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)

# Plot learning curves
plt.plot(train_sizes, train_mean, label='Training score')
plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1)
plt.plot(train_sizes, test_mean, label='Cross-validation score')
plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.1)
plt.xlabel('Number of samples')
plt.ylabel('Accuracy')
plt.title('Learning Curves')
plt.legend()
plt.show()

"""# Conclusion

### After comparing all the above implementation models, we conclude that Naive Bayes Algorithm gives us the maximum accuracy for determining the click  probability. We believe in future there will be fewer ads, but they will be more relevant. And also these ads will cost more and will be worth it.
"""