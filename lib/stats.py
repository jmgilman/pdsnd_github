"""
Helper functions for calculating statistical data
"""

from datetime import datetime
import lib.util as util

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
    result['month'] = int(data[util.COLS['start_time']].dt.month.mode()[0])
    result['day_of_week'] = int(
        data[util.COLS['start_time']].dt.dayofweek.mode()[0])
    result['hour'] = int(data[util.COLS['start_time']].dt.hour.mode()[0])
    
    # Format results
    month_dict = util.get_months_dict()
    day_dict = util.get_days_dict()

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
    result['start_station'] = data[util.COLS['start_station']].mode()[0]
    result['end_station'] = data[util.COLS['end_station']].mode()[0]
    result['trip'] = data.groupby(
        [util.COLS['start_station'], util.COLS['end_station']]).size().idxmax()

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
        (data[util.COLS['end_time']] - data[util.COLS['start_time']]).sum())
    result['avg_time'] = str(
        (data[util.COLS['end_time']] - data[util.COLS['start_time']]).mean())

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

    counts = data[util.COLS['user_type']].value_counts()
    result['type_count'] = tuple(zip(counts.index,counts))

    if util.COLS['gender'] in data.columns:
        counts = data[util.COLS['gender']].value_counts()
        result['gender_count'] = tuple(zip(counts.index,counts))
    else:
        result['gender_count'] = None

    if util.COLS['birth_year'] in data.columns:
        result['earliest_year'] = int(data[util.COLS['birth_year']].min())
        result['recent_year'] = int(data[util.COLS['birth_year']].max())
        result['common_year'] = int(data[util.COLS['birth_year']].mode())
    else:
        result['earliest_year'] = None
        result['recent_year'] = None
        result['common_year'] = None

    return result