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
from browserstack_sdk.sdk_cli.bstack1llll11l1ll_opy_ import bstack1llll1ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import (
    bstack1llllll1l11_opy_,
    bstack11111ll1l1_opy_,
    bstack1llllll11ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll1l11l1_opy_ import bstack1lll111llll_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll11l1ll_opy_ import bstack1llll1ll1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1llll1l1l1l_opy_(bstack1llll1ll1l1_opy_):
    bstack1ll11lll1l1_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1lll111llll_opy_.bstack1ll1ll11111_opy_((bstack1llllll1l11_opy_.bstack11111l111l_opy_, bstack11111ll1l1_opy_.PRE), self.bstack1ll11l1l111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11l1l111_opy_(
        self,
        f: bstack1lll111llll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll11l1111l_opy_(hub_url):
            if not bstack1llll1l1l1l_opy_.bstack1ll11lll1l1_opy_:
                self.logger.warning(bstack11l1lll_opy_ (u"ࠦࡱࡵࡣࡢ࡮ࠣࡷࡪࡲࡦ࠮ࡪࡨࡥࡱࠦࡦ࡭ࡱࡺࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢ࡬ࡲ࡫ࡸࡡࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧᆙ") + str(hub_url) + bstack11l1lll_opy_ (u"ࠧࠨᆚ"))
                bstack1llll1l1l1l_opy_.bstack1ll11lll1l1_opy_ = True
            return
        bstack1ll11llllll_opy_ = f.bstack1ll11ll111l_opy_(*args)
        bstack1ll11l1l1l1_opy_ = f.bstack1ll11l111ll_opy_(*args)
        if bstack1ll11llllll_opy_ and bstack1ll11llllll_opy_.lower() == bstack11l1lll_opy_ (u"ࠨࡦࡪࡰࡧࡩࡱ࡫࡭ࡦࡰࡷࠦᆛ") and bstack1ll11l1l1l1_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll11l1l1l1_opy_.get(bstack11l1lll_opy_ (u"ࠢࡶࡵ࡬ࡲ࡬ࠨᆜ"), None), bstack1ll11l1l1l1_opy_.get(bstack11l1lll_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᆝ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack11l1lll_opy_ (u"ࠤࡾࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦࡿ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡵࡲࠡࡣࡵ࡫ࡸ࠴ࡵࡴ࡫ࡱ࡫ࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡷࡣ࡯ࡹࡪࡃࠢᆞ") + str(locator_value) + bstack11l1lll_opy_ (u"ࠥࠦᆟ"))
                return
            def bstack1llllll1l1l_opy_(driver, bstack1ll11l11lll_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll11l11lll_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll11l11ll1_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack11l1lll_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࠢᆠ") + str(locator_value) + bstack11l1lll_opy_ (u"ࠧࠨᆡ"))
                    else:
                        self.logger.warning(bstack11l1lll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹ࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤᆢ") + str(response) + bstack11l1lll_opy_ (u"ࠢࠣᆣ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll11l11l1l_opy_(
                        driver, bstack1ll11l11lll_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1llllll1l1l_opy_.__name__ = bstack1ll11llllll_opy_
            return bstack1llllll1l1l_opy_
    def __1ll11l11l1l_opy_(
        self,
        driver,
        bstack1ll11l11lll_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll11l11ll1_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack11l1lll_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡸࡷ࡯ࡧࡨࡧࡵࡩࡩࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣᆤ") + str(locator_value) + bstack11l1lll_opy_ (u"ࠤࠥᆥ"))
                bstack1ll11l11l11_opy_ = self.bstack1ll11l1l11l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack11l1lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡪࡨࡥࡱ࡯࡮ࡨࡡࡵࡩࡸࡻ࡬ࡵ࠿ࠥᆦ") + str(bstack1ll11l11l11_opy_) + bstack11l1lll_opy_ (u"ࠦࠧᆧ"))
                if bstack1ll11l11l11_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack11l1lll_opy_ (u"ࠧࡻࡳࡪࡰࡪࠦᆨ"): bstack1ll11l11l11_opy_.locator_type,
                            bstack11l1lll_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᆩ"): bstack1ll11l11l11_opy_.locator_value,
                        }
                    )
                    return bstack1ll11l11lll_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack11l1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡊࡡࡇࡉࡇ࡛ࡇࠣᆪ"), False):
                    self.logger.info(bstack1lll11ll111_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠰ࡱ࡮ࡹࡳࡪࡰࡪ࠾ࠥࡹ࡬ࡦࡧࡳࠬ࠸࠶ࠩࠡ࡮ࡨࡸࡹ࡯࡮ࡨࠢࡼࡳࡺࠦࡩ࡯ࡵࡳࡩࡨࡺࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࡸࠨᆫ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack11l1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰ࡲࡴ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࡁࠧᆬ") + str(response) + bstack11l1lll_opy_ (u"ࠥࠦᆭ"))
        except Exception as err:
            self.logger.warning(bstack11l1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠࡦࡴࡵࡳࡷࡀࠠࠣᆮ") + str(err) + bstack11l1lll_opy_ (u"ࠧࠨᆯ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll11l111l1_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def bstack1ll11l11ll1_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack11l1lll_opy_ (u"ࠨ࠰ࠣᆰ"),
    ):
        self.bstack1ll1l11ll11_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack11l1lll_opy_ (u"ࠢࠣᆱ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1llll111ll1_opy_.AISelfHealStep(req)
            self.logger.info(bstack11l1lll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᆲ") + str(r) + bstack11l1lll_opy_ (u"ࠤࠥᆳ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᆴ") + str(e) + bstack11l1lll_opy_ (u"ࠦࠧᆵ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11l11111_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def bstack1ll11l1l11l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack11l1lll_opy_ (u"ࠧ࠶ࠢᆶ")):
        self.bstack1ll1l11ll11_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1llll111ll1_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack11l1lll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᆷ") + str(r) + bstack11l1lll_opy_ (u"ࠢࠣᆸ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1lll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᆹ") + str(e) + bstack11l1lll_opy_ (u"ࠤࠥᆺ"))
            traceback.print_exc()
            raise e