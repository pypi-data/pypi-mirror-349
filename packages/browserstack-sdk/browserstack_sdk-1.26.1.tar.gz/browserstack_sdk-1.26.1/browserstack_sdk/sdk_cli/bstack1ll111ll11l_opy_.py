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
    bstack1llllll111l_opy_,
    bstack1llllll11ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll1l11l1_opy_ import bstack1lll111llll_opy_
from browserstack_sdk.sdk_cli.bstack1llll111l11_opy_ import bstack1lll11l111l_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll11l_opy_ import bstack11111ll11l_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1llll11l1ll_opy_ import bstack1llll1ll1l1_opy_
import weakref
class bstack1ll111lll11_opy_(bstack1llll1ll1l1_opy_):
    bstack1ll111l1lll_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1llllll11ll_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1llllll11ll_opy_]]
    def __init__(self, bstack1ll111l1lll_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1ll111llll1_opy_ = dict()
        self.bstack1ll111l1lll_opy_ = bstack1ll111l1lll_opy_
        self.frameworks = frameworks
        bstack1lll11l111l_opy_.bstack1ll1ll11111_opy_((bstack1llllll1l11_opy_.bstack11111l1l11_opy_, bstack11111ll1l1_opy_.POST), self.__1ll111lll1l_opy_)
        if any(bstack1lll111llll_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1lll111llll_opy_.bstack1ll1ll11111_opy_(
                (bstack1llllll1l11_opy_.bstack11111l111l_opy_, bstack11111ll1l1_opy_.PRE), self.__1ll111lllll_opy_
            )
            bstack1lll111llll_opy_.bstack1ll1ll11111_opy_(
                (bstack1llllll1l11_opy_.QUIT, bstack11111ll1l1_opy_.POST), self.__1ll111ll111_opy_
            )
    def __1ll111lll1l_opy_(
        self,
        f: bstack1lll11l111l_opy_,
        bstack1ll111l1l11_opy_: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack11l1lll_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣᆾ"):
                return
            contexts = bstack1ll111l1l11_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11l1lll_opy_ (u"ࠢࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠧᆿ") in page.url:
                                self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡕࡷࡳࡷ࡯࡮ࡨࠢࡷ࡬ࡪࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠥᇀ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1llllll111l_opy_.bstack111111llll_opy_(instance, self.bstack1ll111l1lll_opy_, True)
                                self.logger.debug(bstack11l1lll_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡱࡣࡪࡩࡤ࡯࡮ࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᇁ") + str(instance.ref()) + bstack11l1lll_opy_ (u"ࠥࠦᇂ"))
        except Exception as e:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡲࡪࡰࡪࠤࡳ࡫ࡷࠡࡲࡤ࡫ࡪࠦ࠺ࠣᇃ"),e)
    def __1ll111lllll_opy_(
        self,
        f: bstack1lll111llll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1llllll111l_opy_.bstack1llllll11l1_opy_(instance, self.bstack1ll111l1lll_opy_, False):
            return
        if not f.bstack1ll11l1111l_opy_(f.hub_url(driver)):
            self.bstack1ll111llll1_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1llllll111l_opy_.bstack111111llll_opy_(instance, self.bstack1ll111l1lll_opy_, True)
            self.logger.debug(bstack11l1lll_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡥࡴ࡬ࡺࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᇄ") + str(instance.ref()) + bstack11l1lll_opy_ (u"ࠨࠢᇅ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1llllll111l_opy_.bstack111111llll_opy_(instance, self.bstack1ll111l1lll_opy_, True)
        self.logger.debug(bstack11l1lll_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᇆ") + str(instance.ref()) + bstack11l1lll_opy_ (u"ࠣࠤᇇ"))
    def __1ll111ll111_opy_(
        self,
        f: bstack1lll111llll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll111l11ll_opy_(instance)
        self.logger.debug(bstack11l1lll_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡴࡹ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᇈ") + str(instance.ref()) + bstack11l1lll_opy_ (u"ࠥࠦᇉ"))
    def bstack1ll111l11l1_opy_(self, context: bstack11111ll11l_opy_, reverse=True) -> List[Tuple[Callable, bstack1llllll11ll_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll111l1ll1_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1lll111llll_opy_.bstack1ll111ll1l1_opy_(data[1])
                    and data[1].bstack1ll111l1ll1_opy_(context)
                    and getattr(data[0](), bstack11l1lll_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᇊ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack11111ll111_opy_, reverse=reverse)
    def bstack1ll111ll1ll_opy_(self, context: bstack11111ll11l_opy_, reverse=True) -> List[Tuple[Callable, bstack1llllll11ll_opy_]]:
        matches = []
        for data in self.bstack1ll111llll1_opy_.values():
            if (
                data[1].bstack1ll111l1ll1_opy_(context)
                and getattr(data[0](), bstack11l1lll_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᇋ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack11111ll111_opy_, reverse=reverse)
    def bstack1ll111l1l1l_opy_(self, instance: bstack1llllll11ll_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll111l11ll_opy_(self, instance: bstack1llllll11ll_opy_) -> bool:
        if self.bstack1ll111l1l1l_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1llllll111l_opy_.bstack111111llll_opy_(instance, self.bstack1ll111l1lll_opy_, False)
            return True
        return False