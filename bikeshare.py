import time
import pandas as pd

# Table of cities and file names for processing.
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'}

# Reference tables for valid months and days. Used across functions to
# ensure consistency.
# All is included to support input validation
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
        'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
       (str) city - name of the city to analyze
       (str) month - name of the month to filter by, or "all" for no month
                      filter
       (str) day - name of the day of week to filter by, or "all" for no day
                    filter
    """
    # Local copies of the return variables.
    gf_city = ' '
    gf_month = ' '
    gf_day = ' '

    print('Start by entering which city you want to explore.')
    print('Data is available for Chicago, New York City, and Washington.')

    # get user input for city(chicago, new york city, washington).
    # Validate city against global table
    # Exit if quit is entered
    while gf_city.lower != 'quit':
        print('Enter one of the 3 cities below. '
              'You can enter quit if you would like to exit the process.')
        gf_city = input('Explore: ').lower()
        if CITY_DATA.get(gf_city) is not None:
            print("Exploring data for the city of: " + gf_city.title())
            break
        elif gf_city != 'quit':
            print('Sorry there is no data available for the city you entered')
        else:
            break

    # get user input for Month(January through June data available).
    if gf_city != 'quit':
        while gf_month != 'quit':
            print('Now enter one of the months below.  '
                  'You can enter quit if you would like to exit the process.')
            print('Months available are ', months)
            gf_month = input('Explore: ').lower()
            if gf_month in months:
                print("Exploring data for the city of: " + gf_city.title())
                print("               in the month of: " + gf_month.title())
                break
            elif gf_month != 'quit':
                print('Sorry there is no data available for '
                      'the month you entered')
            else:
                break

    # get user input for Day of the Week.
    if gf_city != 'quit' and gf_month != 'quit':
        while gf_day != 'quit':
            print('Now enter one of the days of the week below. '
                  'You can enter quit if you would like to exit the process.')
            print('Days available are ', days)
            gf_day = input('Explore: ').lower()
            if gf_day in days:
                print("Exploring data for the city of: " + gf_city.title())
                print("               in the month of: " + gf_month.title())
                print("                            on: " + gf_day.title())
                break
            elif gf_day != 'quit':
                print('Sorry there is no data available for '
                      'the day you entered')
            else:
                break

    return gf_city, gf_month, gf_day


def load_data(city, month, day):
    """
    Loads data for the specified city, month and day if applicable.

    Args:
       (str) city - name of the city to analyze
       (str) month - name of the month to filter by,
                      or "all" to apply no month filter
       (str) day - name of the day of week to filter by,
                    or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_index = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month_index]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    trip_count = df.shape[0]
    print(trip_count, 'trips were selected for evaluation')

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('the most popular month to rent is: ',
          months[popular_month - 1].title())

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('the most popular day of the week to rent is: ',
          popular_day.title())

    # display the most common start hour

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour(from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print('the most popular hour to rent is: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_station = df['Start Station'].mode()[0]
    popular_station_count = len(df[df['Start Station'] == popular_station])
    print('the most popular station at which to start is: ', popular_station,
          ' occurring ', popular_station_count, ' times')

    # display most commonly used end station
    popular_station = df['End Station'].mode()[0]
    popular_station_count = len(df[df['End Station'] == popular_station])
    print('the most popular station at which to end is: ', popular_station,
          ' occurring ', popular_station_count, ' times')

    # display most frequent combination of start station and end station trip
    popular_station = (df['Start Station'] +
                       '/' +
                       df['End Station']).mode()[0]
    popular_station_count = len(df[df['Start Station'] + '/' + df[
        'End Station'] == popular_station])
    print('the most popular station combination at which to start/end is: ',
          popular_station, ' occurring ', popular_station_count, ' times')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_duration = df['Trip Duration'].sum()
    print('the total travel time for the selected trips is: ', trip_duration)

    # display mean travel time
    trip_duration = df['Trip Duration'].mean()
    print('the average travel time for the selected trips is: ',
          trip_duration)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print('Count of trips by user types: ')
    print(user_types_counts)

    if 'Gender' and 'Birth Year' in df.columns:
        # Display counts of gender
        user_types_counts = df['Gender'].value_counts(dropna=False)
        print('Count of trips by Gender: ')
        print('NaN = trips with no gender specified: ')
        print(user_types_counts, '\n')

        # Display earliest, most recent, and most common year of birth
        user_birth_year = int(df['Birth Year'].min())
        print('Earliest user birth year: ', user_birth_year)
        user_birth_year = int(df['Birth Year'].max())
        print('Most recent user birth year: ', user_birth_year)
        user_birth_year = int(df['Birth Year'].mode())
        print('Most common user birth year: ', user_birth_year)

    else:
        print('Gender and Birth Date are unavailable for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_display(df):
    """Displays 5 lines of data at a time from the data set. """
    # User input loop control
    display_data = 'yes'
    display_index = 0

    # Set the Panda option to allow all columns to be displayed.
    pd.set_option('display.max_columns', None)
    # Set the Panda option to allow the columns to be displayed across the
    # page.
    pd.set_option('display.width', None)

    print('\nWould you like to individual trip data?  '
          'Enter Yes to return data on 5 trips. ')
    print(
        'Continue entering Yes to see the next 5 trips as long as you want.')
    print('Enter No to bypass or stop showing trip data.')
    print('Some fields may show the value NaN.  This indicates no value is '
          'available for that field.')
    while display_data == 'yes':
        display_data = input('Show trip data?: ').lower()
        if display_data == 'yes':
            # Display the next 5 rows
            # Skip the first column which is a record counter
            print(df.iloc[display_index:display_index + 5, 1:9])
            display_index = display_index + 5
        elif display_data == 'no':
            print('Exiting trip display')
        else:
            print('Only Yes and No are valid entries.  You entered ',
                  display_data)
            display_data = 'yes'
    # Reset the Panda option for all columns
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')


def main():
    """
        Setting to control looping through the process.
    """
    # Setting to control looping through the process.
    restart = 'yes'

    while restart == 'yes':
        city, month, day = get_filters()
        if city != 'quit' and month != 'quit' and day != 'quit':
            df = load_data(city, month, day)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            trip_display(df)
        else:
            restart = 'no'


if __name__ == "__main__":
    print('Hello! Let\'s explore some US bikeshare data!')
    main()

print('Process ending')
