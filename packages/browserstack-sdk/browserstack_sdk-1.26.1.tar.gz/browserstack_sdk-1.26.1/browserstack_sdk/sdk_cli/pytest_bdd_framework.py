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
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lllllll11l_opy_ import bstack11111l1lll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1lllll_opy_ import bstack1l111l111ll_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll11llll1_opy_,
    bstack1llll1111ll_opy_,
    bstack1ll1lll1111_opy_,
    bstack1l111l11l1l_opy_,
    bstack1lll1l11111_opy_,
)
import traceback
from bstack_utils.helper import bstack1ll11111l1l_opy_
from bstack_utils.bstack11l1lll1l1_opy_ import bstack1lll1lll111_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1lll11ll1ll_opy_ import bstack1lll1lll1l1_opy_
from browserstack_sdk.sdk_cli.bstack11111llll1_opy_ import bstack1111l111l1_opy_
bstack1l1lllll111_opy_ = bstack1ll11111l1l_opy_()
bstack1l1lll1llll_opy_ = bstack11l1lll_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᎉ")
bstack1l11l1ll1l1_opy_ = bstack11l1lll_opy_ (u"ࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢᎊ")
bstack1l11l11l1ll_opy_ = bstack11l1lll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦᎋ")
bstack1l1111llll1_opy_ = 1.0
_1ll111l111l_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l11l1lllll_opy_ = bstack11l1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᎌ")
    bstack1l111ll11l1_opy_ = bstack11l1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠧᎍ")
    bstack1l11ll11111_opy_ = bstack11l1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᎎ")
    bstack1l11l1111l1_opy_ = bstack11l1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࠦᎏ")
    bstack1l1111lll11_opy_ = bstack11l1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨ᎐")
    bstack1l11l1ll1ll_opy_: bool
    bstack11111llll1_opy_: bstack1111l111l1_opy_  = None
    bstack1l111lll111_opy_ = [
        bstack1lll11llll1_opy_.BEFORE_ALL,
        bstack1lll11llll1_opy_.AFTER_ALL,
        bstack1lll11llll1_opy_.BEFORE_EACH,
        bstack1lll11llll1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111l1l11l_opy_: Dict[str, str],
        bstack1ll1l1l1111_opy_: List[str]=[bstack11l1lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣ᎑")],
        bstack11111llll1_opy_: bstack1111l111l1_opy_ = None,
        bstack1llll111ll1_opy_=None
    ):
        super().__init__(bstack1ll1l1l1111_opy_, bstack1l111l1l11l_opy_, bstack11111llll1_opy_)
        self.bstack1l11l1ll1ll_opy_ = any(bstack11l1lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤ᎒") in item.lower() for item in bstack1ll1l1l1111_opy_)
        self.bstack1llll111ll1_opy_ = bstack1llll111ll1_opy_
    def track_event(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll11llll1_opy_,
        test_hook_state: bstack1ll1lll1111_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll11llll1_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l111lll111_opy_:
            bstack1l111l111ll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll11llll1_opy_.NONE:
            self.logger.warning(bstack11l1lll_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࠢ᎓") + str(test_hook_state) + bstack11l1lll_opy_ (u"ࠢࠣ᎔"))
            return
        if not self.bstack1l11l1ll1ll_opy_:
            self.logger.warning(bstack11l1lll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠾ࠤ᎕") + str(str(self.bstack1ll1l1l1111_opy_)) + bstack11l1lll_opy_ (u"ࠤࠥ᎖"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11l1lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ᎗") + str(kwargs) + bstack11l1lll_opy_ (u"ࠦࠧ᎘"))
            return
        instance = self.__1l11l11ll1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡧࡲࡨࡵࡀࠦ᎙") + str(args) + bstack11l1lll_opy_ (u"ࠨࠢ᎚"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111lll111_opy_ and test_hook_state == bstack1ll1lll1111_opy_.PRE:
                bstack1ll1l11llll_opy_ = bstack1lll1lll111_opy_.bstack1ll1l11l1ll_opy_(EVENTS.bstack11ll11l1l_opy_.value)
                name = str(EVENTS.bstack11ll11l1l_opy_.name)+bstack11l1lll_opy_ (u"ࠢ࠻ࠤ᎛")+str(test_framework_state.name)
                TestFramework.bstack1l111l1l1l1_opy_(instance, name, bstack1ll1l11llll_opy_)
        except Exception as e:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵࠤࡵࡸࡥ࠻ࠢࡾࢁࠧ᎜").format(e))
        try:
            if test_framework_state == bstack1lll11llll1_opy_.TEST:
                if not TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1l1111ll1l1_opy_) and test_hook_state == bstack1ll1lll1111_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l11l1l111l_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack11l1lll_opy_ (u"ࠤ࡯ࡳࡦࡪࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤ᎝") + str(test_hook_state) + bstack11l1lll_opy_ (u"ࠥࠦ᎞"))
                if test_hook_state == bstack1ll1lll1111_opy_.PRE and not TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1ll1111l11l_opy_):
                    TestFramework.bstack111111llll_opy_(instance, TestFramework.bstack1ll1111l11l_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11l1lll11_opy_(instance, args)
                    self.logger.debug(bstack11l1lll_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡳࡵࡣࡵࡸࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤ᎟") + str(test_hook_state) + bstack11l1lll_opy_ (u"ࠧࠨᎠ"))
                elif test_hook_state == bstack1ll1lll1111_opy_.POST and not TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1l1llll1l1l_opy_):
                    TestFramework.bstack111111llll_opy_(instance, TestFramework.bstack1l1llll1l1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l1lll_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡧࡱࡨࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᎡ") + str(test_hook_state) + bstack11l1lll_opy_ (u"ࠢࠣᎢ"))
            elif test_framework_state == bstack1lll11llll1_opy_.STEP:
                if test_hook_state == bstack1ll1lll1111_opy_.PRE:
                    PytestBDDFramework.__1l11l11111l_opy_(instance, args)
                elif test_hook_state == bstack1ll1lll1111_opy_.POST:
                    PytestBDDFramework.__1l111lll11l_opy_(instance, args)
            elif test_framework_state == bstack1lll11llll1_opy_.LOG and test_hook_state == bstack1ll1lll1111_opy_.POST:
                PytestBDDFramework.__1l111l111l1_opy_(instance, *args)
            elif test_framework_state == bstack1lll11llll1_opy_.LOG_REPORT and test_hook_state == bstack1ll1lll1111_opy_.POST:
                self.__1l111llllll_opy_(instance, *args)
                self.__1l111l1l1ll_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l111lll111_opy_:
                self.__1l11l1l1l11_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᎣ") + str(instance.ref()) + bstack11l1lll_opy_ (u"ࠤࠥᎤ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11ll111l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111lll111_opy_ and test_hook_state == bstack1ll1lll1111_opy_.POST:
                name = str(EVENTS.bstack11ll11l1l_opy_.name)+bstack11l1lll_opy_ (u"ࠥ࠾ࠧᎥ")+str(test_framework_state.name)
                bstack1ll1l11llll_opy_ = TestFramework.bstack1l11l11lll1_opy_(instance, name)
                bstack1lll1lll111_opy_.end(EVENTS.bstack11ll11l1l_opy_.value, bstack1ll1l11llll_opy_+bstack11l1lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᎦ"), bstack1ll1l11llll_opy_+bstack11l1lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᎧ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᎨ").format(e))
    def bstack1l1lll11l1l_opy_(self):
        return self.bstack1l11l1ll1ll_opy_
    def __1l11ll11l11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11l1lll_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᎩ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1lll111ll_opy_(rep, [bstack11l1lll_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᎪ"), bstack11l1lll_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᎫ"), bstack11l1lll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᎬ"), bstack11l1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᎭ"), bstack11l1lll_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨᎮ"), bstack11l1lll_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᎯ")])
        return None
    def __1l111llllll_opy_(self, instance: bstack1llll1111ll_opy_, *args):
        result = self.__1l11ll11l11_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111l111ll_opy_ = None
        if result.get(bstack11l1lll_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᎰ"), None) == bstack11l1lll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᎱ") and len(args) > 1 and getattr(args[1], bstack11l1lll_opy_ (u"ࠤࡨࡼࡨ࡯࡮ࡧࡱࠥᎲ"), None) is not None:
            failure = [{bstack11l1lll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭Ꮃ"): [args[1].excinfo.exconly(), result.get(bstack11l1lll_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᎴ"), None)]}]
            bstack1111l111ll_opy_ = bstack11l1lll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᎵ") if bstack11l1lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᎶ") in getattr(args[1].excinfo, bstack11l1lll_opy_ (u"ࠢࡵࡻࡳࡩࡳࡧ࡭ࡦࠤᎷ"), bstack11l1lll_opy_ (u"ࠣࠤᎸ")) else bstack11l1lll_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᎹ")
        bstack1l111llll1l_opy_ = result.get(bstack11l1lll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᎺ"), TestFramework.bstack1l11l1lll1l_opy_)
        if bstack1l111llll1l_opy_ != TestFramework.bstack1l11l1lll1l_opy_:
            TestFramework.bstack111111llll_opy_(instance, TestFramework.bstack1l1lll1l1l1_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11l1l1l1l_opy_(instance, {
            TestFramework.bstack1l1l1l11111_opy_: failure,
            TestFramework.bstack1l111l1ll11_opy_: bstack1111l111ll_opy_,
            TestFramework.bstack1l1l1l1l1ll_opy_: bstack1l111llll1l_opy_,
        })
    def __1l11l11ll1l_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll11llll1_opy_,
        test_hook_state: bstack1ll1lll1111_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll11llll1_opy_.SETUP_FIXTURE:
            instance = self.__1l11l11ll11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11ll11lll_opy_ bstack1l111l1lll1_opy_ this to be bstack11l1lll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᎻ")
            if test_framework_state == bstack1lll11llll1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111l1llll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll11llll1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11l1lll_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᎼ"), None), bstack11l1lll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᎽ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11l1lll_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᎾ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack11l1lll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᎿ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack11111l1111_opy_(target) if target else None
        return instance
    def __1l11l1l1l11_opy_(
        self,
        instance: bstack1llll1111ll_opy_,
        test_framework_state: bstack1lll11llll1_opy_,
        test_hook_state: bstack1ll1lll1111_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l111l1ll1l_opy_ = TestFramework.bstack1llllll11l1_opy_(instance, PytestBDDFramework.bstack1l111ll11l1_opy_, {})
        if not key in bstack1l111l1ll1l_opy_:
            bstack1l111l1ll1l_opy_[key] = []
        bstack1l11ll1l111_opy_ = TestFramework.bstack1llllll11l1_opy_(instance, PytestBDDFramework.bstack1l11ll11111_opy_, {})
        if not key in bstack1l11ll1l111_opy_:
            bstack1l11ll1l111_opy_[key] = []
        bstack1l111l11lll_opy_ = {
            PytestBDDFramework.bstack1l111ll11l1_opy_: bstack1l111l1ll1l_opy_,
            PytestBDDFramework.bstack1l11ll11111_opy_: bstack1l11ll1l111_opy_,
        }
        if test_hook_state == bstack1ll1lll1111_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack11l1lll_opy_ (u"ࠤ࡮ࡩࡾࠨᏀ"): key,
                TestFramework.bstack1l111l11111_opy_: uuid4().__str__(),
                TestFramework.bstack1l11l111l11_opy_: TestFramework.bstack1l11l1l11ll_opy_,
                TestFramework.bstack1l111ll1l1l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1111ll1ll_opy_: [],
                TestFramework.bstack1l11l111111_opy_: hook_name,
                TestFramework.bstack1l1111ll11l_opy_: bstack1lll1lll1l1_opy_.bstack1l11l1ll111_opy_()
            }
            bstack1l111l1ll1l_opy_[key].append(hook)
            bstack1l111l11lll_opy_[PytestBDDFramework.bstack1l11l1111l1_opy_] = key
        elif test_hook_state == bstack1ll1lll1111_opy_.POST:
            bstack1l11l1l1lll_opy_ = bstack1l111l1ll1l_opy_.get(key, [])
            hook = bstack1l11l1l1lll_opy_.pop() if bstack1l11l1l1lll_opy_ else None
            if hook:
                result = self.__1l11ll11l11_opy_(*args)
                if result:
                    bstack1l11ll11l1l_opy_ = result.get(bstack11l1lll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᏁ"), TestFramework.bstack1l11l1l11ll_opy_)
                    if bstack1l11ll11l1l_opy_ != TestFramework.bstack1l11l1l11ll_opy_:
                        hook[TestFramework.bstack1l11l111l11_opy_] = bstack1l11ll11l1l_opy_
                hook[TestFramework.bstack1l11l11l111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l1111ll11l_opy_] = bstack1lll1lll1l1_opy_.bstack1l11l1ll111_opy_()
                self.bstack1l11l11llll_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11l111l1l_opy_, [])
                self.bstack1l1llll111l_opy_(instance, logs)
                bstack1l11ll1l111_opy_[key].append(hook)
                bstack1l111l11lll_opy_[PytestBDDFramework.bstack1l1111lll11_opy_] = key
        TestFramework.bstack1l11l1l1l1l_opy_(instance, bstack1l111l11lll_opy_)
        self.logger.debug(bstack11l1lll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡬ࡴࡵ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡰ࡫ࡹࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࡃࡻࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࡽࠡࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠿ࠥᏂ") + str(bstack1l11ll1l111_opy_) + bstack11l1lll_opy_ (u"ࠧࠨᏃ"))
    def __1l11l11ll11_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll11llll1_opy_,
        test_hook_state: bstack1ll1lll1111_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1lll111ll_opy_(args[0], [bstack11l1lll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᏄ"), bstack11l1lll_opy_ (u"ࠢࡢࡴࡪࡲࡦࡳࡥࠣᏅ"), bstack11l1lll_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᏆ"), bstack11l1lll_opy_ (u"ࠤ࡬ࡨࡸࠨᏇ"), bstack11l1lll_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࠧᏈ"), bstack11l1lll_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᏉ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack11l1lll_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᏊ")) else fixturedef.get(bstack11l1lll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᏋ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11l1lll_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࠧᏌ")) else None
        node = request.node if hasattr(request, bstack11l1lll_opy_ (u"ࠣࡰࡲࡨࡪࠨᏍ")) else None
        target = request.node.nodeid if hasattr(node, bstack11l1lll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᏎ")) else None
        baseid = fixturedef.get(bstack11l1lll_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᏏ"), None) or bstack11l1lll_opy_ (u"ࠦࠧᏐ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11l1lll_opy_ (u"ࠧࡥࡰࡺࡨࡸࡲࡨ࡯ࡴࡦ࡯ࠥᏑ")):
            target = PytestBDDFramework.__1l111l11l11_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11l1lll_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᏒ")) else None
            if target and not TestFramework.bstack11111l1111_opy_(target):
                self.__1l111l1llll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11l1lll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡱࡳࡩ࡫࠽ࡼࡰࡲࡨࡪࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᏓ") + str(test_hook_state) + bstack11l1lll_opy_ (u"ࠣࠤᏔ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11l1lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᏕ") + str(target) + bstack11l1lll_opy_ (u"ࠥࠦᏖ"))
            return None
        instance = TestFramework.bstack11111l1111_opy_(target)
        if not instance:
            self.logger.warning(bstack11l1lll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡦࡦࡹࡥࡪࡦࡀࡿࡧࡧࡳࡦ࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᏗ") + str(target) + bstack11l1lll_opy_ (u"ࠧࠨᏘ"))
            return None
        bstack1l11ll1111l_opy_ = TestFramework.bstack1llllll11l1_opy_(instance, PytestBDDFramework.bstack1l11l1lllll_opy_, {})
        if os.getenv(bstack11l1lll_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡌࡉ࡙ࡖࡘࡖࡊ࡙ࠢᏙ"), bstack11l1lll_opy_ (u"ࠢ࠲ࠤᏚ")) == bstack11l1lll_opy_ (u"ࠣ࠳ࠥᏛ"):
            bstack1l11l11l11l_opy_ = bstack11l1lll_opy_ (u"ࠤ࠽ࠦᏜ").join((scope, fixturename))
            bstack1l11ll111ll_opy_ = datetime.now(tz=timezone.utc)
            bstack1l111llll11_opy_ = {
                bstack11l1lll_opy_ (u"ࠥ࡯ࡪࡿࠢᏝ"): bstack1l11l11l11l_opy_,
                bstack11l1lll_opy_ (u"ࠦࡹࡧࡧࡴࠤᏞ"): PytestBDDFramework.__1l111l1111l_opy_(request.node, scenario),
                bstack11l1lll_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࠨᏟ"): fixturedef,
                bstack11l1lll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᏠ"): scope,
                bstack11l1lll_opy_ (u"ࠢࡵࡻࡳࡩࠧᏡ"): None,
            }
            try:
                if test_hook_state == bstack1ll1lll1111_opy_.POST and callable(getattr(args[-1], bstack11l1lll_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᏢ"), None)):
                    bstack1l111llll11_opy_[bstack11l1lll_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᏣ")] = TestFramework.bstack1l1lll1lll1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1lll1111_opy_.PRE:
                bstack1l111llll11_opy_[bstack11l1lll_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᏤ")] = uuid4().__str__()
                bstack1l111llll11_opy_[PytestBDDFramework.bstack1l111ll1l1l_opy_] = bstack1l11ll111ll_opy_
            elif test_hook_state == bstack1ll1lll1111_opy_.POST:
                bstack1l111llll11_opy_[PytestBDDFramework.bstack1l11l11l111_opy_] = bstack1l11ll111ll_opy_
            if bstack1l11l11l11l_opy_ in bstack1l11ll1111l_opy_:
                bstack1l11ll1111l_opy_[bstack1l11l11l11l_opy_].update(bstack1l111llll11_opy_)
                self.logger.debug(bstack11l1lll_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࠧᏥ") + str(bstack1l11ll1111l_opy_[bstack1l11l11l11l_opy_]) + bstack11l1lll_opy_ (u"ࠧࠨᏦ"))
            else:
                bstack1l11ll1111l_opy_[bstack1l11l11l11l_opy_] = bstack1l111llll11_opy_
                self.logger.debug(bstack11l1lll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࢀࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࢁࠥࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࠤᏧ") + str(len(bstack1l11ll1111l_opy_)) + bstack11l1lll_opy_ (u"ࠢࠣᏨ"))
        TestFramework.bstack111111llll_opy_(instance, PytestBDDFramework.bstack1l11l1lllll_opy_, bstack1l11ll1111l_opy_)
        self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࡾࡰࡪࡴࠨࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠬࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᏩ") + str(instance.ref()) + bstack11l1lll_opy_ (u"ࠤࠥᏪ"))
        return instance
    def __1l111l1llll_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll11llll1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack11111l1lll_opy_.create_context(target)
        ob = bstack1llll1111ll_opy_(ctx, self.bstack1ll1l1l1111_opy_, self.bstack1l111l1l11l_opy_, test_framework_state)
        TestFramework.bstack1l11l1l1l1l_opy_(ob, {
            TestFramework.bstack1ll1l1lll1l_opy_: context.test_framework_name,
            TestFramework.bstack1l1lllllll1_opy_: context.test_framework_version,
            TestFramework.bstack1l11l1111ll_opy_: [],
            PytestBDDFramework.bstack1l11l1lllll_opy_: {},
            PytestBDDFramework.bstack1l11ll11111_opy_: {},
            PytestBDDFramework.bstack1l111ll11l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack111111llll_opy_(ob, TestFramework.bstack1l11ll1l11l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack111111llll_opy_(ob, TestFramework.bstack1ll11l1l1ll_opy_, context.platform_index)
        TestFramework.bstack1lllllll111_opy_[ctx.id] = ob
        self.logger.debug(bstack11l1lll_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡨࡺࡸ࠯࡫ࡧࡁࢀࡩࡴࡹ࠰࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥᏫ") + str(TestFramework.bstack1lllllll111_opy_.keys()) + bstack11l1lll_opy_ (u"ࠦࠧᏬ"))
        return ob
    @staticmethod
    def __1l11l1lll11_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l1lll_opy_ (u"ࠬ࡯ࡤࠨᏭ"): id(step),
                bstack11l1lll_opy_ (u"࠭ࡴࡦࡺࡷࠫᏮ"): step.name,
                bstack11l1lll_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨᏯ"): step.keyword,
            })
        meta = {
            bstack11l1lll_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩᏰ"): {
                bstack11l1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᏱ"): feature.name,
                bstack11l1lll_opy_ (u"ࠪࡴࡦࡺࡨࠨᏲ"): feature.filename,
                bstack11l1lll_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᏳ"): feature.description
            },
            bstack11l1lll_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧᏴ"): {
                bstack11l1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᏵ"): scenario.name
            },
            bstack11l1lll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭᏶"): steps,
            bstack11l1lll_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪ᏷"): PytestBDDFramework.__1l11l11l1l1_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l11l1l1ll1_opy_: meta
            }
        )
    def bstack1l11l11llll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11l1lll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤࡹ࡮ࡥࠡࡌࡤࡺࡦࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬࡮ࡹࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡃࡩࡧࡦ࡯ࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡬ࡲࡸ࡯ࡤࡦࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠳࡚ࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡉࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠭ࠢࡵࡩࡵࡲࡡࡤࡧࡶࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦࠥ࡯࡮ࠡ࡫ࡷࡷࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡌࡪࠥࡧࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡯ࡤࡸࡨ࡮ࡥࡴࠢࡤࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࠦࡨࡰࡱ࡮࠱ࡱ࡫ࡶࡦ࡮ࠣࡪ࡮ࡲࡥ࠭ࠢ࡬ࡸࠥࡩࡲࡦࡣࡷࡩࡸࠦࡡࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࠣࡻ࡮ࡺࡨࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡙ࠥࡩ࡮࡫࡯ࡥࡷࡲࡹ࠭ࠢ࡬ࡸࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡴࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡥࡽࠥࡸࡥࡱ࡮ࡤࡧ࡮ࡴࡧࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡖ࡫ࡩࠥࡩࡲࡦࡣࡷࡩࡩࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡤࡶࡪࠦࡡࡥࡦࡨࡨࠥࡺ࡯ࠡࡶ࡫ࡩࠥ࡮࡯ࡰ࡭ࠪࡷࠥࠨ࡬ࡰࡩࡶࠦࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࠺ࠡࡖ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷࠥࡧ࡮ࡥࠢ࡫ࡳࡴࡱࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡘࡪࡹࡴࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᏸ")
        global _1ll111l111l_opy_
        platform_index = os.environ[bstack11l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᏹ")]
        bstack1l1llll1111_opy_ = os.path.join(bstack1l1lllll111_opy_, (bstack1l1lll1llll_opy_ + str(platform_index)), bstack1l11l1ll1l1_opy_)
        if not os.path.exists(bstack1l1llll1111_opy_) or not os.path.isdir(bstack1l1llll1111_opy_):
            return
        logs = hook.get(bstack11l1lll_opy_ (u"ࠦࡱࡵࡧࡴࠤᏺ"), [])
        with os.scandir(bstack1l1llll1111_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1ll111l111l_opy_:
                    self.logger.info(bstack11l1lll_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᏻ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11l1lll_opy_ (u"ࠨࠢᏼ")
                    log_entry = bstack1lll1l11111_opy_(
                        kind=bstack11l1lll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᏽ"),
                        message=bstack11l1lll_opy_ (u"ࠣࠤ᏾"),
                        level=bstack11l1lll_opy_ (u"ࠤࠥ᏿"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1ll1ll1l1_opy_=entry.stat().st_size,
                        bstack1l1llll11l1_opy_=bstack11l1lll_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥ᐀"),
                        bstack111ll1l_opy_=os.path.abspath(entry.path),
                        bstack1l111l1l111_opy_=hook.get(TestFramework.bstack1l111l11111_opy_)
                    )
                    logs.append(log_entry)
                    _1ll111l111l_opy_.add(abs_path)
        platform_index = os.environ[bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᐁ")]
        bstack1l111ll11ll_opy_ = os.path.join(bstack1l1lllll111_opy_, (bstack1l1lll1llll_opy_ + str(platform_index)), bstack1l11l1ll1l1_opy_, bstack1l11l11l1ll_opy_)
        if not os.path.exists(bstack1l111ll11ll_opy_) or not os.path.isdir(bstack1l111ll11ll_opy_):
            self.logger.info(bstack11l1lll_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢᐂ").format(bstack1l111ll11ll_opy_))
        else:
            self.logger.info(bstack11l1lll_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᐃ").format(bstack1l111ll11ll_opy_))
            with os.scandir(bstack1l111ll11ll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1ll111l111l_opy_:
                        self.logger.info(bstack11l1lll_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᐄ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11l1lll_opy_ (u"ࠣࠤᐅ")
                        log_entry = bstack1lll1l11111_opy_(
                            kind=bstack11l1lll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᐆ"),
                            message=bstack11l1lll_opy_ (u"ࠥࠦᐇ"),
                            level=bstack11l1lll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᐈ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1ll1ll1l1_opy_=entry.stat().st_size,
                            bstack1l1llll11l1_opy_=bstack11l1lll_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᐉ"),
                            bstack111ll1l_opy_=os.path.abspath(entry.path),
                            bstack1ll1111ll11_opy_=hook.get(TestFramework.bstack1l111l11111_opy_)
                        )
                        logs.append(log_entry)
                        _1ll111l111l_opy_.add(abs_path)
        hook[bstack11l1lll_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᐊ")] = logs
    def bstack1l1llll111l_opy_(
        self,
        bstack1l1lll1ll1l_opy_: bstack1llll1111ll_opy_,
        entries: List[bstack1lll1l11111_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11l1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᐋ"))
        req.platform_index = TestFramework.bstack1llllll11l1_opy_(bstack1l1lll1ll1l_opy_, TestFramework.bstack1ll11l1l1ll_opy_)
        req.execution_context.hash = str(bstack1l1lll1ll1l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll1ll1l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll1ll1l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllll11l1_opy_(bstack1l1lll1ll1l_opy_, TestFramework.bstack1ll1l1lll1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllll11l1_opy_(bstack1l1lll1ll1l_opy_, TestFramework.bstack1l1lllllll1_opy_)
            log_entry.uuid = entry.bstack1l111l1l111_opy_
            log_entry.test_framework_state = bstack1l1lll1ll1l_opy_.state.name
            log_entry.message = entry.message.encode(bstack11l1lll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᐌ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11l1lll_opy_ (u"ࠤࠥᐍ")
            if entry.kind == bstack11l1lll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᐎ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll1ll1l1_opy_
                log_entry.file_path = entry.bstack111ll1l_opy_
        def bstack1l1lll11l11_opy_():
            bstack11llll111l_opy_ = datetime.now()
            try:
                self.bstack1llll111ll1_opy_.LogCreatedEvent(req)
                bstack1l1lll1ll1l_opy_.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᐏ"), datetime.now() - bstack11llll111l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1lll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࢀࠦᐐ").format(str(e)))
                traceback.print_exc()
        self.bstack11111llll1_opy_.enqueue(bstack1l1lll11l11_opy_)
    def __1l111l1l1ll_opy_(self, instance) -> None:
        bstack11l1lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᐑ")
        bstack1l111l11lll_opy_ = {bstack11l1lll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᐒ"): bstack1lll1lll1l1_opy_.bstack1l11l1ll111_opy_()}
        TestFramework.bstack1l11l1l1l1l_opy_(instance, bstack1l111l11lll_opy_)
    @staticmethod
    def __1l11l11111l_opy_(instance, args):
        request, bstack1l11l1ll11l_opy_ = args
        bstack1l111ll1111_opy_ = id(bstack1l11l1ll11l_opy_)
        bstack1l111ll1lll_opy_ = instance.data[TestFramework.bstack1l11l1l1ll1_opy_]
        step = next(filter(lambda st: st[bstack11l1lll_opy_ (u"ࠨ࡫ࡧࠫᐓ")] == bstack1l111ll1111_opy_, bstack1l111ll1lll_opy_[bstack11l1lll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᐔ")]), None)
        step.update({
            bstack11l1lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᐕ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l111ll1lll_opy_[bstack11l1lll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᐖ")]) if st[bstack11l1lll_opy_ (u"ࠬ࡯ࡤࠨᐗ")] == step[bstack11l1lll_opy_ (u"࠭ࡩࡥࠩᐘ")]), None)
        if index is not None:
            bstack1l111ll1lll_opy_[bstack11l1lll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐙ")][index] = step
        instance.data[TestFramework.bstack1l11l1l1ll1_opy_] = bstack1l111ll1lll_opy_
    @staticmethod
    def __1l111lll11l_opy_(instance, args):
        bstack11l1lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡽࡨࡦࡰࠣࡰࡪࡴࠠࡢࡴࡪࡷࠥ࡯ࡳࠡ࠴࠯ࠤ࡮ࡺࠠࡴ࡫ࡪࡲ࡮࡬ࡩࡦࡵࠣࡸ࡭࡫ࡲࡦࠢ࡬ࡷࠥࡴ࡯ࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡤࡶ࡬ࡹࠠࡢࡴࡨࠤ࠲࡛ࠦࡳࡧࡴࡹࡪࡹࡴ࠭ࠢࡶࡸࡪࡶ࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡪࠥࡧࡲࡨࡵࠣࡥࡷ࡫ࠠ࠴ࠢࡷ࡬ࡪࡴࠠࡵࡪࡨࠤࡱࡧࡳࡵࠢࡹࡥࡱࡻࡥࠡ࡫ࡶࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᐚ")
        bstack1l11l1l1111_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l11l1ll11l_opy_ = args[1]
        bstack1l111ll1111_opy_ = id(bstack1l11l1ll11l_opy_)
        bstack1l111ll1lll_opy_ = instance.data[TestFramework.bstack1l11l1l1ll1_opy_]
        step = None
        if bstack1l111ll1111_opy_ is not None and bstack1l111ll1lll_opy_.get(bstack11l1lll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᐛ")):
            step = next(filter(lambda st: st[bstack11l1lll_opy_ (u"ࠪ࡭ࡩ࠭ᐜ")] == bstack1l111ll1111_opy_, bstack1l111ll1lll_opy_[bstack11l1lll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᐝ")]), None)
            step.update({
                bstack11l1lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᐞ"): bstack1l11l1l1111_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack11l1lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᐟ"): bstack11l1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᐠ"),
                bstack11l1lll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᐡ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack11l1lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᐢ"): bstack11l1lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᐣ"),
                })
        index = next((i for i, st in enumerate(bstack1l111ll1lll_opy_[bstack11l1lll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᐤ")]) if st[bstack11l1lll_opy_ (u"ࠬ࡯ࡤࠨᐥ")] == step[bstack11l1lll_opy_ (u"࠭ࡩࡥࠩᐦ")]), None)
        if index is not None:
            bstack1l111ll1lll_opy_[bstack11l1lll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐧ")][index] = step
        instance.data[TestFramework.bstack1l11l1l1ll1_opy_] = bstack1l111ll1lll_opy_
    @staticmethod
    def __1l11l11l1l1_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack11l1lll_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᐨ")):
                examples = list(node.callspec.params[bstack11l1lll_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨᐩ")].values())
            return examples
        except:
            return []
    def bstack1l1ll1l1lll_opy_(self, instance: bstack1llll1111ll_opy_, bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_]):
        bstack1l11ll11ll1_opy_ = (
            PytestBDDFramework.bstack1l11l1111l1_opy_
            if bstack11111l11l1_opy_[1] == bstack1ll1lll1111_opy_.PRE
            else PytestBDDFramework.bstack1l1111lll11_opy_
        )
        hook = PytestBDDFramework.bstack1l111lll1l1_opy_(instance, bstack1l11ll11ll1_opy_)
        entries = hook.get(TestFramework.bstack1l1111ll1ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1l11l1111ll_opy_, []))
        return entries
    def bstack1ll11111l11_opy_(self, instance: bstack1llll1111ll_opy_, bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_]):
        bstack1l11ll11ll1_opy_ = (
            PytestBDDFramework.bstack1l11l1111l1_opy_
            if bstack11111l11l1_opy_[1] == bstack1ll1lll1111_opy_.PRE
            else PytestBDDFramework.bstack1l1111lll11_opy_
        )
        PytestBDDFramework.bstack1l111lllll1_opy_(instance, bstack1l11ll11ll1_opy_)
        TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1l11l1111ll_opy_, []).clear()
    @staticmethod
    def bstack1l111lll1l1_opy_(instance: bstack1llll1111ll_opy_, bstack1l11ll11ll1_opy_: str):
        bstack1l11l111ll1_opy_ = (
            PytestBDDFramework.bstack1l11ll11111_opy_
            if bstack1l11ll11ll1_opy_ == PytestBDDFramework.bstack1l1111lll11_opy_
            else PytestBDDFramework.bstack1l111ll11l1_opy_
        )
        bstack1l111ll1l11_opy_ = TestFramework.bstack1llllll11l1_opy_(instance, bstack1l11ll11ll1_opy_, None)
        bstack1l1111lll1l_opy_ = TestFramework.bstack1llllll11l1_opy_(instance, bstack1l11l111ll1_opy_, None) if bstack1l111ll1l11_opy_ else None
        return (
            bstack1l1111lll1l_opy_[bstack1l111ll1l11_opy_][-1]
            if isinstance(bstack1l1111lll1l_opy_, dict) and len(bstack1l1111lll1l_opy_.get(bstack1l111ll1l11_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111lllll1_opy_(instance: bstack1llll1111ll_opy_, bstack1l11ll11ll1_opy_: str):
        hook = PytestBDDFramework.bstack1l111lll1l1_opy_(instance, bstack1l11ll11ll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1111ll1ll_opy_, []).clear()
    @staticmethod
    def __1l111l111l1_opy_(instance: bstack1llll1111ll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11l1lll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡦࡳࡷࡪࡳࠣᐪ"), None)):
            return
        if os.getenv(bstack11l1lll_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡐࡔࡍࡓࠣᐫ"), bstack11l1lll_opy_ (u"ࠧ࠷ࠢᐬ")) != bstack11l1lll_opy_ (u"ࠨ࠱ࠣᐭ"):
            PytestBDDFramework.logger.warning(bstack11l1lll_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡯࡮ࡨࠢࡦࡥࡵࡲ࡯ࡨࠤᐮ"))
            return
        bstack1l1111lllll_opy_ = {
            bstack11l1lll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᐯ"): (PytestBDDFramework.bstack1l11l1111l1_opy_, PytestBDDFramework.bstack1l111ll11l1_opy_),
            bstack11l1lll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᐰ"): (PytestBDDFramework.bstack1l1111lll11_opy_, PytestBDDFramework.bstack1l11ll11111_opy_),
        }
        for when in (bstack11l1lll_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᐱ"), bstack11l1lll_opy_ (u"ࠦࡨࡧ࡬࡭ࠤᐲ"), bstack11l1lll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᐳ")):
            bstack1l111ll1ll1_opy_ = args[1].get_records(when)
            if not bstack1l111ll1ll1_opy_:
                continue
            records = [
                bstack1lll1l11111_opy_(
                    kind=TestFramework.bstack1l1ll1llll1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11l1lll_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠤᐴ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11l1lll_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࠣᐵ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111ll1ll1_opy_
                if isinstance(getattr(r, bstack11l1lll_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᐶ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l111l11ll1_opy_, bstack1l11l111ll1_opy_ = bstack1l1111lllll_opy_.get(when, (None, None))
            bstack1l11l1llll1_opy_ = TestFramework.bstack1llllll11l1_opy_(instance, bstack1l111l11ll1_opy_, None) if bstack1l111l11ll1_opy_ else None
            bstack1l1111lll1l_opy_ = TestFramework.bstack1llllll11l1_opy_(instance, bstack1l11l111ll1_opy_, None) if bstack1l11l1llll1_opy_ else None
            if isinstance(bstack1l1111lll1l_opy_, dict) and len(bstack1l1111lll1l_opy_.get(bstack1l11l1llll1_opy_, [])) > 0:
                hook = bstack1l1111lll1l_opy_[bstack1l11l1llll1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l1111ll1ll_opy_ in hook:
                    hook[TestFramework.bstack1l1111ll1ll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1l11l1111ll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l11l1l111l_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack11ll111l11_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l11ll1l1l1_opy_(request.node, scenario)
        bstack1l11l1l11l1_opy_ = feature.filename
        if not bstack11ll111l11_opy_ or not test_name or not bstack1l11l1l11l1_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll11lll11l_opy_: uuid4().__str__(),
            TestFramework.bstack1l1111ll1l1_opy_: bstack11ll111l11_opy_,
            TestFramework.bstack1ll1l111lll_opy_: test_name,
            TestFramework.bstack1l1ll111l11_opy_: bstack11ll111l11_opy_,
            TestFramework.bstack1l111lll1ll_opy_: bstack1l11l1l11l1_opy_,
            TestFramework.bstack1l11l111lll_opy_: PytestBDDFramework.__1l111l1111l_opy_(feature, scenario),
            TestFramework.bstack1l111ll111l_opy_: code,
            TestFramework.bstack1l1l1l1l1ll_opy_: TestFramework.bstack1l11l1lll1l_opy_,
            TestFramework.bstack1l11llll11l_opy_: test_name
        }
    @staticmethod
    def __1l11ll1l1l1_opy_(node, scenario):
        if hasattr(node, bstack11l1lll_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᐷ")):
            parts = node.nodeid.rsplit(bstack11l1lll_opy_ (u"ࠥ࡟ࠧᐸ"))
            params = parts[-1]
            return bstack11l1lll_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦᐹ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l111l1111l_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack11l1lll_opy_ (u"ࠬࡺࡡࡨࡵࠪᐺ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack11l1lll_opy_ (u"࠭ࡴࡢࡩࡶࠫᐻ")) else [])
    @staticmethod
    def __1l111l11l11_opy_(location):
        return bstack11l1lll_opy_ (u"ࠢ࠻࠼ࠥᐼ").join(filter(lambda x: isinstance(x, str), location))