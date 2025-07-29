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
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll11llll1_opy_,
    bstack1llll1111ll_opy_,
    bstack1ll1lll1111_opy_,
    bstack1l111l11l1l_opy_,
    bstack1lll1l11111_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1ll11111l1l_opy_
from bstack_utils.bstack11l1lll1l1_opy_ import bstack1lll1lll111_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack11111llll1_opy_ import bstack1111l111l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll11ll1ll_opy_ import bstack1lll1lll1l1_opy_
from bstack_utils.bstack11l11111ll_opy_ import bstack11l111l11l_opy_
bstack1l1lllll111_opy_ = bstack1ll11111l1l_opy_()
bstack1l1111llll1_opy_ = 1.0
bstack1l1lll1llll_opy_ = bstack11l1lll_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣᐽ")
bstack1l1111l11ll_opy_ = bstack11l1lll_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧᐾ")
bstack1l1111l1l1l_opy_ = bstack11l1lll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᐿ")
bstack1l1111l1lll_opy_ = bstack11l1lll_opy_ (u"ࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢᑀ")
bstack1l1111l1l11_opy_ = bstack11l1lll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦᑁ")
_1ll111l111l_opy_ = set()
class bstack1lll11l1lll_opy_(TestFramework):
    bstack1l11l1lllll_opy_ = bstack11l1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᑂ")
    bstack1l111ll11l1_opy_ = bstack11l1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠧᑃ")
    bstack1l11ll11111_opy_ = bstack11l1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᑄ")
    bstack1l11l1111l1_opy_ = bstack11l1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࠦᑅ")
    bstack1l1111lll11_opy_ = bstack11l1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᑆ")
    bstack1l11l1ll1ll_opy_: bool
    bstack11111llll1_opy_: bstack1111l111l1_opy_  = None
    bstack1llll111ll1_opy_ = None
    bstack1l111lll111_opy_ = [
        bstack1lll11llll1_opy_.BEFORE_ALL,
        bstack1lll11llll1_opy_.AFTER_ALL,
        bstack1lll11llll1_opy_.BEFORE_EACH,
        bstack1lll11llll1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111l1l11l_opy_: Dict[str, str],
        bstack1ll1l1l1111_opy_: List[str]=[bstack11l1lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᑇ")],
        bstack11111llll1_opy_: bstack1111l111l1_opy_=None,
        bstack1llll111ll1_opy_=None
    ):
        super().__init__(bstack1ll1l1l1111_opy_, bstack1l111l1l11l_opy_, bstack11111llll1_opy_)
        self.bstack1l11l1ll1ll_opy_ = any(bstack11l1lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᑈ") in item.lower() for item in bstack1ll1l1l1111_opy_)
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
        if test_framework_state == bstack1lll11llll1_opy_.TEST or test_framework_state in bstack1lll11l1lll_opy_.bstack1l111lll111_opy_:
            bstack1l111l111ll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll11llll1_opy_.NONE:
            self.logger.warning(bstack11l1lll_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࠢᑉ") + str(test_hook_state) + bstack11l1lll_opy_ (u"ࠢࠣᑊ"))
            return
        if not self.bstack1l11l1ll1ll_opy_:
            self.logger.warning(bstack11l1lll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠾ࠤᑋ") + str(str(self.bstack1ll1l1l1111_opy_)) + bstack11l1lll_opy_ (u"ࠤࠥᑌ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11l1lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᑍ") + str(kwargs) + bstack11l1lll_opy_ (u"ࠦࠧᑎ"))
            return
        instance = self.__1l11l11ll1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡧࡲࡨࡵࡀࠦᑏ") + str(args) + bstack11l1lll_opy_ (u"ࠨࠢᑐ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1lll11l1lll_opy_.bstack1l111lll111_opy_ and test_hook_state == bstack1ll1lll1111_opy_.PRE:
                bstack1ll1l11llll_opy_ = bstack1lll1lll111_opy_.bstack1ll1l11l1ll_opy_(EVENTS.bstack11ll11l1l_opy_.value)
                name = str(EVENTS.bstack11ll11l1l_opy_.name)+bstack11l1lll_opy_ (u"ࠢ࠻ࠤᑑ")+str(test_framework_state.name)
                TestFramework.bstack1l111l1l1l1_opy_(instance, name, bstack1ll1l11llll_opy_)
        except Exception as e:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵࠤࡵࡸࡥ࠻ࠢࡾࢁࠧᑒ").format(e))
        try:
            if not TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1l1111ll1l1_opy_) and test_hook_state == bstack1ll1lll1111_opy_.PRE:
                test = bstack1lll11l1lll_opy_.__1l11l1l111l_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11l1lll_opy_ (u"ࠤ࡯ࡳࡦࡪࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᑓ") + str(test_hook_state) + bstack11l1lll_opy_ (u"ࠥࠦᑔ"))
            if test_framework_state == bstack1lll11llll1_opy_.TEST:
                if test_hook_state == bstack1ll1lll1111_opy_.PRE and not TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1ll1111l11l_opy_):
                    TestFramework.bstack111111llll_opy_(instance, TestFramework.bstack1ll1111l11l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l1lll_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡳࡵࡣࡵࡸࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᑕ") + str(test_hook_state) + bstack11l1lll_opy_ (u"ࠧࠨᑖ"))
                elif test_hook_state == bstack1ll1lll1111_opy_.POST and not TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1l1llll1l1l_opy_):
                    TestFramework.bstack111111llll_opy_(instance, TestFramework.bstack1l1llll1l1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l1lll_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡧࡱࡨࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᑗ") + str(test_hook_state) + bstack11l1lll_opy_ (u"ࠢࠣᑘ"))
            elif test_framework_state == bstack1lll11llll1_opy_.LOG and test_hook_state == bstack1ll1lll1111_opy_.POST:
                bstack1lll11l1lll_opy_.__1l111l111l1_opy_(instance, *args)
            elif test_framework_state == bstack1lll11llll1_opy_.LOG_REPORT and test_hook_state == bstack1ll1lll1111_opy_.POST:
                self.__1l111llllll_opy_(instance, *args)
                self.__1l111l1l1ll_opy_(instance)
            elif test_framework_state in bstack1lll11l1lll_opy_.bstack1l111lll111_opy_:
                self.__1l11l1l1l11_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᑙ") + str(instance.ref()) + bstack11l1lll_opy_ (u"ࠤࠥᑚ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11ll111l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1lll11l1lll_opy_.bstack1l111lll111_opy_ and test_hook_state == bstack1ll1lll1111_opy_.POST:
                name = str(EVENTS.bstack11ll11l1l_opy_.name)+bstack11l1lll_opy_ (u"ࠥ࠾ࠧᑛ")+str(test_framework_state.name)
                bstack1ll1l11llll_opy_ = TestFramework.bstack1l11l11lll1_opy_(instance, name)
                bstack1lll1lll111_opy_.end(EVENTS.bstack11ll11l1l_opy_.value, bstack1ll1l11llll_opy_+bstack11l1lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᑜ"), bstack1ll1l11llll_opy_+bstack11l1lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᑝ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᑞ").format(e))
    def bstack1l1lll11l1l_opy_(self):
        return self.bstack1l11l1ll1ll_opy_
    def __1l11ll11l11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11l1lll_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᑟ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1lll111ll_opy_(rep, [bstack11l1lll_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᑠ"), bstack11l1lll_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᑡ"), bstack11l1lll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᑢ"), bstack11l1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᑣ"), bstack11l1lll_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨᑤ"), bstack11l1lll_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᑥ")])
        return None
    def __1l111llllll_opy_(self, instance: bstack1llll1111ll_opy_, *args):
        result = self.__1l11ll11l11_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111l111ll_opy_ = None
        if result.get(bstack11l1lll_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᑦ"), None) == bstack11l1lll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᑧ") and len(args) > 1 and getattr(args[1], bstack11l1lll_opy_ (u"ࠤࡨࡼࡨ࡯࡮ࡧࡱࠥᑨ"), None) is not None:
            failure = [{bstack11l1lll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᑩ"): [args[1].excinfo.exconly(), result.get(bstack11l1lll_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᑪ"), None)]}]
            bstack1111l111ll_opy_ = bstack11l1lll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᑫ") if bstack11l1lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᑬ") in getattr(args[1].excinfo, bstack11l1lll_opy_ (u"ࠢࡵࡻࡳࡩࡳࡧ࡭ࡦࠤᑭ"), bstack11l1lll_opy_ (u"ࠣࠤᑮ")) else bstack11l1lll_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᑯ")
        bstack1l111llll1l_opy_ = result.get(bstack11l1lll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᑰ"), TestFramework.bstack1l11l1lll1l_opy_)
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
            target = None # bstack1l11ll11lll_opy_ bstack1l111l1lll1_opy_ this to be bstack11l1lll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᑱ")
            if test_framework_state == bstack1lll11llll1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111l1llll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll11llll1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11l1lll_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᑲ"), None), bstack11l1lll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᑳ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11l1lll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᑴ"), None):
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
        bstack1l111l1ll1l_opy_ = TestFramework.bstack1llllll11l1_opy_(instance, bstack1lll11l1lll_opy_.bstack1l111ll11l1_opy_, {})
        if not key in bstack1l111l1ll1l_opy_:
            bstack1l111l1ll1l_opy_[key] = []
        bstack1l11ll1l111_opy_ = TestFramework.bstack1llllll11l1_opy_(instance, bstack1lll11l1lll_opy_.bstack1l11ll11111_opy_, {})
        if not key in bstack1l11ll1l111_opy_:
            bstack1l11ll1l111_opy_[key] = []
        bstack1l111l11lll_opy_ = {
            bstack1lll11l1lll_opy_.bstack1l111ll11l1_opy_: bstack1l111l1ll1l_opy_,
            bstack1lll11l1lll_opy_.bstack1l11ll11111_opy_: bstack1l11ll1l111_opy_,
        }
        if test_hook_state == bstack1ll1lll1111_opy_.PRE:
            hook = {
                bstack11l1lll_opy_ (u"ࠣ࡭ࡨࡽࠧᑵ"): key,
                TestFramework.bstack1l111l11111_opy_: uuid4().__str__(),
                TestFramework.bstack1l11l111l11_opy_: TestFramework.bstack1l11l1l11ll_opy_,
                TestFramework.bstack1l111ll1l1l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1111ll1ll_opy_: [],
                TestFramework.bstack1l11l111111_opy_: args[1] if len(args) > 1 else bstack11l1lll_opy_ (u"ࠩࠪᑶ"),
                TestFramework.bstack1l1111ll11l_opy_: bstack1lll1lll1l1_opy_.bstack1l11l1ll111_opy_()
            }
            bstack1l111l1ll1l_opy_[key].append(hook)
            bstack1l111l11lll_opy_[bstack1lll11l1lll_opy_.bstack1l11l1111l1_opy_] = key
        elif test_hook_state == bstack1ll1lll1111_opy_.POST:
            bstack1l11l1l1lll_opy_ = bstack1l111l1ll1l_opy_.get(key, [])
            hook = bstack1l11l1l1lll_opy_.pop() if bstack1l11l1l1lll_opy_ else None
            if hook:
                result = self.__1l11ll11l11_opy_(*args)
                if result:
                    bstack1l11ll11l1l_opy_ = result.get(bstack11l1lll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᑷ"), TestFramework.bstack1l11l1l11ll_opy_)
                    if bstack1l11ll11l1l_opy_ != TestFramework.bstack1l11l1l11ll_opy_:
                        hook[TestFramework.bstack1l11l111l11_opy_] = bstack1l11ll11l1l_opy_
                hook[TestFramework.bstack1l11l11l111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l1111ll11l_opy_]= bstack1lll1lll1l1_opy_.bstack1l11l1ll111_opy_()
                self.bstack1l11l11llll_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11l111l1l_opy_, [])
                if logs: self.bstack1l1llll111l_opy_(instance, logs)
                bstack1l11ll1l111_opy_[key].append(hook)
                bstack1l111l11lll_opy_[bstack1lll11l1lll_opy_.bstack1l1111lll11_opy_] = key
        TestFramework.bstack1l11l1l1l1l_opy_(instance, bstack1l111l11lll_opy_)
        self.logger.debug(bstack11l1lll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡬ࡴࡵ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡰ࡫ࡹࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࡃࡻࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࡽࠡࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠿ࠥᑸ") + str(bstack1l11ll1l111_opy_) + bstack11l1lll_opy_ (u"ࠧࠨᑹ"))
    def __1l11l11ll11_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll11llll1_opy_,
        test_hook_state: bstack1ll1lll1111_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1lll111ll_opy_(args[0], [bstack11l1lll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᑺ"), bstack11l1lll_opy_ (u"ࠢࡢࡴࡪࡲࡦࡳࡥࠣᑻ"), bstack11l1lll_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᑼ"), bstack11l1lll_opy_ (u"ࠤ࡬ࡨࡸࠨᑽ"), bstack11l1lll_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࠧᑾ"), bstack11l1lll_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᑿ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack11l1lll_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᒀ")) else fixturedef.get(bstack11l1lll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᒁ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11l1lll_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࠧᒂ")) else None
        node = request.node if hasattr(request, bstack11l1lll_opy_ (u"ࠣࡰࡲࡨࡪࠨᒃ")) else None
        target = request.node.nodeid if hasattr(node, bstack11l1lll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᒄ")) else None
        baseid = fixturedef.get(bstack11l1lll_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᒅ"), None) or bstack11l1lll_opy_ (u"ࠦࠧᒆ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11l1lll_opy_ (u"ࠧࡥࡰࡺࡨࡸࡲࡨ࡯ࡴࡦ࡯ࠥᒇ")):
            target = bstack1lll11l1lll_opy_.__1l111l11l11_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11l1lll_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᒈ")) else None
            if target and not TestFramework.bstack11111l1111_opy_(target):
                self.__1l111l1llll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11l1lll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡱࡳࡩ࡫࠽ࡼࡰࡲࡨࡪࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᒉ") + str(test_hook_state) + bstack11l1lll_opy_ (u"ࠣࠤᒊ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11l1lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᒋ") + str(target) + bstack11l1lll_opy_ (u"ࠥࠦᒌ"))
            return None
        instance = TestFramework.bstack11111l1111_opy_(target)
        if not instance:
            self.logger.warning(bstack11l1lll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡦࡦࡹࡥࡪࡦࡀࡿࡧࡧࡳࡦ࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᒍ") + str(target) + bstack11l1lll_opy_ (u"ࠧࠨᒎ"))
            return None
        bstack1l11ll1111l_opy_ = TestFramework.bstack1llllll11l1_opy_(instance, bstack1lll11l1lll_opy_.bstack1l11l1lllll_opy_, {})
        if os.getenv(bstack11l1lll_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡌࡉ࡙ࡖࡘࡖࡊ࡙ࠢᒏ"), bstack11l1lll_opy_ (u"ࠢ࠲ࠤᒐ")) == bstack11l1lll_opy_ (u"ࠣ࠳ࠥᒑ"):
            bstack1l11l11l11l_opy_ = bstack11l1lll_opy_ (u"ࠤ࠽ࠦᒒ").join((scope, fixturename))
            bstack1l11ll111ll_opy_ = datetime.now(tz=timezone.utc)
            bstack1l111llll11_opy_ = {
                bstack11l1lll_opy_ (u"ࠥ࡯ࡪࡿࠢᒓ"): bstack1l11l11l11l_opy_,
                bstack11l1lll_opy_ (u"ࠦࡹࡧࡧࡴࠤᒔ"): bstack1lll11l1lll_opy_.__1l111l1111l_opy_(request.node),
                bstack11l1lll_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࠨᒕ"): fixturedef,
                bstack11l1lll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᒖ"): scope,
                bstack11l1lll_opy_ (u"ࠢࡵࡻࡳࡩࠧᒗ"): None,
            }
            try:
                if test_hook_state == bstack1ll1lll1111_opy_.POST and callable(getattr(args[-1], bstack11l1lll_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᒘ"), None)):
                    bstack1l111llll11_opy_[bstack11l1lll_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᒙ")] = TestFramework.bstack1l1lll1lll1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1lll1111_opy_.PRE:
                bstack1l111llll11_opy_[bstack11l1lll_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᒚ")] = uuid4().__str__()
                bstack1l111llll11_opy_[bstack1lll11l1lll_opy_.bstack1l111ll1l1l_opy_] = bstack1l11ll111ll_opy_
            elif test_hook_state == bstack1ll1lll1111_opy_.POST:
                bstack1l111llll11_opy_[bstack1lll11l1lll_opy_.bstack1l11l11l111_opy_] = bstack1l11ll111ll_opy_
            if bstack1l11l11l11l_opy_ in bstack1l11ll1111l_opy_:
                bstack1l11ll1111l_opy_[bstack1l11l11l11l_opy_].update(bstack1l111llll11_opy_)
                self.logger.debug(bstack11l1lll_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࠧᒛ") + str(bstack1l11ll1111l_opy_[bstack1l11l11l11l_opy_]) + bstack11l1lll_opy_ (u"ࠧࠨᒜ"))
            else:
                bstack1l11ll1111l_opy_[bstack1l11l11l11l_opy_] = bstack1l111llll11_opy_
                self.logger.debug(bstack11l1lll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࢀࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࢁࠥࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࠤᒝ") + str(len(bstack1l11ll1111l_opy_)) + bstack11l1lll_opy_ (u"ࠢࠣᒞ"))
        TestFramework.bstack111111llll_opy_(instance, bstack1lll11l1lll_opy_.bstack1l11l1lllll_opy_, bstack1l11ll1111l_opy_)
        self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࡾࡰࡪࡴࠨࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠬࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᒟ") + str(instance.ref()) + bstack11l1lll_opy_ (u"ࠤࠥᒠ"))
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
            bstack1lll11l1lll_opy_.bstack1l11l1lllll_opy_: {},
            bstack1lll11l1lll_opy_.bstack1l11ll11111_opy_: {},
            bstack1lll11l1lll_opy_.bstack1l111ll11l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack111111llll_opy_(ob, TestFramework.bstack1l11ll1l11l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack111111llll_opy_(ob, TestFramework.bstack1ll11l1l1ll_opy_, context.platform_index)
        TestFramework.bstack1lllllll111_opy_[ctx.id] = ob
        self.logger.debug(bstack11l1lll_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡨࡺࡸ࠯࡫ࡧࡁࢀࡩࡴࡹ࠰࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥᒡ") + str(TestFramework.bstack1lllllll111_opy_.keys()) + bstack11l1lll_opy_ (u"ࠦࠧᒢ"))
        return ob
    def bstack1l1ll1l1lll_opy_(self, instance: bstack1llll1111ll_opy_, bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_]):
        bstack1l11ll11ll1_opy_ = (
            bstack1lll11l1lll_opy_.bstack1l11l1111l1_opy_
            if bstack11111l11l1_opy_[1] == bstack1ll1lll1111_opy_.PRE
            else bstack1lll11l1lll_opy_.bstack1l1111lll11_opy_
        )
        hook = bstack1lll11l1lll_opy_.bstack1l111lll1l1_opy_(instance, bstack1l11ll11ll1_opy_)
        entries = hook.get(TestFramework.bstack1l1111ll1ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1l11l1111ll_opy_, []))
        return entries
    def bstack1ll11111l11_opy_(self, instance: bstack1llll1111ll_opy_, bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_]):
        bstack1l11ll11ll1_opy_ = (
            bstack1lll11l1lll_opy_.bstack1l11l1111l1_opy_
            if bstack11111l11l1_opy_[1] == bstack1ll1lll1111_opy_.PRE
            else bstack1lll11l1lll_opy_.bstack1l1111lll11_opy_
        )
        bstack1lll11l1lll_opy_.bstack1l111lllll1_opy_(instance, bstack1l11ll11ll1_opy_)
        TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1l11l1111ll_opy_, []).clear()
    def bstack1l11l11llll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11l1lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡵࡪࡨࠤࡏࡧࡶࡢࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡆ࡬ࡪࡩ࡫ࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡯࡮ࡴ࡫ࡧࡩࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠯ࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌ࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠰ࠥࡸࡥࡱ࡮ࡤࡧࡪࡹࠠࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢࠡ࡫ࡱࠤ࡮ࡺࡳࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡏࡦࠡࡣࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡲࡧࡴࡤࡪࡨࡷࠥࡧࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࠢ࡫ࡳࡴࡱ࠭࡭ࡧࡹࡩࡱࠦࡦࡪ࡮ࡨ࠰ࠥ࡯ࡴࠡࡥࡵࡩࡦࡺࡥࡴࠢࡤࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡷࡪࡶ࡫ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡕ࡬ࡱ࡮ࡲࡡࡳ࡮ࡼ࠰ࠥ࡯ࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦ࡬ࡰࡥࡤࡸࡪࡪࠠࡪࡰࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡨࡹࠡࡴࡨࡴࡱࡧࡣࡪࡰࡪࠤࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤ࡙࡮ࡥࠡࡥࡵࡩࡦࡺࡥࡥࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࡷࠥࡧࡲࡦࠢࡤࡨࡩ࡫ࡤࠡࡶࡲࠤࡹ࡮ࡥࠡࡪࡲࡳࡰ࠭ࡳࠡࠤ࡯ࡳ࡬ࡹࠢࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭࠽ࠤ࡙࡮ࡥࠡࡧࡹࡩࡳࡺࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴ࡭ࡳࠡࡣࡱࡨࠥ࡮࡯ࡰ࡭ࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡵࡪ࡮ࡧࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᒣ")
        global _1ll111l111l_opy_
        platform_index = os.environ[bstack11l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᒤ")]
        bstack1l1llll1111_opy_ = os.path.join(bstack1l1lllll111_opy_, (bstack1l1lll1llll_opy_ + str(platform_index)), bstack1l1111l1lll_opy_)
        if not os.path.exists(bstack1l1llll1111_opy_) or not os.path.isdir(bstack1l1llll1111_opy_):
            self.logger.info(bstack11l1lll_opy_ (u"ࠢࡅ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷࡷࠥࡺ࡯ࠡࡲࡵࡳࡨ࡫ࡳࡴࠢࡾࢁࠧᒥ").format(bstack1l1llll1111_opy_))
            return
        logs = hook.get(bstack11l1lll_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᒦ"), [])
        with os.scandir(bstack1l1llll1111_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1ll111l111l_opy_:
                    self.logger.info(bstack11l1lll_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᒧ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11l1lll_opy_ (u"ࠥࠦᒨ")
                    log_entry = bstack1lll1l11111_opy_(
                        kind=bstack11l1lll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᒩ"),
                        message=bstack11l1lll_opy_ (u"ࠧࠨᒪ"),
                        level=bstack11l1lll_opy_ (u"ࠨࠢᒫ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1ll1ll1l1_opy_=entry.stat().st_size,
                        bstack1l1llll11l1_opy_=bstack11l1lll_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᒬ"),
                        bstack111ll1l_opy_=os.path.abspath(entry.path),
                        bstack1l111l1l111_opy_=hook.get(TestFramework.bstack1l111l11111_opy_)
                    )
                    logs.append(log_entry)
                    _1ll111l111l_opy_.add(abs_path)
        platform_index = os.environ[bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᒭ")]
        bstack1l111ll11ll_opy_ = os.path.join(bstack1l1lllll111_opy_, (bstack1l1lll1llll_opy_ + str(platform_index)), bstack1l1111l1lll_opy_, bstack1l1111l1l11_opy_)
        if not os.path.exists(bstack1l111ll11ll_opy_) or not os.path.isdir(bstack1l111ll11ll_opy_):
            self.logger.info(bstack11l1lll_opy_ (u"ࠤࡑࡳࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡬࡯ࡶࡰࡧࠤࡦࡺ࠺ࠡࡽࢀࠦᒮ").format(bstack1l111ll11ll_opy_))
        else:
            self.logger.info(bstack11l1lll_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᒯ").format(bstack1l111ll11ll_opy_))
            with os.scandir(bstack1l111ll11ll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1ll111l111l_opy_:
                        self.logger.info(bstack11l1lll_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᒰ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11l1lll_opy_ (u"ࠧࠨᒱ")
                        log_entry = bstack1lll1l11111_opy_(
                            kind=bstack11l1lll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᒲ"),
                            message=bstack11l1lll_opy_ (u"ࠢࠣᒳ"),
                            level=bstack11l1lll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᒴ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1ll1ll1l1_opy_=entry.stat().st_size,
                            bstack1l1llll11l1_opy_=bstack11l1lll_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᒵ"),
                            bstack111ll1l_opy_=os.path.abspath(entry.path),
                            bstack1ll1111ll11_opy_=hook.get(TestFramework.bstack1l111l11111_opy_)
                        )
                        logs.append(log_entry)
                        _1ll111l111l_opy_.add(abs_path)
        hook[bstack11l1lll_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᒶ")] = logs
    def bstack1l1llll111l_opy_(
        self,
        bstack1l1lll1ll1l_opy_: bstack1llll1111ll_opy_,
        entries: List[bstack1lll1l11111_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11l1lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣᒷ"))
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
            log_entry.message = entry.message.encode(bstack11l1lll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᒸ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11l1lll_opy_ (u"ࠨࠢᒹ")
            if entry.kind == bstack11l1lll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᒺ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll1ll1l1_opy_
                log_entry.file_path = entry.bstack111ll1l_opy_
        def bstack1l1lll11l11_opy_():
            bstack11llll111l_opy_ = datetime.now()
            try:
                self.bstack1llll111ll1_opy_.LogCreatedEvent(req)
                bstack1l1lll1ll1l_opy_.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧᒻ"), datetime.now() - bstack11llll111l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1lll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡽࠣᒼ").format(str(e)))
                traceback.print_exc()
        self.bstack11111llll1_opy_.enqueue(bstack1l1lll11l11_opy_)
    def __1l111l1l1ll_opy_(self, instance) -> None:
        bstack11l1lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᒽ")
        bstack1l111l11lll_opy_ = {bstack11l1lll_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᒾ"): bstack1lll1lll1l1_opy_.bstack1l11l1ll111_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l11l1l1l1l_opy_(instance, bstack1l111l11lll_opy_)
    @staticmethod
    def bstack1l111lll1l1_opy_(instance: bstack1llll1111ll_opy_, bstack1l11ll11ll1_opy_: str):
        bstack1l11l111ll1_opy_ = (
            bstack1lll11l1lll_opy_.bstack1l11ll11111_opy_
            if bstack1l11ll11ll1_opy_ == bstack1lll11l1lll_opy_.bstack1l1111lll11_opy_
            else bstack1lll11l1lll_opy_.bstack1l111ll11l1_opy_
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
        hook = bstack1lll11l1lll_opy_.bstack1l111lll1l1_opy_(instance, bstack1l11ll11ll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1111ll1ll_opy_, []).clear()
    @staticmethod
    def __1l111l111l1_opy_(instance: bstack1llll1111ll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11l1lll_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡨࡵࡲࡥࡵࠥᒿ"), None)):
            return
        if os.getenv(bstack11l1lll_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡒࡏࡈࡕࠥᓀ"), bstack11l1lll_opy_ (u"ࠢ࠲ࠤᓁ")) != bstack11l1lll_opy_ (u"ࠣ࠳ࠥᓂ"):
            bstack1lll11l1lll_opy_.logger.warning(bstack11l1lll_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡪࡰࡪࠤࡨࡧࡰ࡭ࡱࡪࠦᓃ"))
            return
        bstack1l1111lllll_opy_ = {
            bstack11l1lll_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᓄ"): (bstack1lll11l1lll_opy_.bstack1l11l1111l1_opy_, bstack1lll11l1lll_opy_.bstack1l111ll11l1_opy_),
            bstack11l1lll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᓅ"): (bstack1lll11l1lll_opy_.bstack1l1111lll11_opy_, bstack1lll11l1lll_opy_.bstack1l11ll11111_opy_),
        }
        for when in (bstack11l1lll_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᓆ"), bstack11l1lll_opy_ (u"ࠨࡣࡢ࡮࡯ࠦᓇ"), bstack11l1lll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᓈ")):
            bstack1l111ll1ll1_opy_ = args[1].get_records(when)
            if not bstack1l111ll1ll1_opy_:
                continue
            records = [
                bstack1lll1l11111_opy_(
                    kind=TestFramework.bstack1l1ll1llll1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11l1lll_opy_ (u"ࠣ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨࠦᓉ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11l1lll_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࠥᓊ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111ll1ll1_opy_
                if isinstance(getattr(r, bstack11l1lll_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᓋ"), None), str) and r.message.strip()
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
    def __1l11l1l111l_opy_(test) -> Dict[str, Any]:
        bstack11ll111l11_opy_ = bstack1lll11l1lll_opy_.__1l111l11l11_opy_(test.location) if hasattr(test, bstack11l1lll_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᓌ")) else getattr(test, bstack11l1lll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᓍ"), None)
        test_name = test.name if hasattr(test, bstack11l1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᓎ")) else None
        bstack1l11l1l11l1_opy_ = test.fspath.strpath if hasattr(test, bstack11l1lll_opy_ (u"ࠢࡧࡵࡳࡥࡹ࡮ࠢᓏ")) and test.fspath else None
        if not bstack11ll111l11_opy_ or not test_name or not bstack1l11l1l11l1_opy_:
            return None
        code = None
        if hasattr(test, bstack11l1lll_opy_ (u"ࠣࡱࡥ࡮ࠧᓐ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l1111l1ll1_opy_ = []
        try:
            bstack1l1111l1ll1_opy_ = bstack11l111l11l_opy_.bstack111l1lll1l_opy_(test)
        except:
            bstack1lll11l1lll_opy_.logger.warning(bstack11l1lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡸࡪࡹࡴࠡࡵࡦࡳࡵ࡫ࡳ࠭ࠢࡷࡩࡸࡺࠠࡴࡥࡲࡴࡪࡹࠠࡸ࡫࡯ࡰࠥࡨࡥࠡࡴࡨࡷࡴࡲࡶࡦࡦࠣ࡭ࡳࠦࡃࡍࡋࠥᓑ"))
        return {
            TestFramework.bstack1ll11lll11l_opy_: uuid4().__str__(),
            TestFramework.bstack1l1111ll1l1_opy_: bstack11ll111l11_opy_,
            TestFramework.bstack1ll1l111lll_opy_: test_name,
            TestFramework.bstack1l1ll111l11_opy_: getattr(test, bstack11l1lll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᓒ"), None),
            TestFramework.bstack1l111lll1ll_opy_: bstack1l11l1l11l1_opy_,
            TestFramework.bstack1l11l111lll_opy_: bstack1lll11l1lll_opy_.__1l111l1111l_opy_(test),
            TestFramework.bstack1l111ll111l_opy_: code,
            TestFramework.bstack1l1l1l1l1ll_opy_: TestFramework.bstack1l11l1lll1l_opy_,
            TestFramework.bstack1l11llll11l_opy_: bstack11ll111l11_opy_,
            TestFramework.bstack1l1111ll111_opy_: bstack1l1111l1ll1_opy_
        }
    @staticmethod
    def __1l111l1111l_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack11l1lll_opy_ (u"ࠦࡴࡽ࡮ࡠ࡯ࡤࡶࡰ࡫ࡲࡴࠤᓓ"), [])
            markers.extend([getattr(m, bstack11l1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᓔ"), None) for m in own_markers if getattr(m, bstack11l1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᓕ"), None)])
            current = getattr(current, bstack11l1lll_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢᓖ"), None)
        return markers
    @staticmethod
    def __1l111l11l11_opy_(location):
        return bstack11l1lll_opy_ (u"ࠣ࠼࠽ࠦᓗ").join(filter(lambda x: isinstance(x, str), location))