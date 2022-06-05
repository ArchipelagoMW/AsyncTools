from dataclasses import dataclass
from typing import Dict


@dataclass
class MysterySettings:
    name: str
    description: str
    requires: dict
    game: Dict[str, int]

    def __str__(self) -> str:
        string = "{:<32} {:<4} {:>8}\n".format("GAME", "WGT", "%")
        string += "-" * 46
        string += "\n"
        for game, percentage in sorted(self.weight_percentages().items(), key=lambda x:x[1], reverse=True):
            string += "{:<32} {:<4}  ~{:>6}\n".format(game, self.game[game], "{:.1f}%".format(percentage * 100))

        return string

    def total_game_weights(self) -> int:
        total = 0
        for weight in self.game.values():
            total += weight
        return total

    def weight_percentages(self) -> Dict[str, float]:
        total = self.total_game_weights()
        games: Dict[str, float] = {}

        for game, weight in self.game.items():
            games[game] = weight / total

        return games
