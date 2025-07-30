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
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lllll1lll1_opy_ import bstack1111111l1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack111l1ll1_opy_ import bstack1l11l1111ll_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll1l111ll_opy_,
    bstack1lll11111l1_opy_,
    bstack1llll1lll1l_opy_,
    bstack1l111l111l1_opy_,
    bstack1lll1l11l11_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1lll11l1l_opy_
from bstack_utils.bstack11l11111l_opy_ import bstack1ll1ll1ll11_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1llll1l1l11_opy_ import bstack1lllll1l111_opy_
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import bstack1111l1111l_opy_
bstack1l1llll1l1l_opy_ = bstack1l1lll11l1l_opy_()
bstack1ll1111l1ll_opy_ = bstack111l11_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢ᎔")
bstack1l11l11l111_opy_ = bstack111l11_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦ᎕")
bstack1l11l11ll1l_opy_ = bstack111l11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ᎖")
bstack1l11l1lllll_opy_ = 1.0
_1l1lll1111l_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l11l1ll111_opy_ = bstack111l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥ᎗")
    bstack1l111l1lll1_opy_ = bstack111l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤ᎘")
    bstack1l11ll1111l_opy_ = bstack111l11_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦ᎙")
    bstack1l11l1l1lll_opy_ = bstack111l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣ᎚")
    bstack1l111l1l11l_opy_ = bstack111l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥ᎛")
    bstack1l11l11l11l_opy_: bool
    bstack1111l111l1_opy_: bstack1111l1111l_opy_  = None
    bstack1l11l1ll11l_opy_ = [
        bstack1lll1l111ll_opy_.BEFORE_ALL,
        bstack1lll1l111ll_opy_.AFTER_ALL,
        bstack1lll1l111ll_opy_.BEFORE_EACH,
        bstack1lll1l111ll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11l1l11ll_opy_: Dict[str, str],
        bstack1ll1l1l11l1_opy_: List[str]=[bstack111l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧ᎜")],
        bstack1111l111l1_opy_: bstack1111l1111l_opy_ = None,
        bstack1lll111lll1_opy_=None
    ):
        super().__init__(bstack1ll1l1l11l1_opy_, bstack1l11l1l11ll_opy_, bstack1111l111l1_opy_)
        self.bstack1l11l11l11l_opy_ = any(bstack111l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨ᎝") in item.lower() for item in bstack1ll1l1l11l1_opy_)
        self.bstack1lll111lll1_opy_ = bstack1lll111lll1_opy_
    def track_event(
        self,
        context: bstack1l111l111l1_opy_,
        test_framework_state: bstack1lll1l111ll_opy_,
        test_hook_state: bstack1llll1lll1l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll1l111ll_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l11l1ll11l_opy_:
            bstack1l11l1111ll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll1l111ll_opy_.NONE:
            self.logger.warning(bstack111l11_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦ᎞") + str(test_hook_state) + bstack111l11_opy_ (u"ࠦࠧ᎟"))
            return
        if not self.bstack1l11l11l11l_opy_:
            self.logger.warning(bstack111l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨᎠ") + str(str(self.bstack1ll1l1l11l1_opy_)) + bstack111l11_opy_ (u"ࠨࠢᎡ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack111l11_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᎢ") + str(kwargs) + bstack111l11_opy_ (u"ࠣࠤᎣ"))
            return
        instance = self.__1l111l1ll11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack111l11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣᎤ") + str(args) + bstack111l11_opy_ (u"ࠥࠦᎥ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11l1ll11l_opy_ and test_hook_state == bstack1llll1lll1l_opy_.PRE:
                bstack1ll1l11ll1l_opy_ = bstack1ll1ll1ll11_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack1llll1l11_opy_.value)
                name = str(EVENTS.bstack1llll1l11_opy_.name)+bstack111l11_opy_ (u"ࠦ࠿ࠨᎦ")+str(test_framework_state.name)
                TestFramework.bstack1l11ll111ll_opy_(instance, name, bstack1ll1l11ll1l_opy_)
        except Exception as e:
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤᎧ").format(e))
        try:
            if test_framework_state == bstack1lll1l111ll_opy_.TEST:
                if not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1l111llllll_opy_) and test_hook_state == bstack1llll1lll1l_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l111l11111_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack111l11_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᎨ") + str(test_hook_state) + bstack111l11_opy_ (u"ࠢࠣᎩ"))
                if test_hook_state == bstack1llll1lll1l_opy_.PRE and not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1ll11111111_opy_):
                    TestFramework.bstack111111ll1l_opy_(instance, TestFramework.bstack1ll11111111_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11l1ll1ll_opy_(instance, args)
                    self.logger.debug(bstack111l11_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᎪ") + str(test_hook_state) + bstack111l11_opy_ (u"ࠤࠥᎫ"))
                elif test_hook_state == bstack1llll1lll1l_opy_.POST and not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1ll11111lll_opy_):
                    TestFramework.bstack111111ll1l_opy_(instance, TestFramework.bstack1ll11111lll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111l11_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᎬ") + str(test_hook_state) + bstack111l11_opy_ (u"ࠦࠧᎭ"))
            elif test_framework_state == bstack1lll1l111ll_opy_.STEP:
                if test_hook_state == bstack1llll1lll1l_opy_.PRE:
                    PytestBDDFramework.__1l1111lll1l_opy_(instance, args)
                elif test_hook_state == bstack1llll1lll1l_opy_.POST:
                    PytestBDDFramework.__1l1111lllll_opy_(instance, args)
            elif test_framework_state == bstack1lll1l111ll_opy_.LOG and test_hook_state == bstack1llll1lll1l_opy_.POST:
                PytestBDDFramework.__1l111ll11l1_opy_(instance, *args)
            elif test_framework_state == bstack1lll1l111ll_opy_.LOG_REPORT and test_hook_state == bstack1llll1lll1l_opy_.POST:
                self.__1l111l1111l_opy_(instance, *args)
                self.__1l11l111ll1_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l11l1ll11l_opy_:
                self.__1l111l11lll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᎮ") + str(instance.ref()) + bstack111l11_opy_ (u"ࠨࠢᎯ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11l11l1l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11l1ll11l_opy_ and test_hook_state == bstack1llll1lll1l_opy_.POST:
                name = str(EVENTS.bstack1llll1l11_opy_.name)+bstack111l11_opy_ (u"ࠢ࠻ࠤᎰ")+str(test_framework_state.name)
                bstack1ll1l11ll1l_opy_ = TestFramework.bstack1l111ll1111_opy_(instance, name)
                bstack1ll1ll1ll11_opy_.end(EVENTS.bstack1llll1l11_opy_.value, bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᎱ"), bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᎲ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack111l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᎳ").format(e))
    def bstack1l1lll11lll_opy_(self):
        return self.bstack1l11l11l11l_opy_
    def __1l11l1llll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack111l11_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᎴ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1lllll111_opy_(rep, [bstack111l11_opy_ (u"ࠧࡽࡨࡦࡰࠥᎵ"), bstack111l11_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᎶ"), bstack111l11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᎷ"), bstack111l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᎸ"), bstack111l11_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥᎹ"), bstack111l11_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᎺ")])
        return None
    def __1l111l1111l_opy_(self, instance: bstack1lll11111l1_opy_, *args):
        result = self.__1l11l1llll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111l11ll1_opy_ = None
        if result.get(bstack111l11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᎻ"), None) == bstack111l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᎼ") and len(args) > 1 and getattr(args[1], bstack111l11_opy_ (u"ࠨࡥࡹࡥ࡬ࡲ࡫ࡵࠢᎽ"), None) is not None:
            failure = [{bstack111l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᎾ"): [args[1].excinfo.exconly(), result.get(bstack111l11_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᎿ"), None)]}]
            bstack1111l11ll1_opy_ = bstack111l11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᏀ") if bstack111l11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᏁ") in getattr(args[1].excinfo, bstack111l11_opy_ (u"ࠦࡹࡿࡰࡦࡰࡤࡱࡪࠨᏂ"), bstack111l11_opy_ (u"ࠧࠨᏃ")) else bstack111l11_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᏄ")
        bstack1l111lllll1_opy_ = result.get(bstack111l11_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᏅ"), TestFramework.bstack1l11l111lll_opy_)
        if bstack1l111lllll1_opy_ != TestFramework.bstack1l11l111lll_opy_:
            TestFramework.bstack111111ll1l_opy_(instance, TestFramework.bstack1l1lll11111_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l111lll1l1_opy_(instance, {
            TestFramework.bstack1l1l1l111ll_opy_: failure,
            TestFramework.bstack1l11l1l1111_opy_: bstack1111l11ll1_opy_,
            TestFramework.bstack1l1l1l111l1_opy_: bstack1l111lllll1_opy_,
        })
    def __1l111l1ll11_opy_(
        self,
        context: bstack1l111l111l1_opy_,
        test_framework_state: bstack1lll1l111ll_opy_,
        test_hook_state: bstack1llll1lll1l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll1l111ll_opy_.SETUP_FIXTURE:
            instance = self.__1l11ll1l111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11l1l11l1_opy_ bstack1l11l1l1l1l_opy_ this to be bstack111l11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᏆ")
            if test_framework_state == bstack1lll1l111ll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11ll11l1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll1l111ll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack111l11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᏇ"), None), bstack111l11_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᏈ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack111l11_opy_ (u"ࠦࡳࡵࡤࡦࠤᏉ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack111l11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᏊ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack11111ll111_opy_(target) if target else None
        return instance
    def __1l111l11lll_opy_(
        self,
        instance: bstack1lll11111l1_opy_,
        test_framework_state: bstack1lll1l111ll_opy_,
        test_hook_state: bstack1llll1lll1l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l111l1ll1l_opy_ = TestFramework.bstack1llllll1111_opy_(instance, PytestBDDFramework.bstack1l111l1lll1_opy_, {})
        if not key in bstack1l111l1ll1l_opy_:
            bstack1l111l1ll1l_opy_[key] = []
        bstack1l11l1l1ll1_opy_ = TestFramework.bstack1llllll1111_opy_(instance, PytestBDDFramework.bstack1l11ll1111l_opy_, {})
        if not key in bstack1l11l1l1ll1_opy_:
            bstack1l11l1l1ll1_opy_[key] = []
        bstack1l111l11ll1_opy_ = {
            PytestBDDFramework.bstack1l111l1lll1_opy_: bstack1l111l1ll1l_opy_,
            PytestBDDFramework.bstack1l11ll1111l_opy_: bstack1l11l1l1ll1_opy_,
        }
        if test_hook_state == bstack1llll1lll1l_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack111l11_opy_ (u"ࠨ࡫ࡦࡻࠥᏋ"): key,
                TestFramework.bstack1l11l1lll11_opy_: uuid4().__str__(),
                TestFramework.bstack1l11ll111l1_opy_: TestFramework.bstack1l111l1l1ll_opy_,
                TestFramework.bstack1l111l111ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l111ll1l1l_opy_: [],
                TestFramework.bstack1l11l11l1ll_opy_: hook_name,
                TestFramework.bstack1l11l1ll1l1_opy_: bstack1lllll1l111_opy_.bstack1l1111lll11_opy_()
            }
            bstack1l111l1ll1l_opy_[key].append(hook)
            bstack1l111l11ll1_opy_[PytestBDDFramework.bstack1l11l1l1lll_opy_] = key
        elif test_hook_state == bstack1llll1lll1l_opy_.POST:
            bstack1l111llll1l_opy_ = bstack1l111l1ll1l_opy_.get(key, [])
            hook = bstack1l111llll1l_opy_.pop() if bstack1l111llll1l_opy_ else None
            if hook:
                result = self.__1l11l1llll1_opy_(*args)
                if result:
                    bstack1l11l111111_opy_ = result.get(bstack111l11_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᏌ"), TestFramework.bstack1l111l1l1ll_opy_)
                    if bstack1l11l111111_opy_ != TestFramework.bstack1l111l1l1ll_opy_:
                        hook[TestFramework.bstack1l11ll111l1_opy_] = bstack1l11l111111_opy_
                hook[TestFramework.bstack1l11l1l1l11_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11l1ll1l1_opy_] = bstack1lllll1l111_opy_.bstack1l1111lll11_opy_()
                self.bstack1l111llll11_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11l1l111l_opy_, [])
                self.bstack1l1ll1lll1l_opy_(instance, logs)
                bstack1l11l1l1ll1_opy_[key].append(hook)
                bstack1l111l11ll1_opy_[PytestBDDFramework.bstack1l111l1l11l_opy_] = key
        TestFramework.bstack1l111lll1l1_opy_(instance, bstack1l111l11ll1_opy_)
        self.logger.debug(bstack111l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼ࡭ࡨࡽࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࡀࡿ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࠢᏍ") + str(bstack1l11l1l1ll1_opy_) + bstack111l11_opy_ (u"ࠤࠥᏎ"))
    def __1l11ll1l111_opy_(
        self,
        context: bstack1l111l111l1_opy_,
        test_framework_state: bstack1lll1l111ll_opy_,
        test_hook_state: bstack1llll1lll1l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1lllll111_opy_(args[0], [bstack111l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᏏ"), bstack111l11_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧᏐ"), bstack111l11_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧᏑ"), bstack111l11_opy_ (u"ࠨࡩࡥࡵࠥᏒ"), bstack111l11_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤᏓ"), bstack111l11_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᏔ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack111l11_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᏕ")) else fixturedef.get(bstack111l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᏖ"), None)
        fixturename = request.fixturename if hasattr(request, bstack111l11_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤᏗ")) else None
        node = request.node if hasattr(request, bstack111l11_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᏘ")) else None
        target = request.node.nodeid if hasattr(node, bstack111l11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᏙ")) else None
        baseid = fixturedef.get(bstack111l11_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᏚ"), None) or bstack111l11_opy_ (u"ࠣࠤᏛ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack111l11_opy_ (u"ࠤࡢࡴࡾ࡬ࡵ࡯ࡥ࡬ࡸࡪࡳࠢᏜ")):
            target = PytestBDDFramework.__1l11ll11ll1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack111l11_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᏝ")) else None
            if target and not TestFramework.bstack11111ll111_opy_(target):
                self.__1l11ll11l1l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack111l11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦ࡮ࡰࡦࡨࡁࢀࡴ࡯ࡥࡧࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᏞ") + str(test_hook_state) + bstack111l11_opy_ (u"ࠧࠨᏟ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack111l11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᏠ") + str(target) + bstack111l11_opy_ (u"ࠢࠣᏡ"))
            return None
        instance = TestFramework.bstack11111ll111_opy_(target)
        if not instance:
            self.logger.warning(bstack111l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡣࡣࡶࡩ࡮ࡪ࠽ࡼࡤࡤࡷࡪ࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᏢ") + str(target) + bstack111l11_opy_ (u"ࠤࠥᏣ"))
            return None
        bstack1l111l11l11_opy_ = TestFramework.bstack1llllll1111_opy_(instance, PytestBDDFramework.bstack1l11l1ll111_opy_, {})
        if os.getenv(bstack111l11_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡉࡍ࡝࡚ࡕࡓࡇࡖࠦᏤ"), bstack111l11_opy_ (u"ࠦ࠶ࠨᏥ")) == bstack111l11_opy_ (u"ࠧ࠷ࠢᏦ"):
            bstack1l11l111l1l_opy_ = bstack111l11_opy_ (u"ࠨ࠺ࠣᏧ").join((scope, fixturename))
            bstack1l111ll111l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11ll11111_opy_ = {
                bstack111l11_opy_ (u"ࠢ࡬ࡧࡼࠦᏨ"): bstack1l11l111l1l_opy_,
                bstack111l11_opy_ (u"ࠣࡶࡤ࡫ࡸࠨᏩ"): PytestBDDFramework.__1l11l11lll1_opy_(request.node, scenario),
                bstack111l11_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࠥᏪ"): fixturedef,
                bstack111l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᏫ"): scope,
                bstack111l11_opy_ (u"ࠦࡹࡿࡰࡦࠤᏬ"): None,
            }
            try:
                if test_hook_state == bstack1llll1lll1l_opy_.POST and callable(getattr(args[-1], bstack111l11_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᏭ"), None)):
                    bstack1l11ll11111_opy_[bstack111l11_opy_ (u"ࠨࡴࡺࡲࡨࠦᏮ")] = TestFramework.bstack1l1ll1llll1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1llll1lll1l_opy_.PRE:
                bstack1l11ll11111_opy_[bstack111l11_opy_ (u"ࠢࡶࡷ࡬ࡨࠧᏯ")] = uuid4().__str__()
                bstack1l11ll11111_opy_[PytestBDDFramework.bstack1l111l111ll_opy_] = bstack1l111ll111l_opy_
            elif test_hook_state == bstack1llll1lll1l_opy_.POST:
                bstack1l11ll11111_opy_[PytestBDDFramework.bstack1l11l1l1l11_opy_] = bstack1l111ll111l_opy_
            if bstack1l11l111l1l_opy_ in bstack1l111l11l11_opy_:
                bstack1l111l11l11_opy_[bstack1l11l111l1l_opy_].update(bstack1l11ll11111_opy_)
                self.logger.debug(bstack111l11_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࠤᏰ") + str(bstack1l111l11l11_opy_[bstack1l11l111l1l_opy_]) + bstack111l11_opy_ (u"ࠤࠥᏱ"))
            else:
                bstack1l111l11l11_opy_[bstack1l11l111l1l_opy_] = bstack1l11ll11111_opy_
                self.logger.debug(bstack111l11_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡾࠢࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࠨᏲ") + str(len(bstack1l111l11l11_opy_)) + bstack111l11_opy_ (u"ࠦࠧᏳ"))
        TestFramework.bstack111111ll1l_opy_(instance, PytestBDDFramework.bstack1l11l1ll111_opy_, bstack1l111l11l11_opy_)
        self.logger.debug(bstack111l11_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࡻ࡭ࡧࡱࠬࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᏴ") + str(instance.ref()) + bstack111l11_opy_ (u"ࠨࠢᏵ"))
        return instance
    def __1l11ll11l1l_opy_(
        self,
        context: bstack1l111l111l1_opy_,
        test_framework_state: bstack1lll1l111ll_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1111111l1l_opy_.create_context(target)
        ob = bstack1lll11111l1_opy_(ctx, self.bstack1ll1l1l11l1_opy_, self.bstack1l11l1l11ll_opy_, test_framework_state)
        TestFramework.bstack1l111lll1l1_opy_(ob, {
            TestFramework.bstack1ll11ll1lll_opy_: context.test_framework_name,
            TestFramework.bstack1ll11111l1l_opy_: context.test_framework_version,
            TestFramework.bstack1l11l11llll_opy_: [],
            PytestBDDFramework.bstack1l11l1ll111_opy_: {},
            PytestBDDFramework.bstack1l11ll1111l_opy_: {},
            PytestBDDFramework.bstack1l111l1lll1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack111111ll1l_opy_(ob, TestFramework.bstack1l1111l1lll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack111111ll1l_opy_(ob, TestFramework.bstack1ll1l111lll_opy_, context.platform_index)
        TestFramework.bstack1111111l11_opy_[ctx.id] = ob
        self.logger.debug(bstack111l11_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢ᏶") + str(TestFramework.bstack1111111l11_opy_.keys()) + bstack111l11_opy_ (u"ࠣࠤ᏷"))
        return ob
    @staticmethod
    def __1l11l1ll1ll_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111l11_opy_ (u"ࠩ࡬ࡨࠬᏸ"): id(step),
                bstack111l11_opy_ (u"ࠪࡸࡪࡾࡴࠨᏹ"): step.name,
                bstack111l11_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬᏺ"): step.keyword,
            })
        meta = {
            bstack111l11_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭ᏻ"): {
                bstack111l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᏼ"): feature.name,
                bstack111l11_opy_ (u"ࠧࡱࡣࡷ࡬ࠬᏽ"): feature.filename,
                bstack111l11_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭᏾"): feature.description
            },
            bstack111l11_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ᏿"): {
                bstack111l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ᐀"): scenario.name
            },
            bstack111l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᐁ"): steps,
            bstack111l11_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧᐂ"): PytestBDDFramework.__1l111ll1l11_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l1111ll1ll_opy_: meta
            }
        )
    def bstack1l111llll11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack111l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᐃ")
        global _1l1lll1111l_opy_
        platform_index = os.environ[bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᐄ")]
        bstack1ll1111l111_opy_ = os.path.join(bstack1l1llll1l1l_opy_, (bstack1ll1111l1ll_opy_ + str(platform_index)), bstack1l11l11l111_opy_)
        if not os.path.exists(bstack1ll1111l111_opy_) or not os.path.isdir(bstack1ll1111l111_opy_):
            return
        logs = hook.get(bstack111l11_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᐅ"), [])
        with os.scandir(bstack1ll1111l111_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1lll1111l_opy_:
                    self.logger.info(bstack111l11_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᐆ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack111l11_opy_ (u"ࠥࠦᐇ")
                    log_entry = bstack1lll1l11l11_opy_(
                        kind=bstack111l11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᐈ"),
                        message=bstack111l11_opy_ (u"ࠧࠨᐉ"),
                        level=bstack111l11_opy_ (u"ࠨࠢᐊ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1llllllll_opy_=entry.stat().st_size,
                        bstack1l1ll1l1111_opy_=bstack111l11_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᐋ"),
                        bstack1ll1lll_opy_=os.path.abspath(entry.path),
                        bstack1l1111llll1_opy_=hook.get(TestFramework.bstack1l11l1lll11_opy_)
                    )
                    logs.append(log_entry)
                    _1l1lll1111l_opy_.add(abs_path)
        platform_index = os.environ[bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᐌ")]
        bstack1l11l11ll11_opy_ = os.path.join(bstack1l1llll1l1l_opy_, (bstack1ll1111l1ll_opy_ + str(platform_index)), bstack1l11l11l111_opy_, bstack1l11l11ll1l_opy_)
        if not os.path.exists(bstack1l11l11ll11_opy_) or not os.path.isdir(bstack1l11l11ll11_opy_):
            self.logger.info(bstack111l11_opy_ (u"ࠤࡑࡳࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡬࡯ࡶࡰࡧࠤࡦࡺ࠺ࠡࡽࢀࠦᐍ").format(bstack1l11l11ll11_opy_))
        else:
            self.logger.info(bstack111l11_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᐎ").format(bstack1l11l11ll11_opy_))
            with os.scandir(bstack1l11l11ll11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1lll1111l_opy_:
                        self.logger.info(bstack111l11_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᐏ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack111l11_opy_ (u"ࠧࠨᐐ")
                        log_entry = bstack1lll1l11l11_opy_(
                            kind=bstack111l11_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᐑ"),
                            message=bstack111l11_opy_ (u"ࠢࠣᐒ"),
                            level=bstack111l11_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᐓ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1llllllll_opy_=entry.stat().st_size,
                            bstack1l1ll1l1111_opy_=bstack111l11_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᐔ"),
                            bstack1ll1lll_opy_=os.path.abspath(entry.path),
                            bstack1l1lll111l1_opy_=hook.get(TestFramework.bstack1l11l1lll11_opy_)
                        )
                        logs.append(log_entry)
                        _1l1lll1111l_opy_.add(abs_path)
        hook[bstack111l11_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᐕ")] = logs
    def bstack1l1ll1lll1l_opy_(
        self,
        bstack1l1lll11l11_opy_: bstack1lll11111l1_opy_,
        entries: List[bstack1lll1l11l11_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack111l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣᐖ"))
        req.platform_index = TestFramework.bstack1llllll1111_opy_(bstack1l1lll11l11_opy_, TestFramework.bstack1ll1l111lll_opy_)
        req.execution_context.hash = str(bstack1l1lll11l11_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll11l11_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll11l11_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllll1111_opy_(bstack1l1lll11l11_opy_, TestFramework.bstack1ll11ll1lll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllll1111_opy_(bstack1l1lll11l11_opy_, TestFramework.bstack1ll11111l1l_opy_)
            log_entry.uuid = entry.bstack1l1111llll1_opy_
            log_entry.test_framework_state = bstack1l1lll11l11_opy_.state.name
            log_entry.message = entry.message.encode(bstack111l11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᐗ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack111l11_opy_ (u"ࠨࠢᐘ")
            if entry.kind == bstack111l11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᐙ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1llllllll_opy_
                log_entry.file_path = entry.bstack1ll1lll_opy_
        def bstack1ll1111ll11_opy_():
            bstack111l1l111_opy_ = datetime.now()
            try:
                self.bstack1lll111lll1_opy_.LogCreatedEvent(req)
                bstack1l1lll11l11_opy_.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧᐚ"), datetime.now() - bstack111l1l111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111l11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡽࠣᐛ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l111l1_opy_.enqueue(bstack1ll1111ll11_opy_)
    def __1l11l111ll1_opy_(self, instance) -> None:
        bstack111l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᐜ")
        bstack1l111l11ll1_opy_ = {bstack111l11_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᐝ"): bstack1lllll1l111_opy_.bstack1l1111lll11_opy_()}
        TestFramework.bstack1l111lll1l1_opy_(instance, bstack1l111l11ll1_opy_)
    @staticmethod
    def __1l1111lll1l_opy_(instance, args):
        request, bstack1l1111ll111_opy_ = args
        bstack1l1111ll1l1_opy_ = id(bstack1l1111ll111_opy_)
        bstack1l111ll1lll_opy_ = instance.data[TestFramework.bstack1l1111ll1ll_opy_]
        step = next(filter(lambda st: st[bstack111l11_opy_ (u"ࠬ࡯ࡤࠨᐞ")] == bstack1l1111ll1l1_opy_, bstack1l111ll1lll_opy_[bstack111l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᐟ")]), None)
        step.update({
            bstack111l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᐠ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l111ll1lll_opy_[bstack111l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐡ")]) if st[bstack111l11_opy_ (u"ࠩ࡬ࡨࠬᐢ")] == step[bstack111l11_opy_ (u"ࠪ࡭ࡩ࠭ᐣ")]), None)
        if index is not None:
            bstack1l111ll1lll_opy_[bstack111l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᐤ")][index] = step
        instance.data[TestFramework.bstack1l1111ll1ll_opy_] = bstack1l111ll1lll_opy_
    @staticmethod
    def __1l1111lllll_opy_(instance, args):
        bstack111l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡬ࡪࡴࠠ࡭ࡧࡱࠤࡦࡸࡧࡴࠢ࡬ࡷࠥ࠸ࠬࠡ࡫ࡷࠤࡸ࡯ࡧ࡯࡫ࡩ࡭ࡪࡹࠠࡵࡪࡨࡶࡪࠦࡩࡴࠢࡱࡳࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡡࡳࡩࡶࠤࡦࡸࡥࠡ࠯ࠣ࡟ࡷ࡫ࡱࡶࡧࡶࡸ࠱ࠦࡳࡵࡧࡳࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࡩࡧࠢࡤࡶ࡬ࡹࠠࡢࡴࡨࠤ࠸ࠦࡴࡩࡧࡱࠤࡹ࡮ࡥࠡ࡮ࡤࡷࡹࠦࡶࡢ࡮ࡸࡩࠥ࡯ࡳࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᐥ")
        bstack1l111l1l111_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l1111ll111_opy_ = args[1]
        bstack1l1111ll1l1_opy_ = id(bstack1l1111ll111_opy_)
        bstack1l111ll1lll_opy_ = instance.data[TestFramework.bstack1l1111ll1ll_opy_]
        step = None
        if bstack1l1111ll1l1_opy_ is not None and bstack1l111ll1lll_opy_.get(bstack111l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᐦ")):
            step = next(filter(lambda st: st[bstack111l11_opy_ (u"ࠧࡪࡦࠪᐧ")] == bstack1l1111ll1l1_opy_, bstack1l111ll1lll_opy_[bstack111l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐨ")]), None)
            step.update({
                bstack111l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᐩ"): bstack1l111l1l111_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack111l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᐪ"): bstack111l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᐫ"),
                bstack111l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᐬ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack111l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᐭ"): bstack111l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᐮ"),
                })
        index = next((i for i, st in enumerate(bstack1l111ll1lll_opy_[bstack111l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐯ")]) if st[bstack111l11_opy_ (u"ࠩ࡬ࡨࠬᐰ")] == step[bstack111l11_opy_ (u"ࠪ࡭ࡩ࠭ᐱ")]), None)
        if index is not None:
            bstack1l111ll1lll_opy_[bstack111l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᐲ")][index] = step
        instance.data[TestFramework.bstack1l1111ll1ll_opy_] = bstack1l111ll1lll_opy_
    @staticmethod
    def __1l111ll1l11_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack111l11_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᐳ")):
                examples = list(node.callspec.params[bstack111l11_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬᐴ")].values())
            return examples
        except:
            return []
    def bstack1l1ll1l111l_opy_(self, instance: bstack1lll11111l1_opy_, bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_]):
        bstack1l111lll11l_opy_ = (
            PytestBDDFramework.bstack1l11l1l1lll_opy_
            if bstack11111l1ll1_opy_[1] == bstack1llll1lll1l_opy_.PRE
            else PytestBDDFramework.bstack1l111l1l11l_opy_
        )
        hook = PytestBDDFramework.bstack1l11l11111l_opy_(instance, bstack1l111lll11l_opy_)
        entries = hook.get(TestFramework.bstack1l111ll1l1l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llllll1111_opy_(instance, TestFramework.bstack1l11l11llll_opy_, []))
        return entries
    def bstack1l1lllll1ll_opy_(self, instance: bstack1lll11111l1_opy_, bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_]):
        bstack1l111lll11l_opy_ = (
            PytestBDDFramework.bstack1l11l1l1lll_opy_
            if bstack11111l1ll1_opy_[1] == bstack1llll1lll1l_opy_.PRE
            else PytestBDDFramework.bstack1l111l1l11l_opy_
        )
        PytestBDDFramework.bstack1l111lll1ll_opy_(instance, bstack1l111lll11l_opy_)
        TestFramework.bstack1llllll1111_opy_(instance, TestFramework.bstack1l11l11llll_opy_, []).clear()
    @staticmethod
    def bstack1l11l11111l_opy_(instance: bstack1lll11111l1_opy_, bstack1l111lll11l_opy_: str):
        bstack1l111lll111_opy_ = (
            PytestBDDFramework.bstack1l11ll1111l_opy_
            if bstack1l111lll11l_opy_ == PytestBDDFramework.bstack1l111l1l11l_opy_
            else PytestBDDFramework.bstack1l111l1lll1_opy_
        )
        bstack1l11l111l11_opy_ = TestFramework.bstack1llllll1111_opy_(instance, bstack1l111lll11l_opy_, None)
        bstack1l11ll11lll_opy_ = TestFramework.bstack1llllll1111_opy_(instance, bstack1l111lll111_opy_, None) if bstack1l11l111l11_opy_ else None
        return (
            bstack1l11ll11lll_opy_[bstack1l11l111l11_opy_][-1]
            if isinstance(bstack1l11ll11lll_opy_, dict) and len(bstack1l11ll11lll_opy_.get(bstack1l11l111l11_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111lll1ll_opy_(instance: bstack1lll11111l1_opy_, bstack1l111lll11l_opy_: str):
        hook = PytestBDDFramework.bstack1l11l11111l_opy_(instance, bstack1l111lll11l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l111ll1l1l_opy_, []).clear()
    @staticmethod
    def __1l111ll11l1_opy_(instance: bstack1lll11111l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack111l11_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡣࡰࡴࡧࡷࠧᐵ"), None)):
            return
        if os.getenv(bstack111l11_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧᐶ"), bstack111l11_opy_ (u"ࠤ࠴ࠦᐷ")) != bstack111l11_opy_ (u"ࠥ࠵ࠧᐸ"):
            PytestBDDFramework.logger.warning(bstack111l11_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡣࡢࡲ࡯ࡳ࡬ࠨᐹ"))
            return
        bstack1l111l11l1l_opy_ = {
            bstack111l11_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᐺ"): (PytestBDDFramework.bstack1l11l1l1lll_opy_, PytestBDDFramework.bstack1l111l1lll1_opy_),
            bstack111l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᐻ"): (PytestBDDFramework.bstack1l111l1l11l_opy_, PytestBDDFramework.bstack1l11ll1111l_opy_),
        }
        for when in (bstack111l11_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᐼ"), bstack111l11_opy_ (u"ࠣࡥࡤࡰࡱࠨᐽ"), bstack111l11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᐾ")):
            bstack1l11ll11l11_opy_ = args[1].get_records(when)
            if not bstack1l11ll11l11_opy_:
                continue
            records = [
                bstack1lll1l11l11_opy_(
                    kind=TestFramework.bstack1ll111l1111_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack111l11_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࡰࡤࡱࡪࠨᐿ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack111l11_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࠧᑀ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11ll11l11_opy_
                if isinstance(getattr(r, bstack111l11_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᑁ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11l1111l1_opy_, bstack1l111lll111_opy_ = bstack1l111l11l1l_opy_.get(when, (None, None))
            bstack1l111ll1ll1_opy_ = TestFramework.bstack1llllll1111_opy_(instance, bstack1l11l1111l1_opy_, None) if bstack1l11l1111l1_opy_ else None
            bstack1l11ll11lll_opy_ = TestFramework.bstack1llllll1111_opy_(instance, bstack1l111lll111_opy_, None) if bstack1l111ll1ll1_opy_ else None
            if isinstance(bstack1l11ll11lll_opy_, dict) and len(bstack1l11ll11lll_opy_.get(bstack1l111ll1ll1_opy_, [])) > 0:
                hook = bstack1l11ll11lll_opy_[bstack1l111ll1ll1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l111ll1l1l_opy_ in hook:
                    hook[TestFramework.bstack1l111ll1l1l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1llllll1111_opy_(instance, TestFramework.bstack1l11l11llll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l111l11111_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1ll1l1lll_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l11l1lll1l_opy_(request.node, scenario)
        bstack1l111l1llll_opy_ = feature.filename
        if not bstack1ll1l1lll_opy_ or not test_name or not bstack1l111l1llll_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll11lll11l_opy_: uuid4().__str__(),
            TestFramework.bstack1l111llllll_opy_: bstack1ll1l1lll_opy_,
            TestFramework.bstack1ll1l111l11_opy_: test_name,
            TestFramework.bstack1l1ll111l11_opy_: bstack1ll1l1lll_opy_,
            TestFramework.bstack1l111l1l1l1_opy_: bstack1l111l1llll_opy_,
            TestFramework.bstack1l1111ll11l_opy_: PytestBDDFramework.__1l11l11lll1_opy_(feature, scenario),
            TestFramework.bstack1l111ll11ll_opy_: code,
            TestFramework.bstack1l1l1l111l1_opy_: TestFramework.bstack1l11l111lll_opy_,
            TestFramework.bstack1l11llll1l1_opy_: test_name
        }
    @staticmethod
    def __1l11l1lll1l_opy_(node, scenario):
        if hasattr(node, bstack111l11_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᑂ")):
            parts = node.nodeid.rsplit(bstack111l11_opy_ (u"ࠢ࡜ࠤᑃ"))
            params = parts[-1]
            return bstack111l11_opy_ (u"ࠣࡽࢀࠤࡠࢁࡽࠣᑄ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l11l11lll1_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack111l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᑅ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack111l11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᑆ")) else [])
    @staticmethod
    def __1l11ll11ll1_opy_(location):
        return bstack111l11_opy_ (u"ࠦ࠿ࡀࠢᑇ").join(filter(lambda x: isinstance(x, str), location))