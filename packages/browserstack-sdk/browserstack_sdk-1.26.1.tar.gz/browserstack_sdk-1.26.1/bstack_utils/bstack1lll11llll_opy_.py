# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack1l111l_opy_ = 2048
bstack11l11l1_opy_ = 7
def bstack11l1lll_opy_ (bstack1lllll1_opy_):
    global bstack1l1l111_opy_
    bstack1ll1111_opy_ = ord (bstack1lllll1_opy_ [-1])
    bstack111111_opy_ = bstack1lllll1_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack1ll1111_opy_ % len (bstack111111_opy_)
    bstack111l11l_opy_ = bstack111111_opy_ [:bstack1lll1l1_opy_] + bstack111111_opy_ [bstack1lll1l1_opy_:]
    if bstack1l11_opy_:
        bstack11ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l111l_opy_ - (bstack11l11ll_opy_ + bstack1ll1111_opy_) % bstack11l11l1_opy_) for bstack11l11ll_opy_, char in enumerate (bstack111l11l_opy_)])
    else:
        bstack11ll11_opy_ = str () .join ([chr (ord (char) - bstack1l111l_opy_ - (bstack11l11ll_opy_ + bstack1ll1111_opy_) % bstack11l11l1_opy_) for bstack11l11ll_opy_, char in enumerate (bstack111l11l_opy_)])
    return eval (bstack11ll11_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll1ll11l1_opy_ import bstack11ll1ll1l11_opy_
from bstack_utils.constants import *
import json
class bstack1111ll1ll_opy_:
    def __init__(self, bstack1l11llll1l_opy_, bstack11ll1ll11ll_opy_):
        self.bstack1l11llll1l_opy_ = bstack1l11llll1l_opy_
        self.bstack11ll1ll11ll_opy_ = bstack11ll1ll11ll_opy_
        self.bstack11ll1ll1l1l_opy_ = None
    def __call__(self):
        bstack11ll1lll111_opy_ = {}
        while True:
            self.bstack11ll1ll1l1l_opy_ = bstack11ll1lll111_opy_.get(
                bstack11l1lll_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪᛉ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll1ll1111_opy_ = self.bstack11ll1ll1l1l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll1ll1111_opy_ > 0:
                sleep(bstack11ll1ll1111_opy_ / 1000)
            params = {
                bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᛊ"): self.bstack1l11llll1l_opy_,
                bstack11l1lll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᛋ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11ll1ll111l_opy_ = bstack11l1lll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᛌ") + bstack11ll1ll1ll1_opy_ + bstack11l1lll_opy_ (u"ࠨ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࠥᛍ")
            if self.bstack11ll1ll11ll_opy_.lower() == bstack11l1lll_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡳࠣᛎ"):
                bstack11ll1lll111_opy_ = bstack11ll1ll1l11_opy_.results(bstack11ll1ll111l_opy_, params)
            else:
                bstack11ll1lll111_opy_ = bstack11ll1ll1l11_opy_.bstack11ll1ll1lll_opy_(bstack11ll1ll111l_opy_, params)
            if str(bstack11ll1lll111_opy_.get(bstack11l1lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᛏ"), bstack11l1lll_opy_ (u"ࠩ࠵࠴࠵࠭ᛐ"))) != bstack11l1lll_opy_ (u"ࠪ࠸࠵࠺ࠧᛑ"):
                break
        return bstack11ll1lll111_opy_.get(bstack11l1lll_opy_ (u"ࠫࡩࡧࡴࡢࠩᛒ"), bstack11ll1lll111_opy_)