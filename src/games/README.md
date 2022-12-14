# Documentation for making a new game

Making a new game, for someone to bet currency on is pretty easy, some required functions and the rest is up to you.

NOTE: all commands listed in this file support both normal and slash commands

## Setting up the file

The file requires some functions and classes to work, after that everything is left up to you.

```py
# Minimum requirements
from discord.ext import commands
import discord

class gameTest:
    """
    Breif description of the game, will show in the dropdown.
    """
    def __init__(self, bot: commands.bot) -> None:
        # Default function, Setup and imports the rest of the bot
        self.bot = bot
        pass
    
    # This function is not required, but shows an emoji on the dropdown
    @property
    def display_emoji(self) -> str:
        return "🧪"
    
    # This is a required function, gets called once the bot is selected. Lets the bot do stuff
    def start(self, Interaction: discord.Interaction):
        pass

# Links this game with the rest of the bot
def game_setup(bot):
    return gameTest(bot)
```

The location of the file should be in `/src/games` (where this readme file is)

### Optional (But Highhly recommened) requirements

There are also other things that can be added to make the UX better, these are listed below.

#### Money Selector

These few lines open up a ui in discord that contains buttons to select how much more the user wants to bet on the games outcome. If you use this, module, then having Bank module is also highly recommended.

```py
# Money selector ui
from src.utils.MoneySelector import MoneySelector

def moneyCallback(Interaction: discord.Interaction, value: int):
    print(f"Retrieved {int}")

main = MoneySelector(Interaction, moneyCallback)
main.get_money()
```

#### Aliases and Name

There are other features that can be put in the class as well to save the user time or to make it look better.
Some of these features include aliases or modName.

Aliases lets the user enter one of the alvalible inputs for all of them to work, user has to enter less, win win.
modName just is there to make it look better. For example instead of sending `gameTest` to the user, they can send `game test` which looks better and can be easier to read. (It's called modName to avoid conflicts with other information)

modName works like another aliases to the normal view. But it also has another reason. By deafult, `gameTest` would be used for names of dropdowns and other small things. However having a `modName` tag, will use that instead of the class name. Making it look better in the dropdown menu whilst not breaking the python ruling system (no spaces in names of variables)

These **Must** go below the doc string otherwise the info wont work.

```py
class gameTest:
    aliases = ["test", "idk"]
    modName = "game test"
```

## Testing the file

Due to the nature of how these files are loaded, there is no need to restart the bot after each load, just run the command `{prefix}reloadgames`. You can also run `{prefix}reloadgames {game Module}` to reload one game.

NOTE: If the bot raises a warning saying that the file reloader might have broken, you might have to restart the whole bot.

This will reload all games currently loaded in,. No new games will be loaded though, that will need a bot restart. (Change?)

To test a game, run command `{prefix}playgame` and select the game that you would like to test from the dropdown option that appears.

## Error handling

These games have some default error handlering by default, but some will just completly break (Easier to let them raise an error as that iis more noticable than loggin an error).

### Error situtations (What errors and how to fix)

#### Exception 1: Failed to start game (Breaks)

Cause: a file in `/src/games` does not have the `start` function under the class.

Fix: create function `start` with paramaters `(self, Interaction)`

#### Exception 2: No description provided (Doesn't break)

View: Shows in the dropdown

Cause: A `__doc__` method wasn't found in the class

Fix: add a `__doc__` menu in the class (example above)

#### Exception 3: No Emoji Provided (Doesn't break)

View: Blank image in the dropdown menu

Cause: A `display_emoji` property wasn't found in the class

Fix: add a `display_emoji` property in the class (example above)

#### Other Errors

Cause: Probably something that you did, which the module couldn't load probably

Fix: Make sure you have the required above, if you do make sure that the module isn't broken itself (normally a bot restart can help you find the error better)

## Talking with the accountment system

Please read </src/utils/README.md> for more information

## Example files

If you ever need examples, check the other files in this folder (`/src/games`).
