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
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack1l11111ll1_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack11l1l1l1ll_opy_:
    pass
class bstack1l1111l1ll_opy_:
    bstack1lllllll11_opy_ = bstack111l11_opy_ (u"ࠨࡢࡰࡱࡷࡷࡹࡸࡡࡱࠤჺ")
    CONNECT = bstack111l11_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࠣ჻")
    bstack11ll1l1l1_opy_ = bstack111l11_opy_ (u"ࠣࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠥჼ")
    CONFIG = bstack111l11_opy_ (u"ࠤࡦࡳࡳ࡬ࡩࡨࠤჽ")
    bstack1ll1ll11ll1_opy_ = bstack111l11_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡹࠢჾ")
    bstack11l1ll1l_opy_ = bstack111l11_opy_ (u"ࠦࡪࡾࡩࡵࠤჿ")
class bstack1ll1ll1l111_opy_:
    bstack1ll1ll1l1l1_opy_ = bstack111l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡸࡺࡡࡳࡶࡨࡨࠧᄀ")
    FINISHED = bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᄁ")
class bstack1ll1ll11lll_opy_:
    bstack1ll1ll1l1l1_opy_ = bstack111l11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡶࡸࡦࡸࡴࡦࡦࠥᄂ")
    FINISHED = bstack111l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᄃ")
class bstack1ll1ll11l1l_opy_:
    bstack1ll1ll1l1l1_opy_ = bstack111l11_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡸࡺࡡࡳࡶࡨࡨࠧᄄ")
    FINISHED = bstack111l11_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᄅ")
class bstack1ll1ll1l11l_opy_:
    bstack1ll1ll1l1ll_opy_ = bstack111l11_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡦࡶࡪࡧࡴࡦࡦࠥᄆ")
class bstack1ll1ll11l11_opy_:
    _1llll1l1lll_opy_ = None
    def __new__(cls):
        if not cls._1llll1l1lll_opy_:
            cls._1llll1l1lll_opy_ = super(bstack1ll1ll11l11_opy_, cls).__new__(cls)
        return cls._1llll1l1lll_opy_
    def __init__(self):
        self._hooks = defaultdict(lambda: defaultdict(list))
        self._lock = Lock()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def clear(self):
        with self._lock:
            self._hooks = defaultdict(list)
    def register(self, event_name, callback):
        with self._lock:
            if not callable(callback):
                raise ValueError(bstack111l11_opy_ (u"ࠧࡉࡡ࡭࡮ࡥࡥࡨࡱࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡥࡤࡰࡱࡧࡢ࡭ࡧࠣࡪࡴࡸࠠࠣᄇ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack111l11_opy_ (u"ࠨࡒࡦࡩ࡬ࡷࡹ࡫ࡲࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࠢࠪࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠩࠣࡻ࡮ࡺࡨࠡࡲ࡬ࡨࠥࠨᄈ") + str(pid) + bstack111l11_opy_ (u"ࠢࠣᄉ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack111l11_opy_ (u"ࠣࡐࡲࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࠣࠫࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠪࠤࡼ࡯ࡴࡩࠢࡳ࡭ࡩࠦࠢᄊ") + str(pid) + bstack111l11_opy_ (u"ࠤࠥᄋ"))
                return
            self.logger.debug(bstack111l11_opy_ (u"ࠥࡍࡳࡼ࡯࡬࡫ࡱ࡫ࠥࢁ࡬ࡦࡰࠫࡧࡦࡲ࡬ࡣࡣࡦ࡯ࡸ࠯ࡽࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࡶࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࠠࠨࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠧࠡࡹ࡬ࡸ࡭ࠦࡰࡪࡦࠣࠦᄌ") + str(pid) + bstack111l11_opy_ (u"ࠦࠧᄍ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack111l11_opy_ (u"ࠧࡏ࡮ࡷࡱ࡮ࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࠤࠬࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠫࠥࡽࡩࡵࡪࠣࡴ࡮ࡪࠠࠣᄎ") + str(pid) + bstack111l11_opy_ (u"ࠨࠢᄏ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack111l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࠦࠧࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂ࠭ࠠࡸ࡫ࡷ࡬ࠥࡶࡩࡥࠢࡾࡴ࡮ࡪࡽ࠻ࠢࠥᄐ") + str(e) + bstack111l11_opy_ (u"ࠣࠤᄑ"))
                    traceback.print_exc()
bstack1ll11l11l_opy_ = bstack1ll1ll11l11_opy_()