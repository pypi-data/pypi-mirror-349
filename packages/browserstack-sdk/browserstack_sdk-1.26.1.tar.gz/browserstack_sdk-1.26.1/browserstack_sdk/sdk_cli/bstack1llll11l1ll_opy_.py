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
import logging
import abc
from browserstack_sdk.sdk_cli.bstack11111llll1_opy_ import bstack1111l111l1_opy_
class bstack1llll1ll1l1_opy_(abc.ABC):
    bin_session_id: str
    bstack11111llll1_opy_: bstack1111l111l1_opy_
    def __init__(self):
        self.bstack1llll111ll1_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack11111llll1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1lll1l1lll1_opy_(self):
        return (self.bstack1llll111ll1_opy_ != None and self.bin_session_id != None and self.bstack11111llll1_opy_ != None)
    def configure(self, bstack1llll111ll1_opy_, config, bin_session_id: str, bstack11111llll1_opy_: bstack1111l111l1_opy_):
        self.bstack1llll111ll1_opy_ = bstack1llll111ll1_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack11111llll1_opy_ = bstack11111llll1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࡩࠦ࡭ࡰࡦࡸࡰࡪࠦࡻࡴࡧ࡯ࡪ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟࠯ࡡࡢࡲࡦࡳࡥࡠࡡࢀ࠾ࠥࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡃࠢᆻ") + str(self.bin_session_id) + bstack11l1lll_opy_ (u"ࠦࠧᆼ"))
    def bstack1ll1l11ll11_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11l1lll_opy_ (u"ࠧࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦࡣࡢࡰࡱࡳࡹࠦࡢࡦࠢࡑࡳࡳ࡫ࠢᆽ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False