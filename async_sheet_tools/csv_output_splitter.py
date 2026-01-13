import yaml
import csv
from pyexcel_ods import save_data
from collections import OrderedDict

def format_output_csv():
    # this simply reads the gameoption_whitelist.yaml into a dictionary to have all game relevant options available
    # when filtering for the game name
    with open("gameoption_whitelist.yaml", "r") as options:
        options_dict = yaml.load(options, Loader=yaml.FullLoader)
        print(options_dict)

    # this creates the template for the output where all the actually rolled options gets appended line by line for
    # each slot of a specific game
    generated_options_per_slot = {game:[options_dict[game]] for game in options_dict.keys()}

    # reading the generated csv
    with open("output.csv", "r") as csv_stream:
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
                    slot_options = ["","",""]
                    # actually filter the whitelisted options based on the index of a given option into the temporary
                    # list
                    # skip the first 3 options because those are only there to make is easy to past into the big
                    # async sheet
                    for option in game_option_whitelist[3:]:
                        option_index = all_options_indices[option]
                        slot_options.append(row[option_index])
                    # append that slots options into the output template
                    generated_options_per_slot[game_name].append(slot_options)
                except:
                    # print skipped games
                    print(f"skipped option for {game_name}")
                    pass
    # prep for saving as .ods
    output = OrderedDict()
    for game in options_dict.keys():
        # this creates a sheet for every game
        # maybe it's possible to do that all in one sheet but this is a simple and clean way for now
        output.update({game: [*generated_options_per_slot[game]]})
    # actually save as .ods
    save_data("formatted_options.ods", output)
    print("done")

if __name__ == "__main__":
    format_output_csv()