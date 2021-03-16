from src.SH.definitions import *
from src.SH.components import *
from src.SH.components.component_base import SHGameComponent

class SHGameComponentPost_policyNo_op (SHGameComponent):


    async def __init__(self, parent, client):
        super(SHGameComponentPost_policyNo_op, self).__init__(parent=parent, client=client)
        # ...

    async def Setup(self):
        _board = self.parent.board
        _last_policy_played = _board.lastPolicy
        if _board.policiesPlayed[_last_policy_played] >= _board.board_lengths[_last_policy_played]:
            if _last_policy_played == LIBERAL_POLICY:
                self.parent.set("win_condition", LIBERAL_POLICY_VICTORY)
                self.parent.set("game_over", True)
                self.parent.UpdateToComponent("premise", False)
                await self.parent.Handle(None)
            elif _last_policy_played == FASCIST_POLICY:
                self.parent.set("win_condition", FASCIST_POLICY_VICTORY)
                self.parent.set("game_over", True)
                self.parent.UpdateToComponent("premise", False)
                await self.parent.Handle(None)
            else:
                print ("error in post policy")
        else:
            self.parent.UpdateToComponent("tracker")
            await self.parent.Handle(None)
        

    async def Handle(self, context):
        pass

    async def Teardown(self):
        pass
