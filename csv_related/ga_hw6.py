'''
Supervised Learning (aka "predictive modeling")
- PRedict an outcome based on input data
- Example: predict whether an email is spam or ham
- Goal is to generalize
'''

#two categories of supervised learning:
# Regression
# - outcome we are tring to predict is continuious
# - Examples: price, blood pressure

# Classification
# - Outcome we are trying to predict is categorical (values in a finite set)
# - Examples: spam/ham, cancer class tissue sample

'''
Panda with IMDb data
'''

'''
Basic Level
'''

import pandas as pd
import matplotlib.pyplot as plt

#read in 'imdb_1000.csv' and store it in a DataFrame named movies
movies = pd.read_csv('imdb_1000.csv')

#check the number of rows and columns
moviesShape = movies.shape

#check the data type of each column
moviesDtype = movies.dtypes

#calculate the average movie duration
moviesDuration = movies.duration.mean()

#sort the DataFrame by duration to find the shortest and longest movies
durationShortest = movies.sort_values('duration').head(1) #shortest
durationLongest = movies.sort_values('duration').tail(1) #longest

#create a histogram of duration, choosing an "appropriate" number of bins
moviesDurationHistogram = movies.duration.plot(kind='hist', bins=20)
#plt.show()

#use a box plot to displa the same data
boxPlotOfDurationHist = movies.duration.plot(kind='box')
#plt.show()

'''
Intermediate Level
'''

#count how many movies have each of the content ratings
countOfMoviesWithContentRating = movies.content_rating.value_counts()

#use a visualiztion to display that same data, including a title and x and y labels
movies.content_rating.value_counts().plot(kind='bar', title='Top 1000 Movies')
plt.xlabel('Content Rating')
plt.ylabel('Number of Movies')
#plt.show()

#convert the following content rating to "UNRATED": NOT RATED, APPROVED, PASSED, GP
movies.content_rating.replace(['NOT RATED', 'APPROVED', 'PASSED', 'GP'], 'UNRATED', inplace=True)

#convert the following content rating to "NC-17":X, TV-MA
movies.content_rating.replace(['X', 'TV-MA'], 'NC-17', inplace=True)

#count the number of missing values in each column
missingValues = movies.isnull().sum()

#if there are missing values: examin them, then fill them in with "reasonable" values
movies[movies.content_rating.isnull()]
movies.content_rating.fillna('UNRATED', inplace=True)
missingValuesAfter = movies.isnull().sum()
#print(missingValues, '\n', '\n', missingValuesAfter)

#calculate the average star rating for movies 2 hours or longer,
#and compare that with the average star rating for movies shorter than 2 hours
aboveTwoHours = movies[movies.duration >= 120].star_rating.mean()
belowTwoHours = movies[movies.duration < 120].star_rating.mean()

#use a visualization to detect whether there is a relationship between duration and star rating
movies.plot(kind='scatter', x='duration', y='star_rating', alpha=0.2)

#calculate the average duration for each genre
avgDuration = movies.groupby('genre').duration.mean()

'''
Advanced Level
'''

#visualize the relationship between content rating and duration
movies.boxplot(column='duration', by='content_rating')
movies.hist(column='duration', by='content_rating', sharex=True)

#determine the top rated movie (by star rating) for each genre
movies.sort_values('star_rating', ascending=False).groupby('genre').title.first()
movies.groupby('genre').title.first() #equivalent, since DataFrame is already sorted by star rating

#check if there are multiple movies with the same title, and if so, determine if they are actually duplicates
dupe_titles = movies[movies.title.duplicated()].title
movies[movies.title.isin(dupe_titles)]

#calculate the average star rating for each genre, but only include genres with at least 10 movies

#option 1: manually create a list of relevant genres, then filter using that list
movies.genre.value_counts()
top_genres = ['Drama', 'Comedy', 'Action', 'Crime',
              'Biography', 'Adventure', 'Animation', 'Horror', 'Mystery']
movies[movies.genre.isin(top_genres)].groupby('genre').star_rating.mean()

#option 2: automatically create a list of relevant genre, then filter using that list
genre_counts = movies.genre.value_counts()
top_grenres = genre_counts[genre_counts <= 10].index
movies[movies.genre.isin(top_genres)].groupby('genre').star_rating.mean()

#option 3: calculate the average star rating for all genres, then filter using a boolean Series
movies.groupby('genre').star_rating.mean()[movies.genre.value_counts() >= 10]

#option 4: aggregate by count and mean, then filter using the count
genre_rating = movies.groupby('genre').star_rating.agg(['count', 'mean'])
genre_rating[genre_rating['count'] >= 10]

