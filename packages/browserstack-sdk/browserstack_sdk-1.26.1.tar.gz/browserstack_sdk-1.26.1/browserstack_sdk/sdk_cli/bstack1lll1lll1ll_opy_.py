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
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import (
    bstack1llllll1l11_opy_,
    bstack11111ll1l1_opy_,
    bstack1llllll111l_opy_,
    bstack1llllll11ll_opy_,
    bstack11111ll11l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll1l11l1_opy_ import bstack1lll111llll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_, bstack1llll1111ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111ll11l_opy_ import bstack1ll111lll11_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll1l1ll1_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1llll1lll1l_opy_(bstack1ll111lll11_opy_):
    bstack1l1l11lll11_opy_ = bstack11l1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡵ࡭ࡻ࡫ࡲࡴࠤጧ")
    bstack1l1lll1111l_opy_ = bstack11l1lll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥጨ")
    bstack1l1l1l1l111_opy_ = bstack11l1lll_opy_ (u"ࠧࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢጩ")
    bstack1l1l1l1ll11_opy_ = bstack11l1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨጪ")
    bstack1l1l1l111ll_opy_ = bstack11l1lll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡲࡦࡨࡶࠦጫ")
    bstack1l1ll1l11ll_opy_ = bstack11l1lll_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪࠢጬ")
    bstack1l1l1l11l11_opy_ = bstack11l1lll_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧጭ")
    bstack1l1l1l1ll1l_opy_ = bstack11l1lll_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠣጮ")
    def __init__(self):
        super().__init__(bstack1ll111l1lll_opy_=self.bstack1l1l11lll11_opy_, frameworks=[bstack1lll111llll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1ll11111_opy_((bstack1lll11llll1_opy_.BEFORE_EACH, bstack1ll1lll1111_opy_.POST), self.bstack1l11lll1ll1_opy_)
        TestFramework.bstack1ll1ll11111_opy_((bstack1lll11llll1_opy_.TEST, bstack1ll1lll1111_opy_.PRE), self.bstack1ll1l11ll1l_opy_)
        TestFramework.bstack1ll1ll11111_opy_((bstack1lll11llll1_opy_.TEST, bstack1ll1lll1111_opy_.POST), self.bstack1ll11ll11l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11lll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1111ll_opy_,
        bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1lll11111_opy_ = self.bstack1l11lllllll_opy_(instance.context)
        if not bstack1l1lll11111_opy_:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢጯ") + str(bstack11111l11l1_opy_) + bstack11l1lll_opy_ (u"ࠧࠨጰ"))
        f.bstack111111llll_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1lll1111l_opy_, bstack1l1lll11111_opy_)
        bstack1l11lll1lll_opy_ = self.bstack1l11lllllll_opy_(instance.context, bstack1l11llllll1_opy_=False)
        f.bstack111111llll_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1l1l1l111_opy_, bstack1l11lll1lll_opy_)
    def bstack1ll1l11ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1111ll_opy_,
        bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lll1ll1_opy_(f, instance, bstack11111l11l1_opy_, *args, **kwargs)
        if not f.bstack1llllll11l1_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1l1l11l11_opy_, False):
            self.__1l11llll111_opy_(f,instance,bstack11111l11l1_opy_)
    def bstack1ll11ll11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1111ll_opy_,
        bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lll1ll1_opy_(f, instance, bstack11111l11l1_opy_, *args, **kwargs)
        if not f.bstack1llllll11l1_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1l1l11l11_opy_, False):
            self.__1l11llll111_opy_(f, instance, bstack11111l11l1_opy_)
        if not f.bstack1llllll11l1_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1l1l1ll1l_opy_, False):
            self.__1l11lllll11_opy_(f, instance, bstack11111l11l1_opy_)
    def bstack1l11lllll1l_opy_(
        self,
        f: bstack1lll111llll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll111ll1l1_opy_(instance):
            return
        if f.bstack1llllll11l1_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1l1l1ll1l_opy_, False):
            return
        driver.execute_script(
            bstack11l1lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦጱ").format(
                json.dumps(
                    {
                        bstack11l1lll_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢጲ"): bstack11l1lll_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦጳ"),
                        bstack11l1lll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧጴ"): {bstack11l1lll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥጵ"): result},
                    }
                )
            )
        )
        f.bstack111111llll_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1l1l1ll1l_opy_, True)
    def bstack1l11lllllll_opy_(self, context: bstack11111ll11l_opy_, bstack1l11llllll1_opy_= True):
        if bstack1l11llllll1_opy_:
            bstack1l1lll11111_opy_ = self.bstack1ll111l11l1_opy_(context, reverse=True)
        else:
            bstack1l1lll11111_opy_ = self.bstack1ll111ll1ll_opy_(context, reverse=True)
        return [f for f in bstack1l1lll11111_opy_ if f[1].state != bstack1llllll1l11_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1l111l1l_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def __1l11lllll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1111ll_opy_,
        bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤጶ")).get(bstack11l1lll_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤጷ")):
            bstack1l1lll11111_opy_ = f.bstack1llllll11l1_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1lll1111l_opy_, [])
            if not bstack1l1lll11111_opy_:
                self.logger.debug(bstack11l1lll_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤጸ") + str(bstack11111l11l1_opy_) + bstack11l1lll_opy_ (u"ࠢࠣጹ"))
                return
            driver = bstack1l1lll11111_opy_[0][0]()
            status = f.bstack1llllll11l1_opy_(instance, TestFramework.bstack1l1l1l1l1ll_opy_, None)
            if not status:
                self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥጺ") + str(bstack11111l11l1_opy_) + bstack11l1lll_opy_ (u"ࠤࠥጻ"))
                return
            bstack1l1l1l111l1_opy_ = {bstack11l1lll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥጼ"): status.lower()}
            bstack1l1l11lll1l_opy_ = f.bstack1llllll11l1_opy_(instance, TestFramework.bstack1l1l1l11111_opy_, None)
            if status.lower() == bstack11l1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫጽ") and bstack1l1l11lll1l_opy_ is not None:
                bstack1l1l1l111l1_opy_[bstack11l1lll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬጾ")] = bstack1l1l11lll1l_opy_[0][bstack11l1lll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩጿ")][0] if isinstance(bstack1l1l11lll1l_opy_, list) else str(bstack1l1l11lll1l_opy_)
            driver.execute_script(
                bstack11l1lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧፀ").format(
                    json.dumps(
                        {
                            bstack11l1lll_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣፁ"): bstack11l1lll_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧፂ"),
                            bstack11l1lll_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨፃ"): bstack1l1l1l111l1_opy_,
                        }
                    )
                )
            )
            f.bstack111111llll_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1l1l1ll1l_opy_, True)
    @measure(event_name=EVENTS.bstack1ll1l1ll11_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def __1l11llll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1111ll_opy_,
        bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤፄ")).get(bstack11l1lll_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢፅ")):
            test_name = f.bstack1llllll11l1_opy_(instance, TestFramework.bstack1l11llll11l_opy_, None)
            if not test_name:
                self.logger.debug(bstack11l1lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧፆ"))
                return
            bstack1l1lll11111_opy_ = f.bstack1llllll11l1_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1lll1111l_opy_, [])
            if not bstack1l1lll11111_opy_:
                self.logger.debug(bstack11l1lll_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤፇ") + str(bstack11111l11l1_opy_) + bstack11l1lll_opy_ (u"ࠣࠤፈ"))
                return
            for bstack1l1ll11111l_opy_, bstack1l11llll1l1_opy_ in bstack1l1lll11111_opy_:
                if not bstack1lll111llll_opy_.bstack1ll111ll1l1_opy_(bstack1l11llll1l1_opy_):
                    continue
                driver = bstack1l1ll11111l_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack11l1lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢፉ").format(
                        json.dumps(
                            {
                                bstack11l1lll_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥፊ"): bstack11l1lll_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧፋ"),
                                bstack11l1lll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣፌ"): {bstack11l1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦፍ"): test_name},
                            }
                        )
                    )
                )
            f.bstack111111llll_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1l1l11l11_opy_, True)
    def bstack1ll111111ll_opy_(
        self,
        instance: bstack1llll1111ll_opy_,
        f: TestFramework,
        bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lll1ll1_opy_(f, instance, bstack11111l11l1_opy_, *args, **kwargs)
        bstack1l1lll11111_opy_ = [d for d, _ in f.bstack1llllll11l1_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1lll1111l_opy_, [])]
        if not bstack1l1lll11111_opy_:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢፎ"))
            return
        if not bstack1l1ll1l1ll1_opy_():
            self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨፏ"))
            return
        for bstack1l11llll1ll_opy_ in bstack1l1lll11111_opy_:
            driver = bstack1l11llll1ll_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack11l1lll_opy_ (u"ࠤࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡕࡼࡲࡨࡀࠢፐ") + str(timestamp)
            driver.execute_script(
                bstack11l1lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣፑ").format(
                    json.dumps(
                        {
                            bstack11l1lll_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦፒ"): bstack11l1lll_opy_ (u"ࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢፓ"),
                            bstack11l1lll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤፔ"): {
                                bstack11l1lll_opy_ (u"ࠢࡵࡻࡳࡩࠧፕ"): bstack11l1lll_opy_ (u"ࠣࡃࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠧፖ"),
                                bstack11l1lll_opy_ (u"ࠤࡧࡥࡹࡧࠢፗ"): data,
                                bstack11l1lll_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࠤፘ"): bstack11l1lll_opy_ (u"ࠦࡩ࡫ࡢࡶࡩࠥፙ")
                            }
                        }
                    )
                )
            )
    def bstack1l1lll1ll11_opy_(
        self,
        instance: bstack1llll1111ll_opy_,
        f: TestFramework,
        bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lll1ll1_opy_(f, instance, bstack11111l11l1_opy_, *args, **kwargs)
        bstack1l1lll11111_opy_ = [d for _, d in f.bstack1llllll11l1_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1lll1111l_opy_, [])] + [d for _, d in f.bstack1llllll11l1_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1l1l1l111_opy_, [])]
        keys = [
            bstack1llll1lll1l_opy_.bstack1l1lll1111l_opy_,
            bstack1llll1lll1l_opy_.bstack1l1l1l1l111_opy_,
        ]
        bstack1l1lll11111_opy_ = [
            d for key in keys for _, d in f.bstack1llllll11l1_opy_(instance, key, [])
        ]
        if not bstack1l1lll11111_opy_:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡰࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢፚ"))
            return
        if f.bstack1llllll11l1_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1ll1l11ll_opy_, False):
            self.logger.debug(bstack11l1lll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡄࡄࡗࠤࡦࡲࡲࡦࡣࡧࡽࠥࡩࡲࡦࡣࡷࡩࡩࠨ፛"))
            return
        self.bstack1ll1l11ll11_opy_()
        bstack11llll111l_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1ll11l1l1ll_opy_)
        req.test_framework_name = TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1ll1l1lll1l_opy_)
        req.test_framework_version = TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1l1lllllll1_opy_)
        req.test_framework_state = bstack11111l11l1_opy_[0].name
        req.test_hook_state = bstack11111l11l1_opy_[1].name
        req.test_uuid = TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1ll11lll11l_opy_)
        for driver in bstack1l1lll11111_opy_:
            session = req.automation_sessions.add()
            session.provider = (
                bstack11l1lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠨ፜")
                if bstack1lll111llll_opy_.bstack1llllll11l1_opy_(driver, bstack1lll111llll_opy_.bstack1l11lll1l1l_opy_, False)
                else bstack11l1lll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠢ፝")
            )
            session.ref = driver.ref()
            session.hub_url = bstack1lll111llll_opy_.bstack1llllll11l1_opy_(driver, bstack1lll111llll_opy_.bstack1l1l1lll111_opy_, bstack11l1lll_opy_ (u"ࠤࠥ፞"))
            session.framework_name = driver.framework_name
            session.framework_version = driver.framework_version
            session.framework_session_id = bstack1lll111llll_opy_.bstack1llllll11l1_opy_(driver, bstack1lll111llll_opy_.bstack1l1l1lll11l_opy_, bstack11l1lll_opy_ (u"ࠥࠦ፟"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l1l1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1111ll_opy_,
        bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lll11111_opy_ = f.bstack1llllll11l1_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1lll1111l_opy_, [])
        if not bstack1l1ll1l1ll1_opy_() and len(bstack1l1lll11111_opy_) == 0:
            bstack1l1lll11111_opy_ = f.bstack1llllll11l1_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1l1l1l111_opy_, [])
        if not bstack1l1lll11111_opy_:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ፠") + str(kwargs) + bstack11l1lll_opy_ (u"ࠧࠨ፡"))
            return {}
        if len(bstack1l1lll11111_opy_) > 1:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ።") + str(kwargs) + bstack11l1lll_opy_ (u"ࠢࠣ፣"))
            return {}
        bstack1l1ll11111l_opy_, bstack1l1ll1111ll_opy_ = bstack1l1lll11111_opy_[0]
        driver = bstack1l1ll11111l_opy_()
        if not driver:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ፤") + str(kwargs) + bstack11l1lll_opy_ (u"ࠤࠥ፥"))
            return {}
        capabilities = f.bstack1llllll11l1_opy_(bstack1l1ll1111ll_opy_, bstack1lll111llll_opy_.bstack1l1l1llllll_opy_)
        if not capabilities:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ፦") + str(kwargs) + bstack11l1lll_opy_ (u"ࠦࠧ፧"))
            return {}
        return capabilities.get(bstack11l1lll_opy_ (u"ࠧࡧ࡬ࡸࡣࡼࡷࡒࡧࡴࡤࡪࠥ፨"), {})
    def bstack1ll11ll1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1111ll_opy_,
        bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lll11111_opy_ = f.bstack1llllll11l1_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1lll1111l_opy_, [])
        if not bstack1l1ll1l1ll1_opy_() and len(bstack1l1lll11111_opy_) == 0:
            bstack1l1lll11111_opy_ = f.bstack1llllll11l1_opy_(instance, bstack1llll1lll1l_opy_.bstack1l1l1l1l111_opy_, [])
        if not bstack1l1lll11111_opy_:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ፩") + str(kwargs) + bstack11l1lll_opy_ (u"ࠢࠣ፪"))
            return
        if len(bstack1l1lll11111_opy_) > 1:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࡱ࡫࡮ࠩࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ፫") + str(kwargs) + bstack11l1lll_opy_ (u"ࠤࠥ፬"))
        bstack1l1ll11111l_opy_, bstack1l1ll1111ll_opy_ = bstack1l1lll11111_opy_[0]
        driver = bstack1l1ll11111l_opy_()
        if not driver:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ፭") + str(kwargs) + bstack11l1lll_opy_ (u"ࠦࠧ፮"))
            return
        return driver