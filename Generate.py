import os, yaml

from colorama import Fore
from Mystery import MysterySettings


# Define games and requirements here.
meta_settings = MysterySettings(
    name="Player{player}",
    description="Archipelago Async Mystery Filler Settings",
    requires={
        "version": "0.3.2",
        "plando": "bosses, items, text, connections"
    },
    game={
        "A Link to the Past": 150,
        "Factorio":            20,
        "Minecraft":           50,
        "Slay the Spire":      20,
        "Risk of Rain 2":      30,
        "Subnautica":           5,
        "Ocarina of Time":     40,
        "Timespinner":         50,
        "Secret of Evermore":  10,
        "Super Metroid":       30,
        "Rogue Legacy":        50,
        "Super Mario 64":      20,
        "VVVVVV":              20,
        "Meritous":            10,
        "SMZ3":                30,
    }
)


# Please don't look too closely at this code below. kthx -Phar
def main():
    # Create output directory, if it does not exist.
    if not os.path.exists("output/"):
        os.mkdir("output/")

    # Delete any old mystery.yaml file, if it exists.
    if os.path.exists("output/mystery.yaml"):
        os.remove("output/mystery.yaml")

    print(meta_settings)
    print("Attempting to generate yaml file...")

    # Merge together each game yaml into our mystery settings.
    with open("output/mystery.yaml", "w+") as file:
        mystery = {
            "name": meta_settings.name,
            "description": meta_settings.description,
            "requires": meta_settings.requires,
            "game": meta_settings.game
        }
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
