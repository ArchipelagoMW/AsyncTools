import yaml
import csv
import argparse
import tkinter as tk
from tkinter import filedialog
from pyexcel_ods import save_data
from collections import OrderedDict

def format_output_csv(filename:str = "output.csv", output_filename:str = "formatted_options.ods"):
    # this simply reads the gameoption_whitelist.yaml into a dictionary to have all game relevant options available
    # when filtering for the game name
    with open("gameoption_whitelist.yaml", "r") as options:
        options_dict = yaml.load(options, Loader=yaml.FullLoader)
        # print(options_dict)

    # this creates the template for the output where all the actually rolled options gets appended line by line for
    # each slot of a specific game
    generated_options_per_slot = {game:[options_dict[game]] for game in options_dict.keys()}


    # reading the generated csv
    with open(filename, "r") as csv_stream:
        options_csv = csv.reader(csv_stream)
        # looping over each line from the csv
        for index, row in enumerate(options_csv):
            if index == 0:
                # get all the actually rolled options and their index in the list
                # the index is used to filter for the relevant options later
                all_options_indices = {option_name:index for index, option_name in enumerate(row)}
            else:
                game_name = row[1]
                # try just for good measure to filter out games that are not included in the gameoption_whitelist.yaml
                try:
                    # retrieve the options-list to whitelist for the current lines game
                    game_option_whitelist = options_dict[game_name]
                    # temp list to store filtered options in
                    slot_options = ["",""]
                    # actually filter the whitelisted options based on the index of a given option into the temporary
                    # list
                    # skip the first 2 options because those are only there to make is easy to past into the big
                    # async sheet
                    for option in game_option_whitelist[2:]:
                        option_index = all_options_indices[option]
                        slot_options.append(row[option_index])
                    # append that slots options into the output template
                    generated_options_per_slot[game_name].append(slot_options)
                except:
                    # print skipped games
                    print(f"skipped option for {game_name}, option: {option}")
                    pass
    # prep for saving as .ods
    output = OrderedDict()
    for game in options_dict.keys():
        # this creates a sheet for every game
        # maybe it's possible to do that all in one sheet but this is a simple and clean way for now
        output.update({game: [*generated_options_per_slot[game]]})
    # actually save as .ods
    save_data(f"{output_filename}.ods", output)
    print("done")

if __name__ == "__main__":
    cmd_parser = argparse.ArgumentParser(
        prog="Big Async Options Sheet creator",
        description="""This script is used for converting the generations options-CSV into the format of the 
        Big-Async spreadsheet and separating each games the options  
        """,
    )
    cmd_parser.add_argument("-I", "--input", type=str)
    cmd_parser.add_argument("-O", "--output", type=str)
    cmd_args = cmd_parser.parse_args()

    if cmd_args.input is None: # check for cmd parameter used for input filename/filepath
        root = tk.Tk()
        root.withdraw()
        print("""
Please select the CSV-File you got from the generation output.
        """)
        input_file_path = tk.filedialog.askopenfile()
        input_file_path = input_file_path.name
    else:
        input_file_path = cmd_args.input

    if cmd_args.output is None: # check for cmd parameter used for output filename
        output_file_name = "formatted_options"
    else:
        output_file_name = cmd_args.output
    print(f"""
Using '{input_file_path}' as input filename.
Using '{output_file_name}' as output filename.
    """)
    # print(f"input csv-file: {input_file_path}")
    # print(f"outout ods-file: {output_file_path}")

    format_output_csv(input_file_path, output_file_name)