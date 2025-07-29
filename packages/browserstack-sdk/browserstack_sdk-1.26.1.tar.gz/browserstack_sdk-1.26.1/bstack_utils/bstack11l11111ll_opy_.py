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
import threading
from bstack_utils.helper import bstack1llll1l11_opy_
from bstack_utils.constants import bstack11ll11lll11_opy_, EVENTS, STAGE
from bstack_utils.bstack1l11l1lll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11l111l11l_opy_:
    bstack1111llll1ll_opy_ = None
    @classmethod
    def bstack1llll1111l_opy_(cls):
        if cls.on() and os.getenv(bstack11l1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣῥ")):
            logger.info(
                bstack11l1lll_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧῦ").format(os.getenv(bstack11l1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥῧ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪῨ"), None) is None or os.environ[bstack11l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫῩ")] == bstack11l1lll_opy_ (u"ࠣࡰࡸࡰࡱࠨῪ"):
            return False
        return True
    @classmethod
    def bstack11111ll1l11_opy_(cls, bs_config, framework=bstack11l1lll_opy_ (u"ࠤࠥΎ")):
        bstack11ll1l11lll_opy_ = False
        for fw in bstack11ll11lll11_opy_:
            if fw in framework:
                bstack11ll1l11lll_opy_ = True
        return bstack1llll1l11_opy_(bs_config.get(bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧῬ"), bstack11ll1l11lll_opy_))
    @classmethod
    def bstack11111l1ll1l_opy_(cls, framework):
        return framework in bstack11ll11lll11_opy_
    @classmethod
    def bstack1111l1l11ll_opy_(cls, bs_config, framework):
        return cls.bstack11111ll1l11_opy_(bs_config, framework) is True and cls.bstack11111l1ll1l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11l1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ῭"), None)
    @staticmethod
    def bstack111lll1111_opy_():
        if getattr(threading.current_thread(), bstack11l1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ΅"), None):
            return {
                bstack11l1lll_opy_ (u"࠭ࡴࡺࡲࡨࠫ`"): bstack11l1lll_opy_ (u"ࠧࡵࡧࡶࡸࠬ῰"),
                bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ῱"): getattr(threading.current_thread(), bstack11l1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ῲ"), None)
            }
        if getattr(threading.current_thread(), bstack11l1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧῳ"), None):
            return {
                bstack11l1lll_opy_ (u"ࠫࡹࡿࡰࡦࠩῴ"): bstack11l1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ῵"),
                bstack11l1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ῶ"): getattr(threading.current_thread(), bstack11l1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫῷ"), None)
            }
        return None
    @staticmethod
    def bstack11111l1l1ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l111l11l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111l1lll1l_opy_(test, hook_name=None):
        bstack11111l1l1l1_opy_ = test.parent
        if hook_name in [bstack11l1lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭Ὸ"), bstack11l1lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪΌ"), bstack11l1lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩῺ"), bstack11l1lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭Ώ")]:
            bstack11111l1l1l1_opy_ = test
        scope = []
        while bstack11111l1l1l1_opy_ is not None:
            scope.append(bstack11111l1l1l1_opy_.name)
            bstack11111l1l1l1_opy_ = bstack11111l1l1l1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack11111l1ll11_opy_(hook_type):
        if hook_type == bstack11l1lll_opy_ (u"ࠧࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠥῼ"):
            return bstack11l1lll_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡮࡯ࡰ࡭ࠥ´")
        elif hook_type == bstack11l1lll_opy_ (u"ࠢࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠦ῾"):
            return bstack11l1lll_opy_ (u"ࠣࡖࡨࡥࡷࡪ࡯ࡸࡰࠣ࡬ࡴࡵ࡫ࠣ῿")
    @staticmethod
    def bstack11111l1lll1_opy_(bstack11lll1ll_opy_):
        try:
            if not bstack11l111l11l_opy_.on():
                return bstack11lll1ll_opy_
            if os.environ.get(bstack11l1lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠢ "), None) == bstack11l1lll_opy_ (u"ࠥࡸࡷࡻࡥࠣ "):
                tests = os.environ.get(bstack11l1lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠣ "), None)
                if tests is None or tests == bstack11l1lll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ "):
                    return bstack11lll1ll_opy_
                bstack11lll1ll_opy_ = tests.split(bstack11l1lll_opy_ (u"࠭ࠬࠨ "))
                return bstack11lll1ll_opy_
        except Exception as exc:
            logger.debug(bstack11l1lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡦࡴࡸࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡀࠠࠣ ") + str(str(exc)) + bstack11l1lll_opy_ (u"ࠣࠤ "))
        return bstack11lll1ll_opy_