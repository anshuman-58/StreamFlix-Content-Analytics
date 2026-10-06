import pandas as pd
ratings = pd.read_csv('data/ratings.csv')
reviews = pd.read_csv('data/reviews.csv')
subscribers = pd.read_csv('data/subscribers.csv')
titles = pd.read_csv('data/titles.csv')
watch_history = pd.read_csv('data/watch_history.csv')
watchlist = pd.read_csv('data/watchlist.csv')

print('All 6 files loaded successfully!')

# Check for missing values and duplicates in each dataset
print("Ratings:")
print(ratings.isnull().sum())
print(ratings.duplicated().sum(), "duplicates")

print("Reviews:")
print(reviews.isnull().sum())
print(reviews.duplicated().sum())

print("Subscribers:")
print(subscribers.isnull().sum())
print(subscribers.duplicated().sum())

print("Titles:")
print(titles.isnull().sum())
print(titles.duplicated().sum())

print("Watch History:")
print(watch_history.isnull().sum())
print(watch_history.duplicated().sum())

print("Watchlist:")
print(watchlist.isnull().sum())
print(watchlist.duplicated().sum())

# Count subscribers who have a churn date
print(subscribers['churn_date'].notnull().sum() , "subscribers have a churn date")

# Count titles with a license expiration date
print(titles['license_expiry'].notnull().sum(), "titles have a license expiration date")

# check data types of all columns
print("Data Types:" , titles.dtypes)

# Check basic information of titles dataset
print("Titles Dataset Info:")
print(titles.info())

# convert license_expiry column to datetime format
titles['license_expiry'] = pd.to_datetime(titles['license_expiry'], errors='coerce')
print(titles['license_expiry'].dtypes)

print(titles['license_expiry'].isna().sum(), "titles have missing license expiration dates")

# Create churn status based on churn date
subscribers['churned'] = subscribers['churn_date'].notna()
print(subscribers['churned'].value_counts(), "subscribers have churned vs not churned")

# calculate churn rate
churn_rate = subscribers['churned'].mean()*100
print("churn rate:" , round(churn_rate, 2), "%")

# check data types of all columns in subscribers dataset
print("Data Types:" , subscribers.dtypes)

# converting subscribers date columns to datetime format
subscribers['signup_date'] = pd.to_datetime(subscribers['signup_date'], errors = 'coerce')
subscribers['churn_date'] = pd.to_datetime(subscribers['churn_date'], errors = 'coerce')
print(subscribers[['churn_date' , 'signup_date']].dtypes)

# check minimum and maximum age of subscribers
print("Minimum age of subscribers:", subscribers['age'].min())
print("Maximum age of subscribers:", subscribers['age'].max())

# check active and inactive subscribers
print(subscribers["is_active"].value_counts())

# check the plan types of subscribers
print(subscribers["plan_type"].value_counts())

# check payment methods of subscribers
print(subscribers["payment_method"].value_counts())

# check the countries of subscribers
print(subscribers["country"].value_counts())

# check missing values in country column
print(subscribers['country'].isnull().sum(), "subscribers have missing country information")

# check monthly subscription price range
print("Minimum monthly subscription price:", subscribers['monthly_price_usd'].min())
print("Maximum monthly subscription price:", subscribers['monthly_price_usd'].max())

# calculate total monthly recurring revenue
monthly_revenue = subscribers['monthly_price_usd'].sum()
print("Total monthly recurring revenue: $", round(monthly_revenue, 2))

# plan wise monthly revenue
plan_revenue = subscribers.groupby('plan_type')['monthly_price_usd'].sum()
print("Plan wise monthly revenue: $", plan_revenue)

# analyze subscribers and revenue by plan type
plan_analysis = subscribers.groupby('plan_type').agg(
    subscribers = ('subscriber_id', 'count'),
    monthly_revenue = ('monthly_price_usd', 'sum'),
)
print("Plan Analysis:")
print(plan_analysis)  

# analyze churn by subscription plan
plan_churn = subscribers.groupby('plan_type')['churned'].agg(total_subscribers='count', churned='sum')
plan_churn['churn_rate'] = (
    plan_churn["churned"] / plan_churn["total_subscribers"]
) * 100
print("Plan-wise Churn Rate:")
print(plan_churn)

# calculate churn by country
country_churn = subscribers.groupby('country')['churned'].agg(
    total_subscribers = 'count', churned = 'sum'
)
country_churn['churn_rate'] = (
    country_churn['churned'] / country_churn['total_subscribers'] * 100
).round(2)
print("Country-wise Churn Rate:")
print(country_churn.sort_values('churn_rate' , ascending=False) )

# analyze churn for countries with atleast 500 subscribers
country_churn_500 = country_churn[country_churn['total_subscribers']>=500
                                  ].sort_values('churn_rate', ascending = False)
print(country_churn_500)

# check content distribution by genre
genre_counts = titles['primary_genre'].value_counts()
print("Titles by Genre" , genre_counts)

# Analyze quality and popularty by genre
genre_analysis = titles.groupby('primary_genre')[['quality_score' , 'popularity_score']].mean().round(2)

print('Genre-wise Quality and Popularity: ')
print(genre_analysis.sort_values('quality_score',ascending=False))

# Analyze content type
type_counts = titles['type'].value_counts()

print('Content type Distibution: ' , type_counts)

# Compare Movies vs TV Shows
type_analysis = titles.groupby('type')[['quality_score', 'popularity_score', 'total_watch_hours' ]].mean().round(2)
print("Movies vs TV Shows Analysis: " , type_analysis)

# analyxe license expiry
license_expiry_count = titles['license_expiry'].notna().sum()
print("titles with licese expiry:" , license_expiry_count)
print("titles without license expiry:" , titles['license_expiry'].isna().sum())

# check ratings data info
ratings.info()
# check rating distribution
print(ratings['rating'].value_counts().sort_index())

# calculate average rating
average_rating = ratings['rating'].mean()
print("Average rating;" , round(average_rating,2))

# titles wise average rating
title_ratings = ratings.groupby('title_id')['rating'].agg(
    total_ratings='count' , average_rating='mean'
)
title_ratings['average_rating']=title_ratings['average_rating'].round(2)
print("Titles wise average rating:")
print(title_ratings.sort_values('average_rating', ascending=False).head(10))

# rating fistribution in percentage
rating_percentage = ratings['rating'].value_counts(normalize=True).sort_index()* 100
print("Ratings Distribution (%):")
print(rating_percentage.round(2))

# Review data overview
print("reviews shape:",reviews.shape)
print("missing values:", reviews.isnull().sum)
print("data types" , reviews.dtypes)

# sentiment distribution
print("sentiment distribution: " , reviews['sentiment'].value_counts())

# sentiment percentage
sentiment_percentage = reviews['sentiment'].value_counts(normalize=True)*100

print("sentiment percentage; ", sentiment_percentage.round(2))

# hrlpful votes by sentiment
helpful_by_sentiment = reviews.groupby('sentiment')['helpful_votes'].mean().round(2)
print("Average helpful votes by sentiments: ", helpful_by_sentiment)

# reviews by year
reviews['review_date']= pd.to_datetime(reviews['review_date'])
review_by_year = reviews['review_date'].dt.year.value_counts().sort_index()
print("reviews by year: ", review_by_year)

# watch history data overreview
print("watch history shape:" , watch_history.shape)
print("missing values: ", watch_history.isnull().sum())
print("data types" , watch_history.dtypes)

# calculate total watch hours
total_watch_hours = watch_history['watch_duration_min'].sum()/60
print("total watch hours: ", round(total_watch_hours , 2) )

# average watch duration 
average_watch_duration = watch_history['watch_duration_min'].mean()
print("average watch duration in min :" , round(average_watch_duration,2))

# average completion percentage
average_completion = watch_history['completion_pct'].mean()
print("average completion rate :" , round(average_completion,2))

# device wise watch time
device_watch = watch_history.groupby('device')['watch_duration_min'].sum()/60
print("device-wise watch time :", device_watch.round(2).sort_values(ascending=False))

# device wise percentage
device_watch_percentage = (
    watch_history.groupby('device')['watch_duration_min'].sum()/watch_history['watch_duration_min'].sum()*100).round(2)
print("device wise watch time percentage: " , device_watch_percentage)

# completion status analysis
completion_analysis = watch_history.groupby('completed').size()
print("completion status: ", completion_analysis)

# completion rate
completion_percentage = (
    watch_history['completed'].value_counts(normalize=True)*100).round(2)
print("completion percentage :" , completion_percentage)    

# watch list data overview
print("watch list data shape: " , watchlist.shape)
print("missing values: ",watchlist.isnull().sum())
print("data types: ", watchlist.dtypes )

# watchlist watched status
watched_count = watchlist['watched'].value_counts()
print("watchlist watched status",watched_count)

watched_percentage =( watchlist['watched'].value_counts(normalize=True)*100).round(2)
print("watched percentage: ", watched_percentage)

# watchlist additions by year
watchlist['added_date'] = pd.to_datetime(watchlist['added_date'])
watchlist_by_year = watchlist['added_date'].dt.year.value_counts().sort_index()
print("watchlist additions by year: " , watchlist_by_year)