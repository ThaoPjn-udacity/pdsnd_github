import time
import pandas as pd
import numpy as np

#ThaoNTT1 refactor 1st
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

#ThaoNTT1 refactor 2nd
CITIES = ['chicago', 'new york', 'washington']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_valid_input(prompt, valid_options):
    """
    Prompts the user for input and ensures it matches one of the valid options.

    Args:
        prompt (str): The input prompt to display.
        valid_options (list): A list of valid input options.

    Returns:
        str: The user's validated input.
    """
    while True:
        user_input = input(prompt).lower()
        if user_input in valid_options:
            return user_input
        else:
            print(f"Invalid input. Please choose from {', '.join(valid_options)}.")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = get_valid_input("Please choose a city (Chicago, New York City, Washington):\n", CITIES)
    filter_type = get_valid_input("Would you like to filter data by month, day, or none?\n", ['month', 'day', 'none'])

    if filter_type == 'month':
        month = get_valid_input("Enter a month (January to June or 'all'):\n", MONTHS)
        day = 'all'
    elif filter_type == 'day':
        day = get_valid_input("Enter a day (Sunday to Saturday or 'all'):\n", DAYS)
        month = 'all'
    else:
        month, day = 'all', 'all'

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        month_idx = MONTHS.index(month) + 1
        df = df[df['month'] == month_idx]

    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day.lower()]

    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    print(f"Most Common Month: {MONTHS[popular_month - 1].title()}")

    popular_day = df['day_of_week'].mode()[0]
    print(f"Most Common Day of the Week: {popular_day}")

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {popular_hour % 12 or 12}{' AM' if popular_hour < 12 else ' PM'}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print(f"Most Common Start Station: {df['Start Station'].mode()[0]}")
    print(f"Most Common End Station: {df['End Station'].mode()[0]}")
    common_trip = (df['Start Station'] + " to " + df['End Station']).mode()[0]
    print(f"Most Common Trip: {common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    avg_duration = df['Trip Duration'].mean()

    print(f"Total Travel Time: {total_duration // 3600}h {(total_duration % 3600) // 60}m {total_duration % 60}s")
    print(f"Average Travel Time: {avg_duration // 60}m {avg_duration % 60:.0f}s")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("User Types:\n", df['User Type'].value_counts())

    if 'Gender' in df:
        print("\nGender Counts:\n", df['Gender'].value_counts())
    else:
        print("\nGender data not available for this city.")

    if 'Birth Year' in df:
        print(f"\nEarliest Year: {int(df['Birth Year'].min())}")
        print(f"Most Recent Year: {int(df['Birth Year'].max())}")
        print(f"Most Common Year: {int(df['Birth Year'].mode()[0])}")
    else:
        print("\nBirth year data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_data(df):
    """
    Displays 5 rows of data at a time upon user request.

    Args:
        df (DataFrame): The data to display.
    """
    start_loc = 0
    while True:
        show_data = input("\nDo you want to see 5 rows of data? Enter yes or no: ").lower()
        if show_data == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            if start_loc >= len(df):
                print("\nNo more data to display.")
                break
        elif show_data == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
