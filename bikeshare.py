import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months_dict = {'1': 'january','2': 'february',
            '3': 'march','4': 'april',
            '5': 'may','6': 'june','none': 'all'}
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cities_dict = {'C' : 'chicago',
                   'N' : 'new york city',
                'W': 'washington'}

    days_dict = {'1': 'Sunday','2': 'Monday','3': 'Tuesday',
                '4': 'Wednesday','5': 'Thursday',
                '6': 'Friday','7': 'Saturday','none': 'all'}
    # trimmng all of these chars if mistakenly entered
    trimmed_chars = "' -_,.()"
    # Welcome message
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city_input = input("\nTo choose the city you want to explore as specified below.\nIf you want chicago city enter:(C),\nIf you want New York city enter:(N),\nIf you want Washington city enter:(W).\n\n").title().strip(trimmed_chars)
            city = cities_dict[city_input]
            break
        except :
            if city_input not in cities_dict:
                print("Oops!")
                print("Your input is not valid.\nPlease Try again...")
    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month_input = input("\nIf you want to explore data in a particular month.\nPlease choose the number corresponding to it as specified in the list below:\n(1) for January,\n(2) for February,\n(3) for March,\n(4) for April,\n(5) for May,\n(6) for June,\nOr enter (None) if you want to see the data of all of the months\n\n").strip(trimmed_chars)
            month = months_dict[month_input]
            break
        except:
            if month_input not in months_dict:
                print("Oops!")
                print("Your input is not valid.\nPlease Try again...")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day_input = input("If you want to explore data in a particular day.\nPlease choose the number corresponding to it as specified in the list below:\n(1) for Sunday,\n(2) for Monday,\n(3) for Tuesday,\n(4) for Wednesday,\n(5) for Thursday,\n(6) for Friday,\n(7) for Saturday.\nOr enter (None) if you want to see the data of all of the days\n\n").strip(trimmed_chars)
            day = days_dict[day_input]
            break
        except:
            if day_input not in days_dict:
                print("Oops!")
                print("Your input is not valid.\nPlease Try again...")

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day Of Week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month =  months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df["Month"] == month]


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df["Day Of Week"] == day.title()]
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel.

    Args:
        (Pandas DataFrame) df - name of the  pandas data frame to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        most common month
        most common day of week
        most common start hour
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month only if user didn't filter
    if month == 'all':
        most_common_month = df['Month'].mode()[0]
        print("-Most Popular month: {}\n".format(months_dict[str(most_common_month)].title()))

    # display the most common day of week only if user didn't filter
    if day == 'all':
        most_common_day = df['Day Of Week'].mode()[0]
        print("-Most Popular day: {}\n".format(most_common_day.title()))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_st_hour = df['hour'].mode()[0]
    print("-Most Popular start hour: {} *24 Hours format*\n".format(most_common_st_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        (Pandas DataFrame) df - name of the  pandas data frame to analyze
    Returns:
        most common start station
        most common end station
        most common trip from start to end
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("-Most Popular start station: {}\n".format(popular_start_station.title()))
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("-Most Popular end station: {}\n".format(popular_end_station.title()))

    # display most frequent combination of start station and end station trip
    sub_df = df['Start Station'] + '-' +  df['End Station']
    popular_trip = sub_df.mode()[0]
    print("-Most Popular Trip: {}".format(popular_trip))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Args:
        (Pandas DataFrame) df - name of the  pandas data frame to analyze
    Returns:
        total travel time
        average travel time

    """

    print('\nCalculating Trip Duration stats...\n')
    start_time = time.time()
    # convert time in seconds into time in days, hours, minutes and seconds.
    def convert_time(time_in_sec):
        """convert time in seconds into time in days, hours, minutes and seconds.

        Args:
            (str): time_in_sec - time in seconds to convert

        Returns:
            (str): Time converted into days, hours, minutes and seconds format
        """
        days = time_in_sec // 86400
        hours = (time_in_sec % 86400) // 3600
        minutes = ((time_in_sec % 86400) % 3600) // 60
        seconds = round(((time_in_sec % 86400) % 3600) % 60)
        return("{} days, {} hours, {} minutes and {} seconds".format(days, hours, minutes, seconds))

    # display total travel time
    total_travel_duration = df['Trip Duration'].sum()

    print("-Total Travel time is: {} seconds\n".format(total_travel_duration))
    print("which is: {}\n".format(convert_time(total_travel_duration)))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("-Mean Trip Time is: {} seconds\n".format(mean_travel_time))
    print("which is: {}\n".format(convert_time(mean_travel_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users.

    Args:
        (Pandas DataFrame) df - name of the  pandas data frame to analyze
        (str) city - name of the city to check if Gender and Birth Year data is available
    Returns:
        counts of each user type
        counts of each gender (only available for NYC and Chicago)
        earliest, most recent, most common year of birth (only available for NYC and Chicago)
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print("-The count of user types is: \n", user_types,"\n")

    #shecks if the gender and user type data available or not
    if city != 'washington':
        # Display counts of gender
        user_genders = df["Gender"].value_counts()
        print("-The count of user genders is: \n", user_genders,"\n")


        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df["Birth Year"].min()
        most_recent_birth_year = df["Birth Year"].max()
        most_common_birth_year = df["Birth Year"].mode()[0]

        print("-The earliest year of birth is: {}\n".format(earliest_birth_year))
        print("-The most recent year of birth is: {}\n".format(most_recent_birth_year))
        print("-The most common year of birth is: {}\n".format(most_common_birth_year))
    else:
        print("We are afraid that gender and year of birth data is not provided for washington city...")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(city):
    """
    askig the user if he wants to see a chunk of the raw data.

    Args:
        (str) city - name of the city from which raw data will be displayed.

    returns:
        (Pandas DataFrame): 5 new rows of the raw data every time the user inputs 'yes'

    """
    # trimmng all of these chars if mistakenly entered
    trimmed_chars = "' -_,.()"
    #while the answer is yes the program will show a new set of five rows of raw input one at a time
    i = 0
    while True:
        try:
            answer = input("Would you like to explore more raw data of these statistics??\nIf so, Enter: yes\nIf not, Just Type anything -maybe a farewell message :)- then press enter.\n\n").lower().strip(trimmed_chars)
            if answer != 'yes':
                print("Goodbye :D.....")
                break
            df = load_data(city, 'all', 'all')
            print(df.iloc[i*5 : (i*5) + 5, :],'\n')
            i += 1
            print('You have accessed ({}) chunks of raw data\n'.format(i))
            print('-'*40)
        except:
            print("Goodbye :D.....")


def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Have a nice day :D....")
            break
if __name__ == "__main__":
	main()
