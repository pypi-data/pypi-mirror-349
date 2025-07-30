# coding: UTF-8
import sys
bstack11l_opy_ = sys.version_info [0] == 2
bstack11l1_opy_ = 2048
bstack1l1l1l_opy_ = 7
def bstack111l11_opy_ (bstack111111l_opy_):
    global bstack11lllll_opy_
    bstack111l11l_opy_ = ord (bstack111111l_opy_ [-1])
    bstack11l1ll_opy_ = bstack111111l_opy_ [:-1]
    bstack11l11l1_opy_ = bstack111l11l_opy_ % len (bstack11l1ll_opy_)
    bstack11111ll_opy_ = bstack11l1ll_opy_ [:bstack11l11l1_opy_] + bstack11l1ll_opy_ [bstack11l11l1_opy_:]
    if bstack11l_opy_:
        bstack1llllll1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1_opy_ - (bstack11lll_opy_ + bstack111l11l_opy_) % bstack1l1l1l_opy_) for bstack11lll_opy_, char in enumerate (bstack11111ll_opy_)])
    else:
        bstack1llllll1_opy_ = str () .join ([chr (ord (char) - bstack11l1_opy_ - (bstack11lll_opy_ + bstack111l11l_opy_) % bstack1l1l1l_opy_) for bstack11lll_opy_, char in enumerate (bstack11111ll_opy_)])
    return eval (bstack1llllll1_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1lllllll11l_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1111111l1l_opy_:
    bstack1l111111l1l_opy_ = bstack111l11_opy_ (u"ࠦࡧ࡫࡮ࡤࡪࡰࡥࡷࡱࠢᕊ")
    context: bstack1lllllll11l_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1lllllll11l_opy_):
        self.context = context
        self.data = dict({bstack1111111l1l_opy_.bstack1l111111l1l_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᕋ"), bstack111l11_opy_ (u"࠭࠰ࠨᕌ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack111111llll_opy_(self, target: object):
        return bstack1111111l1l_opy_.create_context(target) == self.context
    def bstack1ll111llll1_opy_(self, context: bstack1lllllll11l_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1l1ll111l1_opy_(self, key: str, value: timedelta):
        self.data[bstack1111111l1l_opy_.bstack1l111111l1l_opy_][key] += value
    def bstack1ll1lll1l11_opy_(self) -> dict:
        return self.data[bstack1111111l1l_opy_.bstack1l111111l1l_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1lllllll11l_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )