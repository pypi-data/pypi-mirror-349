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
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11l1111_opy_ import bstack1lll11l1lll_opy_
from browserstack_sdk.sdk_cli.bstack111111l11l_opy_ import (
    bstack1llllll1l1l_opy_,
    bstack111111l1l1_opy_,
    bstack11111111ll_opy_,
)
from bstack_utils.helper import  bstack1l1lllll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll111llll_opy_ import bstack1llll1ll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l111ll_opy_, bstack1lll11111l1_opy_, bstack1llll1lll1l_opy_, bstack1lll1l11l11_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l111lll_opy_ import bstack111ll111_opy_
from browserstack_sdk.sdk_cli.bstack1llll1lll11_opy_ import bstack1ll1ll1lll1_opy_
from bstack_utils.percy import bstack1111111ll_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lllll1l1ll_opy_(bstack1lll11l1lll_opy_):
    def __init__(self, bstack1l1ll111ll1_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1ll111ll1_opy_ = bstack1l1ll111ll1_opy_
        self.percy = bstack1111111ll_opy_()
        self.bstack111ll11l_opy_ = bstack111ll111_opy_()
        self.bstack1l1ll111lll_opy_()
        bstack1llll1ll111_opy_.bstack1ll11ll11ll_opy_((bstack1llllll1l1l_opy_.bstack111111111l_opy_, bstack111111l1l1_opy_.PRE), self.bstack1l1ll111l1l_opy_)
        TestFramework.bstack1ll11ll11ll_opy_((bstack1lll1l111ll_opy_.TEST, bstack1llll1lll1l_opy_.POST), self.bstack1ll1l1lll1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lllllll1_opy_(self, instance: bstack11111111ll_opy_, driver: object):
        bstack1l1lllll1l1_opy_ = TestFramework.bstack1lllll1llll_opy_(instance.context)
        for t in bstack1l1lllll1l1_opy_:
            bstack1ll1111l11l_opy_ = TestFramework.bstack1llllll1111_opy_(t, bstack1ll1ll1lll1_opy_.bstack1l1llll111l_opy_, [])
            if any(instance is d[1] for d in bstack1ll1111l11l_opy_) or instance == driver:
                return t
    def bstack1l1ll111l1l_opy_(
        self,
        f: bstack1llll1ll111_opy_,
        driver: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1llll1ll111_opy_.bstack1ll1l11lll1_opy_(method_name):
                return
            platform_index = f.bstack1llllll1111_opy_(instance, bstack1llll1ll111_opy_.bstack1ll1l111lll_opy_, 0)
            bstack1l1lll11l11_opy_ = self.bstack1l1lllllll1_opy_(instance, driver)
            bstack1l1ll11l11l_opy_ = TestFramework.bstack1llllll1111_opy_(bstack1l1lll11l11_opy_, TestFramework.bstack1l1ll111l11_opy_, None)
            if not bstack1l1ll11l11l_opy_:
                self.logger.debug(bstack111l11_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡲࡦࡶࡸࡶࡳ࡯࡮ࡨࠢࡤࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡩࡴࠢࡱࡳࡹࠦࡹࡦࡶࠣࡷࡹࡧࡲࡵࡧࡧࠦቈ"))
                return
            driver_command = f.bstack1ll1l11111l_opy_(*args)
            for command in bstack11lllll1_opy_:
                if command == driver_command:
                    self.bstack11l11l1l_opy_(driver, platform_index)
            bstack1111lllll_opy_ = self.percy.bstack111ll1lll_opy_()
            if driver_command in bstack1l11l11l1_opy_[bstack1111lllll_opy_]:
                self.bstack111ll11l_opy_.bstack1l1ll1l1l1_opy_(bstack1l1ll11l11l_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack111l11_opy_ (u"ࠧࡵ࡮ࡠࡲࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡦࡴࡵࡳࡷࠨ቉"), e)
    def bstack1ll1l1lll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11111l1_opy_,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11l11111l_opy_ import bstack1ll1ll1ll11_opy_
        bstack1ll1111l11l_opy_ = f.bstack1llllll1111_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1llll111l_opy_, [])
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack111l11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣቊ") + str(kwargs) + bstack111l11_opy_ (u"ࠢࠣቋ"))
            return
        if len(bstack1ll1111l11l_opy_) > 1:
            self.logger.debug(bstack111l11_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥቌ") + str(kwargs) + bstack111l11_opy_ (u"ࠤࠥቍ"))
        bstack1l1ll1111l1_opy_, bstack1l1ll1111ll_opy_ = bstack1ll1111l11l_opy_[0]
        driver = bstack1l1ll1111l1_opy_()
        if not driver:
            self.logger.debug(bstack111l11_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ቎") + str(kwargs) + bstack111l11_opy_ (u"ࠦࠧ቏"))
            return
        bstack1l1ll11ll1l_opy_ = {
            TestFramework.bstack1ll1l111l11_opy_: bstack111l11_opy_ (u"ࠧࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣቐ"),
            TestFramework.bstack1ll11lll11l_opy_: bstack111l11_opy_ (u"ࠨࡴࡦࡵࡷࠤࡺࡻࡩࡥࠤቑ"),
            TestFramework.bstack1l1ll111l11_opy_: bstack111l11_opy_ (u"ࠢࡵࡧࡶࡸࠥࡸࡥࡳࡷࡱࠤࡳࡧ࡭ࡦࠤቒ")
        }
        bstack1l1ll11l111_opy_ = { key: f.bstack1llllll1111_opy_(instance, key) for key in bstack1l1ll11ll1l_opy_ }
        bstack1l1ll11111l_opy_ = [key for key, value in bstack1l1ll11l111_opy_.items() if not value]
        if bstack1l1ll11111l_opy_:
            for key in bstack1l1ll11111l_opy_:
                self.logger.debug(bstack111l11_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠦቓ") + str(key) + bstack111l11_opy_ (u"ࠤࠥቔ"))
            return
        platform_index = f.bstack1llllll1111_opy_(instance, bstack1llll1ll111_opy_.bstack1ll1l111lll_opy_, 0)
        if self.bstack1l1ll111ll1_opy_.percy_capture_mode == bstack111l11_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧቕ"):
            bstack11l1l1lll_opy_ = bstack1l1ll11l111_opy_.get(TestFramework.bstack1l1ll111l11_opy_) + bstack111l11_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢቖ")
            bstack1ll1l11ll1l_opy_ = bstack1ll1ll1ll11_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack1l1ll11ll11_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack11l1l1lll_opy_,
                bstack11ll111lll_opy_=bstack1l1ll11l111_opy_[TestFramework.bstack1ll1l111l11_opy_],
                bstack1ll1111l_opy_=bstack1l1ll11l111_opy_[TestFramework.bstack1ll11lll11l_opy_],
                bstack1l1l1111l1_opy_=platform_index
            )
            bstack1ll1ll1ll11_opy_.end(EVENTS.bstack1l1ll11ll11_opy_.value, bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ቗"), bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦቘ"), True, None, None, None, None, test_name=bstack11l1l1lll_opy_)
    def bstack11l11l1l_opy_(self, driver, platform_index):
        if self.bstack111ll11l_opy_.bstack111111111_opy_() is True or self.bstack111ll11l_opy_.capturing() is True:
            return
        self.bstack111ll11l_opy_.bstack1ll1ll1ll1_opy_()
        while not self.bstack111ll11l_opy_.bstack111111111_opy_():
            bstack1l1ll11l11l_opy_ = self.bstack111ll11l_opy_.bstack1lll11111_opy_()
            self.bstack1l11l111_opy_(driver, bstack1l1ll11l11l_opy_, platform_index)
        self.bstack111ll11l_opy_.bstack1l1l1l11l_opy_()
    def bstack1l11l111_opy_(self, driver, bstack1llll111l_opy_, platform_index, test=None):
        from bstack_utils.bstack11l11111l_opy_ import bstack1ll1ll1ll11_opy_
        bstack1ll1l11ll1l_opy_ = bstack1ll1ll1ll11_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack11l1lllll_opy_.value)
        if test != None:
            bstack11ll111lll_opy_ = getattr(test, bstack111l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ቙"), None)
            bstack1ll1111l_opy_ = getattr(test, bstack111l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ቚ"), None)
            PercySDK.screenshot(driver, bstack1llll111l_opy_, bstack11ll111lll_opy_=bstack11ll111lll_opy_, bstack1ll1111l_opy_=bstack1ll1111l_opy_, bstack1l1l1111l1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1llll111l_opy_)
        bstack1ll1ll1ll11_opy_.end(EVENTS.bstack11l1lllll_opy_.value, bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤቛ"), bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣቜ"), True, None, None, None, None, test_name=bstack1llll111l_opy_)
    def bstack1l1ll111lll_opy_(self):
        os.environ[bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩቝ")] = str(self.bstack1l1ll111ll1_opy_.success)
        os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩ቞")] = str(self.bstack1l1ll111ll1_opy_.percy_capture_mode)
        self.percy.bstack1l1ll11l1ll_opy_(self.bstack1l1ll111ll1_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1ll11l1l1_opy_(self.bstack1l1ll111ll1_opy_.percy_build_id)