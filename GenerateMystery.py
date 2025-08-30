import os
import yaml
from colorama import Fore
from datetime import date


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


class GameSettings(MysterySettings):
    def __init__(self, name: str, description: str, requires: dict, game: str, game_options: dict):
        super().__init__(name, description, requires, game)

        self[game] = game_options


def main():
    # Create output directory, if it does not exist.
    if not os.path.exists("output/"):
        os.mkdir("output/")

    # Delete any old mystery.yaml file, if it exists.
    if os.path.exists("output/mystery.yaml"):
        os.remove("output/mystery.yaml")

    # Load meta data first.
    mystery: dict
    meta: dict = {
        "meta_description": "Created by AsyncTools",
        None: {
            "progression_balancing": 0,
        }
    }
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
    for game in mystery["game"].keys():
        try:
            print(f"Loading ./games/{game}.yaml...")
            with open(f"games/{game}.yaml", encoding="utf-8-sig") as game_file:
                game_settings: dict = yaml.unsafe_load(game_file)

                # Ensure that game_settings only has one property which has the same name as the file.
                if len(game_settings.items()) > 1:
                    raise ValueError(f"Found {len(game_settings)} top-level keys in `./games/{game}.yaml`")
                if game not in game_settings:
                    raise ValueError(f"Could not find `{game}` top-level key in `./games/{game}.yaml`")
                
                # Allow for certain yaml options to be set during a specific month. Note that this is set at yaml creation, not at generation start.
                if "current_month" in game_settings[game]:
                    game_settings[game]["current_month"] = date.today().strftime("%B")

                mystery.update(game_settings)
        except FileNotFoundError:
            print(Fore.RED + f"\nUnable to find game settings file `./games/{game}.yaml` in games directory.")
            exit(1)
        except ValueError as e:
            print(Fore.RED + f"\nGame settings dict should only have 1 key named after the game.\n\t{e}")
            exit(2)
        meta_path = os.path.join("games", f"{game}.meta.yaml")
        if os.path.exists(meta_path):
            with open(meta_path) as meta_file:
                meta_settings: dict = yaml.unsafe_load(meta_file)
            if len(meta_settings.items()) > 1:
                raise ValueError(f"Found {len(meta_settings)} top-level keys in `{meta_path}`")
            if game not in meta_settings:
                raise ValueError(f"Could not find `{game}` top-level key in `{meta_path}`")
            meta.update(meta_settings)

    with open("output/weights.yaml", "w+") as file:
        yaml.dump(dict(mystery), file)
    with open("output/games.yaml", "w+") as file:
        games = list(mystery["game"])
        last_key = games[-1]
        for game in games:
            game_options = GameSettings(mystery["name"], mystery["description"], mystery["requires"], game, mystery[game])
            yaml.dump(dict(game_options), file)
            if game != last_key:
                file.write("\n---\n\n")
    print(Fore.GREEN + "\nOutputted settings file to `./output/weights.yaml`")
    meta_path = os.path.join("output", "meta.yaml")
    with open(meta_path, "w+") as file:
        yaml.dump(meta, file)
    print(Fore.GREEN + f"\nOutputted meta file to `{meta_path}`")


if __name__ == "__main__":
    main()
