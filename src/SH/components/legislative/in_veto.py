from src.SH.definitions import *
from src.SH.components.component_base import SHGameComponent
from src.utils import message as msg

class SHGameComponentLegislativeIn_veto (SHGameComponent):

    async def __init__(self, parent, client):
        super(SHGameComponentLegislativeIn_veto, self).__init__(parent=parent, client=client)
        # ...

    async def Setup(self):
        self.draw = self.parent.deck.draw(3)
        await self.deal_to_president()

    async def Handle(self, context):
        if context[0] == "message":
            # TODO allow people to type in text as well?
            pass
        # if they added a reaction
        elif context[0] == "reaction" and context[3] == "add":
            _event = context[1]
            _message = context[2]
            _emoji_val = self.parent.request_emoji_value(_event.emoji)
            if _emoji_val == None:
                return
            if self.status == "await_president_discard" or self.status == "await_chancellor_discard":
                _card_pos = _emoji_val - 1
                _valid_discards = list(x for x in range(len(self.draw)))
                if _card_pos != None and _card_pos in _valid_discards:
                    if self.status == "await_president_discard":
                        _discarded_card = self.draw[_card_pos]
                        del self.draw[_card_pos]
                        self.parent.deck.discard_policy(_discarded_card)
                        await self.deal_to_chancellor()
                        return
                    elif self.status == "await_chancellor_discard":
                        _played_card = self.draw[_card_pos]
                        del self.draw[_card_pos]
                        for card_remaining in self.draw: # should always be 1 element only, but why not
                            self.parent.deck.discard_policy(card_remaining)
                        self.status = "await_chancellor_veto"

                        _veto_msg = self.parent.message_seat(self.parent.get("s_chancellor"), "Would you like to veto both of these policies?")
                        await _veto_msg.add_reaction(self.parent.request_emoji("ja"))
                        await _veto_msg.add_reaction(self.parent.request_emoji("nein"))

                        # await self.parent.enact_policy(_played_card, was_topdecked=False, fire_event=False)
                        return
                else:
                    if self.status == "await_president_discard":
                        await self.parent.message_seat(self.parent.get("s_president"), content="Illegal discard.")
                    elif self.status == "await_chancellor_discard":
                        await self.parent.message_seat(self.parent.get("s_chancellor"), content="Illegal discard.")
            # veto part
            elif self.status == "await_chancellor_veto":
                if _emoji_val == "ja":
                    self.status = "await_president_veto"
                    _veto_msg = self.parent.message_seat(self.parent.get("s_president"), "Would you like to veto both of these policies?")
                    await _veto_msg.add_reaction(self.parent.request_emoji("ja"))
                    await _veto_msg.add_reaction(self.parent.request_emoji("nein"))
                #TODO finish this
                    

            

    async def Teardown(self):
        pass

    ##
    # Shows the president their draw, and sets a flag
    # indicating that it is the president's turn to discard.
    # Could in theory be combined into one method with deal_to_chancellor
    # as much of the code is repeated.
    #
    async def deal_to_president(self):
        _fas_emoji = self.parent.request_emoji("F")
        _lib_emoji = self.parent.request_emoji("L")
        print("draw", self.draw)
        _draw_contents = ''.join([_fas_emoji if x == FASCIST_POLICY else _lib_emoji for x in self.draw])
        _message_content = "Your draw: " + _draw_contents + "\nChoose a policy to discard."
        self.private_message = await self.parent.message_seat(self.parent.get("s_president"), content=_message_content)
        self.status = "await_president_discard"
        for i in range(len(self.draw)):
            await self.private_message.add_reaction(self.parent.request_emoji(i + 1))

    ##
    # Shows the chancellor their draw, and sets a flag
    # indicating that it is the chancellor's turn to discard.
    #
    async def deal_to_chancellor(self):
        _fas_emoji = self.parent.request_emoji("F")
        _lib_emoji = self.parent.request_emoji("L")
        _draw_contents = ''.join([_fas_emoji if x == FASCIST_POLICY else _lib_emoji for x in self.draw])
        _message_content = "Your draw: " + _draw_contents + "\nChoose a policy to play."
        self.private_message = await self.parent.message_seat(self.parent.get("s_chancellor"), content=_message_content)
        self.status = "await_chancellor_discard"
        for i in range(len(self.draw)):
            await self.private_message.add_reaction(self.parent.request_emoji(i + 1))