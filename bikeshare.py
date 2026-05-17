import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list = ", ".join([city.title() for city in CITY_DATA.keys()])
    city_choice = f"Which city would you like to analyze ({city_list}): "
    
    while True:
        city = input(city_choice).lower()
        if city in CITY_DATA:
            break
        else:
            print("Sorry! Invalid entry. Please choose from Chicago, New York City, or Washington.")

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Which month would you like to view (Please choose a month from january to june, or choose 'all'): ").lower()
        if month in months:
            break
        else:
            print("Sorry! Invalid entry. Please choose from january, february, ... , june, or choose 'all'")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Which day would you like to view (Please choose a day of the week, or choose 'all'): ").lower()
        if day in days:
            break
        else:
            print("Sorry! Invalid entry. Please choose from 'all', 'monday', 'tuesday', 'wednesday',... 'sunday', or choose 'all'")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    # Implement safeguards against invalid user inputs that can potentially break the codes.
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months.index(month) + 1
        df = df[df['month'] == month_num]
        
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print(f"Most common month: {most_common_month}")

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f"Most common day: {most_common_day}")

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print(f"Most common start hour: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"Most popular start station: {most_common_start_station}")

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"Most popular end station: {most_common_end_station}")

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    most_frequent_trip = df['trip'].mode()[0]
    print(f"Most Frequent Trip: {most_frequent_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_travel_time:,.2f} seconds")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean Travel Time: {mean_travel_time:,.2f} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print("Counts of User Types:")
    print(user_types_count)

    # Display counts of gender
    if 'Gender' in df.columns:
        print("\nCounts of Gender:")
        gender_count = df['Gender'].value_counts()
        print(gender_count)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
            print("\nBirth Year Statistics:")
            earliest_year = int(df['Birth Year'].min())
            most_recent_year = int(df['Birth Year'].max())
            most_common_year = int(df['Birth Year'].mode()[0])
            print(f"Earliest Year of Birth: {earliest_year}")
            print(f"Most Recent Year of Birth: {most_recent_year}")
            print(f"Most Common Year of Birth: {most_common_year}")
    else:
            print("\nNo birth year data was found for this city!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_raw_data(df):
    """Displays 5 lines of raw data at a time upon user request."""
    
    start_location = 0
    
    while True:
        if start_location == 0:
            user_input = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n').lower().strip()
        else:
            user_input = input('\nWould you like to continue viewing more data? Enter yes or no.\n').lower().strip()
        
        while user_input not in ['yes', 'no']:
            print("Invalid input. Please enter 'yes' or 'no'.")
            if start_location == 0:
                user_input = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n').lower().strip()
            else:
                user_input = input('\nWould you like to continue viewing more data? Enter yes or no?\n').lower().strip()
                
        if user_input == 'yes':
            if start_location < len(df):
                print(df.iloc[start_location:start_location + 5])
                start_location += 5
                
                if start_location >= len(df):
                    print("\nNo more data to display.")
                    break
            else:
                print("\nNo more data to display.")
                break
        else:
            print("\nGoing back to main menu...")
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        # Handle when the dataframe is empty
        if df.empty:
            print("\nNo data found for the selected filters. Please try a different month/day combination.")
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
            else:
                continue

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()