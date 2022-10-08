import aenum
from .bank import Effect as Effect
from _typeshed import Incomplete

class Items(aenum.Enum):
    coin_multiplier: Incomplete
    wipe_effect: Incomplete
    lucky_potion: Incomplete

class Coin_State(aenum.MultiValueEnum):
    heads: Incomplete
    tails: Incomplete
