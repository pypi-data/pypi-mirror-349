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
from browserstack_sdk.sdk_cli.bstack1lll11l1111_opy_ import bstack1lll11l1lll_opy_
from browserstack_sdk.sdk_cli.bstack111111l11l_opy_ import (
    bstack1llllll1l1l_opy_,
    bstack111111l1l1_opy_,
    bstack1lllllll1l1_opy_,
    bstack11111111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll111llll_opy_ import bstack1llll1ll111_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1l11l_opy_ import bstack1lll111ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1lll1_opy_ import bstack1lllllll11l_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1lll11l1111_opy_ import bstack1lll11l1lll_opy_
import weakref
class bstack1ll111ll111_opy_(bstack1lll11l1lll_opy_):
    bstack1ll111lllll_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack11111111ll_opy_]]
    pages: Dict[str, Tuple[Callable, bstack11111111ll_opy_]]
    def __init__(self, bstack1ll111lllll_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1ll111l11ll_opy_ = dict()
        self.bstack1ll111lllll_opy_ = bstack1ll111lllll_opy_
        self.frameworks = frameworks
        bstack1lll111ll1l_opy_.bstack1ll11ll11ll_opy_((bstack1llllll1l1l_opy_.bstack1lllllll1ll_opy_, bstack111111l1l1_opy_.POST), self.__1ll111ll1l1_opy_)
        if any(bstack1llll1ll111_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1llll1ll111_opy_.bstack1ll11ll11ll_opy_(
                (bstack1llllll1l1l_opy_.bstack111111111l_opy_, bstack111111l1l1_opy_.PRE), self.__1ll111lll11_opy_
            )
            bstack1llll1ll111_opy_.bstack1ll11ll11ll_opy_(
                (bstack1llllll1l1l_opy_.QUIT, bstack111111l1l1_opy_.POST), self.__1ll111l11l1_opy_
            )
    def __1ll111ll1l1_opy_(
        self,
        f: bstack1lll111ll1l_opy_,
        bstack1ll111l1l1l_opy_: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack111l11_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣᆾ"):
                return
            contexts = bstack1ll111l1l1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack111l11_opy_ (u"ࠢࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠧᆿ") in page.url:
                                self.logger.debug(bstack111l11_opy_ (u"ࠣࡕࡷࡳࡷ࡯࡮ࡨࠢࡷ࡬ࡪࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠥᇀ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1lllllll1l1_opy_.bstack111111ll1l_opy_(instance, self.bstack1ll111lllll_opy_, True)
                                self.logger.debug(bstack111l11_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡱࡣࡪࡩࡤ࡯࡮ࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᇁ") + str(instance.ref()) + bstack111l11_opy_ (u"ࠥࠦᇂ"))
        except Exception as e:
            self.logger.debug(bstack111l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡲࡪࡰࡪࠤࡳ࡫ࡷࠡࡲࡤ࡫ࡪࠦ࠺ࠣᇃ"),e)
    def __1ll111lll11_opy_(
        self,
        f: bstack1llll1ll111_opy_,
        driver: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1lllllll1l1_opy_.bstack1llllll1111_opy_(instance, self.bstack1ll111lllll_opy_, False):
            return
        if not f.bstack1ll11l111ll_opy_(f.hub_url(driver)):
            self.bstack1ll111l11ll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1lllllll1l1_opy_.bstack111111ll1l_opy_(instance, self.bstack1ll111lllll_opy_, True)
            self.logger.debug(bstack111l11_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡥࡴ࡬ࡺࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᇄ") + str(instance.ref()) + bstack111l11_opy_ (u"ࠨࠢᇅ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1lllllll1l1_opy_.bstack111111ll1l_opy_(instance, self.bstack1ll111lllll_opy_, True)
        self.logger.debug(bstack111l11_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᇆ") + str(instance.ref()) + bstack111l11_opy_ (u"ࠣࠤᇇ"))
    def __1ll111l11l1_opy_(
        self,
        f: bstack1llll1ll111_opy_,
        driver: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l1ll1_opy_: Tuple[bstack1llllll1l1l_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll111lll1l_opy_(instance)
        self.logger.debug(bstack111l11_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡴࡹ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᇈ") + str(instance.ref()) + bstack111l11_opy_ (u"ࠥࠦᇉ"))
    def bstack1ll111ll1ll_opy_(self, context: bstack1lllllll11l_opy_, reverse=True) -> List[Tuple[Callable, bstack11111111ll_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll111llll1_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1llll1ll111_opy_.bstack1ll111ll11l_opy_(data[1])
                    and data[1].bstack1ll111llll1_opy_(context)
                    and getattr(data[0](), bstack111l11_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᇊ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1llllll1ll1_opy_, reverse=reverse)
    def bstack1ll111l1l11_opy_(self, context: bstack1lllllll11l_opy_, reverse=True) -> List[Tuple[Callable, bstack11111111ll_opy_]]:
        matches = []
        for data in self.bstack1ll111l11ll_opy_.values():
            if (
                data[1].bstack1ll111llll1_opy_(context)
                and getattr(data[0](), bstack111l11_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᇋ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1llllll1ll1_opy_, reverse=reverse)
    def bstack1ll111l1lll_opy_(self, instance: bstack11111111ll_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll111lll1l_opy_(self, instance: bstack11111111ll_opy_) -> bool:
        if self.bstack1ll111l1lll_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1lllllll1l1_opy_.bstack111111ll1l_opy_(instance, self.bstack1ll111lllll_opy_, False)
            return True
        return False