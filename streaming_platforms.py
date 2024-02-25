#!/usr/bin/env python
# coding: utf-8

# # 1. Importing the Libraries

# In[ ]:


# importing packages
import yaml
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import mysql.connector
import seaborn as sns
import warnings 
warnings.filterwarnings('ignore')


# # 2. Data Extraction

# In[ ]:


# Load the configuration file
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# Access the database configuration
db_config = config['database_config']
host = db_config['host']
user = db_config['user']
password = db_config['password']
database = db_config['database']

# # Access dataset paths
# dataset1_path = config['dataset_paths']['dataset1']
# dataset2_path = config['dataset_paths']['dataset2']
# dataset3_path = config['dataset_paths']['dataset3']


# # loading the data 
# # Use the paths from the configuration to read datasets
# amazon_df = pd.read_csv(dataset1_path)
# disney_df = pd.read_csv(dataset2_path)
# netflix_df = pd.read_csv(dataset3_path)

amazon_df = pd.read_csv("datasets\\amazon_prime_titles.csv")
disney_df = pd.read_csv("datasets\\disney_plus_titles.csv")
netflix_df = pd.read_csv("datasets\\netflix_titles.csv")


# # 3. Exploratory Data Analysis
# 
# ## 3.1 Shape

# In[ ]:


amazon_df.shape


# In[ ]:


disney_df.shape


# In[ ]:


netflix_df.shape


# ## 3.2 Data Types

# In[ ]:


amazon_df.info()


# In[ ]:


disney_df.info()


# In[ ]:


netflix_df.info()


# ## 3.3 Checking missing values

# In[ ]:


amazon_df.isnull().sum()


# In[ ]:


disney_df.isnull().sum()


# In[ ]:


netflix_df.isnull().sum()


# ## 3.4 Checking duplicate values

# In[ ]:


amazon_df.duplicated().sum()


# In[ ]:


disney_df.duplicated().sum()


# In[ ]:


netflix_df.duplicated().sum()


# ## 3.4 Describe

# In[ ]:


amazon_df.describe().round(2)


# In[ ]:


disney_df.describe().round(2)


# In[ ]:


netflix_df.describe().round(2)


# # 4. Data Transformation
# 
# ## 4.1 Data Cleaning
# 
# ### 4.1.1 Amazon
# 
# Country and date_added columns have more than 80% of the missing values and hence dropping them.

# In[ ]:


# Dropping columns 

amazon_df = amazon_df.drop(['country', 'date_added'], axis=1)

# Removing rows with null values in 'rating' column

amazon_df.dropna(subset=['rating'], inplace=True)

# Dropping irrelevant columns for analysis

amazon_df = amazon_df.drop(['show_id','director','cast'], axis=1)


# ### 4.1.2 Disney_Plus

# In[ ]:


# Dropping columns 

disney_df = disney_df.drop(['country', 'date_added'], axis=1)

# Removing rows with null values in 'rating' column

disney_df.dropna(subset=['rating'], inplace=True)

# Dropping irrelevant columns for analysis

disney_df = disney_df.drop(['show_id','director','cast'], axis=1)


# ### 4.1.3 Netflix

# In[ ]:


# Dropping columns 

netflix_df = netflix_df.drop(['country', 'date_added'], axis=1)

# Removing rows with null values in 'rating' column

netflix_df.dropna(subset=['rating', 'duration'], inplace=True)

# Dropping irrelevant columns for analysis

netflix_df = netflix_df.drop(['show_id','director','cast'], axis=1)


# ## 4.2 Adding new columns

# In[ ]:


amazon_df['platform'] = 'Amazon Prime'
amazon_df['headquarters'] = 'Seattle, Washington'
amazon_df['date_founded'] = '02/02/2005'

disney_df['platform'] = 'Disney Plus'
disney_df['headquarters'] = 'Los Angeles, California'
disney_df['date_founded'] = '11/12/2019'

netflix_df['platform'] = 'Netflix'
netflix_df['headquarters'] = 'Los Gatos, California'
netflix_df['date_founded'] = '08/29/1997'


# ## 4.3 Merging the data frames
# 
# Merging all the three data frames to a single dataframe for analysis.

# In[ ]:


streaming_platforms_df = pd.concat([amazon_df,disney_df,netflix_df], ignore_index=True)

streaming_platforms_df.head()


# In[ ]:


streaming_platforms_df.shape


# ## 4.4 Renaming the Column

# In[ ]:


streaming_platforms_df.rename(columns={'listed_in':'genre'}, inplace=True)


# ## 4.5 Formatting the data types
# 
# Convert the string data type of 'date_founded' to datetime.

# In[ ]:


streaming_platforms_df['date_founded'] = pd.to_datetime(streaming_platforms_df['date_founded'])


# ## 4.6 Replacing the column values
# 
# The dataset contains several redundant rating categories. For example, rating category 16, AGES_16_, 16+ represent the same category 16+. For analysis purpose, we replace the rating category values to a unified value.

# In[ ]:


streaming_platforms_df['rating'].value_counts()


# In[ ]:


streaming_platforms_df['rating'].replace(['16','AGES_16_'], '16+', inplace=True)
streaming_platforms_df['rating'].replace(['AGES_18_'], '18+', inplace=True)
streaming_platforms_df['rating'].replace(['ALL_AGES'], 'ALL', inplace=True)
streaming_platforms_df['rating'].replace(['TV-NR','UNRATED','NOT_RATE','UR'], 'NR', inplace=True)


# In[ ]:


streaming_platforms_df.head()


# In[ ]:


streaming_platforms_df.tail()


# ### 5. Data Loading

# In[ ]:


try:
    # Connect to MySQL
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="matrix01M"
    )

   
    cursor = connection.cursor()

    # Name of the database you wish to create
    database_name = 'Group_5'
    
    # SQL statement to execute
    sql = f"CREATE DATABASE IF NOT EXISTS {database_name}"

    # Execute the SQL statement
    cursor.execute(sql)

    # Select Database
    cursor.execute(f"USE {database_name}")

    
    # Define SQL statements to create tables
    create_movie_table_query = """
    CREATE TABLE IF NOT EXISTS movie (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        release_year INT,
        rating VARCHAR(10),
        duration VARCHAR(20),
        description TEXT,
        platform VARCHAR(50),
        headquarters VARCHAR(100),
        date_founded DATE
    )
    """

    create_genre_table_query = """
    CREATE TABLE IF NOT EXISTS genre (
        id INT AUTO_INCREMENT PRIMARY KEY,
        genre_name VARCHAR(255) UNIQUE
    )
    """

    create_streaming_platform_table_query = """
    CREATE TABLE IF NOT EXISTS streaming_platform (
        id INT AUTO_INCREMENT PRIMARY KEY,
        platform_name VARCHAR(50) UNIQUE,
        headquarters VARCHAR(100),
        date_founded DATE
    )
    """

    create_tv_show_table_query = """
    CREATE TABLE IF NOT EXISTS tv_show (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        release_year INT,
        rating VARCHAR(10),
        duration VARCHAR(20),
        description TEXT,
        platform VARCHAR(50),
        headquarters VARCHAR(100),
        date_founded DATE
    )
    """

    # Execute the queries
    cursor.execute(create_movie_table_query)
    cursor.execute(create_genre_table_query)
    cursor.execute(create_streaming_platform_table_query)
    cursor.execute(create_tv_show_table_query)

    # Commit the transaction
    connection.commit()

    print("Tables created successfully!")

except mysql.connector.Error as error:
    print("Error:", error)


# In[ ]:


# Create rating table
try:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rating (
        id INT AUTO_INCREMENT PRIMARY KEY,
        rating_value VARCHAR(10) NOT NULL
    )
    """)
    
    print("Table 'rating' created successfully!")

except mysql.connector.Error as error:
    print("Error:", error)


# In[ ]:


#See the tables for Group_5 schema 
query = "SHOW TABLES"
cursor.execute(query)
tables = cursor.fetchall()

# Print the table names
for table in tables:
    print(table[0])


# ### Load data into SQL database tables 

# In[ ]:


# Iterate over each row in the DataFrame
for index, row in streaming_platforms_df.iterrows():
    # Check if the platform already exists
    platform_query = "SELECT * FROM streaming_platform WHERE platform_name = %s"
    cursor.execute(platform_query, (row['platform'],))
    existing_platform = cursor.fetchone()

    if not existing_platform:
        # Insert into streaming_platform table
        streaming_platform_query = "INSERT INTO streaming_platform (platform_name, headquarters, date_founded) VALUES (%s, %s, %s)"
        streaming_platform_data = (row['platform'], row['headquarters'], str(row['date_founded']))
        cursor.execute(streaming_platform_query, streaming_platform_data)

    # Insert into movie or TV show table
    if row['type'] == 'Movie':
        movie_query = "INSERT INTO movie (title, release_year, rating, duration, description, platform, headquarters, date_founded) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        movie_data = (row['title'], row['release_year'], row['rating'], row['duration'], row['description'], row['platform'], row['headquarters'], str(row['date_founded']))
        cursor.execute(movie_query, movie_data)
    elif row['type'] == 'TV Show':
        tv_show_query = "INSERT INTO tv_show (title, release_year, rating, duration, description, platform, headquarters, date_founded) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        tv_show_data = (row['title'], row['release_year'], row['rating'], row['duration'], row['description'], row['platform'], row['headquarters'], str(row['date_founded']))
        cursor.execute(tv_show_query, tv_show_data)

# Commit the changes and close the connection
connection.commit()


# In[ ]:


# Still need to do genre, which has multiple genres separated by commas in each response. 


# In[ ]:


query = """
SELECT release_year, COUNT(*) as count
FROM movie
GROUP BY release_year
ORDER BY release_year;
"""

# Use pandas to load the query result into a DataFrame
df_content_per_year = pd.read_sql(query, connection)

# Plotting the data
plt.figure(figsize=(14,6))
sns.barplot(x=df_content_per_year['release_year'], y=df_content_per_year['count'], palette="viridis")
plt.title('Number of Contents Released Each Year')
plt.xlabel('Year')
plt.ylabel('Number of Contents')
plt.xticks(rotation=90)  # Rotate x-axis labels to vertical
plt.tight_layout()
plt.show()


# In[ ]:


print(disney_df.columns)


# In[ ]:


# #Finding number of contents by genre
# #Need to separate each strings in genre since they can have multiple genres in a single program
# genre_count = disney_df['genre'].str.split(',').explode().str.strip().value_counts()

# plt.figure(figsize=(12,8))`
# sns.barplot(y=genre_count.index, x=genre_count.values, palette="viridis")
# plt.xlabel('Number of Contents')
# plt.ylabel('Genre')
# plt.title('Content Counts by Genre')
# plt.show()


# In[ ]:


#Simply looking at percentage of Movie and TV shows 
content_type_dist = disney_df['type'].value_counts()

plt.figure(figsize=(4,4))
content_type_dist.plot.pie(autopct='%1.1f%%', startangle=90)
plt.title('Distribution of Content Types on Disney+')
plt.ylabel('')  #hiding y axis since it is distractive 
plt.show()


# In[ ]:


rating_counts = disney_df['rating'].value_counts()

plt.figure(figsize=(5,3))
sns.barplot(x=rating_counts.index, y=rating_counts.values, palette='viridis')
plt.title('Distribution of Contents by Rating on Disney+')
plt.xlabel('Rating')
plt.ylabel('Number of Contents')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[ ]:


sns.stripplot(x='release_year' , y='rating', data=disney_df)


# In[ ]:


plt.figure(figsize=(10, 6))
rating_counts.sort_index().plot(kind='bar', color='skyblue')
plt.title('Distribution of Age Ratings')
plt.xlabel('Age Rating')
plt.ylabel('Number of Movies')
plt.show()


# In[ ]:


# Distribution of movies by release year
plt.figure(figsize=(12, 6))
sns.histplot(disney_df['release_year'], bins=30, kde=True, color='skyblue')
plt.title('Distribution of Movies by Release Year')
plt.xlabel('Release Year')
plt.ylabel('Number of Movies')
plt.show()


# In[ ]:


# Distribution of movies by release year
plt.figure(figsize=(12, 6))
sns.histplot(netflix_df['release_year'], bins=30, kde=True, color='skyblue')
plt.title('Distribution of Movies by Release Year')
plt.xlabel('Release Year')
plt.ylabel('Number of Movies')
plt.show()


# In[ ]:


# Distribution of movies by release year
plt.figure(figsize=(12, 6))
sns.histplot(amazon_df['release_year'], bins=30, kde=True, color='skyblue')
plt.title('Distribution of Movies by Release Year')
plt.xlabel('Release Year')
plt.ylabel('Number of Movies')
plt.show()


# In[ ]:


query = """
SELECT *
FROM movie;
"""

# Use pandas to load the query result into a DataFrame
movies_df = pd.read_sql(query, connection)


# Distribution of ratings
plt.figure(figsize=(10, 6))
sns.countplot(x='rating', data=movies_df, order=movies_df['rating'].value_counts().index, palette='viridis')
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Number of Movies')
plt.xticks(rotation=45, ha='right')
plt.show()


# In[ ]:


# **** SAME QUERY JUST DIFFERENT COLORS *****
query = """
SELECT *
FROM movie;
"""

# Use pandas to load the query result into a DataFrame
movies_df = pd.read_sql(query, connection)


# Distribution of ratings
plt.figure(figsize=(10, 6))
sns.countplot(x='rating', data=movies_df, order=movies_df['rating'].value_counts().index, palette='plasma')
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Number of Movies')
plt.xticks(rotation=45, ha='right')
plt.show()


# In[ ]:


query = """
SELECT *
FROM tv_show;
"""

# Use pandas to load the query result into a DataFrame
shows_df = pd.read_sql(query, connection)

# Distribution of ratings
plt.figure(figsize=(10, 6))
sns.countplot(x='rating', data=shows_df, order=shows_df['rating'].value_counts().index, palette='viridis')
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Number of TV Shows')
plt.xticks(rotation=45, ha='right')
plt.show()


# In[ ]:


# # **** NO GENRE INFO AVAILABLE ****
# # Top genres
# top_genres = data['listed_in'].value_counts().head(10)

# # Plot Top Genres
# plt.figure(figsize=(12, 6))
# sns.barplot(x=top_genres.values, y=top_genres.index, palette='muted')
# plt.title('Top 10 Genres')
# plt.xlabel('Number of Movies')
# plt.ylabel('Genre')
# plt.show()


# In[ ]:


data_count1=disney_df['rating'].value_counts().reset_index()
plt.figure(figsize=(16,6))
sns.countplot(x='rating',data=disney_df,hue='type',order=disney_df['rating'].value_counts().index)
plt.xticks(rotation=90)
plt.title('Distribution of show rating')
plt.xlabel('Rating')
plt.ylabel('Number of Shows')
plt.show()


# In[ ]:




