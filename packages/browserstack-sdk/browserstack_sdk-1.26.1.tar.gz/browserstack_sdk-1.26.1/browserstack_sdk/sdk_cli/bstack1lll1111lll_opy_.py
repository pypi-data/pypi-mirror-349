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
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll11l1ll_opy_ import bstack1llll1ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import (
    bstack1llllll1l11_opy_,
    bstack11111ll1l1_opy_,
    bstack1llllll11ll_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1llll111l11_opy_ import bstack1lll11l111l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l111ll1_opy_
from bstack_utils.helper import bstack1l1ll1l1ll1_opy_
import threading
import os
import urllib.parse
class bstack1lll11ll1l1_opy_(bstack1llll1ll1l1_opy_):
    def __init__(self, bstack1llll11111l_opy_):
        super().__init__()
        bstack1lll11l111l_opy_.bstack1ll1ll11111_opy_((bstack1llllll1l11_opy_.bstack11111l1l11_opy_, bstack11111ll1l1_opy_.PRE), self.bstack1l1l1ll1ll1_opy_)
        bstack1lll11l111l_opy_.bstack1ll1ll11111_opy_((bstack1llllll1l11_opy_.bstack11111l1l11_opy_, bstack11111ll1l1_opy_.PRE), self.bstack1l1l1ll111l_opy_)
        bstack1lll11l111l_opy_.bstack1ll1ll11111_opy_((bstack1llllll1l11_opy_.bstack1lllllllll1_opy_, bstack11111ll1l1_opy_.PRE), self.bstack1l1l1llll11_opy_)
        bstack1lll11l111l_opy_.bstack1ll1ll11111_opy_((bstack1llllll1l11_opy_.bstack11111l111l_opy_, bstack11111ll1l1_opy_.PRE), self.bstack1l1l1ll1111_opy_)
        bstack1lll11l111l_opy_.bstack1ll1ll11111_opy_((bstack1llllll1l11_opy_.bstack11111l1l11_opy_, bstack11111ll1l1_opy_.PRE), self.bstack1l1l1lll1l1_opy_)
        bstack1lll11l111l_opy_.bstack1ll1ll11111_opy_((bstack1llllll1l11_opy_.QUIT, bstack11111ll1l1_opy_.PRE), self.on_close)
        self.bstack1llll11111l_opy_ = bstack1llll11111l_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1ll1ll1_opy_(
        self,
        f: bstack1lll11l111l_opy_,
        bstack1l1l1ll1l11_opy_: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1lll_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨ቟"):
            return
        if not bstack1l1ll1l1ll1_opy_():
            self.logger.debug(bstack11l1lll_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦ࡬ࡢࡷࡱࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦበ"))
            return
        def wrapped(bstack1l1l1ll1l11_opy_, launch, *args, **kwargs):
            response = self.bstack1l1l1ll1lll_opy_(f.platform_index, instance.ref(), json.dumps({bstack11l1lll_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧቡ"): True}).encode(bstack11l1lll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣቢ")))
            if response is not None and response.capabilities:
                if not bstack1l1ll1l1ll1_opy_():
                    browser = launch(bstack1l1l1ll1l11_opy_)
                    return browser
                bstack1l1l1ll11l1_opy_ = json.loads(response.capabilities.decode(bstack11l1lll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤባ")))
                if not bstack1l1l1ll11l1_opy_: # empty caps bstack1l1l1lllll1_opy_ bstack1l1l1ll11ll_opy_ bstack1l1ll111111_opy_ bstack1lll11l1l1l_opy_ or error in processing
                    return
                bstack1l1l1l1lll1_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l1ll11l1_opy_))
                f.bstack111111llll_opy_(instance, bstack1lll11l111l_opy_.bstack1l1l1lll111_opy_, bstack1l1l1l1lll1_opy_)
                f.bstack111111llll_opy_(instance, bstack1lll11l111l_opy_.bstack1l1l1llllll_opy_, bstack1l1l1ll11l1_opy_)
                browser = bstack1l1l1ll1l11_opy_.connect(bstack1l1l1l1lll1_opy_)
                return browser
        return wrapped
    def bstack1l1l1llll11_opy_(
        self,
        f: bstack1lll11l111l_opy_,
        Connection: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1lll_opy_ (u"ࠦࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠨቤ"):
            self.logger.debug(bstack11l1lll_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦብ"))
            return
        if not bstack1l1ll1l1ll1_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack11l1lll_opy_ (u"࠭ࡰࡢࡴࡤࡱࡸ࠭ቦ"), {}).get(bstack11l1lll_opy_ (u"ࠧࡣࡵࡓࡥࡷࡧ࡭ࡴࠩቧ")):
                    bstack1l1l1l1llll_opy_ = args[0][bstack11l1lll_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣቨ")][bstack11l1lll_opy_ (u"ࠤࡥࡷࡕࡧࡲࡢ࡯ࡶࠦቩ")]
                    session_id = bstack1l1l1l1llll_opy_.get(bstack11l1lll_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡍࡩࠨቪ"))
                    f.bstack111111llll_opy_(instance, bstack1lll11l111l_opy_.bstack1l1l1lll11l_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack11l1lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࠢቫ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1l1lll1l1_opy_(
        self,
        f: bstack1lll11l111l_opy_,
        bstack1l1l1ll1l11_opy_: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1lll_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨቬ"):
            return
        if not bstack1l1ll1l1ll1_opy_():
            self.logger.debug(bstack11l1lll_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡩ࡯࡯ࡰࡨࡧࡹࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦቭ"))
            return
        def wrapped(bstack1l1l1ll1l11_opy_, connect, *args, **kwargs):
            response = self.bstack1l1l1ll1lll_opy_(f.platform_index, instance.ref(), json.dumps({bstack11l1lll_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ቮ"): True}).encode(bstack11l1lll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢቯ")))
            if response is not None and response.capabilities:
                bstack1l1l1ll11l1_opy_ = json.loads(response.capabilities.decode(bstack11l1lll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣተ")))
                if not bstack1l1l1ll11l1_opy_:
                    return
                bstack1l1l1l1lll1_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l1ll11l1_opy_))
                if bstack1l1l1ll11l1_opy_.get(bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩቱ")):
                    browser = bstack1l1l1ll1l11_opy_.bstack1l1l1llll1l_opy_(bstack1l1l1l1lll1_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1l1l1lll1_opy_
                    return connect(bstack1l1l1ll1l11_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1l1ll111l_opy_(
        self,
        f: bstack1lll11l111l_opy_,
        bstack1ll111l1l11_opy_: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1lll_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨቲ"):
            return
        if not bstack1l1ll1l1ll1_opy_():
            self.logger.debug(bstack11l1lll_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦታ"))
            return
        def wrapped(bstack1ll111l1l11_opy_, bstack1l1l1ll1l1l_opy_, *args, **kwargs):
            contexts = bstack1ll111l1l11_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack11l1lll_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦቴ") in page.url:
                                    return page
                    else:
                        return bstack1l1l1ll1l1l_opy_(bstack1ll111l1l11_opy_)
        return wrapped
    def bstack1l1l1ll1lll_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack11l1lll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧት") + str(req) + bstack11l1lll_opy_ (u"ࠣࠤቶ"))
        try:
            r = self.bstack1llll111ll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11l1lll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧቷ") + str(r.success) + bstack11l1lll_opy_ (u"ࠥࠦቸ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1lll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤቹ") + str(e) + bstack11l1lll_opy_ (u"ࠧࠨቺ"))
            traceback.print_exc()
            raise e
    def bstack1l1l1ll1111_opy_(
        self,
        f: bstack1lll11l111l_opy_,
        Connection: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1lll_opy_ (u"ࠨ࡟ࡴࡧࡱࡨࡤࡳࡥࡴࡵࡤ࡫ࡪࡥࡴࡰࡡࡶࡩࡷࡼࡥࡳࠤቻ"):
            return
        if not bstack1l1ll1l1ll1_opy_():
            return
        def wrapped(Connection, bstack1l1l1lll1ll_opy_, *args, **kwargs):
            return bstack1l1l1lll1ll_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1lll11l111l_opy_,
        bstack1l1l1ll1l11_opy_: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1lll_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨቼ"):
            return
        if not bstack1l1ll1l1ll1_opy_():
            self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤ࡮ࡲࡷࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦች"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped