#!/usr/bin/env python3
"""
The main script for performing data analysis. See README for more information.
"""
import calendar
import errno
import glob
import os
import pandas as pd

from datetime import datetime

__author__ = "Joshua Gilman"
__version__ = "0.1.0"
__license__ = "MIT"

COLS = {
    'start_time': 'Start Time',
    'end_time': 'End Time',
    'duration': 'Trip Duration',
    'start_station': 'Start Station',
    'end_station': 'End Station',
    'user_type': 'User Type',
    'gender': 'Gender',
    'birth_year': 'Birth Year'
}
DATA_FOLDER = "data"

"""
Helper functions for dealing with the user interface
"""

def ask_question(question):
    """ Asks the user to answer a yes/no question and returns the response

    Args:
        question (str): The question to ask the user

    Returns:
        True if user answers yes, False if user answers no
    """
    valid_choices = ['yes', 'no', 'y', 'n']
    choice = ""

    while choice not in valid_choices:
        choice = input("{} (yes/no): ".format(question)).lower()

    if choice == 'yes' or choice == 'y':
        return True
    else:
        return False

def get_filtered_data(data):
    """ Gives an interactive session allowing a user to filter data

    Will ask the user how they would like the data filtered: by month, day of
    the week, or both. The data will be filtered and returned based on the given
    answer from the user

    Args:
        data (DataFrame): The data to be filtered
    
    Returns:
        The given DataFrame, filtered via user input
    """
    # Get the unique months represented by the data
    unique_months = get_unique_months(data)

    # Create a mapping for easier user selection
    month_dict = {}
    for month in unique_months:
        month_dict[calendar.month_name[month]] = month

    # Get a dict of the days of the week
    days_of_week_dict = get_days_dict(True)
    
    # Ask the user if they would like to filter by month
    answer = ask_question("Would you like to filter by month?")
    if answer:
        # Get a month selection from the user
        month = get_selection(list(month_dict.keys()))
        month = month_dict[month]

        # Filter the data
        data = data[data[COLS['start_time']].dt.month == month]
    
    # Ask the user if they would like to filter by day
    answer = ask_question("Would you like to filter by day of the week?")
    if answer:
        # Get a month selection from the user
        day_of_week = get_selection(list(days_of_week_dict.keys()))
        day_of_week = days_of_week_dict[day_of_week]

        # Filter the data
        data = data[data[COLS['start_time']].dt.dayofweek == day_of_week]

    return data

def get_selection(choices):
    """ Asks the user to select a single item from a list of items

    Args:
        choices (list<str>): A list of items the user chooses from

    Returns:
        The single item that the user chose
    """
    # Create selection menu
    message = "\nPlease choose from the following:\n"
    for i in range(0, len(choices)):
        message += "\t{}. {}\n".format(i + 1, choices[i])

    # Ask for user input
    print(message)

    choice = ""
    while (not is_selection_valid(choices, choice)):
        choice = input("Please select a choice (1..{}): ".format(len(choices)))

    return choices[int(choice) - 1]

def is_selection_valid(choices, choice):
    """ Returns if the given choice is valid based on the available choices

    Args:
        choices (list<str>): A list of items the user choose from
        choice (str): The user's choice

    Returns:
        True if the choice is valid, False otherwise
    """
    #  Ensure the choice is a numerical value
    if not choice.isnumeric():
        return False

    # Ensure the choice is inbounds
    if int(choice) < 0 or int(choice) > len(choices):
        return False

    return True

def show_calcs(data):
    """ Shows all calculations for the given data

    Calculates and outputs the following data:
        1. Popular times of travel
            * Most common month
            * Most common day of week
            * Most common hour of day
        2. Popular stations and trip
            * Most common start station
            * Most common end station
            * Most common trip from start to end
        3. Trip duration
            * Total travel time
            * Average travel time
        4. User info
            * Counts of each user type
            * Counts of each gender (NYC and Chicago)
            * Eariest, most recent, most common year of both (NYC and Chicago)

    Args:
        data (DataFrame): the data to be processed

    Returns:
        None, outputs all results to the user via STDIO
    """
    # Calculate times of travel and output result
    result = calc_popular_times(data)

    print("\nMost popular times of travel:")
    print("\tMonth: {}".format(result['month']))
    print("\tDay of week: {}".format(result['day_of_week']))
    print("\tHour of day: {}\n".format(result['hour']))

    # Calculate popular stations
    result = calc_popular_stations(data)

    print("Most popular stations for travel:")
    print("\tStarting station: {}".format(result['start_station']))
    print("\tEnding station: {}".format(result['end_station']))
    print("\tTrip: {} to {}\n".format(result['trip'][0], result['trip'][1]))

    # Calculate trip durations
    result = calc_trip_durations(data)

    print("Trip durations:")
    print("\tTotal travel time: {}".format(result['total_time']))
    print("\tAverage travel time: {}\n".format(result['avg_time']))

    # Calculate user info
    result = calc_user_unfo(data)

    print("User information:")
    
    print("\tCounts by user type:")
    for tup in result['type_count']:
        print("\t\t{}: {:,}".format(tup[0], tup[1]))
    
    if result['gender_count']:
        print("\tCounts by gender:")
        for tup in result['gender_count']:
            print("\t\t{}: {:,}".format(tup[0], tup[1]))

    if result['earliest_year']:
        print("\tEarliest birth year: {}".format(result['earliest_year']))
        print("\tMost recent birth year: {}".format(result['recent_year']))
        print("\tMost common birth year: {}\n".format(result['common_year']))



def show_raw_data(data, page_size=5):
    """ Shows the given data, paginated, to the user

    Args:
        data (DataFrame): The DataFrame containing raw data to show the user
        page_size (int): Number of rows to show at a time, defaults to 5

    Returns:
        None
    """
    i = 0
    cont = True

    while cont:
        print("\nDisplaying rows {} through {}...\n\n".format(
              i, i + (page_size - 1)))
        print(data.iloc[i:i+page_size])

        i += page_size

        cont = ask_question("Would you like to see more raw data?")



"""
Helper functions for calculating statistical data
"""

def calc_popular_times(data):
    """ Returns the most popular month, day of week, and hour of day

    Args:
        data (DataFrame): The data to process

    Returns:
        A dictionary with the calculated results:
            { "month": <str>,
              "day_of_week": <str>,
              "hour": <str> <-- Formatted in 12 hour AM/PM
            }
    """
    result = {}

    # Calculate results
    result['month'] = int(data[COLS['start_time']].dt.month.mode()[0])
    result['day_of_week'] = int(
        data[COLS['start_time']].dt.dayofweek.mode()[0])
    result['hour'] = int(data[COLS['start_time']].dt.hour.mode()[0])
    
    # Format results
    month_dict = get_months_dict()
    day_dict = get_days_dict()

    result['month'] = month_dict[result['month']]
    result['day_of_week'] = day_dict[result['day_of_week']]

    dt = datetime.strptime(str(result['hour'])[1:], '%H')
    result['hour'] = dt.strftime('%I %p')

    return result

def calc_popular_stations(data):
    """ Returns the most popular start station, end station, and trip

    Args:
        data (DataFrame): the data to be processed

    Returns:
        A dictionary with the calculated results:
            { "start_station": <str>,
              "end_station": <str>,
              "trip": <tuple(str)> <-- Start station, End station
            }
    """
    result = {}

    # Calculate results
    result['start_station'] = data[COLS['start_station']].mode()[0]
    result['end_station'] = data[COLS['end_station']].mode()[0]
    result['trip'] = data.groupby(
        [COLS['start_station'], COLS['end_station']]).size().idxmax()

    return result

def calc_trip_durations(data):
    """ Returns total travel time and average travel time

    Args:
        data (DataFrame): the data to be processed

    Returns:
        A dictionary with the calculated results:
            { "total_time": <str>,
              "avg_time": <str>,
            }
    """
    result = {}

    # Calculate results
    result['total_time'] = str(
        (data[COLS['end_time']] - data[COLS['start_time']]).sum())
    result['avg_time'] = str(
        (data[COLS['end_time']] - data[COLS['start_time']]).mean())

    return result

def calc_user_unfo(data):
    """ Returns counts of each user type and gender, aas well as earliest, 
        most recent and most common year of birth where applicable

    Args:
        data (DataFrame): the data to be processed

    Returns:
        A dictionary with the calculated results 
        (None for non-applicable values):
            { "type_count": <tuple(tuple<str, int>)>, <-- type name, count
              "gender_count": <tuple(tuple<str, int>)>, <-- gender name, count
              "earliest_year": <int>,
              "recent_year": <int>,
              "common_year": <int>
            }
    """
    result = {}

    counts = data[COLS['user_type']].value_counts()
    result['type_count'] = tuple(zip(counts.index,counts))

    if COLS['gender'] in data.columns:
        counts = data[COLS['gender']].value_counts()
        result['gender_count'] = tuple(zip(counts.index,counts))
    else:
        result['gender_count'] = None

    if COLS['birth_year'] in data.columns:
        result['earliest_year'] = int(data[COLS['birth_year']].min())
        result['recent_year'] = int(data[COLS['birth_year']].max())
        result['common_year'] = int(data[COLS['birth_year']].mode())
    else:
        result['earliest_year'] = None
        result['recent_year'] = None
        result['common_year'] = None

    return result



"""
Helper functions for performing misc tasks
"""

def convert_datetimes(data):
    """ Converts the start time and end time strings to datetimes

    Args:
        data (DataFrame): The data to be processed

    Returns:
        A modified DataFrame with the start and end time converted to datetimes
    """
    data[COLS['start_time']] = pd.to_datetime(data[COLS['start_time']])
    data[COLS['end_time']] = pd.to_datetime(data[COLS['end_time']])

    return data

def format_file_name(path):
    """ Formats a file name to be human readable

    Takes the given relative or absolute file path and humanizes it by replacing
    underscores with spaces and titling the result

    Args:
        path (str): The absolute or relative file path

    Returns:
        The formatted file name
    """
    file_name = os.path.split(path)[-1]
    return file_name.split('.')[0].replace('_', ' ').title()

def get_days_dict(reverse=False):
    """ Returns a dictionary mapping day of week number -> name or vice versa

    Args:
        reverse (bool): if False (default) returns a dictionary mapping day
        numerical value to day name. If True, returns a dictionary mapping
        day name to daynumerical value.

    Returns:
        A dictionary mapping day name and day number
    """
    day_dict = {}

    if not reverse:
        for day in range(0, len(calendar.day_name)):
            day_dict[day] = calendar.day_name[day]
    else:
        for day in range(0, len(calendar.day_name)):
            day_dict[calendar.day_name[day]] = day

    return day_dict

def get_months_dict(reverse=False):
    """ Returns a dictionary mapping month number -> name or vice versa

    Args:
        reverse (bool): if False (default) returns a dictionary mapping month
        numerical value to month name. If True, returns a dictionary mapping
        month name to month numerical value.

    Returns:
        A dictionary mapping month name and month number
    """
    month_dict = {}

    if not reverse:
        for month in range(1, len(calendar.month_name)):
            month_dict[month] = calendar.month_name[month]
    else:
        for month in range(1, len(calendar.month_name)):
            month_dict[calendar.month_name[month]] = month

    return month_dict

def get_unique_months(data):
    """ Given raw data, returns the span of months represented in the data

    Args:
        data (DataFrame): The raw data to be processed

    Returns:
        A list of sorted unique months found in the data by their numerical 
        value
    """
    # Filter all starting and ending months
    start_months = pd.to_datetime(data[COLS['start_time']]).dt.month
    end_months = pd.to_datetime(data[COLS['end_time']]).dt.month
    
    # Combine starting and ending months and return the sorted unique values
    return sorted(start_months.append(end_months).unique())

def glob_data_files(path):
    """ Globs the given path and returns a list of all .csv files 
    
    Args:
        path (str) - An absolute or relative path to the directory with csv data

    Returns:
        A relative or absolute path to every .csv file in the directory
    """
    glob_pattern = "*.csv"
    return glob.glob(os.path.join(path, glob_pattern))

def load_raw_data(file):
    """ Takes a path to a csv file and loads it into a DataFrame

    Args:
        file (str) - An absolute or relative path to the csv file to load

    Returns:
        A DataFrame loaded with the csv file data
    """
    return pd.read_csv(file)




""" Main program """

def main():
    """ Entry point of the script """
    running = True

    while running:
        print("Welcome to the bike share analysis tool!")
        print("Searching for raw data files...")

        # Find all raw csv data
        data_files = glob_data_files(DATA_FOLDER)
        print("Found {} files...".format(len(data_files)))
        
        # Humanize the file names for making a selection
        data_files_dict = {}
        for file in data_files:
            formatted_name = format_file_name(file)
            data_files_dict[formatted_name] = file

        # Ask the user which file to use for this analysis
        choice = get_selection(list(data_files_dict.keys()))

        # Load raw csv data
        print("Loading data file for {}...".format(choice))
        data = load_raw_data(data_files_dict[choice])

        # Convert string dates to datetimes
        data = convert_datetimes(data)

        # Ask the user if they would like to filter the data
        answer = ask_question(
            "Would you like to filter the raw data before processing?")
        if answer:
            data = get_filtered_data(data)

        # Run analysis
        show_calcs(data)

        # Ask the user if they would like to see raw data
        print("There are {} rows in the raw data".format(data.shape[0]))
        answer = ask_question(
            "Would you like to see the paginated raw data?")
        if answer:
            show_raw_data(data)

        # Ask the user if they would like to start over
        running = ask_question("Would you like to start over?")

if __name__ == "__main__":
    """ Run the main function when this script is executed """
    main()