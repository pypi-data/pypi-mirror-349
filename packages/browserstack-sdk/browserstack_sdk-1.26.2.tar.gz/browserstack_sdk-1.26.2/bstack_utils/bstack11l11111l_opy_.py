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
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1lll111lll_opy_ import get_logger
logger = get_logger(__name__)
bstack111l11l11l1_opy_: Dict[str, float] = {}
bstack111l11l1ll1_opy_: List = []
bstack111l11ll1ll_opy_ = 5
bstack111ll1l11_opy_ = os.path.join(os.getcwd(), bstack111l11_opy_ (u"ࠩ࡯ࡳ࡬࠭ᶭ"), bstack111l11_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭ᶮ"))
logging.getLogger(bstack111l11_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰ࠭ᶯ")).setLevel(logging.WARNING)
lock = FileLock(bstack111ll1l11_opy_+bstack111l11_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦᶰ"))
class bstack111l11l11ll_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack111l11ll111_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111l11ll111_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack111l11_opy_ (u"ࠨ࡭ࡦࡣࡶࡹࡷ࡫ࠢᶱ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1ll1ll1ll11_opy_:
    global bstack111l11l11l1_opy_
    @staticmethod
    def bstack1ll11ll11l1_opy_(key: str):
        bstack1ll1l11ll1l_opy_ = bstack1ll1ll1ll11_opy_.bstack11llll11111_opy_(key)
        bstack1ll1ll1ll11_opy_.mark(bstack1ll1l11ll1l_opy_+bstack111l11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᶲ"))
        return bstack1ll1l11ll1l_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111l11l11l1_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack111l11_opy_ (u"ࠣࡇࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᶳ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1ll1ll1ll11_opy_.mark(end)
            bstack1ll1ll1ll11_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack111l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴ࠼ࠣࡿࢂࠨᶴ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111l11l11l1_opy_ or end not in bstack111l11l11l1_opy_:
                logger.debug(bstack111l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡴࡢࡴࡷࠤࡰ࡫ࡹࠡࡹ࡬ࡸ࡭ࠦࡶࡢ࡮ࡸࡩࠥࢁࡽࠡࡱࡵࠤࡪࡴࡤࠡ࡭ࡨࡽࠥࡽࡩࡵࡪࠣࡺࡦࡲࡵࡦࠢࡾࢁࠧᶵ").format(start,end))
                return
            duration: float = bstack111l11l11l1_opy_[end] - bstack111l11l11l1_opy_[start]
            bstack111l11l1l11_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢᶶ"), bstack111l11_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦᶷ")).lower() == bstack111l11_opy_ (u"ࠨࡴࡳࡷࡨࠦᶸ")
            bstack111l11l1lll_opy_: bstack111l11l11ll_opy_ = bstack111l11l11ll_opy_(duration, label, bstack111l11l11l1_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack111l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢᶹ"), 0), command, test_name, hook_type, bstack111l11l1l11_opy_)
            del bstack111l11l11l1_opy_[start]
            del bstack111l11l11l1_opy_[end]
            bstack1ll1ll1ll11_opy_.bstack111l11ll1l1_opy_(bstack111l11l1lll_opy_)
        except Exception as e:
            logger.debug(bstack111l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡦࡣࡶࡹࡷ࡯࡮ࡨࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦᶺ").format(e))
    @staticmethod
    def bstack111l11ll1l1_opy_(bstack111l11l1lll_opy_):
        os.makedirs(os.path.dirname(bstack111ll1l11_opy_)) if not os.path.exists(os.path.dirname(bstack111ll1l11_opy_)) else None
        bstack1ll1ll1ll11_opy_.bstack111l11ll11l_opy_()
        try:
            with lock:
                with open(bstack111ll1l11_opy_, bstack111l11_opy_ (u"ࠤࡵ࠯ࠧᶻ"), encoding=bstack111l11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᶼ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack111l11l1lll_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111l11l1l1l_opy_:
            logger.debug(bstack111l11_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠥࢁࡽࠣᶽ").format(bstack111l11l1l1l_opy_))
            with lock:
                with open(bstack111ll1l11_opy_, bstack111l11_opy_ (u"ࠧࡽࠢᶾ"), encoding=bstack111l11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᶿ")) as file:
                    data = [bstack111l11l1lll_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack111l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡢࡲࡳࡩࡳࡪࠠࡼࡿࠥ᷀").format(str(e)))
        finally:
            if os.path.exists(bstack111ll1l11_opy_+bstack111l11_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢ᷁")):
                os.remove(bstack111ll1l11_opy_+bstack111l11_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫᷂ࠣ"))
    @staticmethod
    def bstack111l11ll11l_opy_():
        attempt = 0
        while (attempt < bstack111l11ll1ll_opy_):
            attempt += 1
            if os.path.exists(bstack111ll1l11_opy_+bstack111l11_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤ᷃")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11llll11111_opy_(label: str) -> str:
        try:
            return bstack111l11_opy_ (u"ࠦࢀࢃ࠺ࡼࡿࠥ᷄").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack111l11_opy_ (u"ࠧࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ᷅").format(e))