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
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack1llllll11ll_opy_, bstack1llllll1l11_opy_, bstack11111ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1llll11l1ll_opy_ import bstack1llll1ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll1ll_opy_ import bstack1llll1lll1l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l11l1_opy_ import bstack1lll111llll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11llll1_opy_, bstack1llll1111ll_opy_, bstack1ll1lll1111_opy_, bstack1lll1l11111_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1ll1l1ll1_opy_, bstack1ll11111l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1lll1l111_opy_ = [bstack11l1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇌ"), bstack11l1lll_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢᇍ"), bstack11l1lll_opy_ (u"ࠣࡥࡲࡲ࡫࡯ࡧࠣᇎ"), bstack11l1lll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࠥᇏ"), bstack11l1lll_opy_ (u"ࠥࡴࡦࡺࡨࠣᇐ")]
bstack1l1lllll111_opy_ = bstack1ll11111l1l_opy_()
bstack1l1lll1llll_opy_ = bstack11l1lll_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᇑ")
bstack1ll1111ll1l_opy_ = {
    bstack11l1lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡏࡴࡦ࡯ࠥᇒ"): bstack1l1lll1l111_opy_,
    bstack11l1lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡐࡢࡥ࡮ࡥ࡬࡫ࠢᇓ"): bstack1l1lll1l111_opy_,
    bstack11l1lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡎࡱࡧࡹࡱ࡫ࠢᇔ"): bstack1l1lll1l111_opy_,
    bstack11l1lll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡅ࡯ࡥࡸࡹࠢᇕ"): bstack1l1lll1l111_opy_,
    bstack11l1lll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡉࡹࡳࡩࡴࡪࡱࡱࠦᇖ"): bstack1l1lll1l111_opy_
    + [
        bstack11l1lll_opy_ (u"ࠥࡳࡷ࡯ࡧࡪࡰࡤࡰࡳࡧ࡭ࡦࠤᇗ"),
        bstack11l1lll_opy_ (u"ࠦࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᇘ"),
        bstack11l1lll_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪ࡯࡮ࡧࡱࠥᇙ"),
        bstack11l1lll_opy_ (u"ࠨ࡫ࡦࡻࡺࡳࡷࡪࡳࠣᇚ"),
        bstack11l1lll_opy_ (u"ࠢࡤࡣ࡯ࡰࡸࡶࡥࡤࠤᇛ"),
        bstack11l1lll_opy_ (u"ࠣࡥࡤࡰࡱࡵࡢ࡫ࠤᇜ"),
        bstack11l1lll_opy_ (u"ࠤࡶࡸࡦࡸࡴࠣᇝ"),
        bstack11l1lll_opy_ (u"ࠥࡷࡹࡵࡰࠣᇞ"),
        bstack11l1lll_opy_ (u"ࠦࡩࡻࡲࡢࡶ࡬ࡳࡳࠨᇟ"),
        bstack11l1lll_opy_ (u"ࠧࡽࡨࡦࡰࠥᇠ"),
    ],
    bstack11l1lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢ࡫ࡱ࠲ࡘ࡫ࡳࡴ࡫ࡲࡲࠧᇡ"): [bstack11l1lll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡶࡡࡵࡪࠥᇢ"), bstack11l1lll_opy_ (u"ࠣࡶࡨࡷࡹࡹࡦࡢ࡫࡯ࡩࡩࠨᇣ"), bstack11l1lll_opy_ (u"ࠤࡷࡩࡸࡺࡳࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠥᇤ"), bstack11l1lll_opy_ (u"ࠥ࡭ࡹ࡫࡭ࡴࠤᇥ")],
    bstack11l1lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡨࡵ࡮ࡧ࡫ࡪ࠲ࡈࡵ࡮ࡧ࡫ࡪࠦᇦ"): [bstack11l1lll_opy_ (u"ࠧ࡯࡮ࡷࡱࡦࡥࡹ࡯࡯࡯ࡡࡳࡥࡷࡧ࡭ࡴࠤᇧ"), bstack11l1lll_opy_ (u"ࠨࡡࡳࡩࡶࠦᇨ")],
    bstack11l1lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡉ࡭ࡽࡺࡵࡳࡧࡇࡩ࡫ࠨᇩ"): [bstack11l1lll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᇪ"), bstack11l1lll_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥᇫ"), bstack11l1lll_opy_ (u"ࠥࡪࡺࡴࡣࠣᇬ"), bstack11l1lll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᇭ"), bstack11l1lll_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢᇮ"), bstack11l1lll_opy_ (u"ࠨࡩࡥࡵࠥᇯ")],
    bstack11l1lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡖࡹࡧࡘࡥࡲࡷࡨࡷࡹࠨᇰ"): [bstack11l1lll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᇱ"), bstack11l1lll_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࠣᇲ"), bstack11l1lll_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᇳ")],
    bstack11l1lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡷࡻ࡮࡯ࡧࡵ࠲ࡈࡧ࡬࡭ࡋࡱࡪࡴࠨᇴ"): [bstack11l1lll_opy_ (u"ࠧࡽࡨࡦࡰࠥᇵ"), bstack11l1lll_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࠨᇶ")],
    bstack11l1lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡑࡳࡩ࡫ࡋࡦࡻࡺࡳࡷࡪࡳࠣᇷ"): [bstack11l1lll_opy_ (u"ࠣࡰࡲࡨࡪࠨᇸ"), bstack11l1lll_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤᇹ")],
    bstack11l1lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦࡸ࡫࠯ࡵࡷࡶࡺࡩࡴࡶࡴࡨࡷ࠳ࡓࡡࡳ࡭ࠥᇺ"): [bstack11l1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇻ"), bstack11l1lll_opy_ (u"ࠧࡧࡲࡨࡵࠥᇼ"), bstack11l1lll_opy_ (u"ࠨ࡫ࡸࡣࡵ࡫ࡸࠨᇽ")],
}
_1ll111l111l_opy_ = set()
class bstack1llll11l11l_opy_(bstack1llll1ll1l1_opy_):
    bstack1l1ll1ll1ll_opy_ = bstack11l1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡥࡧࡧࡵࡶࡪࡪࠢᇾ")
    bstack1ll1111lll1_opy_ = bstack11l1lll_opy_ (u"ࠣࡋࡑࡊࡔࠨᇿ")
    bstack1l1lll11ll1_opy_ = bstack11l1lll_opy_ (u"ࠤࡈࡖࡗࡕࡒࠣሀ")
    bstack1l1ll11lll1_opy_: Callable
    bstack1ll1111111l_opy_: Callable
    def __init__(self, bstack1lll1l11lll_opy_, bstack1llll11111l_opy_):
        super().__init__()
        self.bstack1ll1l11l111_opy_ = bstack1llll11111l_opy_
        if os.getenv(bstack11l1lll_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡒ࠵࠶࡟ࠢሁ"), bstack11l1lll_opy_ (u"ࠦ࠶ࠨሂ")) != bstack11l1lll_opy_ (u"ࠧ࠷ࠢሃ") or not self.is_enabled():
            self.logger.warning(bstack11l1lll_opy_ (u"ࠨࠢሄ") + str(self.__class__.__name__) + bstack11l1lll_opy_ (u"ࠢࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠥህ"))
            return
        TestFramework.bstack1ll1ll11111_opy_((bstack1lll11llll1_opy_.TEST, bstack1ll1lll1111_opy_.PRE), self.bstack1ll1l11ll1l_opy_)
        TestFramework.bstack1ll1ll11111_opy_((bstack1lll11llll1_opy_.TEST, bstack1ll1lll1111_opy_.POST), self.bstack1ll11ll11l1_opy_)
        for event in bstack1lll11llll1_opy_:
            for state in bstack1ll1lll1111_opy_:
                TestFramework.bstack1ll1ll11111_opy_((event, state), self.bstack1l1ll1l11l1_opy_)
        bstack1lll1l11lll_opy_.bstack1ll1ll11111_opy_((bstack1llllll1l11_opy_.bstack11111l111l_opy_, bstack11111ll1l1_opy_.POST), self.bstack1l1lll111l1_opy_)
        self.bstack1l1ll11lll1_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1llll1l11_opy_(bstack1llll11l11l_opy_.bstack1ll1111lll1_opy_, self.bstack1l1ll11lll1_opy_)
        self.bstack1ll1111111l_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1llll1l11_opy_(bstack1llll11l11l_opy_.bstack1l1lll11ll1_opy_, self.bstack1ll1111111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll1l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1111ll_opy_,
        bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1lll11l1l_opy_() and instance:
            bstack1l1ll1lllll_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack11111l11l1_opy_
            if test_framework_state == bstack1lll11llll1_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1lll11llll1_opy_.LOG:
                bstack11llll111l_opy_ = datetime.now()
                entries = f.bstack1l1ll1l1lll_opy_(instance, bstack11111l11l1_opy_)
                if entries:
                    self.bstack1l1llll111l_opy_(instance, entries)
                    instance.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࠣሆ"), datetime.now() - bstack11llll111l_opy_)
                    f.bstack1ll11111l11_opy_(instance, bstack11111l11l1_opy_)
                instance.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧሇ"), datetime.now() - bstack1l1ll1lllll_opy_)
                return # bstack1l1llllll11_opy_ not send this event with the bstack1ll11111lll_opy_ bstack1l1lll11lll_opy_
            elif (
                test_framework_state == bstack1lll11llll1_opy_.TEST
                and test_hook_state == bstack1ll1lll1111_opy_.POST
                and not f.bstack11111l11ll_opy_(instance, TestFramework.bstack1l1lll1l1l1_opy_)
            ):
                self.logger.warning(bstack11l1lll_opy_ (u"ࠥࡨࡷࡵࡰࡱ࡫ࡱ࡫ࠥࡪࡵࡦࠢࡷࡳࠥࡲࡡࡤ࡭ࠣࡳ࡫ࠦࡲࡦࡵࡸࡰࡹࡹࠠࠣለ") + str(TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1l1lll1l1l1_opy_)) + bstack11l1lll_opy_ (u"ࠦࠧሉ"))
                f.bstack111111llll_opy_(instance, bstack1llll11l11l_opy_.bstack1l1ll1ll1ll_opy_, True)
                return # bstack1l1llllll11_opy_ not send this event bstack1l1llll1lll_opy_ bstack1ll11111ll1_opy_
            elif (
                f.bstack1llllll11l1_opy_(instance, bstack1llll11l11l_opy_.bstack1l1ll1ll1ll_opy_, False)
                and test_framework_state == bstack1lll11llll1_opy_.LOG_REPORT
                and test_hook_state == bstack1ll1lll1111_opy_.POST
                and f.bstack11111l11ll_opy_(instance, TestFramework.bstack1l1lll1l1l1_opy_)
            ):
                self.logger.warning(bstack11l1lll_opy_ (u"ࠧ࡯࡮࡫ࡧࡦࡸ࡮ࡴࡧࠡࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡔࡆࡕࡗ࠰࡚ࠥࡥࡴࡶࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࡖࡏࡔࡖࠣࠦሊ") + str(TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1l1lll1l1l1_opy_)) + bstack11l1lll_opy_ (u"ࠨࠢላ"))
                self.bstack1l1ll1l11l1_opy_(f, instance, (bstack1lll11llll1_opy_.TEST, bstack1ll1lll1111_opy_.POST), *args, **kwargs)
            bstack11llll111l_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1ll111111l1_opy_ = sorted(
                filter(lambda x: x.get(bstack11l1lll_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥሌ"), None), data.pop(bstack11l1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣል"), {}).values()),
                key=lambda x: x[bstack11l1lll_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧሎ")],
            )
            if bstack1llll1lll1l_opy_.bstack1l1lll1111l_opy_ in data:
                data.pop(bstack1llll1lll1l_opy_.bstack1l1lll1111l_opy_)
            data.update({bstack11l1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥሏ"): bstack1ll111111l1_opy_})
            instance.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠦ࡯ࡹ࡯࡯࠼ࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤሐ"), datetime.now() - bstack11llll111l_opy_)
            bstack11llll111l_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1ll1lll1l_opy_)
            instance.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠧࡰࡳࡰࡰ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣሑ"), datetime.now() - bstack11llll111l_opy_)
            self.bstack1l1lll11lll_opy_(instance, bstack11111l11l1_opy_, event_json=event_json)
            instance.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤሒ"), datetime.now() - bstack1l1ll1lllll_opy_)
    def bstack1ll1l11ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1111ll_opy_,
        bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11l1lll1l1_opy_ import bstack1lll1lll111_opy_
        bstack1ll1l11llll_opy_ = bstack1lll1lll111_opy_.bstack1ll1l11l1ll_opy_(EVENTS.bstack1l1ll111_opy_.value)
        self.bstack1ll1l11l111_opy_.bstack1ll111111ll_opy_(instance, f, bstack11111l11l1_opy_, *args, **kwargs)
        bstack1lll1lll111_opy_.end(EVENTS.bstack1l1ll111_opy_.value, bstack1ll1l11llll_opy_ + bstack11l1lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢሓ"), bstack1ll1l11llll_opy_ + bstack11l1lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨሔ"), status=True, failure=None, test_name=None)
    def bstack1ll11ll11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1111ll_opy_,
        bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll1l11l111_opy_.bstack1l1lll1ll11_opy_(instance, f, bstack11111l11l1_opy_, *args, **kwargs)
        self.bstack1l1ll1l1111_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1ll11llll_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def bstack1l1ll1l1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1111ll_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤ࡙࡫ࡳࡵࡕࡨࡷࡸ࡯࡯࡯ࡇࡹࡩࡳࡺࠠࡨࡔࡓࡇࠥࡩࡡ࡭࡮࠽ࠤࡓࡵࠠࡷࡣ࡯࡭ࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡥࡣࡷࡥࠧሕ"))
            return
        bstack11llll111l_opy_ = datetime.now()
        try:
            r = self.bstack1llll111ll1_opy_.TestSessionEvent(req)
            instance.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡫ࡶࡦࡰࡷࠦሖ"), datetime.now() - bstack11llll111l_opy_)
            f.bstack111111llll_opy_(instance, self.bstack1ll1l11l111_opy_.bstack1l1ll1l11ll_opy_, r.success)
            if not r.success:
                self.logger.info(bstack11l1lll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨሗ") + str(r) + bstack11l1lll_opy_ (u"ࠧࠨመ"))
        except grpc.RpcError as e:
            self.logger.error(bstack11l1lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦሙ") + str(e) + bstack11l1lll_opy_ (u"ࠢࠣሚ"))
            traceback.print_exc()
            raise e
    def bstack1l1lll111l1_opy_(
        self,
        f: bstack1lll111llll_opy_,
        _driver: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        _1l1ll1ll111_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1lll111llll_opy_.bstack1ll1ll111l1_opy_(method_name):
            return
        if f.bstack1ll11ll111l_opy_(*args) == bstack1lll111llll_opy_.bstack1ll1111llll_opy_:
            bstack1l1ll1lllll_opy_ = datetime.now()
            screenshot = result.get(bstack11l1lll_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢማ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack11l1lll_opy_ (u"ࠤ࡬ࡲࡻࡧ࡬ࡪࡦࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡪ࡯ࡤ࡫ࡪࠦࡢࡢࡵࡨ࠺࠹ࠦࡳࡵࡴࠥሜ"))
                return
            bstack1l1lll1ll1l_opy_ = self.bstack1l1llll1ll1_opy_(instance)
            if bstack1l1lll1ll1l_opy_:
                entry = bstack1lll1l11111_opy_(TestFramework.bstack1l1lllll11l_opy_, screenshot)
                self.bstack1l1llll111l_opy_(bstack1l1lll1ll1l_opy_, [entry])
                instance.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡩࡽ࡫ࡣࡶࡶࡨࠦም"), datetime.now() - bstack1l1ll1lllll_opy_)
            else:
                self.logger.warning(bstack11l1lll_opy_ (u"ࠦࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡸࡪࡹࡴࠡࡨࡲࡶࠥࡽࡨࡪࡥ࡫ࠤࡹ࡮ࡩࡴࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡷࡢࡵࠣࡸࡦࡱࡥ࡯ࠢࡥࡽࠥࡪࡲࡪࡸࡨࡶࡂࠦࡻࡾࠤሞ").format(instance.ref()))
        event = {}
        bstack1l1lll1ll1l_opy_ = self.bstack1l1llll1ll1_opy_(instance)
        if bstack1l1lll1ll1l_opy_:
            self.bstack1l1llll11ll_opy_(event, bstack1l1lll1ll1l_opy_)
            if event.get(bstack11l1lll_opy_ (u"ࠧࡲ࡯ࡨࡵࠥሟ")):
                self.bstack1l1llll111l_opy_(bstack1l1lll1ll1l_opy_, event[bstack11l1lll_opy_ (u"ࠨ࡬ࡰࡩࡶࠦሠ")])
            else:
                self.logger.info(bstack11l1lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦ࡬ࡰࡩࡶࠤ࡫ࡵࡲࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥ࡫ࡶࡦࡰࡷࠦሡ"))
    @measure(event_name=EVENTS.bstack1l1ll1l1l1l_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def bstack1l1llll111l_opy_(
        self,
        bstack1l1lll1ll1l_opy_: bstack1llll1111ll_opy_,
        entries: List[bstack1lll1l11111_opy_],
    ):
        self.bstack1ll1l11ll11_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll11l1_opy_(bstack1l1lll1ll1l_opy_, TestFramework.bstack1ll11l1l1ll_opy_)
        req.execution_context.hash = str(bstack1l1lll1ll1l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll1ll1l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll1ll1l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllll11l1_opy_(bstack1l1lll1ll1l_opy_, TestFramework.bstack1ll1l1lll1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllll11l1_opy_(bstack1l1lll1ll1l_opy_, TestFramework.bstack1l1lllllll1_opy_)
            log_entry.uuid = TestFramework.bstack1llllll11l1_opy_(bstack1l1lll1ll1l_opy_, TestFramework.bstack1ll11lll11l_opy_)
            log_entry.test_framework_state = bstack1l1lll1ll1l_opy_.state.name
            log_entry.message = entry.message.encode(bstack11l1lll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢሢ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11l1lll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦሣ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll1ll1l1_opy_
                log_entry.file_path = entry.bstack111ll1l_opy_
        def bstack1l1lll11l11_opy_():
            bstack11llll111l_opy_ = datetime.now()
            try:
                self.bstack1llll111ll1_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1lllll11l_opy_:
                    bstack1l1lll1ll1l_opy_.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢሤ"), datetime.now() - bstack11llll111l_opy_)
                elif entry.kind == TestFramework.bstack1l1llllllll_opy_:
                    bstack1l1lll1ll1l_opy_.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣሥ"), datetime.now() - bstack11llll111l_opy_)
                else:
                    bstack1l1lll1ll1l_opy_.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡲ࡯ࡨࠤሦ"), datetime.now() - bstack11llll111l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦሧ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack11111llll1_opy_.enqueue(bstack1l1lll11l11_opy_)
    @measure(event_name=EVENTS.bstack1l1lll1l1ll_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def bstack1l1lll11lll_opy_(
        self,
        instance: bstack1llll1111ll_opy_,
        bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_],
        event_json=None,
    ):
        self.bstack1ll1l11ll11_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1ll11l1l1ll_opy_)
        req.test_framework_name = TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1ll1l1lll1l_opy_)
        req.test_framework_version = TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1l1lllllll1_opy_)
        req.test_framework_state = bstack11111l11l1_opy_[0].name
        req.test_hook_state = bstack11111l11l1_opy_[1].name
        started_at = TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1ll1111l11l_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1l1llll1l1l_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1ll1lll1l_opy_)).encode(bstack11l1lll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨረ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1lll11l11_opy_():
            bstack11llll111l_opy_ = datetime.now()
            try:
                self.bstack1llll111ll1_opy_.TestFrameworkEvent(req)
                instance.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤ࡫ࡶࡦࡰࡷࠦሩ"), datetime.now() - bstack11llll111l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1lll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢሪ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack11111llll1_opy_.enqueue(bstack1l1lll11l11_opy_)
    def bstack1l1llll1ll1_opy_(self, instance: bstack1llllll11ll_opy_):
        bstack1l1ll1l1l11_opy_ = TestFramework.bstack111111l11l_opy_(instance.context)
        for t in bstack1l1ll1l1l11_opy_:
            bstack1l1lll11111_opy_ = TestFramework.bstack1llllll11l1_opy_(t, bstack1llll1lll1l_opy_.bstack1l1lll1111l_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll11111_opy_):
                return t
    def bstack1l1lllll1l1_opy_(self, message):
        self.bstack1l1ll11lll1_opy_(message + bstack11l1lll_opy_ (u"ࠥࡠࡳࠨራ"))
    def log_error(self, message):
        self.bstack1ll1111111l_opy_(message + bstack11l1lll_opy_ (u"ࠦࡡࡴࠢሬ"))
    def bstack1l1llll1l11_opy_(self, level, original_func):
        def bstack1ll1111l1l1_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1l1ll1l1l11_opy_ = TestFramework.bstack1l1llllll1l_opy_()
            if not bstack1l1ll1l1l11_opy_:
                return return_value
            bstack1l1lll1ll1l_opy_ = next(
                (
                    instance
                    for instance in bstack1l1ll1l1l11_opy_
                    if TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1ll11lll11l_opy_)
                ),
                None,
            )
            if not bstack1l1lll1ll1l_opy_:
                return
            entry = bstack1lll1l11111_opy_(TestFramework.bstack1l1ll1llll1_opy_, message, level)
            self.bstack1l1llll111l_opy_(bstack1l1lll1ll1l_opy_, [entry])
            return return_value
        return bstack1ll1111l1l1_opy_
    def bstack1l1llll11ll_opy_(self, event: dict, instance=None) -> None:
        global _1ll111l111l_opy_
        levels = [bstack11l1lll_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣር"), bstack11l1lll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥሮ")]
        bstack1l1lll1l11l_opy_ = bstack11l1lll_opy_ (u"ࠢࠣሯ")
        if instance is not None:
            try:
                bstack1l1lll1l11l_opy_ = TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1ll11lll11l_opy_)
            except Exception as e:
                self.logger.warning(bstack11l1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡷࡸ࡭ࡩࠦࡦࡳࡱࡰࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠨሰ").format(e))
        bstack1ll11111111_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩሱ")]
                bstack1l1llll1111_opy_ = os.path.join(bstack1l1lllll111_opy_, (bstack1l1lll1llll_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1llll1111_opy_):
                    self.logger.info(bstack11l1lll_opy_ (u"ࠥࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡮ࡰࡶࠣࡴࡷ࡫ࡳࡦࡰࡷࠤ࡫ࡵࡲࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡚ࠥࡥࡴࡶࠣࡥࡳࡪࠠࡃࡷ࡬ࡰࡩࠦ࡬ࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠥሲ").format(bstack1l1llll1111_opy_))
                file_names = os.listdir(bstack1l1llll1111_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1llll1111_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1ll111l111l_opy_:
                        self.logger.info(bstack11l1lll_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤሳ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1ll1l111l_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1ll1l111l_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack11l1lll_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣሴ"):
                                entry = bstack1lll1l11111_opy_(
                                    kind=bstack11l1lll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣስ"),
                                    message=bstack11l1lll_opy_ (u"ࠢࠣሶ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1ll1ll1l1_opy_=file_size,
                                    bstack1l1llll11l1_opy_=bstack11l1lll_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣሷ"),
                                    bstack111ll1l_opy_=os.path.abspath(file_path),
                                    bstack1l11llll1l_opy_=bstack1l1lll1l11l_opy_
                                )
                            elif level == bstack11l1lll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨሸ"):
                                entry = bstack1lll1l11111_opy_(
                                    kind=bstack11l1lll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧሹ"),
                                    message=bstack11l1lll_opy_ (u"ࠦࠧሺ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1ll1ll1l1_opy_=file_size,
                                    bstack1l1llll11l1_opy_=bstack11l1lll_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧሻ"),
                                    bstack111ll1l_opy_=os.path.abspath(file_path),
                                    bstack1ll1111ll11_opy_=bstack1l1lll1l11l_opy_
                                )
                            bstack1ll11111111_opy_.append(entry)
                            _1ll111l111l_opy_.add(abs_path)
                        except Exception as bstack1ll111l1111_opy_:
                            self.logger.error(bstack11l1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡵࡥ࡮ࡹࡥࡥࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠤሼ").format(bstack1ll111l1111_opy_))
        except Exception as e:
            self.logger.error(bstack11l1lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡶࡦ࡯ࡳࡦࡦࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠥሽ").format(e))
        event[bstack11l1lll_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨሾ")] = bstack1ll11111111_opy_
class bstack1l1ll1lll1l_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1ll1lll11_opy_ = set()
        kwargs[bstack11l1lll_opy_ (u"ࠤࡶ࡯࡮ࡶ࡫ࡦࡻࡶࠦሿ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1ll1ll11l_opy_(obj, self.bstack1l1ll1lll11_opy_)
def bstack1l1lllll1ll_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1ll1ll11l_opy_(obj, bstack1l1ll1lll11_opy_=None, max_depth=3):
    if bstack1l1ll1lll11_opy_ is None:
        bstack1l1ll1lll11_opy_ = set()
    if id(obj) in bstack1l1ll1lll11_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1ll1lll11_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1ll1111l1ll_opy_ = TestFramework.bstack1l1lll1lll1_opy_(obj)
    bstack1ll1111l111_opy_ = next((k.lower() in bstack1ll1111l1ll_opy_.lower() for k in bstack1ll1111ll1l_opy_.keys()), None)
    if bstack1ll1111l111_opy_:
        obj = TestFramework.bstack1l1lll111ll_opy_(obj, bstack1ll1111ll1l_opy_[bstack1ll1111l111_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack11l1lll_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨቀ")):
            keys = getattr(obj, bstack11l1lll_opy_ (u"ࠦࡤࡥࡳ࡭ࡱࡷࡷࡤࡥࠢቁ"), [])
        elif hasattr(obj, bstack11l1lll_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢቂ")):
            keys = getattr(obj, bstack11l1lll_opy_ (u"ࠨ࡟ࡠࡦ࡬ࡧࡹࡥ࡟ࠣቃ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack11l1lll_opy_ (u"ࠢࡠࠤቄ"))}
        if not obj and bstack1ll1111l1ll_opy_ == bstack11l1lll_opy_ (u"ࠣࡲࡤࡸ࡭ࡲࡩࡣ࠰ࡓࡳࡸ࡯ࡸࡑࡣࡷ࡬ࠧቅ"):
            obj = {bstack11l1lll_opy_ (u"ࠤࡳࡥࡹ࡮ࠢቆ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1lllll1ll_opy_(key) or str(key).startswith(bstack11l1lll_opy_ (u"ࠥࡣࠧቇ")):
            continue
        if value is not None and bstack1l1lllll1ll_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1ll1ll11l_opy_(value, bstack1l1ll1lll11_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1ll1ll11l_opy_(o, bstack1l1ll1lll11_opy_, max_depth) for o in value]))
    return result or None