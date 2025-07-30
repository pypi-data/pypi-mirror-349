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
import threading
from bstack_utils.helper import bstack1l1llll1_opy_
from bstack_utils.constants import bstack11ll11l1l11_opy_, EVENTS, STAGE
from bstack_utils.bstack1lll111lll_opy_ import get_logger
logger = get_logger(__name__)
class bstack1lllll1l1l_opy_:
    bstack1111lll11ll_opy_ = None
    @classmethod
    def bstack111l1ll1l_opy_(cls):
        if cls.on() and os.getenv(bstack111l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ῰")):
            logger.info(
                bstack111l11_opy_ (u"ࠨࡘ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠠࡵࡱࠣࡺ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡳࡳࡷࡺࠬࠡ࡫ࡱࡷ࡮࡭ࡨࡵࡵ࠯ࠤࡦࡴࡤࠡ࡯ࡤࡲࡾࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡢࡶࡩࡪ࡭ࡳ࡭ࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧ࡬࡭ࠢࡤࡸࠥࡵ࡮ࡦࠢࡳࡰࡦࡩࡥࠢ࡞ࡱࠫ῱").format(os.getenv(bstack111l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢῲ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧῳ"), None) is None or os.environ[bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨῴ")] == bstack111l11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ῵"):
            return False
        return True
    @classmethod
    def bstack11111ll1l1l_opy_(cls, bs_config, framework=bstack111l11_opy_ (u"ࠨࠢῶ")):
        bstack11ll1l11lll_opy_ = False
        for fw in bstack11ll11l1l11_opy_:
            if fw in framework:
                bstack11ll1l11lll_opy_ = True
        return bstack1l1llll1_opy_(bs_config.get(bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫῷ"), bstack11ll1l11lll_opy_))
    @classmethod
    def bstack11111l1l11l_opy_(cls, framework):
        return framework in bstack11ll11l1l11_opy_
    @classmethod
    def bstack1111l1l111l_opy_(cls, bs_config, framework):
        return cls.bstack11111ll1l1l_opy_(bs_config, framework) is True and cls.bstack11111l1l11l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack111l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬῸ"), None)
    @staticmethod
    def bstack11l1111l11_opy_():
        if getattr(threading.current_thread(), bstack111l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭Ό"), None):
            return {
                bstack111l11_opy_ (u"ࠪࡸࡾࡶࡥࠨῺ"): bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩΏ"),
                bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬῼ"): getattr(threading.current_thread(), bstack111l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ´"), None)
            }
        if getattr(threading.current_thread(), bstack111l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ῾"), None):
            return {
                bstack111l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭῿"): bstack111l11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ "),
                bstack111l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ "): getattr(threading.current_thread(), bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ "), None)
            }
        return None
    @staticmethod
    def bstack11111l1l111_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lllll1l1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111l11llll_opy_(test, hook_name=None):
        bstack11111l11lll_opy_ = test.parent
        if hook_name in [bstack111l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ "), bstack111l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ "), bstack111l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ "), bstack111l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪ ")]:
            bstack11111l11lll_opy_ = test
        scope = []
        while bstack11111l11lll_opy_ is not None:
            scope.append(bstack11111l11lll_opy_.name)
            bstack11111l11lll_opy_ = bstack11111l11lll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack11111l1l1l1_opy_(hook_type):
        if hook_type == bstack111l11_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢ "):
            return bstack111l11_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢ ")
        elif hook_type == bstack111l11_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣ "):
            return bstack111l11_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧ ")
    @staticmethod
    def bstack11111l11ll1_opy_(bstack1ll1l11111_opy_):
        try:
            if not bstack1lllll1l1l_opy_.on():
                return bstack1ll1l11111_opy_
            if os.environ.get(bstack111l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦ​"), None) == bstack111l11_opy_ (u"ࠢࡵࡴࡸࡩࠧ‌"):
                tests = os.environ.get(bstack111l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧ‍"), None)
                if tests is None or tests == bstack111l11_opy_ (u"ࠤࡱࡹࡱࡲࠢ‎"):
                    return bstack1ll1l11111_opy_
                bstack1ll1l11111_opy_ = tests.split(bstack111l11_opy_ (u"ࠪ࠰ࠬ‏"))
                return bstack1ll1l11111_opy_
        except Exception as exc:
            logger.debug(bstack111l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧ‐") + str(str(exc)) + bstack111l11_opy_ (u"ࠧࠨ‑"))
        return bstack1ll1l11111_opy_