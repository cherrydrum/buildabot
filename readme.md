# Build-a-bot quickstart guide
Welcome to the readme of Build-a-bot - a Python module, designed for creating chatbots with ease. The design is similar to Flask: wrap your functions in decorators and see the magic happen.

## Step 1: Write .json state config file
First of all, you should describe the states of your bot. It is written in JSON format, just like this:

```
{
    "states": {

        "start": {
            "start": true,
            "unknown": ['Foo', 'Bar']
        },

        "next": {
            "unknown": ['Foo', 'Bar']
        }

    }
}
```

* Set "start" to **true** for the initial state.
* If bot fails from understanding user input, it will send random line from the "unknown" list.

## Step 2: Initialize the Speech class instance
Don't forget to import your JSON config!
```
import bot
speech = bot.Speech()
sppech.read_states_json('config.json')
```

## Step 2: Design your User class
**Your User class must have two functions: get_state() and set_state(). These functions will be called automatically as the state changes.**

## Step 3: Add some fancy functions
These functions should be the actions your bot will react with. **The first two arguments of the action functions are ALWAYS User object and User message!**

## Step 4: Wrap it in decorators!
Currenty you have 3 types of action decorators in your arsenal.
* ```@speech.greeting()``` - Call function if user does not have saved state (e.g. talking with bot for a first time).
* ```@speech.reaction(statename:str, keywords:list)``` - Call function if specified keyword is met in the message and the dialog is in specific state. Used for choosing one of the options.
* ```@speech.raw(statename:str)``` - Await for raw text input. Use this if you want to get telephones, names, addresses, everything that is not a set of keywords.

## Step 5: Initialize the event loop
All you need to do is call ```speech.process(user_object, message)``` to activate necessary functions. If your bot will fail to understand user input, this function will return a line from the 'unknown' list you have stated earlier.



