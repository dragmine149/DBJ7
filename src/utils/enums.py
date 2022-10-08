import aenum

from .bank import Effect


class Items(aenum.Enum):
    _init_ = "value __doc__ __name__ __price__"
    _order_ = "coin_multiplier wipe_effect lucky_potion"
    coin_multiplier = (
        Effect.coin_multiplier(2),
        "Double your coins for 10 minutes",
        "coin multiplier",
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
