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
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll11l1ll_opy_ import bstack1llll1ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import (
    bstack1llllll1l11_opy_,
    bstack11111ll1l1_opy_,
    bstack1llllll11ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll1l11l1_opy_ import bstack1lll111llll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l111ll1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack11l1lll1l1_opy_ import bstack1lll1lll111_opy_
class bstack1llll1ll11l_opy_(bstack1llll1ll1l1_opy_):
    bstack1l1l1111l1l_opy_ = bstack11l1lll_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶࠥዓ")
    bstack1l1l11111ll_opy_ = bstack11l1lll_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸࠧዔ")
    bstack1l1l11ll1ll_opy_ = bstack11l1lll_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡲࡴࠧዕ")
    def __init__(self, bstack1lll111111l_opy_):
        super().__init__()
        bstack1lll111llll_opy_.bstack1ll1ll11111_opy_((bstack1llllll1l11_opy_.bstack11111l1l11_opy_, bstack11111ll1l1_opy_.PRE), self.bstack1l1l11l11ll_opy_)
        bstack1lll111llll_opy_.bstack1ll1ll11111_opy_((bstack1llllll1l11_opy_.bstack11111l111l_opy_, bstack11111ll1l1_opy_.PRE), self.bstack1ll11l1l111_opy_)
        bstack1lll111llll_opy_.bstack1ll1ll11111_opy_((bstack1llllll1l11_opy_.bstack11111l111l_opy_, bstack11111ll1l1_opy_.POST), self.bstack1l1l111llll_opy_)
        bstack1lll111llll_opy_.bstack1ll1ll11111_opy_((bstack1llllll1l11_opy_.bstack11111l111l_opy_, bstack11111ll1l1_opy_.POST), self.bstack1l1l111111l_opy_)
        bstack1lll111llll_opy_.bstack1ll1ll11111_opy_((bstack1llllll1l11_opy_.QUIT, bstack11111ll1l1_opy_.POST), self.bstack1l1l11l111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11l11ll_opy_(
        self,
        f: bstack1lll111llll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1lll_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣዖ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack11l1lll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥ዗")), str):
                    url = kwargs.get(bstack11l1lll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦዘ"))
                else:
                    url = kwargs.get(bstack11l1lll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧዙ"))._client_config.remote_server_addr
            except Exception as e:
                url = bstack11l1lll_opy_ (u"ࠪࠫዚ")
                self.logger.error(bstack11l1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡹࡷࡲࠠࡧࡴࡲࡱࠥࡪࡲࡪࡸࡨࡶ࠿ࠦࡻࡾࠤዛ").format(e))
            self.bstack1l1l111lll1_opy_(instance, url, f, kwargs)
            self.logger.debug(bstack11l1lll_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠳ࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࡻࡧ࠰ࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࢀ࠾ࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦዜ") + str(kwargs) + bstack11l1lll_opy_ (u"ࠨࠢዝ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
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
        instance, method_name = exec
        if f.bstack1llllll11l1_opy_(instance, bstack1llll1ll11l_opy_.bstack1l1l1111l1l_opy_, False):
            return
        if not f.bstack11111l11ll_opy_(instance, bstack1lll111llll_opy_.bstack1ll11l1l1ll_opy_):
            return
        platform_index = f.bstack1llllll11l1_opy_(instance, bstack1lll111llll_opy_.bstack1ll11l1l1ll_opy_)
        if f.bstack1ll1ll111ll_opy_(method_name, *args) and len(args) > 1:
            bstack11llll111l_opy_ = datetime.now()
            hub_url = bstack1lll111llll_opy_.hub_url(driver)
            self.logger.warning(bstack11l1lll_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬࠾ࠤዞ") + str(hub_url) + bstack11l1lll_opy_ (u"ࠣࠤዟ"))
            bstack1l1l11l11l1_opy_ = args[1][bstack11l1lll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣዠ")] if isinstance(args[1], dict) and bstack11l1lll_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤዡ") in args[1] else None
            bstack1l1l11ll1l1_opy_ = bstack11l1lll_opy_ (u"ࠦࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠤዢ")
            if isinstance(bstack1l1l11l11l1_opy_, dict):
                bstack11llll111l_opy_ = datetime.now()
                r = self.bstack1l1l11ll11l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶࠥዣ"), datetime.now() - bstack11llll111l_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11l1lll_opy_ (u"ࠨࡳࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࡀࠠࠣዤ") + str(r) + bstack11l1lll_opy_ (u"ࠢࠣዥ"))
                        return
                    if r.hub_url:
                        f.bstack1l1l111l111_opy_(instance, driver, r.hub_url)
                        f.bstack111111llll_opy_(instance, bstack1llll1ll11l_opy_.bstack1l1l1111l1l_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11l1lll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢዦ"), e)
    def bstack1l1l111llll_opy_(
        self,
        f: bstack1lll111llll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1lll111llll_opy_.session_id(driver)
            if session_id:
                bstack1l1l111l11l_opy_ = bstack11l1lll_opy_ (u"ࠤࡾࢁ࠿ࡹࡴࡢࡴࡷࠦዧ").format(session_id)
                bstack1lll1lll111_opy_.mark(bstack1l1l111l11l_opy_)
    def bstack1l1l111111l_opy_(
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
        if f.bstack1llllll11l1_opy_(instance, bstack1llll1ll11l_opy_.bstack1l1l11111ll_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1lll111llll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11l1lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡮ࡵࡣࡡࡸࡶࡱࡃࠢየ") + str(hub_url) + bstack11l1lll_opy_ (u"ࠦࠧዩ"))
            return
        framework_session_id = bstack1lll111llll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11l1lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣዪ") + str(framework_session_id) + bstack11l1lll_opy_ (u"ࠨࠢያ"))
            return
        if bstack1lll111llll_opy_.bstack1l1l1111ll1_opy_(*args) == bstack1lll111llll_opy_.bstack1l1l11l1lll_opy_:
            bstack1l1l1111lll_opy_ = bstack11l1lll_opy_ (u"ࠢࡼࡿ࠽ࡩࡳࡪࠢዬ").format(framework_session_id)
            bstack1l1l111l11l_opy_ = bstack11l1lll_opy_ (u"ࠣࡽࢀ࠾ࡸࡺࡡࡳࡶࠥይ").format(framework_session_id)
            bstack1lll1lll111_opy_.end(
                label=bstack11l1lll_opy_ (u"ࠤࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡰࡵࡷ࠱࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠧዮ"),
                start=bstack1l1l111l11l_opy_,
                end=bstack1l1l1111lll_opy_,
                status=True,
                failure=None
            )
            bstack11llll111l_opy_ = datetime.now()
            r = self.bstack1l1l111ll1l_opy_(
                ref,
                f.bstack1llllll11l1_opy_(instance, bstack1lll111llll_opy_.bstack1ll11l1l1ll_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵࠤዯ"), datetime.now() - bstack11llll111l_opy_)
            f.bstack111111llll_opy_(instance, bstack1llll1ll11l_opy_.bstack1l1l11111ll_opy_, r.success)
    def bstack1l1l11l111l_opy_(
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
        if f.bstack1llllll11l1_opy_(instance, bstack1llll1ll11l_opy_.bstack1l1l11ll1ll_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1lll111llll_opy_.session_id(driver)
        hub_url = bstack1lll111llll_opy_.hub_url(driver)
        bstack11llll111l_opy_ = datetime.now()
        r = self.bstack1l1l111l1ll_opy_(
            ref,
            f.bstack1llllll11l1_opy_(instance, bstack1lll111llll_opy_.bstack1ll11l1l1ll_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱࠤደ"), datetime.now() - bstack11llll111l_opy_)
        f.bstack111111llll_opy_(instance, bstack1llll1ll11l_opy_.bstack1l1l11ll1ll_opy_, r.success)
    @measure(event_name=EVENTS.bstack1lll111ll1_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def bstack1l1l1ll1lll_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack11l1lll_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࠥዱ") + str(req) + bstack11l1lll_opy_ (u"ࠨࠢዲ"))
        try:
            r = self.bstack1llll111ll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11l1lll_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥዳ") + str(r.success) + bstack11l1lll_opy_ (u"ࠣࠤዴ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1lll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢድ") + str(e) + bstack11l1lll_opy_ (u"ࠥࠦዶ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11ll111_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def bstack1l1l11ll11l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll1l11ll11_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack11l1lll_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥࠨዷ") + str(req) + bstack11l1lll_opy_ (u"ࠧࠨዸ"))
        try:
            r = self.bstack1llll111ll1_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11l1lll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤዹ") + str(r.success) + bstack11l1lll_opy_ (u"ࠢࠣዺ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1lll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨዻ") + str(e) + bstack11l1lll_opy_ (u"ࠤࠥዼ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l111ll11_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def bstack1l1l111ll1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l11ll11_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11l1lll_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷ࠾ࠥࠨዽ") + str(req) + bstack11l1lll_opy_ (u"ࠦࠧዾ"))
        try:
            r = self.bstack1llll111ll1_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11l1lll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢዿ") + str(r) + bstack11l1lll_opy_ (u"ࠨࠢጀ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1lll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧጁ") + str(e) + bstack11l1lll_opy_ (u"ࠣࠤጂ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11111l1_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def bstack1l1l111l1ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l11ll11_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11l1lll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱ࠼ࠣࠦጃ") + str(req) + bstack11l1lll_opy_ (u"ࠥࠦጄ"))
        try:
            r = self.bstack1llll111ll1_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11l1lll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨጅ") + str(r) + bstack11l1lll_opy_ (u"ࠧࠨጆ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦጇ") + str(e) + bstack11l1lll_opy_ (u"ࠢࠣገ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll11l1ll_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def bstack1l1l111lll1_opy_(self, instance: bstack1llllll11ll_opy_, url: str, f: bstack1lll111llll_opy_, kwargs):
        bstack1l1l11l1l1l_opy_ = version.parse(f.framework_version)
        bstack1l1l111l1l1_opy_ = kwargs.get(bstack11l1lll_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤጉ"))
        bstack1l1l1111111_opy_ = kwargs.get(bstack11l1lll_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤጊ"))
        bstack1l1l1ll11l1_opy_ = {}
        bstack1l1l1111l11_opy_ = {}
        bstack1l1l11l1111_opy_ = None
        bstack1l1l11l1ll1_opy_ = {}
        if bstack1l1l1111111_opy_ is not None or bstack1l1l111l1l1_opy_ is not None: # check top level caps
            if bstack1l1l1111111_opy_ is not None:
                bstack1l1l11l1ll1_opy_[bstack11l1lll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪጋ")] = bstack1l1l1111111_opy_
            if bstack1l1l111l1l1_opy_ is not None and callable(getattr(bstack1l1l111l1l1_opy_, bstack11l1lll_opy_ (u"ࠦࡹࡵ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨጌ"))):
                bstack1l1l11l1ll1_opy_[bstack11l1lll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸࡥࡡࡴࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨግ")] = bstack1l1l111l1l1_opy_.to_capabilities()
        response = self.bstack1l1l1ll1lll_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l1l11l1ll1_opy_).encode(bstack11l1lll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧጎ")))
        if response is not None and response.capabilities:
            bstack1l1l1ll11l1_opy_ = json.loads(response.capabilities.decode(bstack11l1lll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨጏ")))
            if not bstack1l1l1ll11l1_opy_: # empty caps bstack1l1l1lllll1_opy_ bstack1l1l1ll11ll_opy_ bstack1l1ll111111_opy_ bstack1lll11l1l1l_opy_ or error in processing
                return
            bstack1l1l11l1111_opy_ = f.bstack1ll1lllll1l_opy_[bstack11l1lll_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡩࡶࡴࡳ࡟ࡤࡣࡳࡷࠧጐ")](bstack1l1l1ll11l1_opy_)
        if bstack1l1l111l1l1_opy_ is not None and bstack1l1l11l1l1l_opy_ >= version.parse(bstack11l1lll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ጑")):
            bstack1l1l1111l11_opy_ = None
        if (
                not bstack1l1l111l1l1_opy_ and not bstack1l1l1111111_opy_
        ) or (
                bstack1l1l11l1l1l_opy_ < version.parse(bstack11l1lll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩጒ"))
        ):
            bstack1l1l1111l11_opy_ = {}
            bstack1l1l1111l11_opy_.update(bstack1l1l1ll11l1_opy_)
        self.logger.info(bstack1l111ll1_opy_)
        if os.environ.get(bstack11l1lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠢጓ")).lower().__eq__(bstack11l1lll_opy_ (u"ࠧࡺࡲࡶࡧࠥጔ")):
            kwargs.update(
                {
                    bstack11l1lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤጕ"): f.bstack1l1l11l1l11_opy_,
                }
            )
        if bstack1l1l11l1l1l_opy_ >= version.parse(bstack11l1lll_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ጖")):
            if bstack1l1l1111111_opy_ is not None:
                del kwargs[bstack11l1lll_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ጗")]
            kwargs.update(
                {
                    bstack11l1lll_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥጘ"): bstack1l1l11l1111_opy_,
                    bstack11l1lll_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢጙ"): True,
                    bstack11l1lll_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦጚ"): None,
                }
            )
        elif bstack1l1l11l1l1l_opy_ >= version.parse(bstack11l1lll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫጛ")):
            kwargs.update(
                {
                    bstack11l1lll_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨጜ"): bstack1l1l1111l11_opy_,
                    bstack11l1lll_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣጝ"): bstack1l1l11l1111_opy_,
                    bstack11l1lll_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧጞ"): True,
                    bstack11l1lll_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤጟ"): None,
                }
            )
        elif bstack1l1l11l1l1l_opy_ >= version.parse(bstack11l1lll_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪጠ")):
            kwargs.update(
                {
                    bstack11l1lll_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦጡ"): bstack1l1l1111l11_opy_,
                    bstack11l1lll_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤጢ"): True,
                    bstack11l1lll_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨጣ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11l1lll_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢጤ"): bstack1l1l1111l11_opy_,
                    bstack11l1lll_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧጥ"): True,
                    bstack11l1lll_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤጦ"): None,
                }
            )