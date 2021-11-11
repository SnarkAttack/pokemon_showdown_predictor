
import abc
from re import S, split

# Abstract Classes

class ShowdownMessage(abc.ABC):

    def __init__(self, message_str):
        self.message_str = message_str
        self.frm = None
        self.of = None

    def set_from(self, frm):
        self.frm = frm

    def set_of(self, of):
        self.of = of

class PokemonBasedMessage(ShowdownMessage, abc.ABC):

    split_chars = ": "

    def __init__(self, message_str, pokemon):
        super().__init__(message_str)

        self.position, self.name = pokemon.split(self.split_chars)

    @property
    def pokemon(self):
        return self.split_chars.join([self.position, self.name])

    @property
    def player(self):
        return self.position[:-1]

class PokemonTargetMessage(PokemonBasedMessage, abc.ABC):

    def __init__(self, message_str, pokemon, target):
        super().__init__(message_str, pokemon)
        self.target = target

class ChangeMessage(PokemonBasedMessage, abc.ABC):

    def __init__(self, message_str, pokemon, details, hp_status):
        super().__init__(message_str, pokemon)
        self.details = details
        self.hp_status = hp_status

class BoostInfoMessage(PokemonBasedMessage, abc.ABC):

    def __init__(self, message_str, pokemon, stat, amount):
        super().__init__(message_str, pokemon)
        self.stat = stat
        self.amount = amount

class ConditionMessage(ShowdownMessage, abc.ABC):

    def __init__(self, message_str, condition):
        super().__init__(message_str)
        self.condition = condition

class SideConditionMessage(ConditionMessage, abc.ABC):

    def __init__(self, message_str, side, condition):
        super().__init__(message_str, condition)
        self.side = side

class PokemonHPMessage(PokemonBasedMessage, abc.ABC):

    def __init__(self, message_str, pokemon, hp_status):
        super().__init__(message_str, pokemon)
        self.hp_status = hp_status

class PokemonEffectMessage(PokemonBasedMessage, abc.ABC):

    def __init__(self, message_str, pokemon, effect, of=None):
        super().__init__(message_str, pokemon)
        self.effect = effect
        self.of = of

class PokemonStatusMessage(PokemonEffectMessage, abc.ABC):

    def __init__(self, message_str, pokemon, effect):
        super().__init__(message_str, pokemon, effect)

    @property
    def status(self):
        return self.effect

class ItemBasedMessage(PokemonEffectMessage, abc.ABC):

    def __init__(self, message_str, pokemon, item, effect):
        super().__init__(message_str, pokemon, effect)
        self.item = item

class AbilityBasedMessage(PokemonEffectMessage, abc.ABC):

    def __init__(self, message_str, pokemon, ability, effect):
        super().__init__(message_str, pokemon, effect)
        self.ability = ability

    @property
    def source(self):
        return self.pokemon

# MessageMessage is used both for miscellaneoius messages (as decribed by POkemon Showdown)
# as well as as base class for message only, subclasses

class MessageMessage(ShowdownMessage):

    def __init__(self, message, message_str="-message"):
        super().__init__(message_str)
        self.message = message

# Battle Initialization Messages

class PlayerMessage(ShowdownMessage):

    def __init__(self, player, username, avatar, rating):
        super().__init__("player")
        self.player = player
        self.username = username
        self.avatar = avatar
        self.rating = rating

class TeamsizeMessage(ShowdownMessage):

    def __init__(self, player, number):
        super().__init__("teamsize")
        self.player = player
        self.number = number

class GametypeMessage(ShowdownMessage):

    def __init__(self, gametype):
        super().__init__("gametype")
        self.gametype = gametype

class GenMessage(ShowdownMessage):

    def __init__(self, gennum):
        super().__init__("gen")
        self.gennum = gennum

class TierMessage(ShowdownMessage):

    def __init__(self, formatname):
        super().__init__("tier")
        self.formatname = formatname

class RatedMessage(MessageMessage):

    def __init__(self, message=None):
        super().__init__("rated", message)

class RuleMessage(ShowdownMessage):

    def __init__(self, rule):
        super().__init__("rule")

        self.rule, self.description = rule.split(': ')

class ClearPokeMessage(ShowdownMessage):

    def __init__(self):
        super().__init__("clearpoke")

class PokeMessage(ShowdownMessage):

    split_chars = ", "

    def __init__(self, player, details, item):
        super().__init__("poke")
        self.player = player
        self.item = item

        pokemon_details = details.split(self.split_chars)

        self.name = pokemon_details[0]
        self.level = pokemon_details[1][1:]

        if len(pokemon_details) == 3:
            self.gender = pokemon_details[2]
        else:
            self.gender = None

    @property
    def details(self):
        to_concat = [self.name, self.level]
        if self.gender is not None:
            to_concat.append(self.gender)

        self.split_chars.join(to_concat)

class StartMessage(ShowdownMessage):

    def __init__(self):
        super().__init__("start")

# Battle Progress Messages

class SpacerMessage(ShowdownMessage):

    def __init__(self):
        super().__init__("")

class RequestMessage(ShowdownMessage):

    def __init__(self, request):
        super().__init__("request")
        self.request = request

class InactiveMessage(MessageMessage):

    def __init__(self, message):
        super().__init__("inactive", message)

class InactiveOffMessage(MessageMessage):

    def __init__(self, message):
        super().__init__("inactiveoff", message)

class UpkeepMessage(ShowdownMessage):

    def __init__(self):
        super().__init__("upkeep")

class TurnMessage(ShowdownMessage):

    def __init__(self, number):
        super().__init__("turn")
        self.number = number

class WinMessage(ShowdownMessage):

    def __init__(self, user):
        super().__init__("win")
        self.user = user

class TieMessage(ShowdownMessage):

    def __init__(self):
        super().__init__("tie")

class TimeMessage(ShowdownMessage):
    
    def __init__(self, timestamp):
        super().__init__("t:")
        self.timestamp = timestamp

# Major Action Messages

class MoveMessage(PokemonTargetMessage):

    def __init__(self, pokemon, move, target, info=None):
        # Info field can collect things like spread move info
        super().__init__("move", pokemon, target)
        self.move = move
        self.info = info

class SwitchMessage(ChangeMessage):

    def __init__(self, pokemon, details, hp_status):
        super().__init__("switch", pokemon, details, hp_status)

class DragMessage(ChangeMessage):

    def __init__(self, pokemon, details, hp_status):
        super().__init__("drag", pokemon, details, hp_status)

class DetailsChangeMessage(ChangeMessage):

    def __init__(self, pokemon, details, hp_status):
        super().__init__("detailschange", pokemon, details, hp_status)

class FormeChangeMessage(ChangeMessage):

    def __init__(self, pokemon, species, hp_status):
        super().__init__("-formechange", pokemon, species, hp_status)

    @property
    def species(self):
        return self.details

class ReplaceMessage(ChangeMessage):

    def __init__(self, pokemon, details, hp_status):
        super().__init__("replace", pokemon, details, hp_status)

class SwapMessage(PokemonBasedMessage):

    def __init__(self, pokemon, position):
        super.__init__("swap", pokemon)
        self.position = position

class CantMessage(PokemonBasedMessage):

    def __init__(self, pokemon, reason, move=None):
        super().__init__("cant", pokemon)
        self.reason = reason
        self.move = move

class FaintMessage(PokemonBasedMessage):

    def __init__(self, pokemon):
        super().__init__("faint", pokemon)

# Minor Action Messages

class FailMessage(PokemonBasedMessage):

    def __init__(self, pokemon, action):
        super().__init__("-fail", pokemon)
        self.action = action

class BlockMessage(PokemonBasedMessage):

    def __init__(self, pokemon, effect, move, attacker):
        super().__init__("-block", pokemon)
        self.effect = effect
        self.move = move
        self.attacker = attacker

class NoTargetMessage(PokemonBasedMessage):

    def __init__(self, pokemon):
        super().__init__("-notarget", pokemon)

class MissMessage(PokemonTargetMessage):

    def __init__(self, source, target):
        super().__init__("-miss", source, target)

    @property
    def source(self):
        return self.pokemon

class DamageMessage(PokemonHPMessage):

    def __init__(self, pokemon, hp_status):
        super().__init__("-damage", pokemon, hp_status)

class HealMessage(PokemonHPMessage):

    def __init__(self, pokemon, hp_status, info=None):
        # Info field is here to catch [silent] command from dynamaxing,
        # we never actually use it
        super().__init__("-heal", pokemon, hp_status)

class SetHPMessage(PokemonBasedMessage):

    def __init__(self, pokemon, hp):
        super().__init__("-sethp", pokemon)
        self.hp = hp

class StatusMessage(PokemonStatusMessage):

    def __init__(self, pokemon, status):
        super().__init__("-status", pokemon, status)

class CureStatusMessage(PokemonStatusMessage):

    def __init__(self, pokemon, status):
        super().__init__("-curestatus", pokemon, status)

class CureTeamMessage(PokemonBasedMessage):

    def __init__(self, pokemon):
        super().__init__('-cureteam', pokemon)

class BoostMessage(BoostInfoMessage):

    def __init__(self, pokemon, stat, amount):
        super().__init__('-boost', pokemon, stat, amount)

class UnboostMessage(BoostInfoMessage):

    def __init__(self, pokemon, stat, amount): 
        super().__init__('-unboost', pokemon, stat, amount)

class SetBoostMessage(BoostInfoMessage):

    def __init__(self, pokemon, stat, amount):
        super().__init__('-setboost', pokemon, stat, amount)

class SwapBoostMessage(PokemonTargetMessage):

    def __init__(self, source, target, stats):
        super().__init__("-swapboost", source, target)
        self.stats = stats

    @property
    def source(self):
        return self.pokemon

class InvertBoostMessage(PokemonBasedMessage):

    def __init__(self, pokemon):
        super().__init__("-invertboost", pokemon)

class ClearBoostMessage(PokemonBasedMessage):

    def __init__(self, pokemon):
        super().__init__("-clearboost", pokemon)

class ClearAllBoostMessage(ShowdownMessage):

    def __init__(self):
        super().__init__("-clearallboost")

class ClearPositiveBoostMessage(PokemonTargetMessage):

    def __init__(self, target, pokemon, effect):
        super().__init__("-clearpositiveboost", pokemon, target)
        self.effect = effect

class ClearNegativeBoostMessage(PokemonBasedMessage):

    def __init__(self, pokemon):
        super().__init__("-clearngativeboost", pokemon)

class CopyBoostMessage(PokemonTargetMessage):

    def __init__(self, pokemon, target):
        super().__init__("-copyboost", pokemon, target)

class WeatherMessage(ShowdownMessage):

    def __init__(self, weather, upkeep=None):
        super().__init__("-weather")
        self.weather = weather
        self.upkeep = upkeep

class FieldStartMessage(ConditionMessage):

    def __init__(self, condition):
        super().__init__("-fieldstart", condition)

class FieldEndMessage(ConditionMessage):

    def __init__(self, condition):
        super().__init__("-fieldend", condition)

class SideStartMessage(SideConditionMessage):

    def __init__(self, side, condition):
        super().__init__("-sidestart", side, condition)

class SideEndMessage(SideConditionMessage):

    def __init__(self, side, condition):
        super().__init__("-sideend", side, condition)

class SwapSideConditionsMessage(ShowdownMessage):

    def __init__(self):
        super().__init__("-swapsideconditions")

class StartEffectMessage(PokemonEffectMessage):

    def __init__(self, pokemon, effect, of=None):
        super().__init__("-start", pokemon, effect, of)

class EndEffectMessage(PokemonEffectMessage):

    def __init__(self, pokemon, effect, of=None):
        super().__init__("-end", pokemon, effect, of)

class CritMessage(PokemonBasedMessage):

    def __init__(self, pokemon):
        super().__init__("-crit", pokemon)

class SuperEffectiveMessage(PokemonBasedMessage):

    def __init__(self, pokemon):
        super().__init__("-supereffective", pokemon)

class ResistedMessage(PokemonBasedMessage):

    def __init__(self, pokemon):
        super().__init__("-resisted", pokemon)

class ImmuneMessage(PokemonBasedMessage):

    def __init__(self, pokemon):
        super().__init__("-immune", pokemon)

class ItemMessage(ItemBasedMessage):
    
    def __init__(self, pokemon, item, effect=None):
        super().__init__("-item", pokemon, item, effect)

class EndItemMessage(ItemBasedMessage):

    def __init__(self, pokemon, item, effect=None):
        super().__init__("-enditem", pokemon, item, effect)

class AbilityMessage(AbilityBasedMessage):

    def __init__(self, pokemon, ability, effect):
        super().__init__("-ability", pokemon, ability, effect)

class EndAbilityMessage(PokemonBasedMessage):

    def __init__(self, pokemon):
        super().__init__("-endability", pokemon)

class TransformMessage(PokemonBasedMessage):

    def __init__(self, pokemon):
        super().__init__("-transform", pokemon)

class MegaMessage(PokemonBasedMessage):

    def __init__(self, pokemon, megastone):
        super().__init__("-mega", pokemon)
        self.megastone = megastone

class PrimalMessage(PokemonBasedMessage):

    def __init__(self, pokemon):
        super().__init__("-primal", pokemon)

class BurstMessage(PokemonBasedMessage):

    def __init__(self, pokemon, species, item):
        super().__init__('-burst', pokemon)
        self.species = species
        self.item = item

class ZPowerMessage(PokemonBasedMessage):
    
    def __init__(self, pokemon):
        super().__init__("-zpower", pokemon)

class ZBrokenMessage(PokemonBasedMessage):

    def __init__(self, pokemon):
        super().__init__("-zbroken", pokemon)

class ActivateMessage(ShowdownMessage):

    def __init__(self, effect, cause=None):
        super().__init__("-activate")
        self.effect = effect
        self.cause = None

class HintMessage(ShowdownMessage):

    def __init__(self, message):
        super().__init__("-hint")
        self.message = message

class CenterMessage(ShowdownMessage):

    def __init__(self):
        super().__init__("-center")

# MessageMessage is defined above as it is a superclass to others

class CombineMessage(ShowdownMessage):

    def __init__(self):
        super().__init__("-combine")

class WaitingMessage(PokemonTargetMessage):

    def __init__(self, source, target):
        super().__init__("-waiting", source, target)

class PrepareMessage(PokemonTargetMessage):

    def __init__(self, attacker, move, defender=None):
        super().__init__("-prepare", attacker, defender)
        self.move = move

class MustRechargeMessage(PokemonBasedMessage):

    def __init__(self, pokemon):
        super().__init__("-mustrecharge", pokemon)

class NothingMessage(ShowdownMessage):

    def __init__(self):
        super().__init__("-nothing")

class HitCountMessage(PokemonBasedMessage):

    def __init__(self, pokemon, num):
        super().__init__("-hitcount", pokemon)
        self.num = num

class SingleMoveMessage(PokemonBasedMessage):

    def __init__(self, pokemon, move):
        super().__init__("-singlemove", pokemon)
        self.move = move

class SingleTurnMessage(PokemonBasedMessage):

    def __init__(self, pokemon, move):
        super().__init__("-singleturn", pokemon)
        self.move = move

class_lookup = {
    "player": PlayerMessage,
    "teamsize": TeamsizeMessage,
    "gametype": GametypeMessage,
    "gen": GenMessage,
    "tier": TierMessage,
    "rated": RatedMessage,
    "rule": RuleMessage,
    "clearpoke": ClearPokeMessage,
    "poke": PokeMessage,
    "start": StartMessage,
    "request": RequestMessage,
    "inactive": InactiveMessage,
    "inactiveoff": InactiveOffMessage,
    "upkeep": UpkeepMessage,
    "turn": TurnMessage,
    "win": WinMessage,
    "tie": TieMessage,
    "t:": TimeMessage,
    "move": MoveMessage,
    "switch": SwitchMessage,
    "drag": DragMessage,
    "detailschange": DetailsChangeMessage,
    "-formchange": FormeChangeMessage,
    "replace": ReplaceMessage,
    "swap": SwapMessage,
    "cant": CantMessage,
    "faint": FaintMessage,
    "-fail": FailMessage,
    "-block": BlockMessage,
    "-notarget": NoTargetMessage,
    "-miss": MissMessage,
    "-damage": DamageMessage,
    "-heal": HealMessage,
    "-sethp": SetHPMessage,
    "-status": StatusMessage,
    "-curestatus": CureStatusMessage,
    "-cureteam": CureTeamMessage,
    "-boost": BoostMessage,
    "-unboost": UnboostMessage,
    "-swapboost": SwapBoostMessage,
    "-invertboost": InvertBoostMessage,
    "-clearboost": ClearBoostMessage,
    "-clearallboost": ClearAllBoostMessage,
    "-clearpositiveboost": ClearPositiveBoostMessage,
    "-clearnegativeboost": ClearNegativeBoostMessage,
    "-copyboost": CopyBoostMessage,
    "-weather": WeatherMessage,
    "-fieldstart": FieldStartMessage,
    "-fieldend": FieldEndMessage,
    "-sidestart": SideStartMessage,
    "-sideend": SideEndMessage,
    "-swapsideconditions": SwapSideConditionsMessage,
    "-start": StartEffectMessage,
    "-end": EndEffectMessage,
    "-crit": CritMessage,
    "-supereffective": SuperEffectiveMessage,
    "-resisted": ResistedMessage,
    "-immune": ImmuneMessage,
    "-item": ItemMessage,
    "-enditem": EndItemMessage,
    "-ability": AbilityMessage,
    "-endability": EndAbilityMessage,
    "-transform": TransformMessage,
    "-mega": MegaMessage,
    "-primal": PrimalMessage,
    "-burst": BurstMessage,
    "-zpower": ZPowerMessage,
    "-zbroken": ZBrokenMessage,
    "-activate": ActivateMessage,
    "-hint": HintMessage,
    "-center": CenterMessage,
    "-message": MessageMessage,
    "-combine": CombineMessage,
    "-waiting": WaitingMessage,
    "-prepare": PrepareMessage,
    "-mustrecharge": MustRechargeMessage,
    "-nothing": NothingMessage,
    "-hitcount": HitCountMessage,
    "-singlemove": SingleMoveMessage,
    "-singleturn": SingleTurnMessage
}

def check_for_special_value(split_message, special_val):

    for idx, s in enumerate(split_message):
        if special_val in s:
            return idx

    return -1

def generate_replay_commands(battle_messages):

    match_history = []

    for message in battle_messages:

        if message == '|':
            continue

        split_message = message.split('|')

        if len(split_message) <= 1:
            print(message)
            continue

        from_text = None
        of_text = None

        from_idx = check_for_special_value(split_message, '[from]')
        if from_idx != -1:
            from_text = split_message[from_idx]
            del split_message[from_idx]

        of_idx = check_for_special_value(split_message, '[of]')
        if of_idx != -1:
            of_text = split_message[of_idx]
            del split_message[of_idx]

        cls = class_lookup.get(split_message[1], None)
        if cls is None:
            print(f"Unknown command: {message}")
            continue
        #print(f"Class: {cls}, text: {message}")

        msg_cls = cls(*split_message[2:])
        if from_text is not None:
            msg_cls.set_from(from_text)
        if of_text is not None:
            msg_cls.set_of(of_text)

        match_history.append(msg_cls)

    return match_history
        


