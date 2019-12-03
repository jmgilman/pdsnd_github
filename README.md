# Bike Share Analysis Tool

This tool consists of a single script which performs various pre-determined
calculations on raw bike share data from motivateco.com given in CSV format. For
each run of the tool, the following statistics are calculated:

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

## Usage
Clone or download the source documents to your computer. **You must supply the
appropriate CSV files in order for the script to execute properly.** Place each
of these .csv files in a directory entitled `data` in the root directory of the
project. It's recommended you name the .csv files after their respective city
names, using underscores to denote spaces. 

Run the `bikeshare.py` file to begin the interactive session. Follow the prompts
in order to begin the data processing. You will have the option to filter by
month, day of the week, or both. After filtering, the above statistics will be
outputted to the terminal. After the calculations are performed, you will have
the option to view the raw data, paginated by 5 rows at a time. Finally, you
will be offered to run the analysis again from the beginning, choosing new data
and filters as needed.

## Example
```
Welcome to the bike share analysis tool!
Searching for raw data files...
Found 3 files...

Please choose from the following:
        1. Chicago
        2. New York City
        3. Washington

Please select a choice (1..3): 1
Loading data file for Chicago...
Would you like to filter the raw data before processing? (yes/no): yes
Would you like to filter by month? (yes/no): yes

Please choose from the following:
        1. January
        2. February
        3. March
        4. April
        5. May
        6. June
        7. July

Please select a choice (1..7): 5
Would you like to filter by day of the week? (yes/no): no

Most popular times of travel:
        Month: May
        Day of week: Monday
        Hour of day: 07 AM

Most popular stations for travel:
        Starting station: Streeter Dr & Grand Ave
        Ending station: Streeter Dr & Grand Ave
        Trip: Lake Shore Dr & Monroe St to Streeter Dr & Grand Ave

Trip durations:
        Total travel time: 754 days 08:16:03
        Average travel time: 0 days 00:16:16.336798

User information:
        Counts by user type:
                Subscriber: 51,020
                Customer: 15,735
        Counts by gender:
                Male: 38,284
                Female: 12,750
        Earliest birth year: 1899
        Most recent birth year: 2016
        Most common birth year: 1989

There are 66755 rows in the raw data
Would you like to see the paginated raw data? (yes/no): yes

Displaying rows 0 through 4...


    Unnamed: 0          Start Time            End Time  Trip Duration  ...                     End Station   User Type  Gender Birth Year
1       955915 2017-05-25 18:19:03 2017-05-25 18:45:53           1610  ...    Sheffield Ave & Waveland Ave  Subscriber  Female     1992.0
6       961916 2017-05-26 09:41:44 2017-05-26 09:46:25            281  ...            Wood St & Hubbard St  Subscriber  Female     1983.0
13     1023296 2017-05-30 15:46:18 2017-05-30 15:52:12            354  ...               Clark St & Elm St  Subscriber    Male     1985.0
15      958716 2017-05-25 22:59:33 2017-05-25 23:07:19            466  ...  Sheffield Ave & Wrightwood Ave  Subscriber  Female     1985.0
16      718598 2017-05-03 13:20:38 2017-05-03 13:31:13            635  ...              Daley Center Plaza  Subscriber    Male     1967.0

[5 rows x 9 columns]
Would you like to see more raw data? (yes/no): no
Would you like to start over? (yes/no): no
```

## Credits

Architecture and raw bike share data provided from motivateco.com. 