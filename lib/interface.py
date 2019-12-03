"""
Helper functions for dealing with the user interface
"""

import calendar
import lib.stats as stats
import lib.util as util
import pandas as pd

__author__ = "Joshua Gilman"
__version__ = "0.1.0"
__license__ = "MIT"

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
    unique_months = util.get_unique_months(data)

    # Create a mapping for easier user selection
    month_dict = {}
    for month in unique_months:
        month_dict[calendar.month_name[month]] = month

    # Get a dict of the days of the week
    days_of_week_dict = util.get_days_dict(True)
    
    # Ask the user if they would like to filter by month
    answer = ask_question("Would you like to filter by month?")
    if answer:
        # Get a month selection from the user
        month = get_selection(list(month_dict.keys()))
        month = month_dict[month]

        # Filter the data
        data = data[data[util.COLS['start_time']].dt.month == month]
    
    # Ask the user if they would like to filter by day
    answer = ask_question("Would you like to filter by day of the week?")
    if answer:
        # Get a month selection from the user
        day_of_week = get_selection(list(days_of_week_dict.keys()))
        day_of_week = days_of_week_dict[day_of_week]

        # Filter the data
        data = data[data[util.COLS['start_time']].dt.dayofweek == day_of_week]

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
    result = stats.calc_popular_times(data)

    print("\nMost popular times of travel:")
    print("\tMonth: {}".format(result['month']))
    print("\tDay of week: {}".format(result['day_of_week']))
    print("\tHour of day: {}\n".format(result['hour']))

    # Calculate popular stations
    result = stats.calc_popular_stations(data)

    print("Most popular stations for travel:")
    print("\tStarting station: {}".format(result['start_station']))
    print("\tEnding station: {}".format(result['end_station']))
    print("\tTrip: {} to {}\n".format(result['trip'][0], result['trip'][1]))

    # Calculate trip durations
    result = stats.calc_trip_durations(data)

    print("Trip durations:")
    print("\tTotal travel time: {}".format(result['total_time']))
    print("\tAverage travel time: {}\n".format(result['avg_time']))

    # Calculate user info
    result = stats.calc_user_unfo(data)

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
            