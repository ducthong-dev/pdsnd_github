import time
import pandas as pd
import numpy as np

# Define constant variables to reduce repetive code
CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}
MONTH_OPTIONS = ["all", "january", "february", "march", "april", "may", "june"]
DAYS_OPTIONS = [
    "all",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]
PROMPT_RESULT = ["yes", "no"]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # TODO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_choice = input("What is the city you want to analyze?").lower()
    while city_choice not in CITY_DATA:
        city_choice = input(
            "Not valid input! \n What is the city you want to analyze?"
        ).lower()
    # TODO: get user input for month (all, january, february, ... , june)
    month_choice = input(
        "What is the month you want to analyze? (Your must specific a month between January and June or All to select all month)"
    ).lower()
    while month_choice not in MONTH_OPTIONS:
        month_choice = input(
            "Not valid input! \n What is the month you want to analyze? (Your must specific a month between January and June or All to select all month)"
        ).lower()
    # TODO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_choice = input(
        "What is the day in week you want to analyze? (Specific a day or all)"
    ).lower()
    while day_choice not in DAYS_OPTIONS:
        day_choice = input(
            "Not valid input! \n What is the day in week you want to analyze? (Specific a day or all))"
        ).lower()
    print("-" * 40)
    return city_choice, month_choice, day_choice


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

    # Load csv file
    df = pd.read_csv(CITY_DATA[city])

    # Convert "Start Time" to datetime
    start_time_col = df["Start Time"]
    df["Start Time"] = pd.to_datetime(start_time_col)

    # Get month and day info from start time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()

    # Filter month bu user's month choice
    if month != "all":
        # Get user's month choice by using index
        month = MONTH_OPTIONS[1:].index(month) + 1
        # Filtering by month to create new dataframe
        df = df[df["month"] == month]

    # Filter day by user's day choice
    if day != "all":
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # Convert "Start Time" to datetime
    start_time_col = df["Start Time"]
    df["Start Time"] = pd.to_datetime(start_time_col)

    # TODO: display the most common month
    # Get month and day info from start time
    df["month"] = start_time_col.dt.month
    # Finding the most common month
    common_month = df["month"].mode()[0]
    print(f"Most Common Month: {MONTH_OPTIONS[1:][common_month - 1]}")

    # TODO: display the most common day of week
    # get days from the start time column to create a day_of_week column
    df["day_of_week"] = df["Start Time"].dt.dayofweek
    # Finding the most common day of the week from 0 to 6
    common_day = df["day_of_week"].mode()[0]
    print(f"Most common day: {DAYS_OPTIONS[1:][common_day]}")

    # TODO: display the most common start hour
    # Get hour from the start time column
    df["hour"] = df["Start Time"].dt.hour
    # Finding the most common hour from 0 to 23
    common_hour = df["hour"].mode()[0]
    print(f"Most common start hour: {common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # TODO: display most commonly used start station
    print(f'Most Common Start Station: {df["Start Station"].mode()[0]}')

    # TODO: display most commonly used end station
    print(f'Most Common End Station: {df["End Station"].mode()[0]}')

    # TODO: display most frequent combination of start station and end station trip
    print(
        f'Most Frequent Combination of Start Station and End Station Trips:\n\n {df.groupby(["Start Station", "End Station"]).size().nlargest(1)}'
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # TODO: display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print(f"The total travel time is : {total_travel_time}.")

    # TODO: display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print(f"The mean travel time is : {mean_travel_time}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # TODO: Display counts of user types
    user_types_count = df["User Type"].value_counts()
    print(f"Distribution for user types: {user_types_count}")

    # TODO: Display counts of gender
    if "Gender" in df.columns:
        gender_count = df["Gender"].value_counts()
        print(f"Distribution for each gender: {gender_count}")
    else:
        print(f"There is no data of user gender in {city.title()}")

    # TODO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        print(f'Earliest year of birth:" {df["Birth Year"].min()}')
        print(f'Most recent year of birth: {df["Birth Year"].max()}')
        print(f'Most common year of birth: {df["Birth Year"].mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Processing time statistical
        time_stats(df)
        # Station statistical
        station_stats(df)
        # Trip duration statistical
        trip_duration_stats(df)
        # User statistical
        user_stats(df, city)

        # Ask user want to see more detail about data or not
        user_input = input("Would you like to see more data? (Enter:Yes/No).\n")

        # Ask again when user input invalid answer
        while user_input.lower() not in PROMPT_RESULT:
            user_input = input("Please Enter Yes or No:\n")
            user_input = user_input.lower()

        index = 0
        while True:
            if user_input.lower() == "yes":
                print(df.iloc[index : index + 5])
                index += 5
                user_input = input(
                    "\nWould you like to see more data? (Type:Yes/No).\n"
                )
                while user_input.lower() not in PROMPT_RESULT:
                    user_input = input("Please Enter Yes or No:\n")
                    user_input = user_input.lower()
            else:
                break

        # Ask user want to restart application or not
        restart = input("\nWould you like to restart? Enter yes or no.\n")
        while restart.lower() not in PROMPT_RESULT:
            restart = input("Please Enter Yes or No:\n")
            restart = restart.lower()
        if restart.lower() != "yes":
            print("Good Bye!")
            break


if __name__ == "__main__":
    main()
