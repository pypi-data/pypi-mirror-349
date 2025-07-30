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
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack111111l11l_opy_ import (
    bstack1llllll1l1l_opy_,
    bstack111111l1l1_opy_,
    bstack1lllllll1l1_opy_,
    bstack11111111ll_opy_,
    bstack1lllllll11l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll111llll_opy_ import bstack1llll1ll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_, bstack1lll11111l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l1ll1_opy_ import bstack1ll111ll111_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1ll1111llll_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1ll1ll1lll1_opy_(bstack1ll111ll111_opy_):
    bstack1l1l1l1ll1l_opy_ = bstack111l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡵ࡭ࡻ࡫ࡲࡴࠤጧ")
    bstack1l1llll111l_opy_ = bstack111l11_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥጨ")
    bstack1l1l11lll1l_opy_ = bstack111l11_opy_ (u"ࠧࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢጩ")
    bstack1l1l1l1l111_opy_ = bstack111l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨጪ")
    bstack1l1l1l11l11_opy_ = bstack111l11_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡲࡦࡨࡶࠦጫ")
    bstack1l1llll11ll_opy_ = bstack111l11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪࠢጬ")
    bstack1l1l1l1l11l_opy_ = bstack111l11_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧጭ")
    bstack1l1l11lllll_opy_ = bstack111l11_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠣጮ")
    def __init__(self):
        super().__init__(bstack1ll111lllll_opy_=self.bstack1l1l1l1ll1l_opy_, frameworks=[bstack1llll1ll111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll11ll11ll_opy_((bstack1lll1l111ll_opy_.BEFORE_EACH, bstack1llll1lll1l_opy_.POST), self.bstack1l11llllll1_opy_)
        TestFramework.bstack1ll11ll11ll_opy_((bstack1lll1l111ll_opy_.TEST, bstack1llll1lll1l_opy_.PRE), self.bstack1ll1l1lll11_opy_)
        TestFramework.bstack1ll11ll11ll_opy_((bstack1lll1l111ll_opy_.TEST, bstack1llll1lll1l_opy_.POST), self.bstack1ll1l1lll1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11llllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11111l1_opy_,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1ll1111l11l_opy_ = self.bstack1l11lll11ll_opy_(instance.context)
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack111l11_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢጯ") + str(bstack11111l1ll1_opy_) + bstack111l11_opy_ (u"ࠧࠨጰ"))
        f.bstack111111ll1l_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1llll111l_opy_, bstack1ll1111l11l_opy_)
        bstack1l11llll11l_opy_ = self.bstack1l11lll11ll_opy_(instance.context, bstack1l11llll1ll_opy_=False)
        f.bstack111111ll1l_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l11lll1l_opy_, bstack1l11llll11l_opy_)
    def bstack1ll1l1lll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11111l1_opy_,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11llllll1_opy_(f, instance, bstack11111l1ll1_opy_, *args, **kwargs)
        if not f.bstack1llllll1111_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l1l1l11l_opy_, False):
            self.__1l11lll1ll1_opy_(f,instance,bstack11111l1ll1_opy_)
    def bstack1ll1l1lll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11111l1_opy_,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11llllll1_opy_(f, instance, bstack11111l1ll1_opy_, *args, **kwargs)
        if not f.bstack1llllll1111_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l1l1l11l_opy_, False):
            self.__1l11lll1ll1_opy_(f, instance, bstack11111l1ll1_opy_)
        if not f.bstack1llllll1111_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l11lllll_opy_, False):
            self.__1l11lllll1l_opy_(f, instance, bstack11111l1ll1_opy_)
    def bstack1l11llll111_opy_(
        self,
        f: bstack1llll1ll111_opy_,
        driver: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll111ll11l_opy_(instance):
            return
        if f.bstack1llllll1111_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l11lllll_opy_, False):
            return
        driver.execute_script(
            bstack111l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦጱ").format(
                json.dumps(
                    {
                        bstack111l11_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢጲ"): bstack111l11_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦጳ"),
                        bstack111l11_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧጴ"): {bstack111l11_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥጵ"): result},
                    }
                )
            )
        )
        f.bstack111111ll1l_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l11lllll_opy_, True)
    def bstack1l11lll11ll_opy_(self, context: bstack1lllllll11l_opy_, bstack1l11llll1ll_opy_= True):
        if bstack1l11llll1ll_opy_:
            bstack1ll1111l11l_opy_ = self.bstack1ll111ll1ll_opy_(context, reverse=True)
        else:
            bstack1ll1111l11l_opy_ = self.bstack1ll111l1l11_opy_(context, reverse=True)
        return [f for f in bstack1ll1111l11l_opy_ if f[1].state != bstack1llllll1l1l_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11111l111_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
    def __1l11lllll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11111l1_opy_,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤጶ")).get(bstack111l11_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤጷ")):
            bstack1ll1111l11l_opy_ = f.bstack1llllll1111_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1llll111l_opy_, [])
            if not bstack1ll1111l11l_opy_:
                self.logger.debug(bstack111l11_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤጸ") + str(bstack11111l1ll1_opy_) + bstack111l11_opy_ (u"ࠢࠣጹ"))
                return
            driver = bstack1ll1111l11l_opy_[0][0]()
            status = f.bstack1llllll1111_opy_(instance, TestFramework.bstack1l1l1l111l1_opy_, None)
            if not status:
                self.logger.debug(bstack111l11_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥጺ") + str(bstack11111l1ll1_opy_) + bstack111l11_opy_ (u"ࠤࠥጻ"))
                return
            bstack1l1l1l1l1l1_opy_ = {bstack111l11_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥጼ"): status.lower()}
            bstack1l1l1l11111_opy_ = f.bstack1llllll1111_opy_(instance, TestFramework.bstack1l1l1l111ll_opy_, None)
            if status.lower() == bstack111l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫጽ") and bstack1l1l1l11111_opy_ is not None:
                bstack1l1l1l1l1l1_opy_[bstack111l11_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬጾ")] = bstack1l1l1l11111_opy_[0][bstack111l11_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩጿ")][0] if isinstance(bstack1l1l1l11111_opy_, list) else str(bstack1l1l1l11111_opy_)
            driver.execute_script(
                bstack111l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧፀ").format(
                    json.dumps(
                        {
                            bstack111l11_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣፁ"): bstack111l11_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧፂ"),
                            bstack111l11_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨፃ"): bstack1l1l1l1l1l1_opy_,
                        }
                    )
                )
            )
            f.bstack111111ll1l_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l11lllll_opy_, True)
    @measure(event_name=EVENTS.bstack1llll1l1_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
    def __1l11lll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11111l1_opy_,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤፄ")).get(bstack111l11_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢፅ")):
            test_name = f.bstack1llllll1111_opy_(instance, TestFramework.bstack1l11llll1l1_opy_, None)
            if not test_name:
                self.logger.debug(bstack111l11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧፆ"))
                return
            bstack1ll1111l11l_opy_ = f.bstack1llllll1111_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1llll111l_opy_, [])
            if not bstack1ll1111l11l_opy_:
                self.logger.debug(bstack111l11_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤፇ") + str(bstack11111l1ll1_opy_) + bstack111l11_opy_ (u"ࠣࠤፈ"))
                return
            for bstack1l1ll1111l1_opy_, bstack1l11lllllll_opy_ in bstack1ll1111l11l_opy_:
                if not bstack1llll1ll111_opy_.bstack1ll111ll11l_opy_(bstack1l11lllllll_opy_):
                    continue
                driver = bstack1l1ll1111l1_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack111l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢፉ").format(
                        json.dumps(
                            {
                                bstack111l11_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥፊ"): bstack111l11_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧፋ"),
                                bstack111l11_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣፌ"): {bstack111l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦፍ"): test_name},
                            }
                        )
                    )
                )
            f.bstack111111ll1l_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l1l1l11l_opy_, True)
    def bstack1ll111111ll_opy_(
        self,
        instance: bstack1lll11111l1_opy_,
        f: TestFramework,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11llllll1_opy_(f, instance, bstack11111l1ll1_opy_, *args, **kwargs)
        bstack1ll1111l11l_opy_ = [d for d, _ in f.bstack1llllll1111_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1llll111l_opy_, [])]
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack111l11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢፎ"))
            return
        if not bstack1ll1111llll_opy_():
            self.logger.debug(bstack111l11_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨፏ"))
            return
        for bstack1l11lll1lll_opy_ in bstack1ll1111l11l_opy_:
            driver = bstack1l11lll1lll_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack111l11_opy_ (u"ࠤࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡕࡼࡲࡨࡀࠢፐ") + str(timestamp)
            driver.execute_script(
                bstack111l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣፑ").format(
                    json.dumps(
                        {
                            bstack111l11_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦፒ"): bstack111l11_opy_ (u"ࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢፓ"),
                            bstack111l11_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤፔ"): {
                                bstack111l11_opy_ (u"ࠢࡵࡻࡳࡩࠧፕ"): bstack111l11_opy_ (u"ࠣࡃࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠧፖ"),
                                bstack111l11_opy_ (u"ࠤࡧࡥࡹࡧࠢፗ"): data,
                                bstack111l11_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࠤፘ"): bstack111l11_opy_ (u"ࠦࡩ࡫ࡢࡶࡩࠥፙ")
                            }
                        }
                    )
                )
            )
    def bstack1l1lll1ll1l_opy_(
        self,
        instance: bstack1lll11111l1_opy_,
        f: TestFramework,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11llllll1_opy_(f, instance, bstack11111l1ll1_opy_, *args, **kwargs)
        keys = [
            bstack1ll1ll1lll1_opy_.bstack1l1llll111l_opy_,
            bstack1ll1ll1lll1_opy_.bstack1l1l11lll1l_opy_,
        ]
        bstack1ll1111l11l_opy_ = []
        for key in keys:
            bstack1ll1111l11l_opy_.extend(f.bstack1llllll1111_opy_(instance, key, []))
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡰࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢፚ"))
            return
        if f.bstack1llllll1111_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1llll11ll_opy_, False):
            self.logger.debug(bstack111l11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡄࡄࡗࠤࡦࡲࡲࡦࡣࡧࡽࠥࡩࡲࡦࡣࡷࡩࡩࠨ፛"))
            return
        self.bstack1ll1l1l1l1l_opy_()
        bstack111l1l111_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll1111_opy_(instance, TestFramework.bstack1ll1l111lll_opy_)
        req.test_framework_name = TestFramework.bstack1llllll1111_opy_(instance, TestFramework.bstack1ll11ll1lll_opy_)
        req.test_framework_version = TestFramework.bstack1llllll1111_opy_(instance, TestFramework.bstack1ll11111l1l_opy_)
        req.test_framework_state = bstack11111l1ll1_opy_[0].name
        req.test_hook_state = bstack11111l1ll1_opy_[1].name
        req.test_uuid = TestFramework.bstack1llllll1111_opy_(instance, TestFramework.bstack1ll11lll11l_opy_)
        for bstack1l1ll1111l1_opy_, driver in bstack1ll1111l11l_opy_:
            try:
                webdriver = bstack1l1ll1111l1_opy_()
                if webdriver is None:
                    self.logger.debug(bstack111l11_opy_ (u"ࠢࡘࡧࡥࡈࡷ࡯ࡶࡦࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥ࡯ࡳࠡࡐࡲࡲࡪࠦࠨࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࠣࡩࡽࡶࡩࡳࡧࡧ࠭ࠧ፜"))
                    continue
                session = req.automation_sessions.add()
                session.provider = (
                    bstack111l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠢ፝")
                    if bstack1llll1ll111_opy_.bstack1llllll1111_opy_(driver, bstack1llll1ll111_opy_.bstack1l11lll1l11_opy_, False)
                    else bstack111l11_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠣ፞")
                )
                session.ref = driver.ref()
                session.hub_url = bstack1llll1ll111_opy_.bstack1llllll1111_opy_(driver, bstack1llll1ll111_opy_.bstack1l1l1ll1ll1_opy_, bstack111l11_opy_ (u"ࠥࠦ፟"))
                session.framework_name = driver.framework_name
                session.framework_version = driver.framework_version
                session.framework_session_id = bstack1llll1ll111_opy_.bstack1llllll1111_opy_(driver, bstack1llll1ll111_opy_.bstack1l1l1l1llll_opy_, bstack111l11_opy_ (u"ࠦࠧ፠"))
                caps = None
                if hasattr(webdriver, bstack111l11_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ፡")):
                    try:
                        caps = webdriver.capabilities
                        self.logger.debug(bstack111l11_opy_ (u"ࠨࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡥ࡫ࡵࡩࡨࡺ࡬ࡺࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠮ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨ።"))
                    except Exception as e:
                        self.logger.debug(bstack111l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡺࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡳࡱࡰࠤࡩࡸࡩࡷࡧࡵ࠲ࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠽ࠤࠧ፣") + str(e) + bstack111l11_opy_ (u"ࠣࠤ፤"))
                try:
                    bstack1l11lll1l1l_opy_ = json.dumps(caps).encode(bstack111l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ፥")) if caps else bstack1l11lllll11_opy_ (u"ࠥࡿࢂࠨ፦")
                    req.capabilities = bstack1l11lll1l1l_opy_
                except Exception as e:
                    self.logger.debug(bstack111l11_opy_ (u"ࠦ࡬࡫ࡴࡠࡥࡥࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡲࡩࠦࡳࡦࡴ࡬ࡥࡱ࡯ࡺࡦࠢࡦࡥࡵࡹࠠࡧࡱࡵࠤࡷ࡫ࡱࡶࡧࡶࡸ࠿ࠦࠢ፧") + str(e) + bstack111l11_opy_ (u"ࠧࠨ፨"))
            except Exception as e:
                self.logger.error(bstack111l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡸࡪࡳ࠺ࠡࠤ፩") + str(str(e)) + bstack111l11_opy_ (u"ࠢࠣ፪"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l1l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11111l1_opy_,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs
    ):
        bstack1ll1111l11l_opy_ = f.bstack1llllll1111_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1llll111l_opy_, [])
        if not bstack1ll1111llll_opy_() and len(bstack1ll1111l11l_opy_) == 0:
            bstack1ll1111l11l_opy_ = f.bstack1llllll1111_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l11lll1l_opy_, [])
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack111l11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ፫") + str(kwargs) + bstack111l11_opy_ (u"ࠤࠥ፬"))
            return {}
        if len(bstack1ll1111l11l_opy_) > 1:
            self.logger.debug(bstack111l11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨ፭") + str(kwargs) + bstack111l11_opy_ (u"ࠦࠧ፮"))
            return {}
        bstack1l1ll1111l1_opy_, bstack1l1ll1111ll_opy_ = bstack1ll1111l11l_opy_[0]
        driver = bstack1l1ll1111l1_opy_()
        if not driver:
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ፯") + str(kwargs) + bstack111l11_opy_ (u"ࠨࠢ፰"))
            return {}
        capabilities = f.bstack1llllll1111_opy_(bstack1l1ll1111ll_opy_, bstack1llll1ll111_opy_.bstack1l1l1lllll1_opy_)
        if not capabilities:
            self.logger.debug(bstack111l11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ፱") + str(kwargs) + bstack111l11_opy_ (u"ࠣࠤ፲"))
            return {}
        return capabilities.get(bstack111l11_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢ፳"), {})
    def bstack1ll11llllll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11111l1_opy_,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs
    ):
        bstack1ll1111l11l_opy_ = f.bstack1llllll1111_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1llll111l_opy_, [])
        if not bstack1ll1111llll_opy_() and len(bstack1ll1111l11l_opy_) == 0:
            bstack1ll1111l11l_opy_ = f.bstack1llllll1111_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l11lll1l_opy_, [])
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack111l11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨ፴") + str(kwargs) + bstack111l11_opy_ (u"ࠦࠧ፵"))
            return
        if len(bstack1ll1111l11l_opy_) > 1:
            self.logger.debug(bstack111l11_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ፶") + str(kwargs) + bstack111l11_opy_ (u"ࠨࠢ፷"))
        bstack1l1ll1111l1_opy_, bstack1l1ll1111ll_opy_ = bstack1ll1111l11l_opy_[0]
        driver = bstack1l1ll1111l1_opy_()
        if not driver:
            self.logger.debug(bstack111l11_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ፸") + str(kwargs) + bstack111l11_opy_ (u"ࠣࠤ፹"))
            return
        return driver