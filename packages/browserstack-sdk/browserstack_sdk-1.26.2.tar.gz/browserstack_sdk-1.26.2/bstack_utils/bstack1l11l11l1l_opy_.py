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
import threading
import logging
import bstack_utils.accessibility as bstack11lll1ll1_opy_
from bstack_utils.helper import bstack1l1lllll1l_opy_
logger = logging.getLogger(__name__)
def bstack111l111l1_opy_(bstack11111l1ll_opy_):
  return True if bstack11111l1ll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1l11ll1ll_opy_(context, *args):
    tags = getattr(args[0], bstack111l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᛞ"), [])
    bstack1llll1111_opy_ = bstack11lll1ll1_opy_.bstack1lllll1111_opy_(tags)
    threading.current_thread().isA11yTest = bstack1llll1111_opy_
    try:
      bstack1lll11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack111l111l1_opy_(bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩᛟ")) else context.browser
      if bstack1lll11lll_opy_ and bstack1lll11lll_opy_.session_id and bstack1llll1111_opy_ and bstack1l1lllll1l_opy_(
              threading.current_thread(), bstack111l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᛠ"), None):
          threading.current_thread().isA11yTest = bstack11lll1ll1_opy_.bstack1111ll1l_opy_(bstack1lll11lll_opy_, bstack1llll1111_opy_)
    except Exception as e:
       logger.debug(bstack111l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡢ࠳࠴ࡽࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬᛡ").format(str(e)))
def bstack1l1l1l11ll_opy_(bstack1lll11lll_opy_):
    if bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᛢ"), None) and bstack1l1lllll1l_opy_(
      threading.current_thread(), bstack111l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᛣ"), None) and not bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࠫᛤ"), False):
      threading.current_thread().a11y_stop = True
      bstack11lll1ll1_opy_.bstack1l1ll1ll1_opy_(bstack1lll11lll_opy_, name=bstack111l11_opy_ (u"ࠤࠥᛥ"), path=bstack111l11_opy_ (u"ࠥࠦᛦ"))