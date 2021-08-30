# It is temporary so setting up the database only in this plugin...|SQL|

from sqlalchemy import Column, String, UnicodeText

from userbot.sql_helper import BASE, SESSION

import os

class Railway_Variables(BASE):

    __tablename__ = "Variables_Railway"

    VarName = Column(String(14), primary_key=True)

    Value = Column(UnicodeText, primary_key=True)

    

    def __init__(self, VarName, Value):

        self.Key = VarName

        self.Value = Value

        

Railway_Variables.__table__.create(checkfirst=True)

async def is_set(key):

    """Basically to check if the var is already there or not."""

    try:

        _result = SESSION.query(Railway_Variables).get(key)

        if _result:

            return True

        return None

    finally:

        SESSION.close()

        

async def set_var(key, value):

    """To insert a key and value in the table."""

    to_check = is_set(key)

    if to_check:

        value_match = SESSION.query(Railway_Variables).get(value)

        if value != value_match:

            rem = SESSION.query(Railway_Variables).get(key)

            SESSION.delete(rem)

            SESSION.commit()

            variable = Railway_Variables(key, value)

            SESSION.add(variable)

            SESSION.commit()

            return True

        return False

    variable = Railway_Variables(key, value)

    SESSION.add(variable)

    SESSION.commit()

    return True

async def del_var(key):

    """To delete the variable."""

    to_check = is_set(key)

    if not to_check:

        if await get_var(key):

            return "Click Clack!"

        return False

    rem = SESSION.query(Railway_Variables).get(key)

    SESSION.delete(rem)

    SESSION.commit()

    return Trueasync def del_var(key):

    """To delete the variable."""

    to_check = is_set(key)

    if not to_check:

        if await get_var(key):

            return "Click Clack!"

        return False

    rem = SESSION.query(Railway_Variables).get(key)

    SESSION.delete(rem)

    SESSION.commit()

    return True

async def get_var(key):

    """To get the value of the var"""

    to_check = is_set(key)

    ext_value = os.environ.get(key, None)

    if not to_check:

        if not ext_value:

            return False

        return ext_value

    value = SESSION.query(Railway_Variables).get(value)

    SESSION.close()

    return value

# X----------------------------------------------------------------------X #

from userbot import catub

from ..Config import Config

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "tools"

cmdhd = Config.COMMAND_HAND_LER

tr = cmdhd

@catub.cat_cmd(

    pattern="(set|get|del railway var ([\s\S]*)",

    command=("railwayvar", plugin_category),

    info={

        "header": "To manage railway variables.",

        "flags": {

            "set": "To set a new variable or modify an old one.",

            "get": "To get the value of a variable.",

            "del": "To delete a variable"

        },

        "usage": [

            "{tr}set railway var <var name> <var value>",

            "{tr}get railway var <var name>",

            "{tr}del railway var <var name"

        ],

        "examples": [

            "{tr}get railway var ALIVE_NAME",

            "{tr}set railway var ALIVE_NAME Cat User"

        ]

    }

)

async def railway_variable(rvar):

    """To play with variables🙂"""

    exe = rvar.pattern_match.group(1)

    BOTLOG_CHATID = Config.BOTLOG_CHATID

    

    

    if exe == "set":

        key = rvar.pattern_match.group(2)

        value = rvar.pattern_match.group(3)

        

        if not key or not value:

            return await edit_or_reply(

                var,

                f"__Try typing__ `{tr}help railwayvar` __before proceeding further .__\n"

                "__If you still don't get it, then you should try using this 🔫 on yourself.__"

            )

        

        if not await set_var(key, value):

            return await edit_delete(

                var,

                "__You have already set this var with the same value.__"

            )

                

        await set_var(key, value)

        await edit_delete(var, f"`{key}` **successfully set to  ->  **`value`")

        return await var.client.send_message(

            BOTLOG_CHATID,

            "#RAILWAY_VARIABLE\n\n"

            "**Variable has been set!!**\n"

            f"Variable Name: {key}\n"

            f"Variable Value: {value}"

        )

    

    

    if exe == "get":

        key = rvar.pattern_match.group(2)

        

        if not key:

            return await edit_or_reply(

                var,

                f"__Try typing__ `{tr}help railwayvar` __before proceeding further .__\n"

                "__If you stil don't get it, then you should try using this 🔫 on yourself.__"

            )

        

        if not await get_var(key):

            return await edit_delete(

                var,

                f"__I couldn't find `{key}` __variable. I guess you haven't set that yet.__"

            )

        

        value = await get_var(key)

        return await edit_or_reply(

            var,

            "**ConfigVars:**"

            f"\n\n`{key}` = `{value}`\n"

        )

    

    

    if exe == "del":

        key = rvar.pattern_match.group(2)

        

        if not key:

            return await edit_or_reply(

                var,

                f"__Try typing__ `{tr}help railwayvar` __before proceeding further .__\n"

                "__If you stil don't get it, then you should try using this 🔫 on yourself.__"

            )

        

        if await del_var(key) == "Click Clack!":

            return await edit_or_reply(

                var,

                f"**Error:**\n __I can't delete__ `{key}` __variable. Please delete it manually from__ railway.app"

            )

        

        if not await del_var(key):

            return await edit_reply(var, f"__First set the variable by__ `{tr}set railway var {key} <some value>`")

        

        value = await get_var(key)

        await del_var(key)

        await edit_delete(var, "Successfully deleted the variable " + key)

        return await var.client.send_message(

            BOTLOG_CHATID,

            "#RAILWAY_VARIABLE\n\n"

            "**Variable has been deleted!!**\n"

            f"Variable Name: {key}\n"

            f"Variable Value: {value}"

        )
