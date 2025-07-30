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
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack111111l11l_opy_ import (
    bstack1llllll1l1l_opy_,
    bstack111111l1l1_opy_,
    bstack1lllllll1l1_opy_,
    bstack11111111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll111llll_opy_ import bstack1llll1ll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_, bstack1lll11111l1_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11l1111_opy_ import bstack1lll11l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1lll11_opy_ import bstack1ll1ll1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import bstack1llll11l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1l11l_opy_ import bstack1lll111ll1l_opy_
from bstack_utils.helper import bstack1ll1l1l1l11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11l11111l_opy_ import bstack1ll1ll1ll11_opy_
import grpc
import traceback
import json
class bstack1llll1ll1ll_opy_(bstack1lll11l1lll_opy_):
    bstack1ll11ll111l_opy_ = False
    bstack1ll1l1l1ll1_opy_ = bstack111l11_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸࠢᄒ")
    bstack1ll1l1ll11l_opy_ = bstack111l11_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧ࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࠨᄓ")
    bstack1ll11lll1ll_opy_ = bstack111l11_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣ࡮ࡴࡩࡵࠤᄔ")
    bstack1ll1l11l111_opy_ = bstack111l11_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤ࡯ࡳࡠࡵࡦࡥࡳࡴࡩ࡯ࡩࠥᄕ")
    bstack1ll11llll1l_opy_ = bstack111l11_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡥࡨࡢࡵࡢࡹࡷࡲࠢᄖ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1lll1l11ll1_opy_, bstack1lll1l1l1ll_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        if not self.is_enabled():
            return
        self.bstack1ll11lllll1_opy_ = bstack1lll1l1l1ll_opy_
        bstack1lll1l11ll1_opy_.bstack1ll11ll11ll_opy_((bstack1llllll1l1l_opy_.bstack111111111l_opy_, bstack111111l1l1_opy_.PRE), self.bstack1ll11lll1l1_opy_)
        TestFramework.bstack1ll11ll11ll_opy_((bstack1lll1l111ll_opy_.TEST, bstack1llll1lll1l_opy_.PRE), self.bstack1ll1l1lll11_opy_)
        TestFramework.bstack1ll11ll11ll_opy_((bstack1lll1l111ll_opy_.TEST, bstack1llll1lll1l_opy_.POST), self.bstack1ll1l1lll1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1l1lll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11111l1_opy_,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll11l1lll1_opy_(instance, args)
        test_framework = f.bstack1llllll1111_opy_(instance, TestFramework.bstack1ll11ll1lll_opy_)
        if bstack111l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᄗ") in instance.bstack1ll1l1l11l1_opy_:
            platform_index = f.bstack1llllll1111_opy_(instance, TestFramework.bstack1ll1l111lll_opy_)
            self.accessibility = self.bstack1ll1ll11111_opy_(tags, self.config[bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᄘ")][platform_index])
        else:
            capabilities = self.bstack1ll11lllll1_opy_.bstack1ll1l1l11ll_opy_(f, instance, bstack11111l1ll1_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack111l11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᄙ") + str(kwargs) + bstack111l11_opy_ (u"ࠥࠦᄚ"))
                return
            self.accessibility = self.bstack1ll1ll11111_opy_(tags, capabilities)
        if self.bstack1ll11lllll1_opy_.pages and self.bstack1ll11lllll1_opy_.pages.values():
            bstack1ll1l11llll_opy_ = list(self.bstack1ll11lllll1_opy_.pages.values())
            if bstack1ll1l11llll_opy_ and isinstance(bstack1ll1l11llll_opy_[0], (list, tuple)) and bstack1ll1l11llll_opy_[0]:
                bstack1ll1l111ll1_opy_ = bstack1ll1l11llll_opy_[0][0]
                if callable(bstack1ll1l111ll1_opy_):
                    page = bstack1ll1l111ll1_opy_()
                    def bstack1111l11ll_opy_():
                        self.get_accessibility_results(page, bstack111l11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᄛ"))
                    def bstack1ll1ll1111l_opy_():
                        self.get_accessibility_results_summary(page, bstack111l11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᄜ"))
                    setattr(page, bstack111l11_opy_ (u"ࠨࡧࡦࡶࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡔࡨࡷࡺࡲࡴࡴࠤᄝ"), bstack1111l11ll_opy_)
                    setattr(page, bstack111l11_opy_ (u"ࠢࡨࡧࡷࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡕࡩࡸࡻ࡬ࡵࡕࡸࡱࡲࡧࡲࡺࠤᄞ"), bstack1ll1ll1111l_opy_)
        self.logger.debug(bstack111l11_opy_ (u"ࠣࡵ࡫ࡳࡺࡲࡤࠡࡴࡸࡲࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡼࡡ࡭ࡷࡨࡁࠧᄟ") + str(self.accessibility) + bstack111l11_opy_ (u"ࠤࠥᄠ"))
    def bstack1ll11lll1l1_opy_(
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
            bstack111l1l111_opy_ = datetime.now()
            self.bstack1ll1l1l111l_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻࡫ࡱ࡭ࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡣࡰࡰࡩ࡭࡬ࠨᄡ"), datetime.now() - bstack111l1l111_opy_)
            if (
                not f.bstack1ll1l11lll1_opy_(method_name)
                or f.bstack1ll1l11l1l1_opy_(method_name, *args)
                or f.bstack1ll11l1l1ll_opy_(method_name, *args)
            ):
                return
            if not f.bstack1llllll1111_opy_(instance, bstack1llll1ll1ll_opy_.bstack1ll11lll1ll_opy_, False):
                if not bstack1llll1ll1ll_opy_.bstack1ll11ll111l_opy_:
                    self.logger.warning(bstack111l11_opy_ (u"ࠦࡠࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢᄢ") + str(f.platform_index) + bstack111l11_opy_ (u"ࠧࡣࠠࡢ࠳࠴ࡽࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡭ࡧࡶࡦࠢࡱࡳࡹࠦࡢࡦࡧࡱࠤࡸ࡫ࡴࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡷࡪࡹࡳࡪࡱࡱࠦᄣ"))
                    bstack1llll1ll1ll_opy_.bstack1ll11ll111l_opy_ = True
                return
            bstack1ll1l1111ll_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll1l1111ll_opy_:
                platform_index = f.bstack1llllll1111_opy_(instance, bstack1llll1ll111_opy_.bstack1ll1l111lll_opy_, 0)
                self.logger.debug(bstack111l11_opy_ (u"ࠨ࡮ࡰࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࡻࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᄤ") + str(f.framework_name) + bstack111l11_opy_ (u"ࠢࠣᄥ"))
                return
            bstack1ll1l1ll1ll_opy_ = f.bstack1ll1l11111l_opy_(*args)
            if not bstack1ll1l1ll1ll_opy_:
                self.logger.debug(bstack111l11_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࠥᄦ") + str(method_name) + bstack111l11_opy_ (u"ࠤࠥᄧ"))
                return
            bstack1ll1l111l1l_opy_ = f.bstack1llllll1111_opy_(instance, bstack1llll1ll1ll_opy_.bstack1ll11llll1l_opy_, False)
            if bstack1ll1l1ll1ll_opy_ == bstack111l11_opy_ (u"ࠥ࡫ࡪࡺࠢᄨ") and not bstack1ll1l111l1l_opy_:
                f.bstack111111ll1l_opy_(instance, bstack1llll1ll1ll_opy_.bstack1ll11llll1l_opy_, True)
                bstack1ll1l111l1l_opy_ = True
            if not bstack1ll1l111l1l_opy_:
                self.logger.debug(bstack111l11_opy_ (u"ࠦࡳࡵࠠࡖࡔࡏࠤࡱࡵࡡࡥࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦ࠿ࠥᄩ") + str(bstack1ll1l1ll1ll_opy_) + bstack111l11_opy_ (u"ࠧࠨᄪ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1ll1l1ll1ll_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstack111l11_opy_ (u"ࠨ࡮ࡰࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࡀࠦᄫ") + str(bstack1ll1l1ll1ll_opy_) + bstack111l11_opy_ (u"ࠢࠣᄬ"))
                return
            self.logger.info(bstack111l11_opy_ (u"ࠣࡴࡸࡲࡳ࡯࡮ࡨࠢࡾࡰࡪࡴࠨࡴࡥࡵ࡭ࡵࡺࡳࡠࡶࡲࡣࡷࡻ࡮ࠪࡿࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦ࠿ࠥᄭ") + str(bstack1ll1l1ll1ll_opy_) + bstack111l11_opy_ (u"ࠤࠥᄮ"))
            scripts = [(s, bstack1ll1l1111ll_opy_[s]) for s in scripts_to_run if s in bstack1ll1l1111ll_opy_]
            for script_name, bstack1ll1l1ll111_opy_ in scripts:
                try:
                    bstack111l1l111_opy_ = datetime.now()
                    if script_name == bstack111l11_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᄯ"):
                        result = self.perform_scan(driver, method=bstack1ll1l1ll1ll_opy_, framework_name=f.framework_name)
                    instance.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࠥᄰ") + script_name, datetime.now() - bstack111l1l111_opy_)
                    if isinstance(result, dict) and not result.get(bstack111l11_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᄱ"), True):
                        self.logger.warning(bstack111l11_opy_ (u"ࠨࡳ࡬࡫ࡳࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡳࡧࡰࡥ࡮ࡴࡩ࡯ࡩࠣࡷࡨࡸࡩࡱࡶࡶ࠾ࠥࠨᄲ") + str(result) + bstack111l11_opy_ (u"ࠢࠣᄳ"))
                        break
                except Exception as e:
                    self.logger.error(bstack111l11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡷࡨࡸࡩࡱࡶࡀࡿࡸࡩࡲࡪࡲࡷࡣࡳࡧ࡭ࡦࡿࠣࡩࡷࡸ࡯ࡳ࠿ࠥᄴ") + str(e) + bstack111l11_opy_ (u"ࠤࠥᄵ"))
        except Exception as e:
            self.logger.error(bstack111l11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡦࡴࡵࡳࡷࡃࠢᄶ") + str(e) + bstack111l11_opy_ (u"ࠦࠧᄷ"))
    def bstack1ll1l1lll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11111l1_opy_,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll11l1lll1_opy_(instance, args)
        capabilities = self.bstack1ll11lllll1_opy_.bstack1ll1l1l11ll_opy_(f, instance, bstack11111l1ll1_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll1ll11111_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤᄸ"))
            return
        driver = self.bstack1ll11lllll1_opy_.bstack1ll11llllll_opy_(f, instance, bstack11111l1ll1_opy_, *args, **kwargs)
        test_name = f.bstack1llllll1111_opy_(instance, TestFramework.bstack1ll1l111l11_opy_)
        if not test_name:
            self.logger.debug(bstack111l11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦᄹ"))
            return
        test_uuid = f.bstack1llllll1111_opy_(instance, TestFramework.bstack1ll11lll11l_opy_)
        if not test_uuid:
            self.logger.debug(bstack111l11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧᄺ"))
            return
        if isinstance(self.bstack1ll11lllll1_opy_, bstack1llll11l1l1_opy_):
            framework_name = bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᄻ")
        else:
            framework_name = bstack111l11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᄼ")
        self.bstack1l1ll1ll1_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll1l11ll1l_opy_ = bstack1ll1ll1ll11_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack11l11ll1ll_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack111l11_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࠦᄽ"))
            return
        bstack111l1l111_opy_ = datetime.now()
        bstack1ll1l1ll111_opy_ = self.scripts.get(framework_name, {}).get(bstack111l11_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᄾ"), None)
        if not bstack1ll1l1ll111_opy_:
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡴࡥࡤࡲࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᄿ") + str(framework_name) + bstack111l11_opy_ (u"ࠨࠠࠣᅀ"))
            return
        instance = bstack1lllllll1l1_opy_.bstack11111ll111_opy_(driver)
        if instance:
            if not bstack1lllllll1l1_opy_.bstack1llllll1111_opy_(instance, bstack1llll1ll1ll_opy_.bstack1ll1l11l111_opy_, False):
                bstack1lllllll1l1_opy_.bstack111111ll1l_opy_(instance, bstack1llll1ll1ll_opy_.bstack1ll1l11l111_opy_, True)
            else:
                self.logger.info(bstack111l11_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡱࠤࡵࡸ࡯ࡨࡴࡨࡷࡸࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡱࡪࡺࡨࡰࡦࡀࠦᅁ") + str(method) + bstack111l11_opy_ (u"ࠣࠤᅂ"))
                return
        self.logger.info(bstack111l11_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡃࠢᅃ") + str(method) + bstack111l11_opy_ (u"ࠥࠦᅄ"))
        if framework_name == bstack111l11_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᅅ"):
            result = self.bstack1ll11lllll1_opy_.bstack1ll1l11l11l_opy_(driver, bstack1ll1l1ll111_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l1ll111_opy_, {bstack111l11_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᅆ"): method if method else bstack111l11_opy_ (u"ࠨࠢᅇ")})
        bstack1ll1ll1ll11_opy_.end(EVENTS.bstack11l11ll1ll_opy_.value, bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᅈ"), bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᅉ"), True, None, command=method)
        if instance:
            bstack1lllllll1l1_opy_.bstack111111ll1l_opy_(instance, bstack1llll1ll1ll_opy_.bstack1ll1l11l111_opy_, False)
            instance.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࠨᅊ"), datetime.now() - bstack111l1l111_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll11111l_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack111l11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧᅋ"))
            return
        bstack1ll1l1ll111_opy_ = self.scripts.get(framework_name, {}).get(bstack111l11_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣᅌ"), None)
        if not bstack1ll1l1ll111_opy_:
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᅍ") + str(framework_name) + bstack111l11_opy_ (u"ࠨࠢᅎ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack111l1l111_opy_ = datetime.now()
        if framework_name == bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᅏ"):
            result = self.bstack1ll11lllll1_opy_.bstack1ll1l11l11l_opy_(driver, bstack1ll1l1ll111_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l1ll111_opy_)
        instance = bstack1lllllll1l1_opy_.bstack11111ll111_opy_(driver)
        if instance:
            instance.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࠦᅐ"), datetime.now() - bstack111l1l111_opy_)
        return result
    @measure(event_name=EVENTS.bstack11ll1ll1_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack111l11_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧᅑ"))
            return
        bstack1ll1l1ll111_opy_ = self.scripts.get(framework_name, {}).get(bstack111l11_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢᅒ"), None)
        if not bstack1ll1l1ll111_opy_:
            self.logger.debug(bstack111l11_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᅓ") + str(framework_name) + bstack111l11_opy_ (u"ࠧࠨᅔ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack111l1l111_opy_ = datetime.now()
        if framework_name == bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᅕ"):
            result = self.bstack1ll11lllll1_opy_.bstack1ll1l11l11l_opy_(driver, bstack1ll1l1ll111_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l1ll111_opy_)
        instance = bstack1lllllll1l1_opy_.bstack11111ll111_opy_(driver)
        if instance:
            instance.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࡢࡷࡺࡳ࡭ࡢࡴࡼࠦᅖ"), datetime.now() - bstack111l1l111_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1l1lllll_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
    def bstack1ll1ll111l1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll1l1l1l1l_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1lll111lll1_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack111l11_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᅗ") + str(r) + bstack111l11_opy_ (u"ࠤࠥᅘ"))
            else:
                self.bstack1ll11ll1111_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᅙ") + str(e) + bstack111l11_opy_ (u"ࠦࠧᅚ"))
            traceback.print_exc()
            raise e
    def bstack1ll11ll1111_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡲ࡯ࡢࡦࡢࡧࡴࡴࡦࡪࡩ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧᅛ"))
            return False
        if result.accessibility.options:
            options = result.accessibility.options
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll11lll111_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll1l1l1ll1_opy_ and command.module == self.bstack1ll1l1ll11l_opy_:
                        if command.method and not command.method in bstack1ll11lll111_opy_:
                            bstack1ll11lll111_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll11lll111_opy_[command.method]:
                            bstack1ll11lll111_opy_[command.method][command.name] = list()
                        bstack1ll11lll111_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll11lll111_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll1l1l111l_opy_(
        self,
        f: bstack1llll1ll111_opy_,
        exec: Tuple[bstack11111111ll_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll11lllll1_opy_, bstack1llll11l1l1_opy_) and method_name != bstack111l11_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࠧᅜ"):
            return
        if bstack1lllllll1l1_opy_.bstack11111ll11l_opy_(instance, bstack1llll1ll1ll_opy_.bstack1ll11lll1ll_opy_):
            return
        if f.bstack1ll11ll1l1l_opy_(method_name, *args):
            bstack1ll1l1l1lll_opy_ = False
            desired_capabilities = f.bstack1ll11ll1l11_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll11ll1ll1_opy_(instance)
                platform_index = f.bstack1llllll1111_opy_(instance, bstack1llll1ll111_opy_.bstack1ll1l111lll_opy_, 0)
                bstack1ll1l1111l1_opy_ = datetime.now()
                r = self.bstack1ll1ll111l1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡩ࡯࡯ࡨ࡬࡫ࠧᅝ"), datetime.now() - bstack1ll1l1111l1_opy_)
                bstack1ll1l1l1lll_opy_ = r.success
            else:
                self.logger.error(bstack111l11_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡧࡩࡸ࡯ࡲࡦࡦࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠿ࠥᅞ") + str(desired_capabilities) + bstack111l11_opy_ (u"ࠤࠥᅟ"))
            f.bstack111111ll1l_opy_(instance, bstack1llll1ll1ll_opy_.bstack1ll11lll1ll_opy_, bstack1ll1l1l1lll_opy_)
    def bstack1lllll1111_opy_(self, test_tags):
        bstack1ll1ll111l1_opy_ = self.config.get(bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᅠ"))
        if not bstack1ll1ll111l1_opy_:
            return True
        try:
            include_tags = bstack1ll1ll111l1_opy_[bstack111l11_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᅡ")] if bstack111l11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᅢ") in bstack1ll1ll111l1_opy_ and isinstance(bstack1ll1ll111l1_opy_[bstack111l11_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᅣ")], list) else []
            exclude_tags = bstack1ll1ll111l1_opy_[bstack111l11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᅤ")] if bstack111l11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᅥ") in bstack1ll1ll111l1_opy_ and isinstance(bstack1ll1ll111l1_opy_[bstack111l11_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᅦ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack111l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥᅧ") + str(error))
        return False
    def bstack1l1111lll1_opy_(self, caps):
        try:
            bstack1ll1l111111_opy_ = caps.get(bstack111l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᅨ"), {}).get(bstack111l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᅩ"), caps.get(bstack111l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ᅪ"), bstack111l11_opy_ (u"ࠧࠨᅫ")))
            if bstack1ll1l111111_opy_:
                self.logger.warning(bstack111l11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡆࡨࡷࡰࡺ࡯ࡱࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧᅬ"))
                return False
            browser = caps.get(bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᅭ"), bstack111l11_opy_ (u"ࠪࠫᅮ")).lower()
            if browser != bstack111l11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᅯ"):
                self.logger.warning(bstack111l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᅰ"))
                return False
            bstack1ll1l1llll1_opy_ = bstack1ll1l11ll11_opy_
            if not self.config.get(bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᅱ")) or self.config.get(bstack111l11_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫᅲ")):
                bstack1ll1l1llll1_opy_ = bstack1ll1l1l1111_opy_
            browser_version = caps.get(bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᅳ"))
            if not browser_version:
                browser_version = caps.get(bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᅴ"), {}).get(bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᅵ"), bstack111l11_opy_ (u"ࠫࠬᅶ"))
            if browser_version and browser_version != bstack111l11_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬᅷ") and int(browser_version.split(bstack111l11_opy_ (u"࠭࠮ࠨᅸ"))[0]) <= bstack1ll1l1llll1_opy_:
                self.logger.warning(bstack111l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡࠤᅹ") + str(bstack1ll1l1llll1_opy_) + bstack111l11_opy_ (u"ࠣ࠰ࠥᅺ"))
                return False
            bstack1ll11l1llll_opy_ = caps.get(bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᅻ"), {}).get(bstack111l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᅼ"))
            if not bstack1ll11l1llll_opy_:
                bstack1ll11l1llll_opy_ = caps.get(bstack111l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᅽ"), {})
            if bstack1ll11l1llll_opy_ and bstack111l11_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩᅾ") in bstack1ll11l1llll_opy_.get(bstack111l11_opy_ (u"࠭ࡡࡳࡩࡶࠫᅿ"), []):
                self.logger.warning(bstack111l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤᆀ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack111l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥᆁ") + str(error))
            return False
    def bstack1ll1ll111ll_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1ll1l1ll1l1_opy_ = {
            bstack111l11_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩᆂ"): test_uuid,
        }
        bstack1ll11l1ll1l_opy_ = {}
        if result.success:
            bstack1ll11l1ll1l_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll1l1l1l11_opy_(bstack1ll1l1ll1l1_opy_, bstack1ll11l1ll1l_opy_)
    def bstack1l1ll1ll1_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll1l11ll1l_opy_ = None
        try:
            self.bstack1ll1l1l1l1l_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack111l11_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥᆃ")
            req.script_name = bstack111l11_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤᆄ")
            r = self.bstack1lll111lll1_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack111l11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡥࡴ࡬ࡺࡪࡸࠠࡦࡺࡨࡧࡺࡺࡥࠡࡲࡤࡶࡦࡳࡳࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᆅ") + str(r.error) + bstack111l11_opy_ (u"ࠨࠢᆆ"))
            else:
                bstack1ll1l1ll1l1_opy_ = self.bstack1ll1ll111ll_opy_(test_uuid, r)
                bstack1ll1l1ll111_opy_ = r.script
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪᆇ") + str(bstack1ll1l1ll1l1_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll1l1ll111_opy_:
                self.logger.debug(bstack111l11_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᆈ") + str(framework_name) + bstack111l11_opy_ (u"ࠤࠣࠦᆉ"))
                return
            bstack1ll1l11ll1l_opy_ = bstack1ll1ll1ll11_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack1ll1l11l1ll_opy_.value)
            self.bstack1ll11l1ll11_opy_(driver, bstack1ll1l1ll111_opy_, bstack1ll1l1ll1l1_opy_, framework_name)
            self.logger.info(bstack111l11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨᆊ"))
            bstack1ll1ll1ll11_opy_.end(EVENTS.bstack1ll1l11l1ll_opy_.value, bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᆋ"), bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᆌ"), True, None, command=bstack111l11_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫᆍ"),test_name=name)
        except Exception as bstack1ll11llll11_opy_:
            self.logger.error(bstack111l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᆎ") + bstack111l11_opy_ (u"ࠣࡵࡷࡶ࠭ࡶࡡࡵࡪࠬࠦᆏ") + bstack111l11_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦᆐ") + str(bstack1ll11llll11_opy_))
            bstack1ll1ll1ll11_opy_.end(EVENTS.bstack1ll1l11l1ll_opy_.value, bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᆑ"), bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᆒ"), False, bstack1ll11llll11_opy_, command=bstack111l11_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᆓ"),test_name=name)
    def bstack1ll11l1ll11_opy_(self, driver, bstack1ll1l1ll111_opy_, bstack1ll1l1ll1l1_opy_, framework_name):
        if framework_name == bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᆔ"):
            self.bstack1ll11lllll1_opy_.bstack1ll1l11l11l_opy_(driver, bstack1ll1l1ll111_opy_, bstack1ll1l1ll1l1_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll1l1ll111_opy_, bstack1ll1l1ll1l1_opy_))
    def _1ll11l1lll1_opy_(self, instance: bstack1lll11111l1_opy_, args: Tuple) -> list:
        bstack111l11_opy_ (u"ࠢࠣࠤࡈࡼࡹࡸࡡࡤࡶࠣࡸࡦ࡭ࡳࠡࡤࡤࡷࡪࡪࠠࡰࡰࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࠤࠥࠦᆕ")
        if bstack111l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᆖ") in instance.bstack1ll1l1l11l1_opy_:
            return args[2].tags if hasattr(args[2], bstack111l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᆗ")) else []
        if hasattr(args[0], bstack111l11_opy_ (u"ࠪࡳࡼࡴ࡟࡮ࡣࡵ࡯ࡪࡸࡳࠨᆘ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll1ll11111_opy_(self, tags, capabilities):
        return self.bstack1lllll1111_opy_(tags) and self.bstack1l1111lll1_opy_(capabilities)