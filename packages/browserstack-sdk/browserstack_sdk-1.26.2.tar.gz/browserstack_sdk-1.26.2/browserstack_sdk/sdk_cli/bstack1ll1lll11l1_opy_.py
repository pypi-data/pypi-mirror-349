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
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll1l111ll_opy_,
    bstack1lll11111l1_opy_,
    bstack1llll1lll1l_opy_,
    bstack1l111l111l1_opy_,
    bstack1lll1l11l11_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1lll11l1l_opy_
from bstack_utils.bstack11l11111l_opy_ import bstack1ll1ll1ll11_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import bstack1111l1111l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llll1l1l11_opy_ import bstack1lllll1l111_opy_
from bstack_utils.bstack111lllllll_opy_ import bstack1lllll1l1l_opy_
bstack1l1llll1l1l_opy_ = bstack1l1lll11l1l_opy_()
bstack1l11l1lllll_opy_ = 1.0
bstack1ll1111l1ll_opy_ = bstack111l11_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧᑈ")
bstack1l1111l11ll_opy_ = bstack111l11_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᑉ")
bstack1l1111l1l1l_opy_ = bstack111l11_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᑊ")
bstack1l1111l111l_opy_ = bstack111l11_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦᑋ")
bstack1l1111l1l11_opy_ = bstack111l11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣᑌ")
_1l1lll1111l_opy_ = set()
class bstack1lllll1111l_opy_(TestFramework):
    bstack1l11l1ll111_opy_ = bstack111l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᑍ")
    bstack1l111l1lll1_opy_ = bstack111l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤᑎ")
    bstack1l11ll1111l_opy_ = bstack111l11_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᑏ")
    bstack1l11l1l1lll_opy_ = bstack111l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᑐ")
    bstack1l111l1l11l_opy_ = bstack111l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᑑ")
    bstack1l11l11l11l_opy_: bool
    bstack1111l111l1_opy_: bstack1111l1111l_opy_  = None
    bstack1lll111lll1_opy_ = None
    bstack1l11l1ll11l_opy_ = [
        bstack1lll1l111ll_opy_.BEFORE_ALL,
        bstack1lll1l111ll_opy_.AFTER_ALL,
        bstack1lll1l111ll_opy_.BEFORE_EACH,
        bstack1lll1l111ll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11l1l11ll_opy_: Dict[str, str],
        bstack1ll1l1l11l1_opy_: List[str]=[bstack111l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᑒ")],
        bstack1111l111l1_opy_: bstack1111l1111l_opy_=None,
        bstack1lll111lll1_opy_=None
    ):
        super().__init__(bstack1ll1l1l11l1_opy_, bstack1l11l1l11ll_opy_, bstack1111l111l1_opy_)
        self.bstack1l11l11l11l_opy_ = any(bstack111l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᑓ") in item.lower() for item in bstack1ll1l1l11l1_opy_)
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
        if test_framework_state == bstack1lll1l111ll_opy_.TEST or test_framework_state in bstack1lllll1111l_opy_.bstack1l11l1ll11l_opy_:
            bstack1l11l1111ll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll1l111ll_opy_.NONE:
            self.logger.warning(bstack111l11_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦᑔ") + str(test_hook_state) + bstack111l11_opy_ (u"ࠦࠧᑕ"))
            return
        if not self.bstack1l11l11l11l_opy_:
            self.logger.warning(bstack111l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨᑖ") + str(str(self.bstack1ll1l1l11l1_opy_)) + bstack111l11_opy_ (u"ࠨࠢᑗ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack111l11_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᑘ") + str(kwargs) + bstack111l11_opy_ (u"ࠣࠤᑙ"))
            return
        instance = self.__1l111l1ll11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack111l11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣᑚ") + str(args) + bstack111l11_opy_ (u"ࠥࠦᑛ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1lllll1111l_opy_.bstack1l11l1ll11l_opy_ and test_hook_state == bstack1llll1lll1l_opy_.PRE:
                bstack1ll1l11ll1l_opy_ = bstack1ll1ll1ll11_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack1llll1l11_opy_.value)
                name = str(EVENTS.bstack1llll1l11_opy_.name)+bstack111l11_opy_ (u"ࠦ࠿ࠨᑜ")+str(test_framework_state.name)
                TestFramework.bstack1l11ll111ll_opy_(instance, name, bstack1ll1l11ll1l_opy_)
        except Exception as e:
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤᑝ").format(e))
        try:
            if not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1l111llllll_opy_) and test_hook_state == bstack1llll1lll1l_opy_.PRE:
                test = bstack1lllll1111l_opy_.__1l111l11111_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack111l11_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᑞ") + str(test_hook_state) + bstack111l11_opy_ (u"ࠢࠣᑟ"))
            if test_framework_state == bstack1lll1l111ll_opy_.TEST:
                if test_hook_state == bstack1llll1lll1l_opy_.PRE and not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1ll11111111_opy_):
                    TestFramework.bstack111111ll1l_opy_(instance, TestFramework.bstack1ll11111111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111l11_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᑠ") + str(test_hook_state) + bstack111l11_opy_ (u"ࠤࠥᑡ"))
                elif test_hook_state == bstack1llll1lll1l_opy_.POST and not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1ll11111lll_opy_):
                    TestFramework.bstack111111ll1l_opy_(instance, TestFramework.bstack1ll11111lll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111l11_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᑢ") + str(test_hook_state) + bstack111l11_opy_ (u"ࠦࠧᑣ"))
            elif test_framework_state == bstack1lll1l111ll_opy_.LOG and test_hook_state == bstack1llll1lll1l_opy_.POST:
                bstack1lllll1111l_opy_.__1l111ll11l1_opy_(instance, *args)
            elif test_framework_state == bstack1lll1l111ll_opy_.LOG_REPORT and test_hook_state == bstack1llll1lll1l_opy_.POST:
                self.__1l111l1111l_opy_(instance, *args)
                self.__1l11l111ll1_opy_(instance)
            elif test_framework_state in bstack1lllll1111l_opy_.bstack1l11l1ll11l_opy_:
                self.__1l111l11lll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᑤ") + str(instance.ref()) + bstack111l11_opy_ (u"ࠨࠢᑥ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11l11l1l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1lllll1111l_opy_.bstack1l11l1ll11l_opy_ and test_hook_state == bstack1llll1lll1l_opy_.POST:
                name = str(EVENTS.bstack1llll1l11_opy_.name)+bstack111l11_opy_ (u"ࠢ࠻ࠤᑦ")+str(test_framework_state.name)
                bstack1ll1l11ll1l_opy_ = TestFramework.bstack1l111ll1111_opy_(instance, name)
                bstack1ll1ll1ll11_opy_.end(EVENTS.bstack1llll1l11_opy_.value, bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᑧ"), bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᑨ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack111l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᑩ").format(e))
    def bstack1l1lll11lll_opy_(self):
        return self.bstack1l11l11l11l_opy_
    def __1l11l1llll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack111l11_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᑪ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1lllll111_opy_(rep, [bstack111l11_opy_ (u"ࠧࡽࡨࡦࡰࠥᑫ"), bstack111l11_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᑬ"), bstack111l11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᑭ"), bstack111l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᑮ"), bstack111l11_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥᑯ"), bstack111l11_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᑰ")])
        return None
    def __1l111l1111l_opy_(self, instance: bstack1lll11111l1_opy_, *args):
        result = self.__1l11l1llll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111l11ll1_opy_ = None
        if result.get(bstack111l11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᑱ"), None) == bstack111l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᑲ") and len(args) > 1 and getattr(args[1], bstack111l11_opy_ (u"ࠨࡥࡹࡥ࡬ࡲ࡫ࡵࠢᑳ"), None) is not None:
            failure = [{bstack111l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᑴ"): [args[1].excinfo.exconly(), result.get(bstack111l11_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᑵ"), None)]}]
            bstack1111l11ll1_opy_ = bstack111l11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᑶ") if bstack111l11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᑷ") in getattr(args[1].excinfo, bstack111l11_opy_ (u"ࠦࡹࡿࡰࡦࡰࡤࡱࡪࠨᑸ"), bstack111l11_opy_ (u"ࠧࠨᑹ")) else bstack111l11_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᑺ")
        bstack1l111lllll1_opy_ = result.get(bstack111l11_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᑻ"), TestFramework.bstack1l11l111lll_opy_)
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
            target = None # bstack1l11l1l11l1_opy_ bstack1l11l1l1l1l_opy_ this to be bstack111l11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᑼ")
            if test_framework_state == bstack1lll1l111ll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11ll11l1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll1l111ll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack111l11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᑽ"), None), bstack111l11_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᑾ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack111l11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᑿ"), None):
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
        bstack1l111l1ll1l_opy_ = TestFramework.bstack1llllll1111_opy_(instance, bstack1lllll1111l_opy_.bstack1l111l1lll1_opy_, {})
        if not key in bstack1l111l1ll1l_opy_:
            bstack1l111l1ll1l_opy_[key] = []
        bstack1l11l1l1ll1_opy_ = TestFramework.bstack1llllll1111_opy_(instance, bstack1lllll1111l_opy_.bstack1l11ll1111l_opy_, {})
        if not key in bstack1l11l1l1ll1_opy_:
            bstack1l11l1l1ll1_opy_[key] = []
        bstack1l111l11ll1_opy_ = {
            bstack1lllll1111l_opy_.bstack1l111l1lll1_opy_: bstack1l111l1ll1l_opy_,
            bstack1lllll1111l_opy_.bstack1l11ll1111l_opy_: bstack1l11l1l1ll1_opy_,
        }
        if test_hook_state == bstack1llll1lll1l_opy_.PRE:
            hook = {
                bstack111l11_opy_ (u"ࠧࡱࡥࡺࠤᒀ"): key,
                TestFramework.bstack1l11l1lll11_opy_: uuid4().__str__(),
                TestFramework.bstack1l11ll111l1_opy_: TestFramework.bstack1l111l1l1ll_opy_,
                TestFramework.bstack1l111l111ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l111ll1l1l_opy_: [],
                TestFramework.bstack1l11l11l1ll_opy_: args[1] if len(args) > 1 else bstack111l11_opy_ (u"࠭ࠧᒁ"),
                TestFramework.bstack1l11l1ll1l1_opy_: bstack1lllll1l111_opy_.bstack1l1111lll11_opy_()
            }
            bstack1l111l1ll1l_opy_[key].append(hook)
            bstack1l111l11ll1_opy_[bstack1lllll1111l_opy_.bstack1l11l1l1lll_opy_] = key
        elif test_hook_state == bstack1llll1lll1l_opy_.POST:
            bstack1l111llll1l_opy_ = bstack1l111l1ll1l_opy_.get(key, [])
            hook = bstack1l111llll1l_opy_.pop() if bstack1l111llll1l_opy_ else None
            if hook:
                result = self.__1l11l1llll1_opy_(*args)
                if result:
                    bstack1l11l111111_opy_ = result.get(bstack111l11_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᒂ"), TestFramework.bstack1l111l1l1ll_opy_)
                    if bstack1l11l111111_opy_ != TestFramework.bstack1l111l1l1ll_opy_:
                        hook[TestFramework.bstack1l11ll111l1_opy_] = bstack1l11l111111_opy_
                hook[TestFramework.bstack1l11l1l1l11_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11l1ll1l1_opy_]= bstack1lllll1l111_opy_.bstack1l1111lll11_opy_()
                self.bstack1l111llll11_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11l1l111l_opy_, [])
                if logs: self.bstack1l1ll1lll1l_opy_(instance, logs)
                bstack1l11l1l1ll1_opy_[key].append(hook)
                bstack1l111l11ll1_opy_[bstack1lllll1111l_opy_.bstack1l111l1l11l_opy_] = key
        TestFramework.bstack1l111lll1l1_opy_(instance, bstack1l111l11ll1_opy_)
        self.logger.debug(bstack111l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼ࡭ࡨࡽࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࡀࡿ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࠢᒃ") + str(bstack1l11l1l1ll1_opy_) + bstack111l11_opy_ (u"ࠤࠥᒄ"))
    def __1l11ll1l111_opy_(
        self,
        context: bstack1l111l111l1_opy_,
        test_framework_state: bstack1lll1l111ll_opy_,
        test_hook_state: bstack1llll1lll1l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1lllll111_opy_(args[0], [bstack111l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᒅ"), bstack111l11_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧᒆ"), bstack111l11_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧᒇ"), bstack111l11_opy_ (u"ࠨࡩࡥࡵࠥᒈ"), bstack111l11_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤᒉ"), bstack111l11_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᒊ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack111l11_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᒋ")) else fixturedef.get(bstack111l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᒌ"), None)
        fixturename = request.fixturename if hasattr(request, bstack111l11_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤᒍ")) else None
        node = request.node if hasattr(request, bstack111l11_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᒎ")) else None
        target = request.node.nodeid if hasattr(node, bstack111l11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᒏ")) else None
        baseid = fixturedef.get(bstack111l11_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᒐ"), None) or bstack111l11_opy_ (u"ࠣࠤᒑ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack111l11_opy_ (u"ࠤࡢࡴࡾ࡬ࡵ࡯ࡥ࡬ࡸࡪࡳࠢᒒ")):
            target = bstack1lllll1111l_opy_.__1l11ll11ll1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack111l11_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᒓ")) else None
            if target and not TestFramework.bstack11111ll111_opy_(target):
                self.__1l11ll11l1l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack111l11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦ࡮ࡰࡦࡨࡁࢀࡴ࡯ࡥࡧࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᒔ") + str(test_hook_state) + bstack111l11_opy_ (u"ࠧࠨᒕ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack111l11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᒖ") + str(target) + bstack111l11_opy_ (u"ࠢࠣᒗ"))
            return None
        instance = TestFramework.bstack11111ll111_opy_(target)
        if not instance:
            self.logger.warning(bstack111l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡣࡣࡶࡩ࡮ࡪ࠽ࡼࡤࡤࡷࡪ࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᒘ") + str(target) + bstack111l11_opy_ (u"ࠤࠥᒙ"))
            return None
        bstack1l111l11l11_opy_ = TestFramework.bstack1llllll1111_opy_(instance, bstack1lllll1111l_opy_.bstack1l11l1ll111_opy_, {})
        if os.getenv(bstack111l11_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡉࡍ࡝࡚ࡕࡓࡇࡖࠦᒚ"), bstack111l11_opy_ (u"ࠦ࠶ࠨᒛ")) == bstack111l11_opy_ (u"ࠧ࠷ࠢᒜ"):
            bstack1l11l111l1l_opy_ = bstack111l11_opy_ (u"ࠨ࠺ࠣᒝ").join((scope, fixturename))
            bstack1l111ll111l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11ll11111_opy_ = {
                bstack111l11_opy_ (u"ࠢ࡬ࡧࡼࠦᒞ"): bstack1l11l111l1l_opy_,
                bstack111l11_opy_ (u"ࠣࡶࡤ࡫ࡸࠨᒟ"): bstack1lllll1111l_opy_.__1l11l11lll1_opy_(request.node),
                bstack111l11_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࠥᒠ"): fixturedef,
                bstack111l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᒡ"): scope,
                bstack111l11_opy_ (u"ࠦࡹࡿࡰࡦࠤᒢ"): None,
            }
            try:
                if test_hook_state == bstack1llll1lll1l_opy_.POST and callable(getattr(args[-1], bstack111l11_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᒣ"), None)):
                    bstack1l11ll11111_opy_[bstack111l11_opy_ (u"ࠨࡴࡺࡲࡨࠦᒤ")] = TestFramework.bstack1l1ll1llll1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1llll1lll1l_opy_.PRE:
                bstack1l11ll11111_opy_[bstack111l11_opy_ (u"ࠢࡶࡷ࡬ࡨࠧᒥ")] = uuid4().__str__()
                bstack1l11ll11111_opy_[bstack1lllll1111l_opy_.bstack1l111l111ll_opy_] = bstack1l111ll111l_opy_
            elif test_hook_state == bstack1llll1lll1l_opy_.POST:
                bstack1l11ll11111_opy_[bstack1lllll1111l_opy_.bstack1l11l1l1l11_opy_] = bstack1l111ll111l_opy_
            if bstack1l11l111l1l_opy_ in bstack1l111l11l11_opy_:
                bstack1l111l11l11_opy_[bstack1l11l111l1l_opy_].update(bstack1l11ll11111_opy_)
                self.logger.debug(bstack111l11_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࠤᒦ") + str(bstack1l111l11l11_opy_[bstack1l11l111l1l_opy_]) + bstack111l11_opy_ (u"ࠤࠥᒧ"))
            else:
                bstack1l111l11l11_opy_[bstack1l11l111l1l_opy_] = bstack1l11ll11111_opy_
                self.logger.debug(bstack111l11_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡾࠢࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࠨᒨ") + str(len(bstack1l111l11l11_opy_)) + bstack111l11_opy_ (u"ࠦࠧᒩ"))
        TestFramework.bstack111111ll1l_opy_(instance, bstack1lllll1111l_opy_.bstack1l11l1ll111_opy_, bstack1l111l11l11_opy_)
        self.logger.debug(bstack111l11_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࡻ࡭ࡧࡱࠬࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᒪ") + str(instance.ref()) + bstack111l11_opy_ (u"ࠨࠢᒫ"))
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
            bstack1lllll1111l_opy_.bstack1l11l1ll111_opy_: {},
            bstack1lllll1111l_opy_.bstack1l11ll1111l_opy_: {},
            bstack1lllll1111l_opy_.bstack1l111l1lll1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack111111ll1l_opy_(ob, TestFramework.bstack1l1111l1lll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack111111ll1l_opy_(ob, TestFramework.bstack1ll1l111lll_opy_, context.platform_index)
        TestFramework.bstack1111111l11_opy_[ctx.id] = ob
        self.logger.debug(bstack111l11_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢᒬ") + str(TestFramework.bstack1111111l11_opy_.keys()) + bstack111l11_opy_ (u"ࠣࠤᒭ"))
        return ob
    def bstack1l1ll1l111l_opy_(self, instance: bstack1lll11111l1_opy_, bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_]):
        bstack1l111lll11l_opy_ = (
            bstack1lllll1111l_opy_.bstack1l11l1l1lll_opy_
            if bstack11111l1ll1_opy_[1] == bstack1llll1lll1l_opy_.PRE
            else bstack1lllll1111l_opy_.bstack1l111l1l11l_opy_
        )
        hook = bstack1lllll1111l_opy_.bstack1l11l11111l_opy_(instance, bstack1l111lll11l_opy_)
        entries = hook.get(TestFramework.bstack1l111ll1l1l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llllll1111_opy_(instance, TestFramework.bstack1l11l11llll_opy_, []))
        return entries
    def bstack1l1lllll1ll_opy_(self, instance: bstack1lll11111l1_opy_, bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_]):
        bstack1l111lll11l_opy_ = (
            bstack1lllll1111l_opy_.bstack1l11l1l1lll_opy_
            if bstack11111l1ll1_opy_[1] == bstack1llll1lll1l_opy_.PRE
            else bstack1lllll1111l_opy_.bstack1l111l1l11l_opy_
        )
        bstack1lllll1111l_opy_.bstack1l111lll1ll_opy_(instance, bstack1l111lll11l_opy_)
        TestFramework.bstack1llllll1111_opy_(instance, TestFramework.bstack1l11l11llll_opy_, []).clear()
    def bstack1l111llll11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack111l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤࡹ࡮ࡥࠡࡌࡤࡺࡦࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬࡮ࡹࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡃࡩࡧࡦ࡯ࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡬ࡲࡸ࡯ࡤࡦࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠳࡚ࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡉࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠭ࠢࡵࡩࡵࡲࡡࡤࡧࡶࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦࠥ࡯࡮ࠡ࡫ࡷࡷࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡌࡪࠥࡧࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡯ࡤࡸࡨ࡮ࡥࡴࠢࡤࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࠦࡨࡰࡱ࡮࠱ࡱ࡫ࡶࡦ࡮ࠣࡪ࡮ࡲࡥ࠭ࠢ࡬ࡸࠥࡩࡲࡦࡣࡷࡩࡸࠦࡡࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࠣࡻ࡮ࡺࡨࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡙ࠥࡩ࡮࡫࡯ࡥࡷࡲࡹ࠭ࠢ࡬ࡸࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡴࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡥࡽࠥࡸࡥࡱ࡮ࡤࡧ࡮ࡴࡧࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡖ࡫ࡩࠥࡩࡲࡦࡣࡷࡩࡩࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡤࡶࡪࠦࡡࡥࡦࡨࡨࠥࡺ࡯ࠡࡶ࡫ࡩࠥ࡮࡯ࡰ࡭ࠪࡷࠥࠨ࡬ࡰࡩࡶࠦࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࠺ࠡࡖ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷࠥࡧ࡮ࡥࠢ࡫ࡳࡴࡱࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡘࡪࡹࡴࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᒮ")
        global _1l1lll1111l_opy_
        platform_index = os.environ[bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᒯ")]
        bstack1ll1111l111_opy_ = os.path.join(bstack1l1llll1l1l_opy_, (bstack1ll1111l1ll_opy_ + str(platform_index)), bstack1l1111l111l_opy_)
        if not os.path.exists(bstack1ll1111l111_opy_) or not os.path.isdir(bstack1ll1111l111_opy_):
            self.logger.info(bstack111l11_opy_ (u"ࠦࡉ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴࡴࠢࡷࡳࠥࡶࡲࡰࡥࡨࡷࡸࠦࡻࡾࠤᒰ").format(bstack1ll1111l111_opy_))
            return
        logs = hook.get(bstack111l11_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᒱ"), [])
        with os.scandir(bstack1ll1111l111_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1lll1111l_opy_:
                    self.logger.info(bstack111l11_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᒲ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack111l11_opy_ (u"ࠢࠣᒳ")
                    log_entry = bstack1lll1l11l11_opy_(
                        kind=bstack111l11_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᒴ"),
                        message=bstack111l11_opy_ (u"ࠤࠥᒵ"),
                        level=bstack111l11_opy_ (u"ࠥࠦᒶ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1llllllll_opy_=entry.stat().st_size,
                        bstack1l1ll1l1111_opy_=bstack111l11_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᒷ"),
                        bstack1ll1lll_opy_=os.path.abspath(entry.path),
                        bstack1l1111llll1_opy_=hook.get(TestFramework.bstack1l11l1lll11_opy_)
                    )
                    logs.append(log_entry)
                    _1l1lll1111l_opy_.add(abs_path)
        platform_index = os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᒸ")]
        bstack1l11l11ll11_opy_ = os.path.join(bstack1l1llll1l1l_opy_, (bstack1ll1111l1ll_opy_ + str(platform_index)), bstack1l1111l111l_opy_, bstack1l1111l1l11_opy_)
        if not os.path.exists(bstack1l11l11ll11_opy_) or not os.path.isdir(bstack1l11l11ll11_opy_):
            self.logger.info(bstack111l11_opy_ (u"ࠨࡎࡰࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤࠡࡣࡷ࠾ࠥࢁࡽࠣᒹ").format(bstack1l11l11ll11_opy_))
        else:
            self.logger.info(bstack111l11_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡨࡵࡳࡲࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᒺ").format(bstack1l11l11ll11_opy_))
            with os.scandir(bstack1l11l11ll11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1lll1111l_opy_:
                        self.logger.info(bstack111l11_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᒻ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack111l11_opy_ (u"ࠤࠥᒼ")
                        log_entry = bstack1lll1l11l11_opy_(
                            kind=bstack111l11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᒽ"),
                            message=bstack111l11_opy_ (u"ࠦࠧᒾ"),
                            level=bstack111l11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᒿ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1llllllll_opy_=entry.stat().st_size,
                            bstack1l1ll1l1111_opy_=bstack111l11_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᓀ"),
                            bstack1ll1lll_opy_=os.path.abspath(entry.path),
                            bstack1l1lll111l1_opy_=hook.get(TestFramework.bstack1l11l1lll11_opy_)
                        )
                        logs.append(log_entry)
                        _1l1lll1111l_opy_.add(abs_path)
        hook[bstack111l11_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᓁ")] = logs
    def bstack1l1ll1lll1l_opy_(
        self,
        bstack1l1lll11l11_opy_: bstack1lll11111l1_opy_,
        entries: List[bstack1lll1l11l11_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack111l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧᓂ"))
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
            log_entry.message = entry.message.encode(bstack111l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᓃ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack111l11_opy_ (u"ࠥࠦᓄ")
            if entry.kind == bstack111l11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᓅ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1llllllll_opy_
                log_entry.file_path = entry.bstack1ll1lll_opy_
        def bstack1ll1111ll11_opy_():
            bstack111l1l111_opy_ = datetime.now()
            try:
                self.bstack1lll111lll1_opy_.LogCreatedEvent(req)
                bstack1l1lll11l11_opy_.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᓆ"), datetime.now() - bstack111l1l111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111l11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧᓇ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l111l1_opy_.enqueue(bstack1ll1111ll11_opy_)
    def __1l11l111ll1_opy_(self, instance) -> None:
        bstack111l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᓈ")
        bstack1l111l11ll1_opy_ = {bstack111l11_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᓉ"): bstack1lllll1l111_opy_.bstack1l1111lll11_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l111lll1l1_opy_(instance, bstack1l111l11ll1_opy_)
    @staticmethod
    def bstack1l11l11111l_opy_(instance: bstack1lll11111l1_opy_, bstack1l111lll11l_opy_: str):
        bstack1l111lll111_opy_ = (
            bstack1lllll1111l_opy_.bstack1l11ll1111l_opy_
            if bstack1l111lll11l_opy_ == bstack1lllll1111l_opy_.bstack1l111l1l11l_opy_
            else bstack1lllll1111l_opy_.bstack1l111l1lll1_opy_
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
        hook = bstack1lllll1111l_opy_.bstack1l11l11111l_opy_(instance, bstack1l111lll11l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l111ll1l1l_opy_, []).clear()
    @staticmethod
    def __1l111ll11l1_opy_(instance: bstack1lll11111l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack111l11_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡥࡲࡶࡩࡹࠢᓊ"), None)):
            return
        if os.getenv(bstack111l11_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡏࡓࡌ࡙ࠢᓋ"), bstack111l11_opy_ (u"ࠦ࠶ࠨᓌ")) != bstack111l11_opy_ (u"ࠧ࠷ࠢᓍ"):
            bstack1lllll1111l_opy_.logger.warning(bstack111l11_opy_ (u"ࠨࡩࡨࡰࡲࡶ࡮ࡴࡧࠡࡥࡤࡴࡱࡵࡧࠣᓎ"))
            return
        bstack1l111l11l1l_opy_ = {
            bstack111l11_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᓏ"): (bstack1lllll1111l_opy_.bstack1l11l1l1lll_opy_, bstack1lllll1111l_opy_.bstack1l111l1lll1_opy_),
            bstack111l11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᓐ"): (bstack1lllll1111l_opy_.bstack1l111l1l11l_opy_, bstack1lllll1111l_opy_.bstack1l11ll1111l_opy_),
        }
        for when in (bstack111l11_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᓑ"), bstack111l11_opy_ (u"ࠥࡧࡦࡲ࡬ࠣᓒ"), bstack111l11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᓓ")):
            bstack1l11ll11l11_opy_ = args[1].get_records(when)
            if not bstack1l11ll11l11_opy_:
                continue
            records = [
                bstack1lll1l11l11_opy_(
                    kind=TestFramework.bstack1ll111l1111_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack111l11_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠣᓔ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack111l11_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪࠢᓕ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11ll11l11_opy_
                if isinstance(getattr(r, bstack111l11_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᓖ"), None), str) and r.message.strip()
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
    def __1l111l11111_opy_(test) -> Dict[str, Any]:
        bstack1ll1l1lll_opy_ = bstack1lllll1111l_opy_.__1l11ll11ll1_opy_(test.location) if hasattr(test, bstack111l11_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᓗ")) else getattr(test, bstack111l11_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᓘ"), None)
        test_name = test.name if hasattr(test, bstack111l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᓙ")) else None
        bstack1l111l1llll_opy_ = test.fspath.strpath if hasattr(test, bstack111l11_opy_ (u"ࠦ࡫ࡹࡰࡢࡶ࡫ࠦᓚ")) and test.fspath else None
        if not bstack1ll1l1lll_opy_ or not test_name or not bstack1l111l1llll_opy_:
            return None
        code = None
        if hasattr(test, bstack111l11_opy_ (u"ࠧࡵࡢ࡫ࠤᓛ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l1111l1ll1_opy_ = []
        try:
            bstack1l1111l1ll1_opy_ = bstack1lllll1l1l_opy_.bstack111l11llll_opy_(test)
        except:
            bstack1lllll1111l_opy_.logger.warning(bstack111l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷ࠱ࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶࠤࡼ࡯࡬࡭ࠢࡥࡩࠥࡸࡥࡴࡱ࡯ࡺࡪࡪࠠࡪࡰࠣࡇࡑࡏࠢᓜ"))
        return {
            TestFramework.bstack1ll11lll11l_opy_: uuid4().__str__(),
            TestFramework.bstack1l111llllll_opy_: bstack1ll1l1lll_opy_,
            TestFramework.bstack1ll1l111l11_opy_: test_name,
            TestFramework.bstack1l1ll111l11_opy_: getattr(test, bstack111l11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᓝ"), None),
            TestFramework.bstack1l111l1l1l1_opy_: bstack1l111l1llll_opy_,
            TestFramework.bstack1l1111ll11l_opy_: bstack1lllll1111l_opy_.__1l11l11lll1_opy_(test),
            TestFramework.bstack1l111ll11ll_opy_: code,
            TestFramework.bstack1l1l1l111l1_opy_: TestFramework.bstack1l11l111lll_opy_,
            TestFramework.bstack1l11llll1l1_opy_: bstack1ll1l1lll_opy_,
            TestFramework.bstack1l1111l11l1_opy_: bstack1l1111l1ll1_opy_
        }
    @staticmethod
    def __1l11l11lll1_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack111l11_opy_ (u"ࠣࡱࡺࡲࡤࡳࡡࡳ࡭ࡨࡶࡸࠨᓞ"), [])
            markers.extend([getattr(m, bstack111l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᓟ"), None) for m in own_markers if getattr(m, bstack111l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᓠ"), None)])
            current = getattr(current, bstack111l11_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦᓡ"), None)
        return markers
    @staticmethod
    def __1l11ll11ll1_opy_(location):
        return bstack111l11_opy_ (u"ࠧࡀ࠺ࠣᓢ").join(filter(lambda x: isinstance(x, str), location))