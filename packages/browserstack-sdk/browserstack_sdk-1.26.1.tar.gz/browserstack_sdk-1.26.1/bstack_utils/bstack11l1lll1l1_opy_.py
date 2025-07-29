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
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1l11l1lll_opy_ import get_logger
logger = get_logger(__name__)
bstack111l11ll1l1_opy_: Dict[str, float] = {}
bstack111l11ll1ll_opy_: List = []
bstack111l11l1ll1_opy_ = 5
bstack1l1l1ll1l_opy_ = os.path.join(os.getcwd(), bstack11l1lll_opy_ (u"ࠬࡲ࡯ࡨࠩᶢ"), bstack11l1lll_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩᶣ"))
logging.getLogger(bstack11l1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠩᶤ")).setLevel(logging.WARNING)
lock = FileLock(bstack1l1l1ll1l_opy_+bstack11l1lll_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢᶥ"))
class bstack111l11lll1l_opy_:
    duration: float
    name: str
    startTime: float
    worker: int
    status: bool
    failure: str
    details: Optional[str]
    entryType: str
    platform: Optional[int]
    command: Optional[str]
    hookType: Optional[str]
    cli: Optional[bool]
    def __init__(self, duration: float, name: str, start_time: float, bstack111l11lllll_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111l11lllll_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack11l1lll_opy_ (u"ࠤࡰࡩࡦࡹࡵࡳࡧࠥᶦ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll1lll111_opy_:
    global bstack111l11ll1l1_opy_
    @staticmethod
    def bstack1ll1l11l1ll_opy_(key: str):
        bstack1ll1l11llll_opy_ = bstack1lll1lll111_opy_.bstack11lll1l1111_opy_(key)
        bstack1lll1lll111_opy_.mark(bstack1ll1l11llll_opy_+bstack11l1lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᶧ"))
        return bstack1ll1l11llll_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111l11ll1l1_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack11l1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᶨ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll1lll111_opy_.mark(end)
            bstack1lll1lll111_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack11l1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷ࠿ࠦࡻࡾࠤᶩ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111l11ll1l1_opy_ or end not in bstack111l11ll1l1_opy_:
                logger.debug(bstack11l1lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࠠ࡬ࡧࡼࠤࡼ࡯ࡴࡩࠢࡹࡥࡱࡻࡥࠡࡽࢀࠤࡴࡸࠠࡦࡰࡧࠤࡰ࡫ࡹࠡࡹ࡬ࡸ࡭ࠦࡶࡢ࡮ࡸࡩࠥࢁࡽࠣᶪ").format(start,end))
                return
            duration: float = bstack111l11ll1l1_opy_[end] - bstack111l11ll1l1_opy_[start]
            bstack111l11ll111_opy_ = os.environ.get(bstack11l1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡉࡔࡡࡕ࡙ࡓࡔࡉࡏࡉࠥᶫ"), bstack11l1lll_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢᶬ")).lower() == bstack11l1lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᶭ")
            bstack111l11ll11l_opy_: bstack111l11lll1l_opy_ = bstack111l11lll1l_opy_(duration, label, bstack111l11ll1l1_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack11l1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᶮ"), 0), command, test_name, hook_type, bstack111l11ll111_opy_)
            del bstack111l11ll1l1_opy_[start]
            del bstack111l11ll1l1_opy_[end]
            bstack1lll1lll111_opy_.bstack111l11l1lll_opy_(bstack111l11ll11l_opy_)
        except Exception as e:
            logger.debug(bstack11l1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡩࡦࡹࡵࡳ࡫ࡱ࡫ࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢᶯ").format(e))
    @staticmethod
    def bstack111l11l1lll_opy_(bstack111l11ll11l_opy_):
        os.makedirs(os.path.dirname(bstack1l1l1ll1l_opy_)) if not os.path.exists(os.path.dirname(bstack1l1l1ll1l_opy_)) else None
        bstack1lll1lll111_opy_.bstack111l11lll11_opy_()
        try:
            with lock:
                with open(bstack1l1l1ll1l_opy_, bstack11l1lll_opy_ (u"ࠧࡸࠫࠣᶰ"), encoding=bstack11l1lll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᶱ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack111l11ll11l_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111l11llll1_opy_:
            logger.debug(bstack11l1lll_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠡࡽࢀࠦᶲ").format(bstack111l11llll1_opy_))
            with lock:
                with open(bstack1l1l1ll1l_opy_, bstack11l1lll_opy_ (u"ࠣࡹࠥᶳ"), encoding=bstack11l1lll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᶴ")) as file:
                    data = [bstack111l11ll11l_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack11l1lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡥࡵࡶࡥ࡯ࡦࠣࡿࢂࠨᶵ").format(str(e)))
        finally:
            if os.path.exists(bstack1l1l1ll1l_opy_+bstack11l1lll_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥᶶ")):
                os.remove(bstack1l1l1ll1l_opy_+bstack11l1lll_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦᶷ"))
    @staticmethod
    def bstack111l11lll11_opy_():
        attempt = 0
        while (attempt < bstack111l11l1ll1_opy_):
            attempt += 1
            if os.path.exists(bstack1l1l1ll1l_opy_+bstack11l1lll_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧᶸ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11lll1l1111_opy_(label: str) -> str:
        try:
            return bstack11l1lll_opy_ (u"ࠢࡼࡿ࠽ࡿࢂࠨᶹ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack11l1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᶺ").format(e))