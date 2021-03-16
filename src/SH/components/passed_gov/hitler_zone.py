from src.SH.definitions import *
from src.SH.components.component_base import SHGameComponent
from src.utils import message as msg

class SHGameComponentPassed_govHitler_zone (SHGameComponent):

    async def __init__(self, parent, client):
        super( parent, client )
        # ...

    async def Setup(self, parent, client):
        ##
        # Appends this government to the gov history
        #
        parent.get("s_government_history").append((self.parent.get("s_president"), self.parent.get("s_chancellor")))

        if parent.s_seats[self.parent.get("s_chancellor")]["role"] == HITLER:
            self.parent.set("game_over", True)
            self.parent.set("win_condition", HITLER_ELECTED)
            self.parent.UpdateToComponent("premise", False)
            await self.parent.Handle(None)
        else:
            self.parent.UpdateToComponent("legislative", False)
            await self.parent.Handle(None)
        
    ##
    # Should not handle any events
    #
    async def Handle(self, context):
        pass

    async def Teardown(self):
        pass