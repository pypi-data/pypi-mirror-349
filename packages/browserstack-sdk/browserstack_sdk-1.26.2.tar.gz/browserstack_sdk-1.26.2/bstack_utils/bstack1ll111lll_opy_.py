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
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll1ll11l1_opy_ import bstack11ll1ll1ll1_opy_
from bstack_utils.constants import *
import json
class bstack1ll1111ll_opy_:
    def __init__(self, bstack111l1l1l_opy_, bstack11ll1ll111l_opy_):
        self.bstack111l1l1l_opy_ = bstack111l1l1l_opy_
        self.bstack11ll1ll111l_opy_ = bstack11ll1ll111l_opy_
        self.bstack11ll1ll1l11_opy_ = None
    def __call__(self):
        bstack11ll1l1lll1_opy_ = {}
        while True:
            self.bstack11ll1ll1l11_opy_ = bstack11ll1l1lll1_opy_.get(
                bstack111l11_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧᛔ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll1ll11ll_opy_ = self.bstack11ll1ll1l11_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll1ll11ll_opy_ > 0:
                sleep(bstack11ll1ll11ll_opy_ / 1000)
            params = {
                bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᛕ"): self.bstack111l1l1l_opy_,
                bstack111l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᛖ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11ll1ll1111_opy_ = bstack111l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᛗ") + bstack11ll1ll1l1l_opy_ + bstack111l11_opy_ (u"ࠥ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࠢᛘ")
            if self.bstack11ll1ll111l_opy_.lower() == bstack111l11_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡷࠧᛙ"):
                bstack11ll1l1lll1_opy_ = bstack11ll1ll1ll1_opy_.results(bstack11ll1ll1111_opy_, params)
            else:
                bstack11ll1l1lll1_opy_ = bstack11ll1ll1ll1_opy_.bstack11ll1l1llll_opy_(bstack11ll1ll1111_opy_, params)
            if str(bstack11ll1l1lll1_opy_.get(bstack111l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᛚ"), bstack111l11_opy_ (u"࠭࠲࠱࠲ࠪᛛ"))) != bstack111l11_opy_ (u"ࠧ࠵࠲࠷ࠫᛜ"):
                break
        return bstack11ll1l1lll1_opy_.get(bstack111l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᛝ"), bstack11ll1l1lll1_opy_)