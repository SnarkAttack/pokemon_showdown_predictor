from src.replay_management.process_replay import parse_replay, ReplayProcessor

battle_commands = parse_replay('replays/Gen8VGC2021Series11-2021-11-08-rustysurfer21-snarkattacks.html')
rp = ReplayProcessor(battle_commands)


init_state_commands = rp.get_battle_initial_state()

print(init_state_commands)

# turn_commands = rp.split_into_turns()

# print(len(turn_commands))

