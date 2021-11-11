from html.parser import HTMLParser
from .showdown_protocol import PlayerMessage, PokeMessage, StartMessage, TurnMessage, WinMessage, generate_replay_commands

class BattleHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.active_reading = False
        self.battle_commands = []

    def handle_starttag(self, tag, attrs):
        if tag == 'script' and 'battle-log-data' in [attr[1] for attr in attrs]:
            self.active_reading = True

    def handle_endtag(self, tag):
        if tag == 'script':
            self.active_reading = False

    def handle_data(self, data):
        if self.active_reading:
            self.battle_commands.append(data)

def parse_replay_file(replay_file):

    with open(replay_file, 'r') as f:
        replay_data = f.read()

    parser = BattleHTMLParser()

    parser.feed(replay_data)

    return parser.battle_commands[0]

def parse_replay(replay_file):

    battle_text = parse_replay_file(replay_file)
    battle_commands_text = battle_text.split('\n')
    battle_commands = generate_replay_commands(battle_commands_text)

    return battle_commands

class ReplayProcessor(object):

    def __init__(self, battle_commands):

        self.battle_commands = battle_commands

        self.players = {}
        self.pokemon = {}

        self._populate_player_lookup()
        self._populate_pokemon_lookup()

        self.battle_state = {}

    def _get_all_commands_of_type(self, command_cls):

        return [(idx, command) for idx, command in enumerate(self.battle_commands) if isinstance(command, command_cls)]

    def _get_nth_command_of_type(self, command_cls, n):

        return self._get_all_commands_of_type(command_cls)[n]

    def _populate_player_lookup(self):

        player_commands = [pc[1] for pc in self._get_all_commands_of_type(PlayerMessage)]

        for pc in player_commands:
            self.players[pc.player] = {
                'username': pc.username,
                'rating': pc.rating
            }

    def _populate_pokemon_lookup(self):

        poke_commands = [pc[1] for pc in self._get_all_commands_of_type(PokeMessage)]

        self.pokemon = {k: {} for k in self.players.keys()}

        for pc in poke_commands:
            self.pokemon[pc.player][pc.name] = {
                'level': pc.level,
                'gender': pc.gender
            }

    def get_battle_initial_state(self):

        start_idx = self._get_nth_command_of_type(StartMessage, 0)[0]
        first_turn_idx = self._get_nth_command_of_type(TurnMessage, 0)[0]

        initial_setup = self.battle_commands[start_idx:first_turn_idx]

        return initial_setup

    def split_into_turns(self):

        tcis = [tc[0] for tc in self._get_all_commands_of_type(TurnMessage)]

        win_idx = self._get_nth_command_of_type(WinMessage, 0)[0]
        tcis.append(win_idx)

        turns = [self.battle_commands[tcis[i]: tcis[i+1]] for i in range(len(tcis)-1)]

        return turns

    def process_turn(self, turn):
        pass



    