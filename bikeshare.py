#!/usr/bin/env python3
"""
The main script for performing data analysis. See README for more information.
"""
import lib.interface as interface
import lib.stats as stats
import lib.util as util

__author__ = "Joshua Gilman"
__version__ = "0.1.0"
__license__ = "MIT"

DATA_FOLDER = "data"

def main():
    """ Entry point of the script """
    running = True

    while running:
        print("Welcome to the bike share analysis tool!")
        print("Searching for raw data files...")

        # Find all raw csv data
        data_files = util.glob_data_files(DATA_FOLDER)
        print("Found {} files...".format(len(data_files)))
        
        # Humanize the file names for making a selection
        data_files_dict = {}
        for file in data_files:
            formatted_name = util.format_file_name(file)
            data_files_dict[formatted_name] = file

        # Ask the user which file to use for this analysis
        choice = interface.get_selection(list(data_files_dict.keys()))

        # Load raw csv data
        print("Loading data file for {}...".format(choice))
        data = util.load_raw_data(data_files_dict[choice])

        # Convert string dates to datetimes
        data = util.convert_datetimes(data)

        # Ask the user if they would like to filter the data
        answer = interface.ask_question(
            "Would you like to filter the raw data before processing?")
        if answer:
            data = interface.get_filtered_data(data)

        # Run analysis
        interface.show_calcs(data)

        # Ask the user if they would like to see raw data
        print("There are {} rows in the raw data".format(data.shape[0]))
        answer = interface.ask_question(
            "Would you like to see the paginated raw data?")
        if answer:
            interface.show_raw_data(data)

        # Ask the user if they would like to start over
        running = interface.ask_question("Would you like to start over?")

if __name__ == "__main__":
    """ Run the main function when this script is executed """
    main()