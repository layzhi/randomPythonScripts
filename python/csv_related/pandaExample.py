import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pdb 
pd.set_option('max_columns', 50)


# create a Series with an arbitrary list
series = pd.Series([7, 'eat', 9, 3.14, 'Happy Eating!'])

# specifying an index
series2 = pd.Series([7, 'eat', 1, 3.14], index=['H', 'a', 'E', '2'])


#Series constructor can convert a dictionary
dict = {'Chicago': 1000, 'New York': 1300, 'Boston': 1500, 'San Francisco': None}
cities = pd.Series(dict)

#use index to select specific items from the Series
cities['Chicago']

#boolean indexing for selection
cities[ cities > 1400]

#check to see if an item is in the Series
'Seattle' in cities
'Boston' in cities

#mathematical operations can be done using scalars and functions
divideByThree = cities / 3
squareCityValues = np.square(cities)

#you can add two series together which returns a union if the index share the same value. 
# If values dont share the same index will produce a Null/NaN (Not a number)
cities[['Chicago', 'New York']] + cities[['New York']]

#NULL checking can be performed with isnull and notnull
nullCheck = cities.notnull()

#use boolean logic to grab the NULL cities
cities.isnull()
cityWithNullValues = cities[cities.isnull()]

'''
Dataframes
'''
footballData = {'year': [2010, 2011, 2012, 2011, 2012, 2010, 2011, 2012],
        'team': ['Bears', 'Bears', 'Bears', 'Packers', 'Packers', 'Lions', 'Lions', 'Lions'],
        'wins': [11, 8, 10, 15, 11, 6, 10, 4],
        'losses': [5, 8, 6, 1, 5, 10, 6, 12]}
football = pd.DataFrame(footballData, columns=['year', 'team', 'wins', 'losses'])

#reading from a csv
from_csv = pd.read_csv('mariano-rivera.csv')

cols = ['num', 'game', 'date', 'team', 'home_away', 'opponent',
        'result', 'quarter', 'distance', 'receiver', 'score_before',
        'score_after']
no_headers = pd.read_csv('peyton-passing-TDs-2012.csv', sep=',', header=None, names=cols)


#manipulation excel files
football.to_excel('football.xlsx', index=False)
del football #delete the dataframe
football = pd.read_excel('football.xlsx', 'Sheet1')

# #read from copying
# readClipboard = pd.read_clipboard()
# readClipboard.head()

url = 'https://raw.github.com/gjreda/best-sandwiches/master/data/best-sandwiches-geocode.tsv'

# fetch the text from the URL and read it into a DataFrame
from_url = pd.read_table(url, sep='\t')
from_url.head(3)


'''
Part 2
'''
# pass in column names for each CSV
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('u.user', sep='|', names=u_cols,
                    encoding='latin-1')

r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings = pd.read_csv('u.data', sep='\t', names=r_cols,
                      encoding='latin-1')

# the movies file contains columns indicating the movie's genres
# let's only load the first five columns of the file with usecols
m_cols = ['movie_id', 'title', 'release_date',
          'video_release_date', 'imdb_url']
movies = pd.read_csv('u.item', sep='|', names=m_cols, usecols=range(5),
                     encoding='latin-1')

#inspection. Getting basic information about your DataFrame
'''
1. instance of dataframe
2. reach row has an index of 0 to N-1.
3. 1682 rows. every row must have an index.
4. dataset have five columns. one isnt populated (video_release_date) and two are missing values
   (release_date and imdb_url)
5. Should use dtypes method to get the datatype of each column
6. approx RAM used to hold the DataFrame
'''
# basicInfo = movies.info() #this will give an output
dataTypes = movies.dtypes
usersDescribe = users.describe()

#slicing
movies.head()
movies.tail(3)
movies[20:23]

#selecting a single column
selectingSingleColumn = users['occupation'].head()

#select multiple columns, simply pass a list of column names to the DataFrame
users[['age', 'zip_code']].head()

#can also store in a variable to use later
columns_you_want = ['occupation', 'sex']
users[columns_you_want].head()

#users older than 25
olderThan25 = users[users.age > '25'].head(10)

#users aged 40 and male
maleAged40 = users[(users.age == '40') & (users.sex == 'M')].head(10)

#if you want to modify the existing DataFrame, use the inplace parameter.
#most DataFrame methods return a new DataFrames

users.set_index('user_id', inplace=True)

#select rows by position using the iloc method
users.iloc[99]

#if you realize that we like the old pandas default index, you can use reset_index
users.reset_index(inplace=True)

#use loc for label-based indexing
#use iloc for positional indexing

'''
Joining in a RELATIONAL manner
'''
#Like SQL's JOIN clause, pandas.merge allows two DataFrames to be joined on one or more keys
#The function provides a series of parameters (on, left_on, right_on, left_index, right_index)

'''
how : {'left', 'right', 'outer', 'inner'}, default 'inner'
left: use only keys from left frame (SQL: left outer join)
right: use only keys from right frame (SQL: right outer join)
outer: use union of keys from both frames (SQL: full outer join)
inner: use intersection of keys from both frames (SQL: inner join)
'''
#example
left_frame = pd.DataFrame({'key': range(5),
                           'left_value': ['a', 'b', 'c', 'd', 'e']})
right_frame = pd.DataFrame({'key': range(2, 7),
                            'right_value': ['f', 'g', 'h', 'i', 'j']})
#inner join (default)
'''
SELECT left_frame.key, left_frame.left_value, right_frame.right_value
    FROM left_frame
    INNER JOIN right_frame
        ON left_frame.key = right_frame.key;
'''
joiningExample = pd.merge(left_frame, right_frame, on='key', how='inner')

#if the key columns were named the same, we could have use the left_on and right_on
#to specify which fields to join from each frame
#pd.merge(left_frame, right_frame, left_on='left_key', right_on='right_key')

#alternatively if "keys" were "indexes" we could use left_index or right_index parameters

#pd.merge(left_frame, right_frame, left_on='key', right_index=True)

#left outer join
'''
SELECT left_frame.key, left_frame.left_value, right_frame.right_value
FROM left_frame
LEFT JOIN right_frame
    ON left_frame.key = right_frame.key;
'''
pd.merge(left_frame, right_frame, on='key', how='left')

#right outer join
'''
SELECT right_frame.key, left_frame.left_value, right_frame.right_value
FROM left_frame
RIGHT JOIN right_frame
    ON left_frame.key = right_frame.key;
'''
pd.merge(left_frame, right_frame, on='key', how='right')

#full outer join
'''
SELECT IFNULL(left_frame.key, right_frame.key) key
        , left_frame.left_value, right_frame.right_value
FROM left_frame
FULL OUTER JOIN right_frame
    ON left_frame.key = right_frame.key;
'''
pd.merge(left_frame, right_frame, on='key', how='outer')

'''
Combining panda.concat -> returns a Series or DataFrame of concatenated objects
'''
pd.concat([left_frame, right_frame])

#objects can be concatentated side-by-side using "axis" parameter
pd.concat([left_frame, right_frame], axis = 1)


'''
Grouping - split-apply-combine strategy for data analysis
'''
#if the data contain "$", python will treat the field as a series of strings
headers = ['name', 'title', 'department', 'salary']
chicagoData = pd.read_csv('city-of-chicago-salaries.csv',
                        header = 0,
                        names=headers,
                          converters={'salary': lambda x: float(x.replace('$', ''))})

#pandas groupby returns a DataFrameGroupBy object which has variety of methods like standard SQL aggregate functions
chicagoByDept = chicagoData.groupby('department')

#calling count returns the total number of NOT NULL values within each column
#if interested in total number of records in each group, use size.
notNullRecords = chicagoByDept.count().head()
totalRecords = chicagoByDept.size().tail()
# print(notNullRecords, '\n', totalRecords)

sumOfDepartment = chicagoByDept.sum()[20:25]
avgOfDepartment = chicagoByDept.mean()[20:25]
meanOfDepartment = chicagoByDept.median()[20:25]

#Operations can be done on an individual Series within a grouped object
'''
SELECT department, COUNT(DISTINCT title)
FROM chicago
GROUP BY department
ORDER BY 2 DESC
LIMIT 5;
'''
aboveSqlStatement = chicagoByDept.title.nunique().sort_values(ascending=False)[:5]


#Split - Apply - Combine
''' 
#return the highest paid person in each department, return multiple if there were many equally high paid person
SELECT *
FROM chicago c
INNER JOIN (
    SELECT department, max(salary) max_salary
    FROM chicago
    GROUP BY department
) m
ON c.department = m.department
AND c.salary = m.max_salary;
'''
def ranker(df):
    """ Assigns a rank to each employee based on salary, with 1 being the highest paid.
    Assumes the data is DESC sorted."""
    df['dept_rank'] = np.arange(len(df)) + 1
    return df
chicagoData.sort_values('salary', ascending=False, inplace=True)
chicagoData = chicagoData.groupby('department').apply(ranker)
#print(chicagoData[chicagoData.dept_rank == 1].head(7))

'''
part 3 of http://www.gregreda.com/2013/10/26/using-pandas-on-the-movielens-dataset/
'''

chicagoData[chicagoData.department == "LAW"][:5]

# pass in column names for each CSV

users = pd.read_csv('u.user', sep='|',
                    encoding='latin-1')

r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings = pd.read_csv('u.data', sep='\t', names=r_cols,
                      encoding='latin-1')

# the movies file contains columns indicating the movie's genres
# let's only load the first five columns of the file with usecols
m_cols = ['movie_id', 'title', 'release_date',
          'video_release_date', 'imdb_url']
movies = pd.read_csv('u.item', sep='|', names=m_cols, usecols=range(5),
                     encoding='latin-1')

#create one merged DataFrame
movie_ratings = pd.merge(movies, ratings)
lens = pd.merge(movie_ratings, users)

#What are the 25 most rated movies?
most_rated = lens.groupby('title').size().sort_values(ascending=False)[:25]

'''
SELECT title, count(1)
FROM lens
GROUP BY title
ORDER BY 2 DESC
LIMIT 25;
'''
lens.title.value_counts()[:25]

#Which movies are most highly rated?
movie_stats = lens.groupby('title').agg({'rating': [np.size, np.mean]})

#sort by rating average
#movie_stats is a DataFrame, use sort method-only
#because our columns are now multilndex, we need to pass in a tuple specifying how to sort
sortRatingAverage = movie_stats.sort_values([('rating', 'mean')], ascending=False).head()

atleast_100 = movie_stats['rating']['size'] >= 100
movie_stats[atleast_100].sort_values([('rating', 'mean')], ascending=False)[:15]

'''
SELECT title, COUNT(1) size, AVG(rating) mean
FROM lens
GROUP BY title
HAVING COUNT(1) >= 100
ORDER BY 3 DESC
LIMIT 15;
'''
#movie_stats = lens.groupby('title').agg({'rating': [np.size, np.mean]})
# atleast_100 = movie_stats['rating'].size >= 100
# movie_stats[atleast_100].sort_values([('rating', 'mean')], ascending=False)[:15]

# #limiting our population going forward
most_50 = lens.groupby('movie_id').size().sort_values(ascending=False)[:50]

'''
Graphing
'''
users.age.plot.hist(bins=30)
plt.title("Distribution of users' ages")
plt.ylabel('Count of Users')
plt.xlabel('age')
#We can also use matplotlib.pyplot to customize our graph a bit

#Binning our users using pandas.cut
labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79']
lens['age_group'] = pd.cut(lens.age, range(
    0, 81, 10), right=False, labels=labels)
lens[['age', 'age_group']].drop_duplicates()[:10]


lens.groupby('age_group').agg({'rating': [np.size, np.mean]})

lens.set_index('movie_id', inplace=True)
by_age = lens.loc[most_50.index].groupby(['title', 'age_group'])
by_age.rating.mean().head(15)

tableOfData = by_age.rating.mean().unstack(1).fillna(0)[10:20]

'''
Additional Resources

pandas documentation
Introduction to pandas by Chris Fonnesbeck
pandas videos from PyCon
pandas and Python top 10
pandasql
Practical pandas by Tom Augspurger (one of the pandas developers)
Video from Tom's pandas tutorial at PyData Seattle 2015
'''
