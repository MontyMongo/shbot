from src.SH.definitions import *
from src.SH.components import *
from src.SH.components.component_base import SHGameComponent

import discord

class SHGameComponentPolicy_powerExecute (SHGameComponent):

    async def __init__(self, parent, client):
        super(SHGameComponentPolicy_powerExecute, self).__init__(parent=parent, client=client)
        # ...

    async def Setup(self):
        _msg = "You must execute a player."
        self.private_message = await self.parent.message_seat(self.parent.get("s_president"), content=_msg)
        # Add all of the seats to their name
        for i in range(self.parent.size):
            await self.private_message.add_reaction(self.parent.request_emoji(i + 1))

    async def Handle(self, context):
        if context[0] == "message":
            # TODO allow people to type in text as well?
            pass
        # if they added a reaction
        elif context[0] == "reaction" and context[3] == "add":
            _event = context[1]
            _message = context[2]
            _target = self.parent.request_emoji_value(_event.emoji)

            if _target != None and self.is_legal_pick(_target):
                _pres = self.parent.get("s_president")
                _role = self.parent.s_seats[_target]["role"]
                _msg = "You execute player " + self.parent.s_seats[_target]["name"] + "."

                await self.parent.message_seat(_pres, content=_msg)
                
                await self.parent.message_main(content="President " + self.parent.s_seats[_pres]["name"] + " chooses to execute " + 
                                                " player " + self.parent.s_seats[_target]["name"] + ".")
                
                self.parent.s_seats[_target]["alive"] = False
                self.parent.set("alive_players", self.parent.get("alive_players") - 1)
                if self.parent.s_seats[_target]["role"] == HITLER:
                    self.parent.set("game_over", True)
                    self.parent.set("win_condition", HITLER_EXECUTED)
                    self.parent.UpdateToComponent("premise", False)

                # TODO remove chat perms of dead player

                self.parent.UpdateToComponent("post_policy", False)
                return
            else:
                await self.parent.message_seat(self.parent.get("s_president"), content="Illegal pick.")

    async def Teardown(self):
        pass

    # TODO 
    def is_legal_pick(self, s_seat_num):
        return 1