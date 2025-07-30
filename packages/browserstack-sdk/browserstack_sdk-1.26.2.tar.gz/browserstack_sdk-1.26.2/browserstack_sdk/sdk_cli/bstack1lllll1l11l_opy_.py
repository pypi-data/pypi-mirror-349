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
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack111111l11l_opy_ import (
    bstack1lllllll1l1_opy_,
    bstack11111111ll_opy_,
    bstack1llllll1l1l_opy_,
    bstack111111l1l1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1lll111ll1l_opy_(bstack1lllllll1l1_opy_):
    bstack1l11ll1l1ll_opy_ = bstack111l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤ፺")
    bstack1l1l1l1llll_opy_ = bstack111l11_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥ፻")
    bstack1l1l1ll1ll1_opy_ = bstack111l11_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧ፼")
    bstack1l1l1lllll1_opy_ = bstack111l11_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ፽")
    bstack1l11ll1ll1l_opy_ = bstack111l11_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤ፾")
    bstack1l11ll1l1l1_opy_ = bstack111l11_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣ፿")
    NAME = bstack111l11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᎀ")
    bstack1l11ll1l11l_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1l1ll11_opy_: Any
    bstack1l11ll1lll1_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack111l11_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤᎁ"), bstack111l11_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦᎂ"), bstack111l11_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᎃ"), bstack111l11_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦᎄ"), bstack111l11_opy_ (u"ࠨࡤࡪࡵࡳࡥࡹࡩࡨࠣᎅ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1lllllllll1_opy_(methods)
    def bstack111111l1ll_opy_(self, instance: bstack11111111ll_opy_, method_name: str, bstack11111111l1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack11111lll11_opy_(
        self,
        target: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack111111lll1_opy_, bstack1l11lll1111_opy_ = bstack11111l1ll1_opy_
        bstack1l11ll1llll_opy_ = bstack1lll111ll1l_opy_.bstack1l11lll11l1_opy_(bstack11111l1ll1_opy_)
        if bstack1l11ll1llll_opy_ in bstack1lll111ll1l_opy_.bstack1l11ll1l11l_opy_:
            bstack1l11lll111l_opy_ = None
            for callback in bstack1lll111ll1l_opy_.bstack1l11ll1l11l_opy_[bstack1l11ll1llll_opy_]:
                try:
                    bstack1l11ll1ll11_opy_ = callback(self, target, exec, bstack11111l1ll1_opy_, result, *args, **kwargs)
                    if bstack1l11lll111l_opy_ == None:
                        bstack1l11lll111l_opy_ = bstack1l11ll1ll11_opy_
                except Exception as e:
                    self.logger.error(bstack111l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧᎆ") + str(e) + bstack111l11_opy_ (u"ࠣࠤᎇ"))
                    traceback.print_exc()
            if bstack1l11lll1111_opy_ == bstack111111l1l1_opy_.PRE and callable(bstack1l11lll111l_opy_):
                return bstack1l11lll111l_opy_
            elif bstack1l11lll1111_opy_ == bstack111111l1l1_opy_.POST and bstack1l11lll111l_opy_:
                return bstack1l11lll111l_opy_
    def bstack1llllllllll_opy_(
        self, method_name, previous_state: bstack1llllll1l1l_opy_, *args, **kwargs
    ) -> bstack1llllll1l1l_opy_:
        if method_name == bstack111l11_opy_ (u"ࠩ࡯ࡥࡺࡴࡣࡩࠩᎈ") or method_name == bstack111l11_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫᎉ") or method_name == bstack111l11_opy_ (u"ࠫࡳ࡫ࡷࡠࡲࡤ࡫ࡪ࠭ᎊ"):
            return bstack1llllll1l1l_opy_.bstack1lllllll1ll_opy_
        if method_name == bstack111l11_opy_ (u"ࠬࡪࡩࡴࡲࡤࡸࡨ࡮ࠧᎋ"):
            return bstack1llllll1l1l_opy_.bstack11111l111l_opy_
        if method_name == bstack111l11_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠬᎌ"):
            return bstack1llllll1l1l_opy_.QUIT
        return bstack1llllll1l1l_opy_.NONE
    @staticmethod
    def bstack1l11lll11l1_opy_(bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_]):
        return bstack111l11_opy_ (u"ࠢ࠻ࠤᎍ").join((bstack1llllll1l1l_opy_(bstack11111l1ll1_opy_[0]).name, bstack111111l1l1_opy_(bstack11111l1ll1_opy_[1]).name))
    @staticmethod
    def bstack1ll11ll11ll_opy_(bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_], callback: Callable):
        bstack1l11ll1llll_opy_ = bstack1lll111ll1l_opy_.bstack1l11lll11l1_opy_(bstack11111l1ll1_opy_)
        if not bstack1l11ll1llll_opy_ in bstack1lll111ll1l_opy_.bstack1l11ll1l11l_opy_:
            bstack1lll111ll1l_opy_.bstack1l11ll1l11l_opy_[bstack1l11ll1llll_opy_] = []
        bstack1lll111ll1l_opy_.bstack1l11ll1l11l_opy_[bstack1l11ll1llll_opy_].append(callback)
    @staticmethod
    def bstack1ll1l11lll1_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll11ll1l1l_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll11ll1l11_opy_(instance: bstack11111111ll_opy_, default_value=None):
        return bstack1lllllll1l1_opy_.bstack1llllll1111_opy_(instance, bstack1lll111ll1l_opy_.bstack1l1l1lllll1_opy_, default_value)
    @staticmethod
    def bstack1ll111ll11l_opy_(instance: bstack11111111ll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll11ll1ll1_opy_(instance: bstack11111111ll_opy_, default_value=None):
        return bstack1lllllll1l1_opy_.bstack1llllll1111_opy_(instance, bstack1lll111ll1l_opy_.bstack1l1l1ll1ll1_opy_, default_value)
    @staticmethod
    def bstack1ll1l11111l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l11l1l1_opy_(method_name: str, *args):
        if not bstack1lll111ll1l_opy_.bstack1ll1l11lll1_opy_(method_name):
            return False
        if not bstack1lll111ll1l_opy_.bstack1l11ll1ll1l_opy_ in bstack1lll111ll1l_opy_.bstack1l1l111lll1_opy_(*args):
            return False
        bstack1ll11l11lll_opy_ = bstack1lll111ll1l_opy_.bstack1ll11l11l1l_opy_(*args)
        return bstack1ll11l11lll_opy_ and bstack111l11_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᎎ") in bstack1ll11l11lll_opy_ and bstack111l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᎏ") in bstack1ll11l11lll_opy_[bstack111l11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥ᎐")]
    @staticmethod
    def bstack1ll11l1l1ll_opy_(method_name: str, *args):
        if not bstack1lll111ll1l_opy_.bstack1ll1l11lll1_opy_(method_name):
            return False
        if not bstack1lll111ll1l_opy_.bstack1l11ll1ll1l_opy_ in bstack1lll111ll1l_opy_.bstack1l1l111lll1_opy_(*args):
            return False
        bstack1ll11l11lll_opy_ = bstack1lll111ll1l_opy_.bstack1ll11l11l1l_opy_(*args)
        return (
            bstack1ll11l11lll_opy_
            and bstack111l11_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦ᎑") in bstack1ll11l11lll_opy_
            and bstack111l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡦࡶ࡮ࡶࡴࠣ᎒") in bstack1ll11l11lll_opy_[bstack111l11_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨ᎓")]
        )
    @staticmethod
    def bstack1l1l111lll1_opy_(*args):
        return str(bstack1lll111ll1l_opy_.bstack1ll1l11111l_opy_(*args)).lower()