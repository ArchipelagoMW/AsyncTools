# AsyncTools

## Mystery Settings YAML Generator

To generate a mystery settings yaml with pre-determined settings in the `games` directory, run `python GenerateMystery.py`. A file will be created in the `output` directory that can then be used to generate filler seeds for Archipelago Asyncs (or whatever purposes you need it for).

### Add a new game to the MSYG

Create a `.yaml` file named after the game you are attempting to add and paste all the game settings into that file and place it inside the `games` directory. Then add the game to the `./games/__meta__.yaml` along with a specific weighting.

So for example, let's say you want to add settings for `Cool Game 2 - Electric Boogaloo`. Create a new file called `Cool Game 2 - Electric Boogaloo.yaml` and place it inside the `games` directory. Then inside that file, copy only the game-specific settings inside. Should look something like this:

```yaml
Cool Game 2 - Electric Boogaloo:
  option_1:
    setting_1: 5
    setting_2: 3
    setting_3: 1
  option_2: true
  option_3: false
  death_link: true
```

Then, in `./games/__meta__.yaml`, add the game along with a weighting for it:

```yaml
name: Player{player}
description: Archipelago Async Mystery Filler Settings
requires:
  version: 0.3.2
  plando: bosses, items, texts, connections

# Define your game here!
game:
  A Link to the Past: 150
  # ...
  Cool Game 2 - Electric Boogaloo: 50

```

Now you can generate `weights.yaml` and `games.yaml` by running `python GenerateMystery.py`

### Update an existing game's settings

To update an existing game's settings, just open the corresponding game file in the `games` directory and make the desired tweaks and save the file.

To update the weighting for a particular game being rolled, open the `./games/__meta__.yaml` file and adjust the number for how much that game is weighted and save the file.

Then run `python GenerateMystery.py` to generate a new `weights.yaml` file.

## YAML Output Converter

`// TODO, write whatever this does`