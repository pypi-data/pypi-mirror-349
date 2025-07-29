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
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import (
    bstack1llllll111l_opy_,
    bstack1llllll11ll_opy_,
    bstack1llllll1l11_opy_,
    bstack11111ll1l1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack11l1lll1l1_opy_ import bstack1lll1lll111_opy_
from bstack_utils.constants import EVENTS
class bstack1lll111llll_opy_(bstack1llllll111l_opy_):
    bstack1l11ll1ll1l_opy_ = bstack11l1lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᓘ")
    NAME = bstack11l1lll_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᓙ")
    bstack1l1l1lll111_opy_ = bstack11l1lll_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧᓚ")
    bstack1l1l1lll11l_opy_ = bstack11l1lll_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᓛ")
    bstack1l11111ll1l_opy_ = bstack11l1lll_opy_ (u"ࠨࡩ࡯ࡲࡸࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᓜ")
    bstack1l1l1llllll_opy_ = bstack11l1lll_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᓝ")
    bstack1l11lll1l1l_opy_ = bstack11l1lll_opy_ (u"ࠣ࡫ࡶࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡬ࡺࡨࠢᓞ")
    bstack1l11111llll_opy_ = bstack11l1lll_opy_ (u"ࠤࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᓟ")
    bstack1l11111l11l_opy_ = bstack11l1lll_opy_ (u"ࠥࡩࡳࡪࡥࡥࡡࡤࡸࠧᓠ")
    bstack1ll11l1l1ll_opy_ = bstack11l1lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࠧᓡ")
    bstack1l1l11l1lll_opy_ = bstack11l1lll_opy_ (u"ࠧࡴࡥࡸࡵࡨࡷࡸ࡯࡯࡯ࠤᓢ")
    bstack1l1111l111l_opy_ = bstack11l1lll_opy_ (u"ࠨࡧࡦࡶࠥᓣ")
    bstack1ll1111llll_opy_ = bstack11l1lll_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᓤ")
    bstack1l11ll1llll_opy_ = bstack11l1lll_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࠦᓥ")
    bstack1l11ll1ll11_opy_ = bstack11l1lll_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࡦࡹࡹ࡯ࡥࠥᓦ")
    bstack1l11111lll1_opy_ = bstack11l1lll_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᓧ")
    bstack1l11111l1ll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l11l1l11_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1lllll1l_opy_: Any
    bstack1l11lll11l1_opy_: Dict
    def __init__(
        self,
        bstack1l1l11l1l11_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1ll1lllll1l_opy_: Dict[str, Any],
        methods=[bstack11l1lll_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨᓨ"), bstack11l1lll_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᓩ"), bstack11l1lll_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᓪ"), bstack11l1lll_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᓫ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1l11l1l11_opy_ = bstack1l1l11l1l11_opy_
        self.platform_index = platform_index
        self.bstack11111111l1_opy_(methods)
        self.bstack1ll1lllll1l_opy_ = bstack1ll1lllll1l_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1llllll111l_opy_.get_data(bstack1lll111llll_opy_.bstack1l1l1lll11l_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1llllll111l_opy_.get_data(bstack1lll111llll_opy_.bstack1l1l1lll111_opy_, target, strict)
    @staticmethod
    def bstack1l11111l1l1_opy_(target: object, strict=True):
        return bstack1llllll111l_opy_.get_data(bstack1lll111llll_opy_.bstack1l11111ll1l_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1llllll111l_opy_.get_data(bstack1lll111llll_opy_.bstack1l1l1llllll_opy_, target, strict)
    @staticmethod
    def bstack1ll111ll1l1_opy_(instance: bstack1llllll11ll_opy_) -> bool:
        return bstack1llllll111l_opy_.bstack1llllll11l1_opy_(instance, bstack1lll111llll_opy_.bstack1l11lll1l1l_opy_, False)
    @staticmethod
    def bstack1ll11llll11_opy_(instance: bstack1llllll11ll_opy_, default_value=None):
        return bstack1llllll111l_opy_.bstack1llllll11l1_opy_(instance, bstack1lll111llll_opy_.bstack1l1l1lll111_opy_, default_value)
    @staticmethod
    def bstack1ll1l111l11_opy_(instance: bstack1llllll11ll_opy_, default_value=None):
        return bstack1llllll111l_opy_.bstack1llllll11l1_opy_(instance, bstack1lll111llll_opy_.bstack1l1l1llllll_opy_, default_value)
    @staticmethod
    def bstack1ll11l1111l_opy_(hub_url: str, bstack1l1111l11l1_opy_=bstack11l1lll_opy_ (u"ࠣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧᓬ")):
        try:
            bstack1l1111l1111_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l1111l1111_opy_.endswith(bstack1l1111l11l1_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1ll111l1_opy_(method_name: str):
        return method_name == bstack11l1lll_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᓭ")
    @staticmethod
    def bstack1ll1ll111ll_opy_(method_name: str, *args):
        return (
            bstack1lll111llll_opy_.bstack1ll1ll111l1_opy_(method_name)
            and bstack1lll111llll_opy_.bstack1l1l1111ll1_opy_(*args) == bstack1lll111llll_opy_.bstack1l1l11l1lll_opy_
        )
    @staticmethod
    def bstack1ll11lll111_opy_(method_name: str, *args):
        if not bstack1lll111llll_opy_.bstack1ll1ll111l1_opy_(method_name):
            return False
        if not bstack1lll111llll_opy_.bstack1l11ll1llll_opy_ in bstack1lll111llll_opy_.bstack1l1l1111ll1_opy_(*args):
            return False
        bstack1ll11l1l1l1_opy_ = bstack1lll111llll_opy_.bstack1ll11l111ll_opy_(*args)
        return bstack1ll11l1l1l1_opy_ and bstack11l1lll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᓮ") in bstack1ll11l1l1l1_opy_ and bstack11l1lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᓯ") in bstack1ll11l1l1l1_opy_[bstack11l1lll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᓰ")]
    @staticmethod
    def bstack1ll1l1lll11_opy_(method_name: str, *args):
        if not bstack1lll111llll_opy_.bstack1ll1ll111l1_opy_(method_name):
            return False
        if not bstack1lll111llll_opy_.bstack1l11ll1llll_opy_ in bstack1lll111llll_opy_.bstack1l1l1111ll1_opy_(*args):
            return False
        bstack1ll11l1l1l1_opy_ = bstack1lll111llll_opy_.bstack1ll11l111ll_opy_(*args)
        return (
            bstack1ll11l1l1l1_opy_
            and bstack11l1lll_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᓱ") in bstack1ll11l1l1l1_opy_
            and bstack11l1lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡨࡸࡩࡱࡶࠥᓲ") in bstack1ll11l1l1l1_opy_[bstack11l1lll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᓳ")]
        )
    @staticmethod
    def bstack1l1l1111ll1_opy_(*args):
        return str(bstack1lll111llll_opy_.bstack1ll11ll111l_opy_(*args)).lower()
    @staticmethod
    def bstack1ll11ll111l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11l111ll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1ll1l11ll1_opy_(driver):
        command_executor = getattr(driver, bstack11l1lll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᓴ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11l1lll_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᓵ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11l1lll_opy_ (u"ࠦࡤࡩ࡬ࡪࡧࡱࡸࡤࡩ࡯࡯ࡨ࡬࡫ࠧᓶ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11l1lll_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡤࡹࡥࡳࡸࡨࡶࡤࡧࡤࡥࡴࠥᓷ"), None)
        return hub_url
    def bstack1l1l111l111_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11l1lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᓸ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11l1lll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᓹ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11l1lll_opy_ (u"ࠣࡡࡸࡶࡱࠨᓺ")):
                setattr(command_executor, bstack11l1lll_opy_ (u"ࠤࡢࡹࡷࡲࠢᓻ"), hub_url)
                result = True
        if result:
            self.bstack1l1l11l1l11_opy_ = hub_url
            bstack1lll111llll_opy_.bstack111111llll_opy_(instance, bstack1lll111llll_opy_.bstack1l1l1lll111_opy_, hub_url)
            bstack1lll111llll_opy_.bstack111111llll_opy_(
                instance, bstack1lll111llll_opy_.bstack1l11lll1l1l_opy_, bstack1lll111llll_opy_.bstack1ll11l1111l_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11lll11ll_opy_(bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_]):
        return bstack11l1lll_opy_ (u"ࠥ࠾ࠧᓼ").join((bstack1llllll1l11_opy_(bstack11111l11l1_opy_[0]).name, bstack11111ll1l1_opy_(bstack11111l11l1_opy_[1]).name))
    @staticmethod
    def bstack1ll1ll11111_opy_(bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_], callback: Callable):
        bstack1l11lll1l11_opy_ = bstack1lll111llll_opy_.bstack1l11lll11ll_opy_(bstack11111l11l1_opy_)
        if not bstack1l11lll1l11_opy_ in bstack1lll111llll_opy_.bstack1l11111l1ll_opy_:
            bstack1lll111llll_opy_.bstack1l11111l1ll_opy_[bstack1l11lll1l11_opy_] = []
        bstack1lll111llll_opy_.bstack1l11111l1ll_opy_[bstack1l11lll1l11_opy_].append(callback)
    def bstack1llllll1111_opy_(self, instance: bstack1llllll11ll_opy_, method_name: str, bstack1111111ll1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11l1lll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᓽ")):
            return
        cmd = args[0] if method_name == bstack11l1lll_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᓾ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l11111ll11_opy_ = bstack11l1lll_opy_ (u"ࠨ࠺ࠣᓿ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠣᔀ") + bstack1l11111ll11_opy_, bstack1111111ll1_opy_)
    def bstack111111ll1l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack11111ll1ll_opy_, bstack1l11lll1111_opy_ = bstack11111l11l1_opy_
        bstack1l11lll1l11_opy_ = bstack1lll111llll_opy_.bstack1l11lll11ll_opy_(bstack11111l11l1_opy_)
        self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡱࡱࡣ࡭ࡵ࡯࡬࠼ࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᔁ") + str(kwargs) + bstack11l1lll_opy_ (u"ࠤࠥᔂ"))
        if bstack11111ll1ll_opy_ == bstack1llllll1l11_opy_.QUIT:
            if bstack1l11lll1111_opy_ == bstack11111ll1l1_opy_.PRE:
                bstack1ll1l11llll_opy_ = bstack1lll1lll111_opy_.bstack1ll1l11l1ll_opy_(EVENTS.bstack1l1l1ll11_opy_.value)
                bstack1llllll111l_opy_.bstack111111llll_opy_(instance, EVENTS.bstack1l1l1ll11_opy_.value, bstack1ll1l11llll_opy_)
                self.logger.debug(bstack11l1lll_opy_ (u"ࠥ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠢᔃ").format(instance, method_name, bstack11111ll1ll_opy_, bstack1l11lll1111_opy_))
        if bstack11111ll1ll_opy_ == bstack1llllll1l11_opy_.bstack11111l1l11_opy_:
            if bstack1l11lll1111_opy_ == bstack11111ll1l1_opy_.POST and not bstack1lll111llll_opy_.bstack1l1l1lll11l_opy_ in instance.data:
                session_id = getattr(target, bstack11l1lll_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᔄ"), None)
                if session_id:
                    instance.data[bstack1lll111llll_opy_.bstack1l1l1lll11l_opy_] = session_id
        elif (
            bstack11111ll1ll_opy_ == bstack1llllll1l11_opy_.bstack11111l111l_opy_
            and bstack1lll111llll_opy_.bstack1l1l1111ll1_opy_(*args) == bstack1lll111llll_opy_.bstack1l1l11l1lll_opy_
        ):
            if bstack1l11lll1111_opy_ == bstack11111ll1l1_opy_.PRE:
                hub_url = bstack1lll111llll_opy_.bstack1ll1l11ll1_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1lll111llll_opy_.bstack1l1l1lll111_opy_: hub_url,
                            bstack1lll111llll_opy_.bstack1l11lll1l1l_opy_: bstack1lll111llll_opy_.bstack1ll11l1111l_opy_(hub_url),
                            bstack1lll111llll_opy_.bstack1ll11l1l1ll_opy_: int(
                                os.environ.get(bstack11l1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᔅ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll11l1l1l1_opy_ = bstack1lll111llll_opy_.bstack1ll11l111ll_opy_(*args)
                bstack1l11111l1l1_opy_ = bstack1ll11l1l1l1_opy_.get(bstack11l1lll_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᔆ"), None) if bstack1ll11l1l1l1_opy_ else None
                if isinstance(bstack1l11111l1l1_opy_, dict):
                    instance.data[bstack1lll111llll_opy_.bstack1l11111ll1l_opy_] = copy.deepcopy(bstack1l11111l1l1_opy_)
                    instance.data[bstack1lll111llll_opy_.bstack1l1l1llllll_opy_] = bstack1l11111l1l1_opy_
            elif bstack1l11lll1111_opy_ == bstack11111ll1l1_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11l1lll_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᔇ"), dict()).get(bstack11l1lll_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠦᔈ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1lll111llll_opy_.bstack1l1l1lll11l_opy_: framework_session_id,
                                bstack1lll111llll_opy_.bstack1l11111llll_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack11111ll1ll_opy_ == bstack1llllll1l11_opy_.bstack11111l111l_opy_
            and bstack1lll111llll_opy_.bstack1l1l1111ll1_opy_(*args) == bstack1lll111llll_opy_.bstack1l11111lll1_opy_
            and bstack1l11lll1111_opy_ == bstack11111ll1l1_opy_.POST
        ):
            instance.data[bstack1lll111llll_opy_.bstack1l11111l11l_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11lll1l11_opy_ in bstack1lll111llll_opy_.bstack1l11111l1ll_opy_:
            bstack1l11lll111l_opy_ = None
            for callback in bstack1lll111llll_opy_.bstack1l11111l1ll_opy_[bstack1l11lll1l11_opy_]:
                try:
                    bstack1l11ll1lll1_opy_ = callback(self, target, exec, bstack11111l11l1_opy_, result, *args, **kwargs)
                    if bstack1l11lll111l_opy_ == None:
                        bstack1l11lll111l_opy_ = bstack1l11ll1lll1_opy_
                except Exception as e:
                    self.logger.error(bstack11l1lll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࠢᔉ") + str(e) + bstack11l1lll_opy_ (u"ࠥࠦᔊ"))
                    traceback.print_exc()
            if bstack11111ll1ll_opy_ == bstack1llllll1l11_opy_.QUIT:
                if bstack1l11lll1111_opy_ == bstack11111ll1l1_opy_.POST:
                    bstack1ll1l11llll_opy_ = bstack1llllll111l_opy_.bstack1llllll11l1_opy_(instance, EVENTS.bstack1l1l1ll11_opy_.value)
                    if bstack1ll1l11llll_opy_!=None:
                        bstack1lll1lll111_opy_.end(EVENTS.bstack1l1l1ll11_opy_.value, bstack1ll1l11llll_opy_+bstack11l1lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᔋ"), bstack1ll1l11llll_opy_+bstack11l1lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᔌ"), True, None)
            if bstack1l11lll1111_opy_ == bstack11111ll1l1_opy_.PRE and callable(bstack1l11lll111l_opy_):
                return bstack1l11lll111l_opy_
            elif bstack1l11lll1111_opy_ == bstack11111ll1l1_opy_.POST and bstack1l11lll111l_opy_:
                return bstack1l11lll111l_opy_
    def bstack111111l1ll_opy_(
        self, method_name, previous_state: bstack1llllll1l11_opy_, *args, **kwargs
    ) -> bstack1llllll1l11_opy_:
        if method_name == bstack11l1lll_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣᔍ") or method_name == bstack11l1lll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᔎ"):
            return bstack1llllll1l11_opy_.bstack11111l1l11_opy_
        if method_name == bstack11l1lll_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᔏ"):
            return bstack1llllll1l11_opy_.QUIT
        if method_name == bstack11l1lll_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᔐ"):
            if previous_state != bstack1llllll1l11_opy_.NONE:
                bstack1ll11llllll_opy_ = bstack1lll111llll_opy_.bstack1l1l1111ll1_opy_(*args)
                if bstack1ll11llllll_opy_ == bstack1lll111llll_opy_.bstack1l1l11l1lll_opy_:
                    return bstack1llllll1l11_opy_.bstack11111l1l11_opy_
            return bstack1llllll1l11_opy_.bstack11111l111l_opy_
        return bstack1llllll1l11_opy_.NONE