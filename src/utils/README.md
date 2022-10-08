# One thing to notice about how bank system works

bank module is in `src.utils.bank` and it have a useful class called `Player_Status` and you can tinker around with it

## `Player_Status`

You can get player statuses like unluckiness/debts/money directly and informations will be saved automatically (how nice)  
And you can get player by user's id with `await Player_Status.get_by_id(user_id)` which returns a instance of class with data required like money,debt,unlucky and last_paid_debt and if the user isn't exist it will create new one in database immediately  
And you can get list of users in database with `await Player_Status.get_users()`

## `Effect`

A nice class for building information about effect that you want.

```py
from .utils import bank
bank.Effect.new_effect(
    effect_name: str,
    game_name: str
    effect_lucky_multiplier: float,
    effect_unlucky_multiplier: float,
    global_effect_lucky_multiplier: float,
    global_effect_unlucky_multiplier: float,
    coin_multiplier: float,
    global_coin_multiplier: float,
    expire_time: datetime
)
```

Game name is for specific game so you can know if effect activated for this game or not

I already have some preset for this! Don't worry!

```py

```

## example code

```py
from .utils import bank
from datetime import datetime
bank.bot = bot # REQUIRED

user = discord.User(...)
account = await bank.Player_Status.get_by_id(user.id)
print(account.user)
print(account.money)
print(account.debt)
print(account.unlucky)
print(account.last_paid_debt)

account.money -= 69 # saved to file automatically
account.last_paid_debt = datetime.now() # only accepts datetime object
account.unlucky += 0.2 # unlucky is in form of 0-1 decimal point

new_account = await bank.Player_Status.intialize_new_user(user.id) # fresh new account reset everything
if not member.id in await bank.Player_Status.get_users():
    await bank.Player_Status.intialize_new_user(user.id) # useful in intialize new user's data
```
