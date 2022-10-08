import aenum
from .bank import Effect
class Items(aenum.Enum):
    _init_ = "value __doc__ __name__"
    coin_multiplier = Effect.coin_booster(
        None
    )
class Coin_State(aenum.MultiValueEnum):
    heads = 1, "heads"
    tails = 0, "tails"

    def __str__(self):
        return self.name


class Shop(aenum.Enum):
    _init_ = "value __doc__ __name__"
    lucky_potion = 0, "Lucky Potion", "Lucky Potion"
    specific_lucky_potion = (
        1,
        "Lucky potion for a specific game",
        "Specific Lucky Potion",
    )
    frenzy_cash = 2, "Cash bonus multiplier", "Frenzy Cash"
    restart = 3, "Restart by remove all of your debt and unluckiness", "Restart"

    def __str__(self):
        return self.name.replace("_", " ").title()
