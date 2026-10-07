from dataclasses import dataclass


@dataclass
class GameLoop:
    game: Risk

    def handle_events(self):
        raise NotImplementedError
