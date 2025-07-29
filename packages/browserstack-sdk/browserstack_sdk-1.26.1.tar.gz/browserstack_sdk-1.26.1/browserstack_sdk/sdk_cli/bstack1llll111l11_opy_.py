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
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import (
    bstack1llllll111l_opy_,
    bstack1llllll11ll_opy_,
    bstack1llllll1l11_opy_,
    bstack11111ll1l1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1lll11l111l_opy_(bstack1llllll111l_opy_):
    bstack1l11ll1ll1l_opy_ = bstack11l1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧ፯")
    bstack1l1l1lll11l_opy_ = bstack11l1lll_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨ፰")
    bstack1l1l1lll111_opy_ = bstack11l1lll_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬ࠣ፱")
    bstack1l1l1llllll_opy_ = bstack11l1lll_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢ፲")
    bstack1l11ll1llll_opy_ = bstack11l1lll_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࠧ፳")
    bstack1l11ll1ll11_opy_ = bstack11l1lll_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࡧࡳࡺࡰࡦࠦ፴")
    NAME = bstack11l1lll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ፵")
    bstack1l11ll1l1ll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1lllll1l_opy_: Any
    bstack1l11lll11l1_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11l1lll_opy_ (u"ࠧࡲࡡࡶࡰࡦ࡬ࠧ፶"), bstack11l1lll_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺࠢ፷"), bstack11l1lll_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤ፸"), bstack11l1lll_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢ፹"), bstack11l1lll_opy_ (u"ࠤࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠦ፺")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack11111111l1_opy_(methods)
    def bstack1llllll1111_opy_(self, instance: bstack1llllll11ll_opy_, method_name: str, bstack1111111ll1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack111111ll1l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack11111ll1ll_opy_, bstack1l11lll1111_opy_ = bstack11111l11l1_opy_
        bstack1l11lll1l11_opy_ = bstack1lll11l111l_opy_.bstack1l11lll11ll_opy_(bstack11111l11l1_opy_)
        if bstack1l11lll1l11_opy_ in bstack1lll11l111l_opy_.bstack1l11ll1l1ll_opy_:
            bstack1l11lll111l_opy_ = None
            for callback in bstack1lll11l111l_opy_.bstack1l11ll1l1ll_opy_[bstack1l11lll1l11_opy_]:
                try:
                    bstack1l11ll1lll1_opy_ = callback(self, target, exec, bstack11111l11l1_opy_, result, *args, **kwargs)
                    if bstack1l11lll111l_opy_ == None:
                        bstack1l11lll111l_opy_ = bstack1l11ll1lll1_opy_
                except Exception as e:
                    self.logger.error(bstack11l1lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࠣ፻") + str(e) + bstack11l1lll_opy_ (u"ࠦࠧ፼"))
                    traceback.print_exc()
            if bstack1l11lll1111_opy_ == bstack11111ll1l1_opy_.PRE and callable(bstack1l11lll111l_opy_):
                return bstack1l11lll111l_opy_
            elif bstack1l11lll1111_opy_ == bstack11111ll1l1_opy_.POST and bstack1l11lll111l_opy_:
                return bstack1l11lll111l_opy_
    def bstack111111l1ll_opy_(
        self, method_name, previous_state: bstack1llllll1l11_opy_, *args, **kwargs
    ) -> bstack1llllll1l11_opy_:
        if method_name == bstack11l1lll_opy_ (u"ࠬࡲࡡࡶࡰࡦ࡬ࠬ፽") or method_name == bstack11l1lll_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࠧ፾") or method_name == bstack11l1lll_opy_ (u"ࠧ࡯ࡧࡺࡣࡵࡧࡧࡦࠩ፿"):
            return bstack1llllll1l11_opy_.bstack11111l1l11_opy_
        if method_name == bstack11l1lll_opy_ (u"ࠨࡦ࡬ࡷࡵࡧࡴࡤࡪࠪᎀ"):
            return bstack1llllll1l11_opy_.bstack1lllllllll1_opy_
        if method_name == bstack11l1lll_opy_ (u"ࠩࡦࡰࡴࡹࡥࠨᎁ"):
            return bstack1llllll1l11_opy_.QUIT
        return bstack1llllll1l11_opy_.NONE
    @staticmethod
    def bstack1l11lll11ll_opy_(bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_]):
        return bstack11l1lll_opy_ (u"ࠥ࠾ࠧᎂ").join((bstack1llllll1l11_opy_(bstack11111l11l1_opy_[0]).name, bstack11111ll1l1_opy_(bstack11111l11l1_opy_[1]).name))
    @staticmethod
    def bstack1ll1ll11111_opy_(bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_], callback: Callable):
        bstack1l11lll1l11_opy_ = bstack1lll11l111l_opy_.bstack1l11lll11ll_opy_(bstack11111l11l1_opy_)
        if not bstack1l11lll1l11_opy_ in bstack1lll11l111l_opy_.bstack1l11ll1l1ll_opy_:
            bstack1lll11l111l_opy_.bstack1l11ll1l1ll_opy_[bstack1l11lll1l11_opy_] = []
        bstack1lll11l111l_opy_.bstack1l11ll1l1ll_opy_[bstack1l11lll1l11_opy_].append(callback)
    @staticmethod
    def bstack1ll1ll111l1_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll1ll111ll_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1l111l11_opy_(instance: bstack1llllll11ll_opy_, default_value=None):
        return bstack1llllll111l_opy_.bstack1llllll11l1_opy_(instance, bstack1lll11l111l_opy_.bstack1l1l1llllll_opy_, default_value)
    @staticmethod
    def bstack1ll111ll1l1_opy_(instance: bstack1llllll11ll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll11llll11_opy_(instance: bstack1llllll11ll_opy_, default_value=None):
        return bstack1llllll111l_opy_.bstack1llllll11l1_opy_(instance, bstack1lll11l111l_opy_.bstack1l1l1lll111_opy_, default_value)
    @staticmethod
    def bstack1ll11ll111l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11lll111_opy_(method_name: str, *args):
        if not bstack1lll11l111l_opy_.bstack1ll1ll111l1_opy_(method_name):
            return False
        if not bstack1lll11l111l_opy_.bstack1l11ll1llll_opy_ in bstack1lll11l111l_opy_.bstack1l1l1111ll1_opy_(*args):
            return False
        bstack1ll11l1l1l1_opy_ = bstack1lll11l111l_opy_.bstack1ll11l111ll_opy_(*args)
        return bstack1ll11l1l1l1_opy_ and bstack11l1lll_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᎃ") in bstack1ll11l1l1l1_opy_ and bstack11l1lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᎄ") in bstack1ll11l1l1l1_opy_[bstack11l1lll_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᎅ")]
    @staticmethod
    def bstack1ll1l1lll11_opy_(method_name: str, *args):
        if not bstack1lll11l111l_opy_.bstack1ll1ll111l1_opy_(method_name):
            return False
        if not bstack1lll11l111l_opy_.bstack1l11ll1llll_opy_ in bstack1lll11l111l_opy_.bstack1l1l1111ll1_opy_(*args):
            return False
        bstack1ll11l1l1l1_opy_ = bstack1lll11l111l_opy_.bstack1ll11l111ll_opy_(*args)
        return (
            bstack1ll11l1l1l1_opy_
            and bstack11l1lll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᎆ") in bstack1ll11l1l1l1_opy_
            and bstack11l1lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸࡩࡲࡪࡲࡷࠦᎇ") in bstack1ll11l1l1l1_opy_[bstack11l1lll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᎈ")]
        )
    @staticmethod
    def bstack1l1l1111ll1_opy_(*args):
        return str(bstack1lll11l111l_opy_.bstack1ll11ll111l_opy_(*args)).lower()