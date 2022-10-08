import aenum

from .bank import Effect


class Items(aenum.Enum):
    _init_ = "value __callme__ __doc__ __price__"
    _order_ = "coin_multiplier wipe_effect lucky_potion"
    coin_multiplier = (
        "coin multiplier",
        Effect.coin_multiplier(2),
        "Double your coins for 10 minutes",
        2000,
    )
    wipe_effect = Effect.wipe_effect(), "Wipe any effect you have", "wipe effect", 100
    lucky_potion = (
        Effect.lucky_potion(),
        "Increase your luck for 10 minutes",
        "lucky potion",
        10000,
    )

    def __str__(self):
        return self.name


class Coin_State(aenum.MultiValueEnum):
    heads = 1, "heads"
    tails = 0, "tails"

    def __str__(self):
        return self.name
