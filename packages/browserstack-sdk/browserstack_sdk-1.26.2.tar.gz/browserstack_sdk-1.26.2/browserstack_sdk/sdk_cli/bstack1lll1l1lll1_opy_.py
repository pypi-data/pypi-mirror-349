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
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack111111l11l_opy_ import (
    bstack1llllll1l1l_opy_,
    bstack111111l1l1_opy_,
    bstack11111111ll_opy_,
    bstack1lllllll11l_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1ll1111llll_opy_, bstack11l11l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll111llll_opy_ import bstack1llll1ll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_, bstack1lll11111l1_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1l11l_opy_ import bstack1lll111ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l1ll1_opy_ import bstack1ll111ll111_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1l11lll11l_opy_ import bstack1l11l111ll_opy_, bstack11ll11l11_opy_, bstack11ll11ll_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1llll11l1l1_opy_(bstack1ll111ll111_opy_):
    bstack1l1l1l1ll1l_opy_ = bstack111l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡴ࡬ࡺࡪࡸࡳࠣቾ")
    bstack1l1llll111l_opy_ = bstack111l11_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤቿ")
    bstack1l1l11lll1l_opy_ = bstack111l11_opy_ (u"ࠦࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨኀ")
    bstack1l1l1l1l111_opy_ = bstack111l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧኁ")
    bstack1l1l1l11l11_opy_ = bstack111l11_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡸࡥࡧࡵࠥኂ")
    bstack1l1llll11ll_opy_ = bstack111l11_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨኃ")
    bstack1l1l1l1l11l_opy_ = bstack111l11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦኄ")
    bstack1l1l11lllll_opy_ = bstack111l11_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠢኅ")
    def __init__(self):
        super().__init__(bstack1ll111lllll_opy_=self.bstack1l1l1l1ll1l_opy_, frameworks=[bstack1llll1ll111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll11ll11ll_opy_((bstack1lll1l111ll_opy_.BEFORE_EACH, bstack1llll1lll1l_opy_.POST), self.bstack1l1l11llll1_opy_)
        if bstack11l11l11_opy_():
            TestFramework.bstack1ll11ll11ll_opy_((bstack1lll1l111ll_opy_.TEST, bstack1llll1lll1l_opy_.POST), self.bstack1ll1l1lll11_opy_)
        else:
            TestFramework.bstack1ll11ll11ll_opy_((bstack1lll1l111ll_opy_.TEST, bstack1llll1lll1l_opy_.PRE), self.bstack1ll1l1lll11_opy_)
        TestFramework.bstack1ll11ll11ll_opy_((bstack1lll1l111ll_opy_.TEST, bstack1llll1lll1l_opy_.POST), self.bstack1ll1l1lll1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11llll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11111l1_opy_,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l1l1ll11_opy_ = self.bstack1l1l1l11lll_opy_(instance.context)
        if not bstack1l1l1l1ll11_opy_:
            self.logger.debug(bstack111l11_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡱࡣࡪࡩ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣኆ") + str(bstack11111l1ll1_opy_) + bstack111l11_opy_ (u"ࠦࠧኇ"))
            return
        f.bstack111111ll1l_opy_(instance, bstack1llll11l1l1_opy_.bstack1l1llll111l_opy_, bstack1l1l1l1ll11_opy_)
    def bstack1l1l1l11lll_opy_(self, context: bstack1lllllll11l_opy_, bstack1l1l11lll11_opy_= True):
        if bstack1l1l11lll11_opy_:
            bstack1l1l1l1ll11_opy_ = self.bstack1ll111ll1ll_opy_(context, reverse=True)
        else:
            bstack1l1l1l1ll11_opy_ = self.bstack1ll111l1l11_opy_(context, reverse=True)
        return [f for f in bstack1l1l1l1ll11_opy_ if f[1].state != bstack1llllll1l1l_opy_.QUIT]
    def bstack1ll1l1lll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11111l1_opy_,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11llll1_opy_(f, instance, bstack11111l1ll1_opy_, *args, **kwargs)
        if not bstack1ll1111llll_opy_:
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣኈ") + str(kwargs) + bstack111l11_opy_ (u"ࠨࠢ኉"))
            return
        bstack1l1l1l1ll11_opy_ = f.bstack1llllll1111_opy_(instance, bstack1llll11l1l1_opy_.bstack1l1llll111l_opy_, [])
        if not bstack1l1l1l1ll11_opy_:
            self.logger.debug(bstack111l11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥኊ") + str(kwargs) + bstack111l11_opy_ (u"ࠣࠤኋ"))
            return
        if len(bstack1l1l1l1ll11_opy_) > 1:
            self.logger.debug(
                bstack1lll1l11111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦኌ"))
        bstack1l1l1l11l1l_opy_, bstack1l1ll1111ll_opy_ = bstack1l1l1l1ll11_opy_[0]
        page = bstack1l1l1l11l1l_opy_()
        if not page:
            self.logger.debug(bstack111l11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥኍ") + str(kwargs) + bstack111l11_opy_ (u"ࠦࠧ኎"))
            return
        bstack1llll1111l_opy_ = getattr(args[0], bstack111l11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧ኏"), None)
        try:
            page.evaluate(bstack111l11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢነ"),
                        bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫኑ") + json.dumps(
                            bstack1llll1111l_opy_) + bstack111l11_opy_ (u"ࠣࡿࢀࠦኒ"))
        except Exception as e:
            self.logger.debug(bstack111l11_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢና"), e)
    def bstack1ll1l1lll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11111l1_opy_,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11llll1_opy_(f, instance, bstack11111l1ll1_opy_, *args, **kwargs)
        if not bstack1ll1111llll_opy_:
            self.logger.debug(bstack111l11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨኔ") + str(kwargs) + bstack111l11_opy_ (u"ࠦࠧን"))
            return
        bstack1l1l1l1ll11_opy_ = f.bstack1llllll1111_opy_(instance, bstack1llll11l1l1_opy_.bstack1l1llll111l_opy_, [])
        if not bstack1l1l1l1ll11_opy_:
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣኖ") + str(kwargs) + bstack111l11_opy_ (u"ࠨࠢኗ"))
            return
        if len(bstack1l1l1l1ll11_opy_) > 1:
            self.logger.debug(
                bstack1lll1l11111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤኘ"))
        bstack1l1l1l11l1l_opy_, bstack1l1ll1111ll_opy_ = bstack1l1l1l1ll11_opy_[0]
        page = bstack1l1l1l11l1l_opy_()
        if not page:
            self.logger.debug(bstack111l11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣኙ") + str(kwargs) + bstack111l11_opy_ (u"ࠤࠥኚ"))
            return
        status = f.bstack1llllll1111_opy_(instance, TestFramework.bstack1l1l1l111l1_opy_, None)
        if not status:
            self.logger.debug(bstack111l11_opy_ (u"ࠥࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨኛ") + str(bstack11111l1ll1_opy_) + bstack111l11_opy_ (u"ࠦࠧኜ"))
            return
        bstack1l1l1l1l1l1_opy_ = {bstack111l11_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧኝ"): status.lower()}
        bstack1l1l1l11111_opy_ = f.bstack1llllll1111_opy_(instance, TestFramework.bstack1l1l1l111ll_opy_, None)
        if status.lower() == bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ኞ") and bstack1l1l1l11111_opy_ is not None:
            bstack1l1l1l1l1l1_opy_[bstack111l11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧኟ")] = bstack1l1l1l11111_opy_[0][bstack111l11_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫአ")][0] if isinstance(bstack1l1l1l11111_opy_, list) else str(bstack1l1l1l11111_opy_)
        try:
              page.evaluate(
                    bstack111l11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥኡ"),
                    bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࠨኢ")
                    + json.dumps(bstack1l1l1l1l1l1_opy_)
                    + bstack111l11_opy_ (u"ࠦࢂࠨኣ")
                )
        except Exception as e:
            self.logger.debug(bstack111l11_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠧኤ"), e)
    def bstack1ll111111ll_opy_(
        self,
        instance: bstack1lll11111l1_opy_,
        f: TestFramework,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11llll1_opy_(f, instance, bstack11111l1ll1_opy_, *args, **kwargs)
        if not bstack1ll1111llll_opy_:
            self.logger.debug(
                bstack1lll1l11111_opy_ (u"ࠨ࡭ࡢࡴ࡮ࡣࡴ࠷࠱ࡺࡡࡶࡽࡳࡩ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢእ"))
            return
        bstack1l1l1l1ll11_opy_ = f.bstack1llllll1111_opy_(instance, bstack1llll11l1l1_opy_.bstack1l1llll111l_opy_, [])
        if not bstack1l1l1l1ll11_opy_:
            self.logger.debug(bstack111l11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥኦ") + str(kwargs) + bstack111l11_opy_ (u"ࠣࠤኧ"))
            return
        if len(bstack1l1l1l1ll11_opy_) > 1:
            self.logger.debug(
                bstack1lll1l11111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦከ"))
        bstack1l1l1l11l1l_opy_, bstack1l1ll1111ll_opy_ = bstack1l1l1l1ll11_opy_[0]
        page = bstack1l1l1l11l1l_opy_()
        if not page:
            self.logger.debug(bstack111l11_opy_ (u"ࠥࡱࡦࡸ࡫ࡠࡱ࠴࠵ࡾࡥࡳࡺࡰࡦ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥኩ") + str(kwargs) + bstack111l11_opy_ (u"ࠦࠧኪ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack111l11_opy_ (u"ࠧࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡘࡿ࡮ࡤ࠼ࠥካ") + str(timestamp)
        try:
            page.evaluate(
                bstack111l11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢኬ"),
                bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬክ").format(
                    json.dumps(
                        {
                            bstack111l11_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣኮ"): bstack111l11_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦኯ"),
                            bstack111l11_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨኰ"): {
                                bstack111l11_opy_ (u"ࠦࡹࡿࡰࡦࠤ኱"): bstack111l11_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤኲ"),
                                bstack111l11_opy_ (u"ࠨࡤࡢࡶࡤࠦኳ"): data,
                                bstack111l11_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨኴ"): bstack111l11_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢኵ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack111l11_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡵ࠱࠲ࡻࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡽࢀࠦ኶"), e)
    def bstack1l1lll1ll1l_opy_(
        self,
        instance: bstack1lll11111l1_opy_,
        f: TestFramework,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11llll1_opy_(f, instance, bstack11111l1ll1_opy_, *args, **kwargs)
        if f.bstack1llllll1111_opy_(instance, bstack1llll11l1l1_opy_.bstack1l1llll11ll_opy_, False):
            return
        self.bstack1ll1l1l1l1l_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll1111_opy_(instance, TestFramework.bstack1ll1l111lll_opy_)
        req.test_framework_name = TestFramework.bstack1llllll1111_opy_(instance, TestFramework.bstack1ll11ll1lll_opy_)
        req.test_framework_version = TestFramework.bstack1llllll1111_opy_(instance, TestFramework.bstack1ll11111l1l_opy_)
        req.test_framework_state = bstack11111l1ll1_opy_[0].name
        req.test_hook_state = bstack11111l1ll1_opy_[1].name
        req.test_uuid = TestFramework.bstack1llllll1111_opy_(instance, TestFramework.bstack1ll11lll11l_opy_)
        for bstack1l1l1l1l1ll_opy_ in bstack1lll111ll1l_opy_.bstack1111111l11_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack111l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤ኷")
                if bstack1ll1111llll_opy_
                else bstack111l11_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥኸ")
            )
            session.ref = bstack1l1l1l1l1ll_opy_.ref()
            session.hub_url = bstack1lll111ll1l_opy_.bstack1llllll1111_opy_(bstack1l1l1l1l1ll_opy_, bstack1lll111ll1l_opy_.bstack1l1l1ll1ll1_opy_, bstack111l11_opy_ (u"ࠧࠨኹ"))
            session.framework_name = bstack1l1l1l1l1ll_opy_.framework_name
            session.framework_version = bstack1l1l1l1l1ll_opy_.framework_version
            session.framework_session_id = bstack1lll111ll1l_opy_.bstack1llllll1111_opy_(bstack1l1l1l1l1ll_opy_, bstack1lll111ll1l_opy_.bstack1l1l1l1llll_opy_, bstack111l11_opy_ (u"ࠨࠢኺ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11llllll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11111l1_opy_,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l1l1ll11_opy_ = f.bstack1llllll1111_opy_(instance, bstack1llll11l1l1_opy_.bstack1l1llll111l_opy_, [])
        if not bstack1l1l1l1ll11_opy_:
            self.logger.debug(bstack111l11_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣኻ") + str(kwargs) + bstack111l11_opy_ (u"ࠣࠤኼ"))
            return
        if len(bstack1l1l1l1ll11_opy_) > 1:
            self.logger.debug(bstack111l11_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥኽ") + str(kwargs) + bstack111l11_opy_ (u"ࠥࠦኾ"))
        bstack1l1l1l11l1l_opy_, bstack1l1ll1111ll_opy_ = bstack1l1l1l1ll11_opy_[0]
        page = bstack1l1l1l11l1l_opy_()
        if not page:
            self.logger.debug(bstack111l11_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ኿") + str(kwargs) + bstack111l11_opy_ (u"ࠧࠨዀ"))
            return
        return page
    def bstack1ll1l1l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11111l1_opy_,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l1l11ll1_opy_ = {}
        for bstack1l1l1l1l1ll_opy_ in bstack1lll111ll1l_opy_.bstack1111111l11_opy_.values():
            caps = bstack1lll111ll1l_opy_.bstack1llllll1111_opy_(bstack1l1l1l1l1ll_opy_, bstack1lll111ll1l_opy_.bstack1l1l1lllll1_opy_, bstack111l11_opy_ (u"ࠨࠢ዁"))
        bstack1l1l1l11ll1_opy_[bstack111l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧዂ")] = caps.get(bstack111l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤዃ"), bstack111l11_opy_ (u"ࠤࠥዄ"))
        bstack1l1l1l11ll1_opy_[bstack111l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤዅ")] = caps.get(bstack111l11_opy_ (u"ࠦࡴࡹࠢ዆"), bstack111l11_opy_ (u"ࠧࠨ዇"))
        bstack1l1l1l11ll1_opy_[bstack111l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣወ")] = caps.get(bstack111l11_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦዉ"), bstack111l11_opy_ (u"ࠣࠤዊ"))
        bstack1l1l1l11ll1_opy_[bstack111l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥዋ")] = caps.get(bstack111l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧዌ"), bstack111l11_opy_ (u"ࠦࠧው"))
        return bstack1l1l1l11ll1_opy_
    def bstack1ll1l11l11l_opy_(self, page: object, bstack1ll1l1ll111_opy_, args={}):
        try:
            bstack1l1l1l1111l_opy_ = bstack111l11_opy_ (u"ࠧࠨࠢࠩࡨࡸࡲࡨࡺࡩࡰࡰࠣࠬ࠳࠴࠮ࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹࠩࠡࡽࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦ࡮ࡦࡹࠣࡔࡷࡵ࡭ࡪࡵࡨࠬ࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠲ࠠࡳࡧ࡭ࡩࡨࡺࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠴ࡰࡶࡵ࡫ࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡻࡧࡰࡢࡦࡴࡪࡹࡾࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࢃࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠬࠬࢀࡧࡲࡨࡡ࡭ࡷࡴࡴࡽࠪࠤࠥࠦዎ")
            bstack1ll1l1ll111_opy_ = bstack1ll1l1ll111_opy_.replace(bstack111l11_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤዏ"), bstack111l11_opy_ (u"ࠢࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹࠢዐ"))
            script = bstack1l1l1l1111l_opy_.format(fn_body=bstack1ll1l1ll111_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack111l11_opy_ (u"ࠣࡣ࠴࠵ࡾࡥࡳࡤࡴ࡬ࡴࡹࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡇࡵࡶࡴࡸࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡢ࠳࠴ࡽࠥࡹࡣࡳ࡫ࡳࡸ࠱ࠦࠢዑ") + str(e) + bstack111l11_opy_ (u"ࠤࠥዒ"))