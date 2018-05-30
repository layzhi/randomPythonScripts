'''
How do I use the pandas library to read data into Python?
How do I use the seaborn library to visualize data?
What is linear regression, and how does it work?
How do I train and interpret a linear regression model in scikit-learn?
What are some evaluation metrics for regression problems?
How do I choose which features to include in my model?
'''
import pandas as pd
import requests

# read CSV file directly from a URL and save the results
data = pd.read_csv('http://www-bcf.usc.edu/~gareth/ISL/Advertising.csv', index_col=0)

'''
DataFrame: rows and columns (like a spreadsheet)
Series: a single column
'''
displayFirstFiveRows = data.head()
displayLastFiveRows = data.tail()
checkShapeOfDataFrame = data.shape

'''
What are the features?

TV: advertising dollars spent on TV for a single product in a given market (in thousands of dollars)
Radio: advertising dollars spent on Radio
Newspaper: advertising dollars spent on Newspaper
What is the response?

Sales: sales of a single product in a given market (in thousands of items)
What else do we know?

Because the response variable is continuous, this is a regression problem.
There are 200 observations (represented by the rows), and each observation is a single market.
'''

#Visualizing data using seaborn
import matplotlib.pyplot as plt
import seaborn as sns
#visualize the relationship between the features and the response using scatterplots
sns.pairplot(data, x_vars=['TV', 'radio', 'newspaper'],y_vars='sales', size=7, aspect=0.7, kind='reg')
#plt.show() #in order to print with seaborn you need to import matplotlib

'''
Linear Regression
Pros: fast, no tuning required, well-understood
Cons: unlikely to produce something accurate
'''

# Preparing X and y using pandas
'''
scikit-learn expects X (feature matrix) and y (response vector) to be NumPy arrays
However, pandas is built on top of NumPy
Thus, X can be a pandas DataFrame and y can be a pandas Series!
'''

#create a Python list of feature names
featureCols = ['TV', 'radio', 'newspaper']
#use the list to select a subset of the original DataFrane
X = data[featureCols]
#or
X = data[['TV', 'radio', 'newspaper']]
firstFiveRows = X.head()
#check type and shape of X
typeOfX = type(X)
shapeOfX = X.shape
# print(typeOfX , ' ', shapeOfX)
y = data['sales']
#or
y = data.sales
firstFiveValueOfY = y.head()

#Splitting X and y into training and testing sets
from sklearn.model_selection import train_test_split
XTrain, XTest, yTrain, yTest, = train_test_split(X,y,random_state=1)

#default split is 75% for training and 25% for testing
# print(XTrain.shape)
# print(yTrain.shape)
# print(XTest.shape)
# print(yTest.shape)

'''
Linear regression in scikit-learn
'''

#import model
from sklearn.linear_model import LinearRegression
#instantiate 
linReg = LinearRegression()
#fit the model to the training data (Learn the coefficients)
linReg.fit(XTrain, yTrain)

'''
Interpreting Model Coefficients
'''
# print the intercept and coefficients
# print(linReg.intercept_)
# print(linReg.coef_)

# pair the feature names with the coefficients
pairNamesAndCoefficients = list(zip(featureCols, linReg.coef_))
# y = 2.88 + 0.0466 * TV + 0.179 * Radio + 0.00345 * Newspaper
# print(pairNamesAndCoefficients)

'''
How do we interpret the TV coefficient (0.0466)?

For a given amount of Radio and Newspaper ad spending, a "unit" increase in TV ad spending is associated with a 0.0466 "unit" increase in Sales.
Or more clearly: For a given amount of Radio and Newspaper ad spending, an additional $1,000 spent on TV ads is associated with an increase in sales of 46.6 items.
Important notes:

This is a statement of association, not causation.
If an increase in TV ad spending was associated with a decrease in sales, $\beta_1$ would be negative.
'''


'''
Making Predictions
'''
# making predictions on the testing set
yPred = linReg.predict(XTest)


'''
More evaluation metrics for regression
-Evaluation metrics for classification problems, such as accuracy, are not useful for regression problems. Instead, we need evaluation metrics designed for comparing continuous values.
'''

# define true and predicted response values
true = [100, 50, 30, 20]
pred = [90, 50, 50, 30]
# MEAN ABSOLUTE ERROR (MAE) is the mean of the absolute value of the error
from sklearn import metrics 
MAEData = metrics.mean_absolute_error(true, pred)

# Mean Squared Error (MSE) is the mean of the squared errors:
MSEData = metrics.mean_squared_error(true, pred)

# Root Mean Squared Error (RMSE) is the square root of the mean of the squared errors:
import numpy as np
RMSEData = np.sqrt(metrics.mean_squared_error(true, pred))

'''
MAE is the easiest to understand, because it's the average error.
MSE is more popular than MAE, because MSE "punishes" larger errors.
RMSE is even more popular than MSE, because RMSE is interpretable in the "y" units.
'''

# Computing the RMSE for our Sales predictions
salesRMSE = np.sqrt(metrics.mean_squared_error(yTest, yPred))

'''
Feature Selection

Does Newspaper "belong" in our model? In other words, does it improve the quality of our predictions?

Let's remove it from the model and check the RMSE!
'''

newFeatureCols = ['TV', 'radio']
# use the list to select a subset of the original DataFrame
newX = data[newFeatureCols]
# select a Series from the DataFrame
newy = data.sales
# split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(newX, newy, random_state = 1)
# fit the model to the training data (Learn the coefficients)
linreg = LinearRegression()
linreg.fit(X_train, y_train)
# make predictions on the testing set
y_pred = linreg.predict(X_test)
# compute the RMSE of our predictions
newPrediction = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
print(salesRMSE, '\n', newPrediction)

'''
The RMSE decreased when we removed Newspaper from the model. (Error is something we want to minimize, so a lower number for RMSE is better.) Thus, it is unlikely that this feature is useful for predicting Sales, and should be removed from the model.
'''

'''
More stuff to look into

- Linear Regression:
https://github.com/justmarkham/DAT5/blob/master/notebooks/09_linear_regression.ipynb
http://www-bcf.usc.edu/~gareth/ISL/
http://www.dataschool.io/15-hours-of-expert-machine-learning-videos/
http://www.dataschool.io/applying-and-interpreting-linear-regression/
http://people.duke.edu/~rnau/regintro.htm

- Pandas
http://www.gregreda.com/2013/10/26/intro-to-pandas-data-structures/
http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
'''
