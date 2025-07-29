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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.accessibility as bstack1l11111lll_opy_
from browserstack_sdk.bstack11ll1l1l1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l11111111_opy_
from bstack_utils.bstack1l11l1l1l1_opy_ import bstack1l1l1l1ll1_opy_
from bstack_utils.constants import bstack1111l1l1l1_opy_
class bstack11ll1l111l_opy_:
    def __init__(self, args, logger, bstack1111lll1ll_opy_, bstack1111ll1l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111lll1ll_opy_ = bstack1111lll1ll_opy_
        self.bstack1111ll1l1l_opy_ = bstack1111ll1l1l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11lll1ll_opy_ = []
        self.bstack1111l1lll1_opy_ = None
        self.bstack1l11ll11l_opy_ = []
        self.bstack1111llll11_opy_ = self.bstack11lll11ll_opy_()
        self.bstack1l1l11111_opy_ = -1
    def bstack1l111111l_opy_(self, bstack1111ll11ll_opy_):
        self.parse_args()
        self.bstack1111l1llll_opy_()
        self.bstack1111ll1lll_opy_(bstack1111ll11ll_opy_)
        self.bstack1111l1l1ll_opy_()
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1111l1l11l_opy_():
        import importlib
        if getattr(importlib, bstack11l1lll_opy_ (u"ࠪࡪ࡮ࡴࡤࡠ࡮ࡲࡥࡩ࡫ࡲࠨ࿻"), False):
            bstack1111lll11l_opy_ = importlib.find_loader(bstack11l1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭࿼"))
        else:
            bstack1111lll11l_opy_ = importlib.util.find_spec(bstack11l1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ࿽"))
    def bstack1111ll111l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l1l11111_opy_ = -1
        if self.bstack1111ll1l1l_opy_ and bstack11l1lll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭࿾") in self.bstack1111lll1ll_opy_:
            self.bstack1l1l11111_opy_ = int(self.bstack1111lll1ll_opy_[bstack11l1lll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ࿿")])
        try:
            bstack1111ll1ll1_opy_ = [bstack11l1lll_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪက"), bstack11l1lll_opy_ (u"ࠩ࠰࠱ࡵࡲࡵࡨ࡫ࡱࡷࠬခ"), bstack11l1lll_opy_ (u"ࠪ࠱ࡵ࠭ဂ")]
            if self.bstack1l1l11111_opy_ >= 0:
                bstack1111ll1ll1_opy_.extend([bstack11l1lll_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬဃ"), bstack11l1lll_opy_ (u"ࠬ࠳࡮ࠨင")])
            for arg in bstack1111ll1ll1_opy_:
                self.bstack1111ll111l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1111l1llll_opy_(self):
        bstack1111l1lll1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1111l1lll1_opy_ = bstack1111l1lll1_opy_
        return bstack1111l1lll1_opy_
    def bstack11l1lll11_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack1111l1l11l_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l11111111_opy_)
    def bstack1111ll1lll_opy_(self, bstack1111ll11ll_opy_):
        bstack11ll1llll1_opy_ = Config.bstack1ll1l1l1l1_opy_()
        if bstack1111ll11ll_opy_:
            self.bstack1111l1lll1_opy_.append(bstack11l1lll_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪစ"))
            self.bstack1111l1lll1_opy_.append(bstack11l1lll_opy_ (u"ࠧࡕࡴࡸࡩࠬဆ"))
        if bstack11ll1llll1_opy_.bstack1111ll11l1_opy_():
            self.bstack1111l1lll1_opy_.append(bstack11l1lll_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧဇ"))
            self.bstack1111l1lll1_opy_.append(bstack11l1lll_opy_ (u"ࠩࡗࡶࡺ࡫ࠧဈ"))
        self.bstack1111l1lll1_opy_.append(bstack11l1lll_opy_ (u"ࠪ࠱ࡵ࠭ဉ"))
        self.bstack1111l1lll1_opy_.append(bstack11l1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠩည"))
        self.bstack1111l1lll1_opy_.append(bstack11l1lll_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧဋ"))
        self.bstack1111l1lll1_opy_.append(bstack11l1lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ဌ"))
        if self.bstack1l1l11111_opy_ > 1:
            self.bstack1111l1lll1_opy_.append(bstack11l1lll_opy_ (u"ࠧ࠮ࡰࠪဍ"))
            self.bstack1111l1lll1_opy_.append(str(self.bstack1l1l11111_opy_))
    def bstack1111l1l1ll_opy_(self):
        if bstack1l1l1l1ll1_opy_.bstack1l1ll11l_opy_(self.bstack1111lll1ll_opy_):
             self.bstack1111l1lll1_opy_ += [
                bstack1111l1l1l1_opy_.get(bstack11l1lll_opy_ (u"ࠨࡴࡨࡶࡺࡴࠧဎ")), str(bstack1l1l1l1ll1_opy_.bstack11l1ll1ll1_opy_(self.bstack1111lll1ll_opy_)),
                bstack1111l1l1l1_opy_.get(bstack11l1lll_opy_ (u"ࠩࡧࡩࡱࡧࡹࠨဏ")), str(bstack1111l1l1l1_opy_.get(bstack11l1lll_opy_ (u"ࠪࡶࡪࡸࡵ࡯࠯ࡧࡩࡱࡧࡹࠨတ")))
            ]
    def bstack1111l1ll11_opy_(self):
        bstack1l11ll11l_opy_ = []
        for spec in self.bstack11lll1ll_opy_:
            bstack1111l1111_opy_ = [spec]
            bstack1111l1111_opy_ += self.bstack1111l1lll1_opy_
            bstack1l11ll11l_opy_.append(bstack1111l1111_opy_)
        self.bstack1l11ll11l_opy_ = bstack1l11ll11l_opy_
        return bstack1l11ll11l_opy_
    def bstack11lll11ll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1111llll11_opy_ = True
            return True
        except Exception as e:
            self.bstack1111llll11_opy_ = False
        return self.bstack1111llll11_opy_
    def bstack1l1ll11l1l_opy_(self, bstack1111lll1l1_opy_, bstack1l111111l_opy_):
        bstack1l111111l_opy_[bstack11l1lll_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫထ")] = self.bstack1111lll1ll_opy_
        multiprocessing.set_start_method(bstack11l1lll_opy_ (u"ࠬࡹࡰࡢࡹࡱࠫဒ"))
        bstack11lll1llll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1111ll1l11_opy_ = manager.list()
        if bstack11l1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩဓ") in self.bstack1111lll1ll_opy_:
            for index, platform in enumerate(self.bstack1111lll1ll_opy_[bstack11l1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪန")]):
                bstack11lll1llll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1111lll1l1_opy_,
                                                            args=(self.bstack1111l1lll1_opy_, bstack1l111111l_opy_, bstack1111ll1l11_opy_)))
            bstack1111lll111_opy_ = len(self.bstack1111lll1ll_opy_[bstack11l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫပ")])
        else:
            bstack11lll1llll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1111lll1l1_opy_,
                                                        args=(self.bstack1111l1lll1_opy_, bstack1l111111l_opy_, bstack1111ll1l11_opy_)))
            bstack1111lll111_opy_ = 1
        i = 0
        for t in bstack11lll1llll_opy_:
            os.environ[bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩဖ")] = str(i)
            if bstack11l1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ဗ") in self.bstack1111lll1ll_opy_:
                os.environ[bstack11l1lll_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬဘ")] = json.dumps(self.bstack1111lll1ll_opy_[bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨမ")][i % bstack1111lll111_opy_])
            i += 1
            t.start()
        for t in bstack11lll1llll_opy_:
            t.join()
        return list(bstack1111ll1l11_opy_)
    @staticmethod
    def bstack11lll1ll11_opy_(driver, bstack1111l1ll1l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪယ"), None)
        if item and getattr(item, bstack11l1lll_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࠩရ"), None) and not getattr(item, bstack11l1lll_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࡤࡪ࡯࡯ࡧࠪလ"), False):
            logger.info(
                bstack11l1lll_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠣဝ"))
            bstack1111ll1111_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l11111lll_opy_.bstack11l1l1ll1_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)