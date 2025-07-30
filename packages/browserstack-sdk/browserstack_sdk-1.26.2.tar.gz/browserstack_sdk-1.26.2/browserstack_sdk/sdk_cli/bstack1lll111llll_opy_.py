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
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack111111l11l_opy_ import (
    bstack1lllllll1l1_opy_,
    bstack11111111ll_opy_,
    bstack1llllll1l1l_opy_,
    bstack111111l1l1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack11l11111l_opy_ import bstack1ll1ll1ll11_opy_
from bstack_utils.constants import EVENTS
class bstack1llll1ll111_opy_(bstack1lllllll1l1_opy_):
    bstack1l11ll1l1ll_opy_ = bstack111l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᓣ")
    NAME = bstack111l11_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᓤ")
    bstack1l1l1ll1ll1_opy_ = bstack111l11_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤᓥ")
    bstack1l1l1l1llll_opy_ = bstack111l11_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᓦ")
    bstack1l11111lll1_opy_ = bstack111l11_opy_ (u"ࠥ࡭ࡳࡶࡵࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᓧ")
    bstack1l1l1lllll1_opy_ = bstack111l11_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᓨ")
    bstack1l11lll1l11_opy_ = bstack111l11_opy_ (u"ࠧ࡯ࡳࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡩࡷࡥࠦᓩ")
    bstack1l111111lll_opy_ = bstack111l11_opy_ (u"ࠨࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᓪ")
    bstack1l11111ll11_opy_ = bstack111l11_opy_ (u"ࠢࡦࡰࡧࡩࡩࡥࡡࡵࠤᓫ")
    bstack1ll1l111lll_opy_ = bstack111l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤᓬ")
    bstack1l1l11l11l1_opy_ = bstack111l11_opy_ (u"ࠤࡱࡩࡼࡹࡥࡴࡵ࡬ࡳࡳࠨᓭ")
    bstack1l11111l111_opy_ = bstack111l11_opy_ (u"ࠥ࡫ࡪࡺࠢᓮ")
    bstack1ll1111ll1l_opy_ = bstack111l11_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣᓯ")
    bstack1l11ll1ll1l_opy_ = bstack111l11_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࠣᓰ")
    bstack1l11ll1l1l1_opy_ = bstack111l11_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࡣࡶࡽࡳࡩࠢᓱ")
    bstack1l11111l1l1_opy_ = bstack111l11_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᓲ")
    bstack1l11111l1ll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l11l1ll1_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1l1ll11_opy_: Any
    bstack1l11ll1lll1_opy_: Dict
    def __init__(
        self,
        bstack1l1l11l1ll1_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lll1l1ll11_opy_: Dict[str, Any],
        methods=[bstack111l11_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᓳ"), bstack111l11_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᓴ"), bstack111l11_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᓵ"), bstack111l11_opy_ (u"ࠦࡶࡻࡩࡵࠤᓶ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1l11l1ll1_opy_ = bstack1l1l11l1ll1_opy_
        self.platform_index = platform_index
        self.bstack1lllllllll1_opy_(methods)
        self.bstack1lll1l1ll11_opy_ = bstack1lll1l1ll11_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1lllllll1l1_opy_.get_data(bstack1llll1ll111_opy_.bstack1l1l1l1llll_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1lllllll1l1_opy_.get_data(bstack1llll1ll111_opy_.bstack1l1l1ll1ll1_opy_, target, strict)
    @staticmethod
    def bstack1l11111l11l_opy_(target: object, strict=True):
        return bstack1lllllll1l1_opy_.get_data(bstack1llll1ll111_opy_.bstack1l11111lll1_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1lllllll1l1_opy_.get_data(bstack1llll1ll111_opy_.bstack1l1l1lllll1_opy_, target, strict)
    @staticmethod
    def bstack1ll111ll11l_opy_(instance: bstack11111111ll_opy_) -> bool:
        return bstack1lllllll1l1_opy_.bstack1llllll1111_opy_(instance, bstack1llll1ll111_opy_.bstack1l11lll1l11_opy_, False)
    @staticmethod
    def bstack1ll11ll1ll1_opy_(instance: bstack11111111ll_opy_, default_value=None):
        return bstack1lllllll1l1_opy_.bstack1llllll1111_opy_(instance, bstack1llll1ll111_opy_.bstack1l1l1ll1ll1_opy_, default_value)
    @staticmethod
    def bstack1ll11ll1l11_opy_(instance: bstack11111111ll_opy_, default_value=None):
        return bstack1lllllll1l1_opy_.bstack1llllll1111_opy_(instance, bstack1llll1ll111_opy_.bstack1l1l1lllll1_opy_, default_value)
    @staticmethod
    def bstack1ll11l111ll_opy_(hub_url: str, bstack1l1111l1111_opy_=bstack111l11_opy_ (u"ࠧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤᓷ")):
        try:
            bstack1l11111ll1l_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l11111ll1l_opy_.endswith(bstack1l1111l1111_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1l11lll1_opy_(method_name: str):
        return method_name == bstack111l11_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᓸ")
    @staticmethod
    def bstack1ll11ll1l1l_opy_(method_name: str, *args):
        return (
            bstack1llll1ll111_opy_.bstack1ll1l11lll1_opy_(method_name)
            and bstack1llll1ll111_opy_.bstack1l1l111lll1_opy_(*args) == bstack1llll1ll111_opy_.bstack1l1l11l11l1_opy_
        )
    @staticmethod
    def bstack1ll1l11l1l1_opy_(method_name: str, *args):
        if not bstack1llll1ll111_opy_.bstack1ll1l11lll1_opy_(method_name):
            return False
        if not bstack1llll1ll111_opy_.bstack1l11ll1ll1l_opy_ in bstack1llll1ll111_opy_.bstack1l1l111lll1_opy_(*args):
            return False
        bstack1ll11l11lll_opy_ = bstack1llll1ll111_opy_.bstack1ll11l11l1l_opy_(*args)
        return bstack1ll11l11lll_opy_ and bstack111l11_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᓹ") in bstack1ll11l11lll_opy_ and bstack111l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᓺ") in bstack1ll11l11lll_opy_[bstack111l11_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᓻ")]
    @staticmethod
    def bstack1ll11l1l1ll_opy_(method_name: str, *args):
        if not bstack1llll1ll111_opy_.bstack1ll1l11lll1_opy_(method_name):
            return False
        if not bstack1llll1ll111_opy_.bstack1l11ll1ll1l_opy_ in bstack1llll1ll111_opy_.bstack1l1l111lll1_opy_(*args):
            return False
        bstack1ll11l11lll_opy_ = bstack1llll1ll111_opy_.bstack1ll11l11l1l_opy_(*args)
        return (
            bstack1ll11l11lll_opy_
            and bstack111l11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᓼ") in bstack1ll11l11lll_opy_
            and bstack111l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡥࡵ࡭ࡵࡺࠢᓽ") in bstack1ll11l11lll_opy_[bstack111l11_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᓾ")]
        )
    @staticmethod
    def bstack1l1l111lll1_opy_(*args):
        return str(bstack1llll1ll111_opy_.bstack1ll1l11111l_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1l11111l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11l11l1l_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1l1ll11l11_opy_(driver):
        command_executor = getattr(driver, bstack111l11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᓿ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack111l11_opy_ (u"ࠢࡠࡷࡵࡰࠧᔀ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack111l11_opy_ (u"ࠣࡡࡦࡰ࡮࡫࡮ࡵࡡࡦࡳࡳ࡬ࡩࡨࠤᔁ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack111l11_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡡࡶࡩࡷࡼࡥࡳࡡࡤࡨࡩࡸࠢᔂ"), None)
        return hub_url
    def bstack1l1l11ll111_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack111l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᔃ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack111l11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᔄ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack111l11_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᔅ")):
                setattr(command_executor, bstack111l11_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᔆ"), hub_url)
                result = True
        if result:
            self.bstack1l1l11l1ll1_opy_ = hub_url
            bstack1llll1ll111_opy_.bstack111111ll1l_opy_(instance, bstack1llll1ll111_opy_.bstack1l1l1ll1ll1_opy_, hub_url)
            bstack1llll1ll111_opy_.bstack111111ll1l_opy_(
                instance, bstack1llll1ll111_opy_.bstack1l11lll1l11_opy_, bstack1llll1ll111_opy_.bstack1ll11l111ll_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11lll11l1_opy_(bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_]):
        return bstack111l11_opy_ (u"ࠢ࠻ࠤᔇ").join((bstack1llllll1l1l_opy_(bstack11111l1ll1_opy_[0]).name, bstack111111l1l1_opy_(bstack11111l1ll1_opy_[1]).name))
    @staticmethod
    def bstack1ll11ll11ll_opy_(bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_], callback: Callable):
        bstack1l11ll1llll_opy_ = bstack1llll1ll111_opy_.bstack1l11lll11l1_opy_(bstack11111l1ll1_opy_)
        if not bstack1l11ll1llll_opy_ in bstack1llll1ll111_opy_.bstack1l11111l1ll_opy_:
            bstack1llll1ll111_opy_.bstack1l11111l1ll_opy_[bstack1l11ll1llll_opy_] = []
        bstack1llll1ll111_opy_.bstack1l11111l1ll_opy_[bstack1l11ll1llll_opy_].append(callback)
    def bstack111111l1ll_opy_(self, instance: bstack11111111ll_opy_, method_name: str, bstack11111111l1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack111l11_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᔈ")):
            return
        cmd = args[0] if method_name == bstack111l11_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᔉ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l11111llll_opy_ = bstack111l11_opy_ (u"ࠥ࠾ࠧᔊ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠧᔋ") + bstack1l11111llll_opy_, bstack11111111l1_opy_)
    def bstack11111lll11_opy_(
        self,
        target: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack111111lll1_opy_, bstack1l11lll1111_opy_ = bstack11111l1ll1_opy_
        bstack1l11ll1llll_opy_ = bstack1llll1ll111_opy_.bstack1l11lll11l1_opy_(bstack11111l1ll1_opy_)
        self.logger.debug(bstack111l11_opy_ (u"ࠧࡵ࡮ࡠࡪࡲࡳࡰࡀࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᔌ") + str(kwargs) + bstack111l11_opy_ (u"ࠨࠢᔍ"))
        if bstack111111lll1_opy_ == bstack1llllll1l1l_opy_.QUIT:
            if bstack1l11lll1111_opy_ == bstack111111l1l1_opy_.PRE:
                bstack1ll1l11ll1l_opy_ = bstack1ll1ll1ll11_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack1l1lll11l_opy_.value)
                bstack1lllllll1l1_opy_.bstack111111ll1l_opy_(instance, EVENTS.bstack1l1lll11l_opy_.value, bstack1ll1l11ll1l_opy_)
                self.logger.debug(bstack111l11_opy_ (u"ࠢࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠦᔎ").format(instance, method_name, bstack111111lll1_opy_, bstack1l11lll1111_opy_))
        if bstack111111lll1_opy_ == bstack1llllll1l1l_opy_.bstack1lllllll1ll_opy_:
            if bstack1l11lll1111_opy_ == bstack111111l1l1_opy_.POST and not bstack1llll1ll111_opy_.bstack1l1l1l1llll_opy_ in instance.data:
                session_id = getattr(target, bstack111l11_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᔏ"), None)
                if session_id:
                    instance.data[bstack1llll1ll111_opy_.bstack1l1l1l1llll_opy_] = session_id
        elif (
            bstack111111lll1_opy_ == bstack1llllll1l1l_opy_.bstack111111111l_opy_
            and bstack1llll1ll111_opy_.bstack1l1l111lll1_opy_(*args) == bstack1llll1ll111_opy_.bstack1l1l11l11l1_opy_
        ):
            if bstack1l11lll1111_opy_ == bstack111111l1l1_opy_.PRE:
                hub_url = bstack1llll1ll111_opy_.bstack1l1ll11l11_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1llll1ll111_opy_.bstack1l1l1ll1ll1_opy_: hub_url,
                            bstack1llll1ll111_opy_.bstack1l11lll1l11_opy_: bstack1llll1ll111_opy_.bstack1ll11l111ll_opy_(hub_url),
                            bstack1llll1ll111_opy_.bstack1ll1l111lll_opy_: int(
                                os.environ.get(bstack111l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᔐ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll11l11lll_opy_ = bstack1llll1ll111_opy_.bstack1ll11l11l1l_opy_(*args)
                bstack1l11111l11l_opy_ = bstack1ll11l11lll_opy_.get(bstack111l11_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᔑ"), None) if bstack1ll11l11lll_opy_ else None
                if isinstance(bstack1l11111l11l_opy_, dict):
                    instance.data[bstack1llll1ll111_opy_.bstack1l11111lll1_opy_] = copy.deepcopy(bstack1l11111l11l_opy_)
                    instance.data[bstack1llll1ll111_opy_.bstack1l1l1lllll1_opy_] = bstack1l11111l11l_opy_
            elif bstack1l11lll1111_opy_ == bstack111111l1l1_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack111l11_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᔒ"), dict()).get(bstack111l11_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡏࡤࠣᔓ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1llll1ll111_opy_.bstack1l1l1l1llll_opy_: framework_session_id,
                                bstack1llll1ll111_opy_.bstack1l111111lll_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack111111lll1_opy_ == bstack1llllll1l1l_opy_.bstack111111111l_opy_
            and bstack1llll1ll111_opy_.bstack1l1l111lll1_opy_(*args) == bstack1llll1ll111_opy_.bstack1l11111l1l1_opy_
            and bstack1l11lll1111_opy_ == bstack111111l1l1_opy_.POST
        ):
            instance.data[bstack1llll1ll111_opy_.bstack1l11111ll11_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11ll1llll_opy_ in bstack1llll1ll111_opy_.bstack1l11111l1ll_opy_:
            bstack1l11lll111l_opy_ = None
            for callback in bstack1llll1ll111_opy_.bstack1l11111l1ll_opy_[bstack1l11ll1llll_opy_]:
                try:
                    bstack1l11ll1ll11_opy_ = callback(self, target, exec, bstack11111l1ll1_opy_, result, *args, **kwargs)
                    if bstack1l11lll111l_opy_ == None:
                        bstack1l11lll111l_opy_ = bstack1l11ll1ll11_opy_
                except Exception as e:
                    self.logger.error(bstack111l11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࠦᔔ") + str(e) + bstack111l11_opy_ (u"ࠢࠣᔕ"))
                    traceback.print_exc()
            if bstack111111lll1_opy_ == bstack1llllll1l1l_opy_.QUIT:
                if bstack1l11lll1111_opy_ == bstack111111l1l1_opy_.POST:
                    bstack1ll1l11ll1l_opy_ = bstack1lllllll1l1_opy_.bstack1llllll1111_opy_(instance, EVENTS.bstack1l1lll11l_opy_.value)
                    if bstack1ll1l11ll1l_opy_!=None:
                        bstack1ll1ll1ll11_opy_.end(EVENTS.bstack1l1lll11l_opy_.value, bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᔖ"), bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᔗ"), True, None)
            if bstack1l11lll1111_opy_ == bstack111111l1l1_opy_.PRE and callable(bstack1l11lll111l_opy_):
                return bstack1l11lll111l_opy_
            elif bstack1l11lll1111_opy_ == bstack111111l1l1_opy_.POST and bstack1l11lll111l_opy_:
                return bstack1l11lll111l_opy_
    def bstack1llllllllll_opy_(
        self, method_name, previous_state: bstack1llllll1l1l_opy_, *args, **kwargs
    ) -> bstack1llllll1l1l_opy_:
        if method_name == bstack111l11_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧᔘ") or method_name == bstack111l11_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᔙ"):
            return bstack1llllll1l1l_opy_.bstack1lllllll1ll_opy_
        if method_name == bstack111l11_opy_ (u"ࠧࡷࡵࡪࡶࠥᔚ"):
            return bstack1llllll1l1l_opy_.QUIT
        if method_name == bstack111l11_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᔛ"):
            if previous_state != bstack1llllll1l1l_opy_.NONE:
                bstack1ll1l1ll1ll_opy_ = bstack1llll1ll111_opy_.bstack1l1l111lll1_opy_(*args)
                if bstack1ll1l1ll1ll_opy_ == bstack1llll1ll111_opy_.bstack1l1l11l11l1_opy_:
                    return bstack1llllll1l1l_opy_.bstack1lllllll1ll_opy_
            return bstack1llllll1l1l_opy_.bstack111111111l_opy_
        return bstack1llllll1l1l_opy_.NONE