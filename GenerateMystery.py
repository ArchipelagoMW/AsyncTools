import os
import yaml
from colorama import Fore


# Please don't look too closely at this code below. kthx -Phar
class MysterySettings(dict):
    def __init__(self, name: str, description: str, requires: dict, game: dict):
        super().__init__()

        self["name"] = name
        self["description"] = description
        self["requires"] = requires
        self["game"] = game

    def __str__(self) -> str:
        string = "{:<32} {:<4} {:>8}\n".format("GAME", "WGT", "%")
        string += "-" * 46
        string += "\n"
        for game, percentage in sorted(self.weight_percentages().items(), key=lambda x:x[1], reverse=True):
            string += "{:<32} {:<4}  ~{:>6}\n".format(game, self["game"][game], "{:.1f}%".format(percentage * 100))

        return string

    def total_game_weights(self) -> int:
        total = 0
        for weight in self["game"].values():
            total += weight
        return total

    def weight_percentages(self) -> dict:
        total = self.total_game_weights()
        games = {}

        for game, weight in self["game"].items():
            games[game] = weight / total

        return games


def main():
    # Create output directory, if it does not exist.
    if not os.path.exists("output/"):
        os.mkdir("output/")

    # Delete any old mystery.yaml file, if it exists.
    if os.path.exists("output/mystery.yaml"):
        os.remove("output/mystery.yaml")

    # Load meta data first.
    mystery: dict
    print("Loading meta player settings...")
    try:
        with open("games/__meta__.yaml") as file:
            data = yaml.unsafe_load(file)
            mystery = MysterySettings(data["name"], data["description"], data["requires"], data["game"])
    except FileNotFoundError:
        print(Fore.RED + "__meta__.yaml not found. Please ensure file exists and rerun generator.")
        exit(3)

    print(f"Estimated chance of a particular game being rolled...\n\n{mystery}")
    print("Attempting to generate yaml file...")

    # Merge together each game yaml into our mystery settings.
    with open("output/mystery.yaml", "w+") as file:
        for game in mystery["game"].keys():
            try:
                print(f"Loading ./games/{game}.yaml...")
                with open(f"games/{game}.yaml") as game_file:
                    game_settings: dict = yaml.unsafe_load(game_file)

                    # Ensure that game_settings only has one property which has the same name as the file.
                    if len(game_settings.items()) > 1:
                        raise ValueError(f"Found {len(game_settings)} top-level keys in `./games/{game}.yaml`")
                    if game not in game_settings:
                        raise ValueError(f"Could not find `{game}` top-level key in `./games/{game}.yaml`")

                    mystery = {**mystery, **game_settings}
            except FileNotFoundError:
                print(Fore.RED + f"\nUnable to find game settings file `./games/{game}.yaml` in games directory.")
                exit(1)
            except ValueError as e:
                print(Fore.RED + f"\nGame settings dict should only have 1 key named after the game.\n\t{e}")
                exit(2)

        yaml.dump(mystery, file)
        print(Fore.GREEN + "\nOutputted settings file to `./output/mystery.yaml`")


if __name__ == "__main__":
    main()
