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
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack11111llll1_opy_ import bstack1111l111l1_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll11l_opy_ import bstack11111l1lll_opy_, bstack11111ll11l_opy_
class bstack1ll1lll1111_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11l1lll_opy_ (u"ࠥࡘࡪࡹࡴࡉࡱࡲ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᔑ").format(self.name)
class bstack1lll11llll1_opy_(Enum):
    NONE = 0
    BEFORE_ALL = 1
    LOG = 2
    SETUP_FIXTURE = 3
    INIT_TEST = 4
    BEFORE_EACH = 5
    AFTER_EACH = 6
    TEST = 7
    STEP = 8
    LOG_REPORT = 9
    AFTER_ALL = 10
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack11l1lll_opy_ (u"࡙ࠦ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧᔒ").format(self.name)
class bstack1llll1111ll_opy_(bstack11111l1lll_opy_):
    bstack1ll1l1l1111_opy_: List[str]
    bstack1l111l1l11l_opy_: Dict[str, str]
    state: bstack1lll11llll1_opy_
    bstack11111ll111_opy_: datetime
    bstack111111l1l1_opy_: datetime
    def __init__(
        self,
        context: bstack11111ll11l_opy_,
        bstack1ll1l1l1111_opy_: List[str],
        bstack1l111l1l11l_opy_: Dict[str, str],
        state=bstack1lll11llll1_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1l1l1111_opy_ = bstack1ll1l1l1111_opy_
        self.bstack1l111l1l11l_opy_ = bstack1l111l1l11l_opy_
        self.state = state
        self.bstack11111ll111_opy_ = datetime.now(tz=timezone.utc)
        self.bstack111111l1l1_opy_ = datetime.now(tz=timezone.utc)
    def bstack111111llll_opy_(self, bstack11111l1ll1_opy_: bstack1lll11llll1_opy_):
        bstack1llllll1ll1_opy_ = bstack1lll11llll1_opy_(bstack11111l1ll1_opy_).name
        if not bstack1llllll1ll1_opy_:
            return False
        if bstack11111l1ll1_opy_ == self.state:
            return False
        self.state = bstack11111l1ll1_opy_
        self.bstack111111l1l1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l111l11l1l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1lll1l11111_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1ll1ll1l1_opy_: int = None
    bstack1l1llll11l1_opy_: str = None
    bstack111ll1l_opy_: str = None
    bstack1l11llll1l_opy_: str = None
    bstack1ll1111ll11_opy_: str = None
    bstack1l111l1l111_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll11lll11l_opy_ = bstack11l1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠣᔓ")
    bstack1l1111ll1l1_opy_ = bstack11l1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡮ࡪࠢᔔ")
    bstack1ll1l111lll_opy_ = bstack11l1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡴࡡ࡮ࡧࠥᔕ")
    bstack1l111lll1ll_opy_ = bstack11l1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡣࡵࡧࡴࡩࠤᔖ")
    bstack1l11l111lll_opy_ = bstack11l1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡵࡣࡪࡷࠧᔗ")
    bstack1l1l1l1l1ll_opy_ = bstack11l1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡨࡷࡺࡲࡴࠣᔘ")
    bstack1l1lll1l1l1_opy_ = bstack11l1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࡡࡤࡸࠧᔙ")
    bstack1ll1111l11l_opy_ = bstack11l1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᔚ")
    bstack1l1llll1l1l_opy_ = bstack11l1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡪࡴࡤࡦࡦࡢࡥࡹࠨᔛ")
    bstack1l11ll1l11l_opy_ = bstack11l1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᔜ")
    bstack1ll1l1lll1l_opy_ = bstack11l1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠢᔝ")
    bstack1l1lllllll1_opy_ = bstack11l1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠦᔞ")
    bstack1l111ll111l_opy_ = bstack11l1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡥࡲࡨࡪࠨᔟ")
    bstack1l1ll111l11_opy_ = bstack11l1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪࠨᔠ")
    bstack1ll11l1l1ll_opy_ = bstack11l1lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࠨᔡ")
    bstack1l1l1l11111_opy_ = bstack11l1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡧࡩ࡭ࡷࡵࡩࠧᔢ")
    bstack1l111l1ll11_opy_ = bstack11l1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠦᔣ")
    bstack1l11l1111ll_opy_ = bstack11l1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡩࡶࠦᔤ")
    bstack1l11l1l1ll1_opy_ = bstack11l1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡮ࡧࡷࡥࠧᔥ")
    bstack1l1111ll111_opy_ = bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡵࡦࡳࡵ࡫ࡳࠨᔦ")
    bstack1l11llll11l_opy_ = bstack11l1lll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧᔧ")
    bstack1l111ll1l1l_opy_ = bstack11l1lll_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᔨ")
    bstack1l11l11l111_opy_ = bstack11l1lll_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᔩ")
    bstack1l111l11111_opy_ = bstack11l1lll_opy_ (u"ࠢࡩࡱࡲ࡯ࡤ࡯ࡤࠣᔪ")
    bstack1l11l111l11_opy_ = bstack11l1lll_opy_ (u"ࠣࡪࡲࡳࡰࡥࡲࡦࡵࡸࡰࡹࠨᔫ")
    bstack1l1111ll1ll_opy_ = bstack11l1lll_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟࡭ࡱࡪࡷࠧᔬ")
    bstack1l11l111111_opy_ = bstack11l1lll_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪࠨᔭ")
    bstack1l11l111l1l_opy_ = bstack11l1lll_opy_ (u"ࠦࡱࡵࡧࡴࠤᔮ")
    bstack1l1111ll11l_opy_ = bstack11l1lll_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᔯ")
    bstack1l11l1lll1l_opy_ = bstack11l1lll_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢᔰ")
    bstack1l11l1l11ll_opy_ = bstack11l1lll_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣᔱ")
    bstack1l1lllll11l_opy_ = bstack11l1lll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠥᔲ")
    bstack1l1ll1llll1_opy_ = bstack11l1lll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡍࡑࡊࠦᔳ")
    bstack1l1llllllll_opy_ = bstack11l1lll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᔴ")
    bstack1lllllll111_opy_: Dict[str, bstack1llll1111ll_opy_] = dict()
    bstack1l11111l1ll_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1l1l1111_opy_: List[str]
    bstack1l111l1l11l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1l1l1111_opy_: List[str],
        bstack1l111l1l11l_opy_: Dict[str, str],
        bstack11111llll1_opy_: bstack1111l111l1_opy_
    ):
        self.bstack1ll1l1l1111_opy_ = bstack1ll1l1l1111_opy_
        self.bstack1l111l1l11l_opy_ = bstack1l111l1l11l_opy_
        self.bstack11111llll1_opy_ = bstack11111llll1_opy_
    def track_event(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll11llll1_opy_,
        test_hook_state: bstack1ll1lll1111_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11l1lll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤࡦࡸࡧࡴ࠿ࡾࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁࡽࠣᔵ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l11ll111l1_opy_(
        self,
        instance: bstack1llll1111ll_opy_,
        bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11lll1l11_opy_ = TestFramework.bstack1l11lll11ll_opy_(bstack11111l11l1_opy_)
        if not bstack1l11lll1l11_opy_ in TestFramework.bstack1l11111l1ll_opy_:
            return
        self.logger.debug(bstack11l1lll_opy_ (u"ࠧ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡼࡿࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࡸࠨᔶ").format(len(TestFramework.bstack1l11111l1ll_opy_[bstack1l11lll1l11_opy_])))
        for callback in TestFramework.bstack1l11111l1ll_opy_[bstack1l11lll1l11_opy_]:
            try:
                callback(self, instance, bstack11111l11l1_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11l1lll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂࠨᔷ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1lll11l1l_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1ll1l1lll_opy_(self, instance, bstack11111l11l1_opy_):
        return
    @abc.abstractmethod
    def bstack1ll11111l11_opy_(self, instance, bstack11111l11l1_opy_):
        return
    @staticmethod
    def bstack11111l1111_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack11111l1lll_opy_.create_context(target)
        instance = TestFramework.bstack1lllllll111_opy_.get(ctx.id, None)
        if instance and instance.bstack1llllllllll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1llllll1l_opy_(reverse=True) -> List[bstack1llll1111ll_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1lllllll111_opy_.values(),
            ),
            key=lambda t: t.bstack11111ll111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack111111l11l_opy_(ctx: bstack11111ll11l_opy_, reverse=True) -> List[bstack1llll1111ll_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1lllllll111_opy_.values(),
            ),
            key=lambda t: t.bstack11111ll111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111l11ll_opy_(instance: bstack1llll1111ll_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llllll11l1_opy_(instance: bstack1llll1111ll_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack111111llll_opy_(instance: bstack1llll1111ll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11l1lll_opy_ (u"ࠢࡴࡧࡷࡣࡸࡺࡡࡵࡧ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢ࡮ࡩࡾࡃࡻࡾࠢࡹࡥࡱࡻࡥ࠾ࡽࢀࠦᔸ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l1l1l1l_opy_(instance: bstack1llll1111ll_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11l1lll_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡪࡴࡴࡳ࡫ࡨࡷࡂࢁࡽࠣᔹ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l11111l111_opy_(instance: bstack1lll11llll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11l1lll_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡡࡶࡸࡦࡺࡥ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡬ࡧࡼࡁࢀࢃࠠࡷࡣ࡯ࡹࡪࡃࡻࡾࠤᔺ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack11111l1111_opy_(target, strict)
        return TestFramework.bstack1llllll11l1_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack11111l1111_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l111l1l1l1_opy_(instance: bstack1llll1111ll_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l11l11lll1_opy_(instance: bstack1llll1111ll_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11lll11ll_opy_(bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_]):
        return bstack11l1lll_opy_ (u"ࠥ࠾ࠧᔻ").join((bstack1lll11llll1_opy_(bstack11111l11l1_opy_[0]).name, bstack1ll1lll1111_opy_(bstack11111l11l1_opy_[1]).name))
    @staticmethod
    def bstack1ll1ll11111_opy_(bstack11111l11l1_opy_: Tuple[bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_], callback: Callable):
        bstack1l11lll1l11_opy_ = TestFramework.bstack1l11lll11ll_opy_(bstack11111l11l1_opy_)
        TestFramework.logger.debug(bstack11l1lll_opy_ (u"ࠦࡸ࡫ࡴࡠࡪࡲࡳࡰࡥࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢ࡫ࡳࡴࡱ࡟ࡳࡧࡪ࡭ࡸࡺࡲࡺࡡ࡮ࡩࡾࡃࡻࡾࠤᔼ").format(bstack1l11lll1l11_opy_))
        if not bstack1l11lll1l11_opy_ in TestFramework.bstack1l11111l1ll_opy_:
            TestFramework.bstack1l11111l1ll_opy_[bstack1l11lll1l11_opy_] = []
        TestFramework.bstack1l11111l1ll_opy_[bstack1l11lll1l11_opy_].append(callback)
    @staticmethod
    def bstack1l1lll1lll1_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11l1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡷ࡭ࡳࡹࠢᔽ"):
            return klass.__qualname__
        return module + bstack11l1lll_opy_ (u"ࠨ࠮ࠣᔾ") + klass.__qualname__
    @staticmethod
    def bstack1l1lll111ll_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}