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
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll11l1111_opy_ import bstack1lll11l1lll_opy_
from browserstack_sdk.sdk_cli.bstack111111l11l_opy_ import (
    bstack1llllll1l1l_opy_,
    bstack111111l1l1_opy_,
    bstack11111111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll111llll_opy_ import bstack1llll1ll111_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1lll1llll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack11l11111l_opy_ import bstack1ll1ll1ll11_opy_
class bstack1lll11ll1ll_opy_(bstack1lll11l1lll_opy_):
    bstack1l1l111111l_opy_ = bstack111l11_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶࠥዓ")
    bstack1l1l111l111_opy_ = bstack111l11_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸࠧዔ")
    bstack1l1l1111lll_opy_ = bstack111l11_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡲࡴࠧዕ")
    def __init__(self, bstack1lll11llll1_opy_):
        super().__init__()
        bstack1llll1ll111_opy_.bstack1ll11ll11ll_opy_((bstack1llllll1l1l_opy_.bstack1lllllll1ll_opy_, bstack111111l1l1_opy_.PRE), self.bstack1l1l11ll11l_opy_)
        bstack1llll1ll111_opy_.bstack1ll11ll11ll_opy_((bstack1llllll1l1l_opy_.bstack111111111l_opy_, bstack111111l1l1_opy_.PRE), self.bstack1ll11l1l1l1_opy_)
        bstack1llll1ll111_opy_.bstack1ll11ll11ll_opy_((bstack1llllll1l1l_opy_.bstack111111111l_opy_, bstack111111l1l1_opy_.POST), self.bstack1l1l11l1l1l_opy_)
        bstack1llll1ll111_opy_.bstack1ll11ll11ll_opy_((bstack1llllll1l1l_opy_.bstack111111111l_opy_, bstack111111l1l1_opy_.POST), self.bstack1l1l11l1111_opy_)
        bstack1llll1ll111_opy_.bstack1ll11ll11ll_opy_((bstack1llllll1l1l_opy_.QUIT, bstack111111l1l1_opy_.POST), self.bstack1l1l11l1l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11ll11l_opy_(
        self,
        f: bstack1llll1ll111_opy_,
        driver: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l11_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣዖ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack111l11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥ዗")), str):
                    url = kwargs.get(bstack111l11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦዘ"))
                else:
                    url = kwargs.get(bstack111l11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧዙ"))._client_config.remote_server_addr
            except Exception as e:
                url = bstack111l11_opy_ (u"ࠪࠫዚ")
                self.logger.error(bstack111l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡹࡷࡲࠠࡧࡴࡲࡱࠥࡪࡲࡪࡸࡨࡶ࠿ࠦࡻࡾࠤዛ").format(e))
            self.bstack1l1l111l11l_opy_(instance, url, f, kwargs)
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠳ࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࡻࡧ࠰ࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࢀ࠾ࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦዜ") + str(kwargs) + bstack111l11_opy_ (u"ࠨࠢዝ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll11l1l1l1_opy_(
        self,
        f: bstack1llll1ll111_opy_,
        driver: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1llllll1111_opy_(instance, bstack1lll11ll1ll_opy_.bstack1l1l111111l_opy_, False):
            return
        if not f.bstack11111ll11l_opy_(instance, bstack1llll1ll111_opy_.bstack1ll1l111lll_opy_):
            return
        platform_index = f.bstack1llllll1111_opy_(instance, bstack1llll1ll111_opy_.bstack1ll1l111lll_opy_)
        if f.bstack1ll11ll1l1l_opy_(method_name, *args) and len(args) > 1:
            bstack111l1l111_opy_ = datetime.now()
            hub_url = bstack1llll1ll111_opy_.hub_url(driver)
            self.logger.warning(bstack111l11_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬࠾ࠤዞ") + str(hub_url) + bstack111l11_opy_ (u"ࠣࠤዟ"))
            bstack1l1l11111ll_opy_ = args[1][bstack111l11_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣዠ")] if isinstance(args[1], dict) and bstack111l11_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤዡ") in args[1] else None
            bstack1l1l111l1l1_opy_ = bstack111l11_opy_ (u"ࠦࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠤዢ")
            if isinstance(bstack1l1l11111ll_opy_, dict):
                bstack111l1l111_opy_ = datetime.now()
                r = self.bstack1l1l111ll1l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶࠥዣ"), datetime.now() - bstack111l1l111_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack111l11_opy_ (u"ࠨࡳࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࡀࠠࠣዤ") + str(r) + bstack111l11_opy_ (u"ࠢࠣዥ"))
                        return
                    if r.hub_url:
                        f.bstack1l1l11ll111_opy_(instance, driver, r.hub_url)
                        f.bstack111111ll1l_opy_(instance, bstack1lll11ll1ll_opy_.bstack1l1l111111l_opy_, True)
                except Exception as e:
                    self.logger.error(bstack111l11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢዦ"), e)
    def bstack1l1l11l1l1l_opy_(
        self,
        f: bstack1llll1ll111_opy_,
        driver: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1llll1ll111_opy_.session_id(driver)
            if session_id:
                bstack1l1l111ll11_opy_ = bstack111l11_opy_ (u"ࠤࡾࢁ࠿ࡹࡴࡢࡴࡷࠦዧ").format(session_id)
                bstack1ll1ll1ll11_opy_.mark(bstack1l1l111ll11_opy_)
    def bstack1l1l11l1111_opy_(
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
        if f.bstack1llllll1111_opy_(instance, bstack1lll11ll1ll_opy_.bstack1l1l111l111_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1llll1ll111_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack111l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡮ࡵࡣࡡࡸࡶࡱࡃࠢየ") + str(hub_url) + bstack111l11_opy_ (u"ࠦࠧዩ"))
            return
        framework_session_id = bstack1llll1ll111_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack111l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣዪ") + str(framework_session_id) + bstack111l11_opy_ (u"ࠨࠢያ"))
            return
        if bstack1llll1ll111_opy_.bstack1l1l111lll1_opy_(*args) == bstack1llll1ll111_opy_.bstack1l1l11l11l1_opy_:
            bstack1l1l11l11ll_opy_ = bstack111l11_opy_ (u"ࠢࡼࡿ࠽ࡩࡳࡪࠢዬ").format(framework_session_id)
            bstack1l1l111ll11_opy_ = bstack111l11_opy_ (u"ࠣࡽࢀ࠾ࡸࡺࡡࡳࡶࠥይ").format(framework_session_id)
            bstack1ll1ll1ll11_opy_.end(
                label=bstack111l11_opy_ (u"ࠤࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡰࡵࡷ࠱࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠧዮ"),
                start=bstack1l1l111ll11_opy_,
                end=bstack1l1l11l11ll_opy_,
                status=True,
                failure=None
            )
            bstack111l1l111_opy_ = datetime.now()
            r = self.bstack1l1l1111111_opy_(
                ref,
                f.bstack1llllll1111_opy_(instance, bstack1llll1ll111_opy_.bstack1ll1l111lll_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵࠤዯ"), datetime.now() - bstack111l1l111_opy_)
            f.bstack111111ll1l_opy_(instance, bstack1lll11ll1ll_opy_.bstack1l1l111l111_opy_, r.success)
    def bstack1l1l11l1l11_opy_(
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
        if f.bstack1llllll1111_opy_(instance, bstack1lll11ll1ll_opy_.bstack1l1l1111lll_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1llll1ll111_opy_.session_id(driver)
        hub_url = bstack1llll1ll111_opy_.hub_url(driver)
        bstack111l1l111_opy_ = datetime.now()
        r = self.bstack1l1l1111ll1_opy_(
            ref,
            f.bstack1llllll1111_opy_(instance, bstack1llll1ll111_opy_.bstack1ll1l111lll_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱࠤደ"), datetime.now() - bstack111l1l111_opy_)
        f.bstack111111ll1l_opy_(instance, bstack1lll11ll1ll_opy_.bstack1l1l1111lll_opy_, r.success)
    @measure(event_name=EVENTS.bstack1l1l1ll1l1_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
    def bstack1l1l1lll1l1_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack111l11_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࠥዱ") + str(req) + bstack111l11_opy_ (u"ࠨࠢዲ"))
        try:
            r = self.bstack1lll111lll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack111l11_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥዳ") + str(r.success) + bstack111l11_opy_ (u"ࠣࠤዴ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢድ") + str(e) + bstack111l11_opy_ (u"ࠥࠦዶ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1111l1l_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
    def bstack1l1l111ll1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll1l1l1l1l_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack111l11_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥࠨዷ") + str(req) + bstack111l11_opy_ (u"ࠧࠨዸ"))
        try:
            r = self.bstack1lll111lll1_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack111l11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤዹ") + str(r.success) + bstack111l11_opy_ (u"ࠢࠣዺ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨዻ") + str(e) + bstack111l11_opy_ (u"ࠤࠥዼ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11ll1l1_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
    def bstack1l1l1111111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l1l1l1l_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack111l11_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷ࠾ࠥࠨዽ") + str(req) + bstack111l11_opy_ (u"ࠦࠧዾ"))
        try:
            r = self.bstack1lll111lll1_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack111l11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢዿ") + str(r) + bstack111l11_opy_ (u"ࠨࠢጀ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧጁ") + str(e) + bstack111l11_opy_ (u"ࠣࠤጂ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11111l1_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
    def bstack1l1l1111ll1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l1l1l1l_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack111l11_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱ࠼ࠣࠦጃ") + str(req) + bstack111l11_opy_ (u"ࠥࠦጄ"))
        try:
            r = self.bstack1lll111lll1_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack111l11_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨጅ") + str(r) + bstack111l11_opy_ (u"ࠧࠨጆ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦጇ") + str(e) + bstack111l11_opy_ (u"ࠢࠣገ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lll111ll_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
    def bstack1l1l111l11l_opy_(self, instance: bstack11111111ll_opy_, url: str, f: bstack1llll1ll111_opy_, kwargs):
        bstack1l1l1111l11_opy_ = version.parse(f.framework_version)
        bstack1l1l111llll_opy_ = kwargs.get(bstack111l11_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤጉ"))
        bstack1l1l11l111l_opy_ = kwargs.get(bstack111l11_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤጊ"))
        bstack1l1ll111111_opy_ = {}
        bstack1l1l11ll1ll_opy_ = {}
        bstack1l1l11l1lll_opy_ = None
        bstack1l1l111l1ll_opy_ = {}
        if bstack1l1l11l111l_opy_ is not None or bstack1l1l111llll_opy_ is not None: # check top level caps
            if bstack1l1l11l111l_opy_ is not None:
                bstack1l1l111l1ll_opy_[bstack111l11_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪጋ")] = bstack1l1l11l111l_opy_
            if bstack1l1l111llll_opy_ is not None and callable(getattr(bstack1l1l111llll_opy_, bstack111l11_opy_ (u"ࠦࡹࡵ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨጌ"))):
                bstack1l1l111l1ll_opy_[bstack111l11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸࡥࡡࡴࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨግ")] = bstack1l1l111llll_opy_.to_capabilities()
        response = self.bstack1l1l1lll1l1_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l1l111l1ll_opy_).encode(bstack111l11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧጎ")))
        if response is not None and response.capabilities:
            bstack1l1ll111111_opy_ = json.loads(response.capabilities.decode(bstack111l11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨጏ")))
            if not bstack1l1ll111111_opy_: # empty caps bstack1l1l1llll1l_opy_ bstack1l1l1llll11_opy_ bstack1l1l1llllll_opy_ bstack1lll11111ll_opy_ or error in processing
                return
            bstack1l1l11l1lll_opy_ = f.bstack1lll1l1ll11_opy_[bstack111l11_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡩࡶࡴࡳ࡟ࡤࡣࡳࡷࠧጐ")](bstack1l1ll111111_opy_)
        if bstack1l1l111llll_opy_ is not None and bstack1l1l1111l11_opy_ >= version.parse(bstack111l11_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ጑")):
            bstack1l1l11ll1ll_opy_ = None
        if (
                not bstack1l1l111llll_opy_ and not bstack1l1l11l111l_opy_
        ) or (
                bstack1l1l1111l11_opy_ < version.parse(bstack111l11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩጒ"))
        ):
            bstack1l1l11ll1ll_opy_ = {}
            bstack1l1l11ll1ll_opy_.update(bstack1l1ll111111_opy_)
        self.logger.info(bstack1lll1llll_opy_)
        if os.environ.get(bstack111l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠢጓ")).lower().__eq__(bstack111l11_opy_ (u"ࠧࡺࡲࡶࡧࠥጔ")):
            kwargs.update(
                {
                    bstack111l11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤጕ"): f.bstack1l1l11l1ll1_opy_,
                }
            )
        if bstack1l1l1111l11_opy_ >= version.parse(bstack111l11_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ጖")):
            if bstack1l1l11l111l_opy_ is not None:
                del kwargs[bstack111l11_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ጗")]
            kwargs.update(
                {
                    bstack111l11_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥጘ"): bstack1l1l11l1lll_opy_,
                    bstack111l11_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢጙ"): True,
                    bstack111l11_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦጚ"): None,
                }
            )
        elif bstack1l1l1111l11_opy_ >= version.parse(bstack111l11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫጛ")):
            kwargs.update(
                {
                    bstack111l11_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨጜ"): bstack1l1l11ll1ll_opy_,
                    bstack111l11_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣጝ"): bstack1l1l11l1lll_opy_,
                    bstack111l11_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧጞ"): True,
                    bstack111l11_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤጟ"): None,
                }
            )
        elif bstack1l1l1111l11_opy_ >= version.parse(bstack111l11_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪጠ")):
            kwargs.update(
                {
                    bstack111l11_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦጡ"): bstack1l1l11ll1ll_opy_,
                    bstack111l11_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤጢ"): True,
                    bstack111l11_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨጣ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack111l11_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢጤ"): bstack1l1l11ll1ll_opy_,
                    bstack111l11_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧጥ"): True,
                    bstack111l11_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤጦ"): None,
                }
            )