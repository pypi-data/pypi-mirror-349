from flet import Page, View
from .FlowViewFtState import FlowViewFtState
from .FlowViewFtParams import FlowViewFtParams
from typing import Optional

class FlowViewFtView:
    def __init__(
            self, 
            page: Page, 
            state: Optional[FlowViewFtState] = None, 
            params: Optional[FlowViewFtParams] = None
        ):
        self.page = page
        self.state = state
        self.params = params
        self.debug = False
        self.error = ""

    def build(self) -> View:
        raise NotImplementedError("You must implement the build() method.")

    def onBuildComplete(self):
        ...
