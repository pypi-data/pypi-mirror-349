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
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import bstack1111l1111l_opy_
class bstack1lll11l1lll_opy_(abc.ABC):
    bin_session_id: str
    bstack1111l111l1_opy_: bstack1111l1111l_opy_
    def __init__(self):
        self.bstack1lll111lll1_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111l111l1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1lll1ll1l11_opy_(self):
        return (self.bstack1lll111lll1_opy_ != None and self.bin_session_id != None and self.bstack1111l111l1_opy_ != None)
    def configure(self, bstack1lll111lll1_opy_, config, bin_session_id: str, bstack1111l111l1_opy_: bstack1111l1111l_opy_):
        self.bstack1lll111lll1_opy_ = bstack1lll111lll1_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111l111l1_opy_ = bstack1111l111l1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack111l11_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࡩࠦ࡭ࡰࡦࡸࡰࡪࠦࡻࡴࡧ࡯ࡪ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟࠯ࡡࡢࡲࡦࡳࡥࡠࡡࢀ࠾ࠥࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡃࠢᆻ") + str(self.bin_session_id) + bstack111l11_opy_ (u"ࠦࠧᆼ"))
    def bstack1ll1l1l1l1l_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack111l11_opy_ (u"ࠧࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦࡣࡢࡰࡱࡳࡹࠦࡢࡦࠢࡑࡳࡳ࡫ࠢᆽ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False