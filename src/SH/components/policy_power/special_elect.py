from src.SH.components import *
from src.SH.components.component_base import SHGameComponent

import discord

class SHGameComponentPolicy_powerSpecial_elect (SHGameComponent):

    async def __init__(self, parent, client):
        super(SHGameComponentPolicy_powerSpecial_elect, self).__init__(parent=parent, client=client)
        # ...

    async def Setup(self):
        _msg = "You must choose the next president."
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
            try:
                _event = context[1]
                _message = context[2]
                _target = self.parent.request_emoji_value(_event.emoji)

                if _target != None and self.is_legal_pick(_target):
                    _pres = self.parent.get("s_president")
                    #_role = self.parent.s_seats[_target]["role"]
                    _msg = "You choose to special elect " + self.parent.s_seats[_target]["name"] + "."
                    print(_msg)
                    _spec = self.parent.get("special_presidents")
                    _spec.append(_target)
                    print("here 2")
                    await self.parent.message_seat(_pres, content=_msg)
                    await self.parent.message_main(content="President " + self.parent.s_seats[_pres]["name"] + " chooses to special elect " + 
                                                    " player " + self.parent.s_seats[_target]["name"] + ".")
                    
                    self.parent.UpdateToComponent("post_policy", False)
                    return
                else:
                    await self.parent.message_seat(self.parent.get("s_president"), content="Illegal pick.")
            except Exception as e:
                print(e)
                return

    async def Teardown(self):
        pass

    # TODO 
    def is_legal_pick(self, s_seat_num):
        return 1