"""
Helper functions for performing misc tasks
"""

import calendar
import errno
import glob
import os
import pandas as pd

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
