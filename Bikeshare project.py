import time
import pandas as pd
import numpy as np

CITY_DATA = {"chicago": "chicago.csv",
    "new york": "new_york_city.csv",
    "washington": "washington.csv"}

def get_filters():
    """Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter"""

    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    month = None
    day = None
    while city is None:
        CityUserInput = input("\nWould you like to see data for Chicago, New York, or Washington?\n")
        if CityUserInput.lower() not in CITY_DATA:
            city = None
        else:
            city = CityUserInput.lower()
    date_filter= None
    while date_filter is None:        
        date_filter = input("\nWould you like to filter the data by month, day, both or not at all?\n")
        if date_filter.lower() in ['month','day','both','not at all']:
            # get user input for month (all, january, february, ... , june)
            # get user input for day of week (all, monday, tuesday, ... sunday)
            if date_filter == "month":
                while month is None:
                    monthUserInput = input("\nWhich month - all, January, February, March, April, May, or June?\n")
                    if monthUserInput.capitalize() not in ["All","January","February","March","April","May","June"]:
                        month = None
                    else: 
                        month = monthUserInput.lower() 
                        day = 'all'
                    
            elif date_filter == "day":
                while day is None:
                    dayUserInput = input("\nWhich day - all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n")
                    if dayUserInput.capitalize() not in ["All","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]:
                        day = None
                    else: 
                        day = dayUserInput.lower() 
                        month = 'all'
            elif date_filter == "both":
                while day is None and month is None:
                    dayUserInput = input("\nWhich day - all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n")
                    monthUserInput = input("\nWhich month - all, January, February, March, April, May, or June?\n")
                    if dayUserInput.capitalize() not in ["All","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"] or monthUserInput.capitalize() not in ["All","January","February","March","April","May","June"]:
                        day = None
                        month = None
                    else: 
                        day = dayUserInput.lower() 
                        month = monthUserInput.lower()
            elif date_filter == "not at all":
                day = 'all'
                month = 'all'
        else:
            date_filter = None
         
    print('-'*40)    
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ["january","february","march","april","may","june"]
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        # filter by day of week to create the new dataframe
        if day != "all":
           df = df[df['day_of_week'] == day.title()]
      
    
    view_data = None
    while view_data is None:
        view_data = input('\nWould you like to view first 5 rows of data? Enter yes or no\n')
        start_loc = 0
        while view_data in ["yes","no"]:
            if view_data == "yes":
                print(df.iloc[start_loc:start_loc+5])
                start_loc += 5
                view_data = input("\nWould you like to view next 5 rows of data? Enter yes or no\n").lower()
            else:
                print('Proceeding')
                break
        else:
            view_data = None   
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('most common month is:',df['month'].mode()[0])
    
    # display the most common day of week
    print('most common day of week is:',df['day_of_week'].mode()[0])

    # display the most common start hour   
    print('most common start hour is:',df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('most commonly used start station is:',df['Start Station'].mode()[0])

    # display most commonly used end station
    print('most commonly used end station is:',df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('most frequent combination of start station and end station trip is:',("from "+df['Start Station']+" to "+df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):  
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('total travel time is:',df['Trip Duration'].sum())

    # display mean travel time
    print('mean travel time is:',df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
     
def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('counts of user types is :',df['User Type'].value_counts())

    # Display counts of gender
    if city != 'washington':
        print('counts of gender is :',df["Gender"].value_counts())
    else:
        print('there is no gender column in washington_data' )

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        df1 = df['Birth Year'].max()
        df2 = df['Birth Year'].min()
        print('most earliest year of birth is:',df2)
        print('most most recent year of birth is:',df1)
        print('most common year of birth is:',df['Birth Year'].mode()[0])
    else:
        print('there is no Birth Year column in washington_data' )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        # print('Nan in df',df.isnull().sum())    # sum of NaN in columns to see how much NaN in our data
        df=df.dropna(axis = 0)                    # we remove rows with NaN 
        # print('Nan in df',df.isnull().sum())
        if df.empty == False:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df,city)
        else:
            print("data_frame is empty after filters")
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()