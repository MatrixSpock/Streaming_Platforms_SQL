# Streaming_Platforms_SQL

The project focuses on establishing a robust data pipeline for three prominent streaming platforms- Netflix, Amazon Prime, and Disney+. The primary objectives of the project include gaining insights into viewer preferences, analyzing the performance of content across platforms, comparing the platforms, and optimizing operational efficiency. The project aims to facilitate data-driven decision-making for content curation, user experience enhancement, and strategic planning in the highly dynamic streaming industry.

We have three datasets, all of which were found on Kaggle.com. The first one is Netflix movies and TV shows. This dataset contains a little over five thousand movie and tv titles, with fifteen columns such as “Title”, “Description”, “imbd score” (Internet Movie Database Score), “release year”, and “genre”, among others. The dataset is split into two CSV files, one for titles and one for credits. The credits CSV has additional information on actors and character names in the movies.

The second dataset is the Disney+ movies and TV shows dataset from Kaggle. This has around 1300 titles, with 12 columns containing parameters such as “title”, “director”, “cast”, and “description”, among others. It is a single CSV file.
 
The last dataset is the Amazon Prime movies and TV shows dataset, from Kaggle as well. This contains 1450 unique titles, with 10 columns containing parameters such as “title”, “director”, “cast”, and “country” among others. This dataset contains very similar parameters to the Disney+ dataset. It is a single CSV file.


Datasets:

https://www.kaggle.com/datasets/shivamb/netflix-shows

https://www.kaggle.com/datasets/shivamb/amazon-prime-movies-and-tv-shows

https://www.kaggle.com/datasets/shivamb/disney-movies-and-tv-shows

To install the required Python packages, run the following command:

```sh
pip install -r requirements.txt
```
# Setup Instructions

To run this project, follow these steps:

## 1. Clone the repository:
```sh
https://github.com/MatrixSpock/Streaming_Platforms_SQL.git
```
## 2. Navigate to the repository directory:
```sh
cd <repository-name>
```
## 3. Create a virtual environment:
```sh
python -m venv venv
```
```sh
source venv/bin/activate # Unix/MacOS
```
```sh
venv\Scripts\Activate # Windows
```
## 4. Install the required dependencies:
```sh
pip install -r requirements.txt
```
## 5. Database Configuration

Before running the application, you need to set up your database configuration. Follow these steps:

### 5.1 Create a file named `config.yml` in the root directory of the project with the following structure:

```yaml
database_config:
  host: <your_database_host>
  user: <your_database_user>
  password: <your_database_password>
```
### 5.2 Replace <your_database_host>, <your_database_user>, <your_database_password>, and <your_database_name> with your actual database host, username, password, and database name, respectively.
### 5.3 Save the config.yml file
Please do not commit config.yml to your version control system. This file is listed in .gitignore for security reasons.

## 6. Start the Jupyter Lab:
```sh
jupyter lab
```
OR
```sh
jupyter notebook
```
