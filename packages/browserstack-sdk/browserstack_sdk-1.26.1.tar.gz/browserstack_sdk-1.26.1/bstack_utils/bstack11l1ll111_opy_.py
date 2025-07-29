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
import threading
import logging
import bstack_utils.accessibility as bstack1l11111lll_opy_
from bstack_utils.helper import bstack111l11lll_opy_
logger = logging.getLogger(__name__)
def bstack111l11ll_opy_(bstack1l11ll1l_opy_):
  return True if bstack1l11ll1l_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1l1111lll_opy_(context, *args):
    tags = getattr(args[0], bstack11l1lll_opy_ (u"ࠬࡺࡡࡨࡵࠪᛓ"), [])
    bstack11ll1l111_opy_ = bstack1l11111lll_opy_.bstack1ll1l1l1ll_opy_(tags)
    threading.current_thread().isA11yTest = bstack11ll1l111_opy_
    try:
      bstack1llll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack111l11ll_opy_(bstack11l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬᛔ")) else context.browser
      if bstack1llll11l_opy_ and bstack1llll11l_opy_.session_id and bstack11ll1l111_opy_ and bstack111l11lll_opy_(
              threading.current_thread(), bstack11l1lll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᛕ"), None):
          threading.current_thread().isA11yTest = bstack1l11111lll_opy_.bstack1lll1ll11l_opy_(bstack1llll11l_opy_, bstack11ll1l111_opy_)
    except Exception as e:
       logger.debug(bstack11l1lll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡥ࠶࠷ࡹࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨᛖ").format(str(e)))
def bstack1ll111lll_opy_(bstack1llll11l_opy_):
    if bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᛗ"), None) and bstack111l11lll_opy_(
      threading.current_thread(), bstack11l1lll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᛘ"), None) and not bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡴࡶࠧᛙ"), False):
      threading.current_thread().a11y_stop = True
      bstack1l11111lll_opy_.bstack11l1l1ll1_opy_(bstack1llll11l_opy_, name=bstack11l1lll_opy_ (u"ࠧࠨᛚ"), path=bstack11l1lll_opy_ (u"ࠨࠢᛛ"))