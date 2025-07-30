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
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll11l1111_opy_ import bstack1lll11l1lll_opy_
from browserstack_sdk.sdk_cli.bstack111111l11l_opy_ import (
    bstack1llllll1l1l_opy_,
    bstack111111l1l1_opy_,
    bstack11111111ll_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1lllll1l11l_opy_ import bstack1lll111ll1l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1lll1llll_opy_
from bstack_utils.helper import bstack1ll1111llll_opy_
import threading
import os
import urllib.parse
class bstack1lll1lll11l_opy_(bstack1lll11l1lll_opy_):
    def __init__(self, bstack1lll1l1l1ll_opy_):
        super().__init__()
        bstack1lll111ll1l_opy_.bstack1ll11ll11ll_opy_((bstack1llllll1l1l_opy_.bstack1lllllll1ll_opy_, bstack111111l1l1_opy_.PRE), self.bstack1l1l1l1lll1_opy_)
        bstack1lll111ll1l_opy_.bstack1ll11ll11ll_opy_((bstack1llllll1l1l_opy_.bstack1lllllll1ll_opy_, bstack111111l1l1_opy_.PRE), self.bstack1l1l1lll111_opy_)
        bstack1lll111ll1l_opy_.bstack1ll11ll11ll_opy_((bstack1llllll1l1l_opy_.bstack11111l111l_opy_, bstack111111l1l1_opy_.PRE), self.bstack1l1l1ll11l1_opy_)
        bstack1lll111ll1l_opy_.bstack1ll11ll11ll_opy_((bstack1llllll1l1l_opy_.bstack111111111l_opy_, bstack111111l1l1_opy_.PRE), self.bstack1l1l1ll1l1l_opy_)
        bstack1lll111ll1l_opy_.bstack1ll11ll11ll_opy_((bstack1llllll1l1l_opy_.bstack1lllllll1ll_opy_, bstack111111l1l1_opy_.PRE), self.bstack1l1l1ll1lll_opy_)
        bstack1lll111ll1l_opy_.bstack1ll11ll11ll_opy_((bstack1llllll1l1l_opy_.QUIT, bstack111111l1l1_opy_.PRE), self.on_close)
        self.bstack1lll1l1l1ll_opy_ = bstack1lll1l1l1ll_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1l1lll1_opy_(
        self,
        f: bstack1lll111ll1l_opy_,
        bstack1l1l1ll111l_opy_: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l11_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨ቟"):
            return
        if not bstack1ll1111llll_opy_():
            self.logger.debug(bstack111l11_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦ࡬ࡢࡷࡱࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦበ"))
            return
        def wrapped(bstack1l1l1ll111l_opy_, launch, *args, **kwargs):
            response = self.bstack1l1l1lll1l1_opy_(f.platform_index, instance.ref(), json.dumps({bstack111l11_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧቡ"): True}).encode(bstack111l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣቢ")))
            if response is not None and response.capabilities:
                if not bstack1ll1111llll_opy_():
                    browser = launch(bstack1l1l1ll111l_opy_)
                    return browser
                bstack1l1ll111111_opy_ = json.loads(response.capabilities.decode(bstack111l11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤባ")))
                if not bstack1l1ll111111_opy_: # empty caps bstack1l1l1llll1l_opy_ bstack1l1l1llll11_opy_ bstack1l1l1llllll_opy_ bstack1lll11111ll_opy_ or error in processing
                    return
                bstack1l1l1ll1l11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1ll111111_opy_))
                f.bstack111111ll1l_opy_(instance, bstack1lll111ll1l_opy_.bstack1l1l1ll1ll1_opy_, bstack1l1l1ll1l11_opy_)
                f.bstack111111ll1l_opy_(instance, bstack1lll111ll1l_opy_.bstack1l1l1lllll1_opy_, bstack1l1ll111111_opy_)
                browser = bstack1l1l1ll111l_opy_.connect(bstack1l1l1ll1l11_opy_)
                return browser
        return wrapped
    def bstack1l1l1ll11l1_opy_(
        self,
        f: bstack1lll111ll1l_opy_,
        Connection: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l11_opy_ (u"ࠦࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠨቤ"):
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦብ"))
            return
        if not bstack1ll1111llll_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack111l11_opy_ (u"࠭ࡰࡢࡴࡤࡱࡸ࠭ቦ"), {}).get(bstack111l11_opy_ (u"ࠧࡣࡵࡓࡥࡷࡧ࡭ࡴࠩቧ")):
                    bstack1l1l1lll1ll_opy_ = args[0][bstack111l11_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣቨ")][bstack111l11_opy_ (u"ࠤࡥࡷࡕࡧࡲࡢ࡯ࡶࠦቩ")]
                    session_id = bstack1l1l1lll1ll_opy_.get(bstack111l11_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡍࡩࠨቪ"))
                    f.bstack111111ll1l_opy_(instance, bstack1lll111ll1l_opy_.bstack1l1l1l1llll_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack111l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࠢቫ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1l1ll1lll_opy_(
        self,
        f: bstack1lll111ll1l_opy_,
        bstack1l1l1ll111l_opy_: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l11_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨቬ"):
            return
        if not bstack1ll1111llll_opy_():
            self.logger.debug(bstack111l11_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡩ࡯࡯ࡰࡨࡧࡹࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦቭ"))
            return
        def wrapped(bstack1l1l1ll111l_opy_, connect, *args, **kwargs):
            response = self.bstack1l1l1lll1l1_opy_(f.platform_index, instance.ref(), json.dumps({bstack111l11_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ቮ"): True}).encode(bstack111l11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢቯ")))
            if response is not None and response.capabilities:
                bstack1l1ll111111_opy_ = json.loads(response.capabilities.decode(bstack111l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣተ")))
                if not bstack1l1ll111111_opy_:
                    return
                bstack1l1l1ll1l11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1ll111111_opy_))
                if bstack1l1ll111111_opy_.get(bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩቱ")):
                    browser = bstack1l1l1ll111l_opy_.bstack1l1l1lll11l_opy_(bstack1l1l1ll1l11_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1l1ll1l11_opy_
                    return connect(bstack1l1l1ll111l_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1l1lll111_opy_(
        self,
        f: bstack1lll111ll1l_opy_,
        bstack1ll111l1l1l_opy_: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l11_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨቲ"):
            return
        if not bstack1ll1111llll_opy_():
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦታ"))
            return
        def wrapped(bstack1ll111l1l1l_opy_, bstack1l1l1ll11ll_opy_, *args, **kwargs):
            contexts = bstack1ll111l1l1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack111l11_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦቴ") in page.url:
                                    return page
                    else:
                        return bstack1l1l1ll11ll_opy_(bstack1ll111l1l1l_opy_)
        return wrapped
    def bstack1l1l1lll1l1_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack111l11_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧት") + str(req) + bstack111l11_opy_ (u"ࠣࠤቶ"))
        try:
            r = self.bstack1lll111lll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack111l11_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧቷ") + str(r.success) + bstack111l11_opy_ (u"ࠥࠦቸ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l11_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤቹ") + str(e) + bstack111l11_opy_ (u"ࠧࠨቺ"))
            traceback.print_exc()
            raise e
    def bstack1l1l1ll1l1l_opy_(
        self,
        f: bstack1lll111ll1l_opy_,
        Connection: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l11_opy_ (u"ࠨ࡟ࡴࡧࡱࡨࡤࡳࡥࡴࡵࡤ࡫ࡪࡥࡴࡰࡡࡶࡩࡷࡼࡥࡳࠤቻ"):
            return
        if not bstack1ll1111llll_opy_():
            return
        def wrapped(Connection, bstack1l1l1ll1111_opy_, *args, **kwargs):
            return bstack1l1l1ll1111_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1lll111ll1l_opy_,
        bstack1l1l1ll111l_opy_: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l11_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨቼ"):
            return
        if not bstack1ll1111llll_opy_():
            self.logger.debug(bstack111l11_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤ࡮ࡲࡷࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦች"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped