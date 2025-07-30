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
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1l111lll1_opy_():
  def __init__(self, args, logger, bstack1111l1l11l_opy_, bstack1111lll1l1_opy_, bstack1111l11lll_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111l1l11l_opy_ = bstack1111l1l11l_opy_
    self.bstack1111lll1l1_opy_ = bstack1111lll1l1_opy_
    self.bstack1111l11lll_opy_ = bstack1111l11lll_opy_
  def bstack1llll111ll_opy_(self, bstack1111l1lll1_opy_, bstack1111lll11_opy_, bstack1111l1l111_opy_=False):
    bstack1lll1ll1ll_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111ll1lll_opy_ = manager.list()
    bstack111l111ll_opy_ = Config.bstack11l11lll1l_opy_()
    if bstack1111l1l111_opy_:
      for index, platform in enumerate(self.bstack1111l1l11l_opy_[bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭သ")]):
        if index == 0:
          bstack1111lll11_opy_[bstack111l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧဟ")] = self.args
        bstack1lll1ll1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l1lll1_opy_,
                                                    args=(bstack1111lll11_opy_, bstack1111ll1lll_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111l1l11l_opy_[bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨဠ")]):
        bstack1lll1ll1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l1lll1_opy_,
                                                    args=(bstack1111lll11_opy_, bstack1111ll1lll_opy_)))
    i = 0
    for t in bstack1lll1ll1ll_opy_:
      try:
        if bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧအ")):
          os.environ[bstack111l11_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨဢ")] = json.dumps(self.bstack1111l1l11l_opy_[bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫဣ")][i % self.bstack1111l11lll_opy_])
      except Exception as e:
        self.logger.debug(bstack111l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤဤ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1lll1ll1ll_opy_:
      t.join()
    return list(bstack1111ll1lll_opy_)