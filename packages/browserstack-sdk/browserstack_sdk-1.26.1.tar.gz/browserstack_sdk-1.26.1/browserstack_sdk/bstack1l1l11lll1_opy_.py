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
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11ll111l1_opy_():
  def __init__(self, args, logger, bstack1111lll1ll_opy_, bstack1111ll1l1l_opy_, bstack1111l11lll_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111lll1ll_opy_ = bstack1111lll1ll_opy_
    self.bstack1111ll1l1l_opy_ = bstack1111ll1l1l_opy_
    self.bstack1111l11lll_opy_ = bstack1111l11lll_opy_
  def bstack1l1ll11l1l_opy_(self, bstack1111lll1l1_opy_, bstack1l111111l_opy_, bstack1111l1l111_opy_=False):
    bstack11lll1llll_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111ll1l11_opy_ = manager.list()
    bstack11ll1llll1_opy_ = Config.bstack1ll1l1l1l1_opy_()
    if bstack1111l1l111_opy_:
      for index, platform in enumerate(self.bstack1111lll1ll_opy_[bstack11l1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭သ")]):
        if index == 0:
          bstack1l111111l_opy_[bstack11l1lll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧဟ")] = self.args
        bstack11lll1llll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111lll1l1_opy_,
                                                    args=(bstack1l111111l_opy_, bstack1111ll1l11_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111lll1ll_opy_[bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨဠ")]):
        bstack11lll1llll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111lll1l1_opy_,
                                                    args=(bstack1l111111l_opy_, bstack1111ll1l11_opy_)))
    i = 0
    for t in bstack11lll1llll_opy_:
      try:
        if bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧအ")):
          os.environ[bstack11l1lll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨဢ")] = json.dumps(self.bstack1111lll1ll_opy_[bstack11l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫဣ")][i % self.bstack1111l11lll_opy_])
      except Exception as e:
        self.logger.debug(bstack11l1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤဤ").format(str(e)))
      i += 1
      t.start()
    for t in bstack11lll1llll_opy_:
      t.join()
    return list(bstack1111ll1l11_opy_)