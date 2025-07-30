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
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import bstack1111l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1lll1_opy_ import bstack1111111l1l_opy_, bstack1lllllll11l_opy_
class bstack1llll1lll1l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack111l11_opy_ (u"ࠢࡕࡧࡶࡸࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᔜ").format(self.name)
class bstack1lll1l111ll_opy_(Enum):
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
        return bstack111l11_opy_ (u"ࠣࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᔝ").format(self.name)
class bstack1lll11111l1_opy_(bstack1111111l1l_opy_):
    bstack1ll1l1l11l1_opy_: List[str]
    bstack1l11l1l11ll_opy_: Dict[str, str]
    state: bstack1lll1l111ll_opy_
    bstack1llllll1ll1_opy_: datetime
    bstack11111ll1ll_opy_: datetime
    def __init__(
        self,
        context: bstack1lllllll11l_opy_,
        bstack1ll1l1l11l1_opy_: List[str],
        bstack1l11l1l11ll_opy_: Dict[str, str],
        state=bstack1lll1l111ll_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1l1l11l1_opy_ = bstack1ll1l1l11l1_opy_
        self.bstack1l11l1l11ll_opy_ = bstack1l11l1l11ll_opy_
        self.state = state
        self.bstack1llllll1ll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack11111ll1ll_opy_ = datetime.now(tz=timezone.utc)
    def bstack111111ll1l_opy_(self, bstack1llllll1lll_opy_: bstack1lll1l111ll_opy_):
        bstack1111111111_opy_ = bstack1lll1l111ll_opy_(bstack1llllll1lll_opy_).name
        if not bstack1111111111_opy_:
            return False
        if bstack1llllll1lll_opy_ == self.state:
            return False
        self.state = bstack1llllll1lll_opy_
        self.bstack11111ll1ll_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l111l111l1_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1lll1l11l11_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1llllllll_opy_: int = None
    bstack1l1ll1l1111_opy_: str = None
    bstack1ll1lll_opy_: str = None
    bstack111l1l1l_opy_: str = None
    bstack1l1lll111l1_opy_: str = None
    bstack1l1111llll1_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll11lll11l_opy_ = bstack111l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧᔞ")
    bstack1l111llllll_opy_ = bstack111l11_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡫ࡧࠦᔟ")
    bstack1ll1l111l11_opy_ = bstack111l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠢᔠ")
    bstack1l111l1l1l1_opy_ = bstack111l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡠࡲࡤࡸ࡭ࠨᔡ")
    bstack1l1111ll11l_opy_ = bstack111l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡹࡧࡧࡴࠤᔢ")
    bstack1l1l1l111l1_opy_ = bstack111l11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᔣ")
    bstack1l1lll11111_opy_ = bstack111l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࡥࡡࡵࠤᔤ")
    bstack1ll11111111_opy_ = bstack111l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᔥ")
    bstack1ll11111lll_opy_ = bstack111l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᔦ")
    bstack1l1111l1lll_opy_ = bstack111l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᔧ")
    bstack1ll11ll1lll_opy_ = bstack111l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠦᔨ")
    bstack1ll11111l1l_opy_ = bstack111l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᔩ")
    bstack1l111ll11ll_opy_ = bstack111l11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡩ࡯ࡥࡧࠥᔪ")
    bstack1l1ll111l11_opy_ = bstack111l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠥᔫ")
    bstack1ll1l111lll_opy_ = bstack111l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠥᔬ")
    bstack1l1l1l111ll_opy_ = bstack111l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࠤᔭ")
    bstack1l11l1l1111_opy_ = bstack111l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠣᔮ")
    bstack1l11l11llll_opy_ = bstack111l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴ࡭ࡳࠣᔯ")
    bstack1l1111ll1ll_opy_ = bstack111l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡲ࡫ࡴࡢࠤᔰ")
    bstack1l1111l11l1_opy_ = bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡹࡣࡰࡲࡨࡷࠬᔱ")
    bstack1l11llll1l1_opy_ = bstack111l11_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤᔲ")
    bstack1l111l111ll_opy_ = bstack111l11_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᔳ")
    bstack1l11l1l1l11_opy_ = bstack111l11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᔴ")
    bstack1l11l1lll11_opy_ = bstack111l11_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡ࡬ࡨࠧᔵ")
    bstack1l11ll111l1_opy_ = bstack111l11_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡶࡪࡹࡵ࡭ࡶࠥᔶ")
    bstack1l111ll1l1l_opy_ = bstack111l11_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡱࡵࡧࡴࠤᔷ")
    bstack1l11l11l1ll_opy_ = bstack111l11_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠥᔸ")
    bstack1l11l1l111l_opy_ = bstack111l11_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᔹ")
    bstack1l11l1ll1l1_opy_ = bstack111l11_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᔺ")
    bstack1l11l111lll_opy_ = bstack111l11_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦᔻ")
    bstack1l111l1l1ll_opy_ = bstack111l11_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧᔼ")
    bstack1l1ll1lll11_opy_ = bstack111l11_opy_ (u"࡚ࠧࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠢᔽ")
    bstack1ll111l1111_opy_ = bstack111l11_opy_ (u"ࠨࡔࡆࡕࡗࡣࡑࡕࡇࠣᔾ")
    bstack1l1llll1ll1_opy_ = bstack111l11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᔿ")
    bstack1111111l11_opy_: Dict[str, bstack1lll11111l1_opy_] = dict()
    bstack1l11111l1ll_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1l1l11l1_opy_: List[str]
    bstack1l11l1l11ll_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1l1l11l1_opy_: List[str],
        bstack1l11l1l11ll_opy_: Dict[str, str],
        bstack1111l111l1_opy_: bstack1111l1111l_opy_
    ):
        self.bstack1ll1l1l11l1_opy_ = bstack1ll1l1l11l1_opy_
        self.bstack1l11l1l11ll_opy_ = bstack1l11l1l11ll_opy_
        self.bstack1111l111l1_opy_ = bstack1111l111l1_opy_
    def track_event(
        self,
        context: bstack1l111l111l1_opy_,
        test_framework_state: bstack1lll1l111ll_opy_,
        test_hook_state: bstack1llll1lll1l_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack111l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡣࡵ࡫ࡸࡃࡻࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾࢁࠧᕀ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l11l11l1l1_opy_(
        self,
        instance: bstack1lll11111l1_opy_,
        bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11ll1llll_opy_ = TestFramework.bstack1l11lll11l1_opy_(bstack11111l1ll1_opy_)
        if not bstack1l11ll1llll_opy_ in TestFramework.bstack1l11111l1ll_opy_:
            return
        self.logger.debug(bstack111l11_opy_ (u"ࠤ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࢀࢃࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠥᕁ").format(len(TestFramework.bstack1l11111l1ll_opy_[bstack1l11ll1llll_opy_])))
        for callback in TestFramework.bstack1l11111l1ll_opy_[bstack1l11ll1llll_opy_]:
            try:
                callback(self, instance, bstack11111l1ll1_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack111l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠥᕂ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1lll11lll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1ll1l111l_opy_(self, instance, bstack11111l1ll1_opy_):
        return
    @abc.abstractmethod
    def bstack1l1lllll1ll_opy_(self, instance, bstack11111l1ll1_opy_):
        return
    @staticmethod
    def bstack11111ll111_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1111111l1l_opy_.create_context(target)
        instance = TestFramework.bstack1111111l11_opy_.get(ctx.id, None)
        if instance and instance.bstack111111llll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1ll1l1ll1_opy_(reverse=True) -> List[bstack1lll11111l1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1111111l11_opy_.values(),
            ),
            key=lambda t: t.bstack1llllll1ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllll1llll_opy_(ctx: bstack1lllllll11l_opy_, reverse=True) -> List[bstack1lll11111l1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1111111l11_opy_.values(),
            ),
            key=lambda t: t.bstack1llllll1ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111ll11l_opy_(instance: bstack1lll11111l1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llllll1111_opy_(instance: bstack1lll11111l1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack111111ll1l_opy_(instance: bstack1lll11111l1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack111l11_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡫ࡦࡻࡀࡿࢂࠦࡶࡢ࡮ࡸࡩࡂࢁࡽࠣᕃ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l111lll1l1_opy_(instance: bstack1lll11111l1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack111l11_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡࡧࡱࡸࡷ࡯ࡥࡴ࠿ࡾࢁࠧᕄ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l111111ll1_opy_(instance: bstack1lll1l111ll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack111l11_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡰ࡫ࡹ࠾ࡽࢀࠤࡻࡧ࡬ࡶࡧࡀࡿࢂࠨᕅ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack11111ll111_opy_(target, strict)
        return TestFramework.bstack1llllll1111_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack11111ll111_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11ll111ll_opy_(instance: bstack1lll11111l1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l111ll1111_opy_(instance: bstack1lll11111l1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11lll11l1_opy_(bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_]):
        return bstack111l11_opy_ (u"ࠢ࠻ࠤᕆ").join((bstack1lll1l111ll_opy_(bstack11111l1ll1_opy_[0]).name, bstack1llll1lll1l_opy_(bstack11111l1ll1_opy_[1]).name))
    @staticmethod
    def bstack1ll11ll11ll_opy_(bstack11111l1ll1_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_], callback: Callable):
        bstack1l11ll1llll_opy_ = TestFramework.bstack1l11lll11l1_opy_(bstack11111l1ll1_opy_)
        TestFramework.logger.debug(bstack111l11_opy_ (u"ࠣࡵࡨࡸࡤ࡮࡯ࡰ࡭ࡢࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡨࡰࡱ࡮ࡣࡷ࡫ࡧࡪࡵࡷࡶࡾࡥ࡫ࡦࡻࡀࡿࢂࠨᕇ").format(bstack1l11ll1llll_opy_))
        if not bstack1l11ll1llll_opy_ in TestFramework.bstack1l11111l1ll_opy_:
            TestFramework.bstack1l11111l1ll_opy_[bstack1l11ll1llll_opy_] = []
        TestFramework.bstack1l11111l1ll_opy_[bstack1l11ll1llll_opy_].append(callback)
    @staticmethod
    def bstack1l1ll1llll1_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack111l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡴࡪࡰࡶࠦᕈ"):
            return klass.__qualname__
        return module + bstack111l11_opy_ (u"ࠥ࠲ࠧᕉ") + klass.__qualname__
    @staticmethod
    def bstack1l1lllll111_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}