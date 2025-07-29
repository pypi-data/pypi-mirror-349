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
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1lllllll11l_opy_ import bstack11111l1lll_opy_, bstack11111ll11l_opy_
import os
import threading
class bstack11111ll1l1_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11l1lll_opy_ (u"ࠤࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣါ").format(self.name)
class bstack1llllll1l11_opy_(Enum):
    NONE = 0
    bstack11111l1l11_opy_ = 1
    bstack1lllllllll1_opy_ = 3
    bstack11111l111l_opy_ = 4
    bstack1llllll1lll_opy_ = 5
    QUIT = 6
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack11l1lll_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥာ").format(self.name)
class bstack1llllll11ll_opy_(bstack11111l1lll_opy_):
    framework_name: str
    framework_version: str
    state: bstack1llllll1l11_opy_
    previous_state: bstack1llllll1l11_opy_
    bstack11111ll111_opy_: datetime
    bstack111111l1l1_opy_: datetime
    def __init__(
        self,
        context: bstack11111ll11l_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1llllll1l11_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1llllll1l11_opy_.NONE
        self.bstack11111ll111_opy_ = datetime.now(tz=timezone.utc)
        self.bstack111111l1l1_opy_ = datetime.now(tz=timezone.utc)
    def bstack111111llll_opy_(self, bstack11111l1ll1_opy_: bstack1llllll1l11_opy_):
        bstack1llllll1ll1_opy_ = bstack1llllll1l11_opy_(bstack11111l1ll1_opy_).name
        if not bstack1llllll1ll1_opy_:
            return False
        if bstack11111l1ll1_opy_ == self.state:
            return False
        if self.state == bstack1llllll1l11_opy_.bstack1lllllllll1_opy_: # bstack1lllllll1l1_opy_ bstack11111l1l1l_opy_ for bstack1111111l1l_opy_ in bstack111111ll11_opy_, it bstack1111111l11_opy_ bstack1lllll1lll1_opy_ bstack1llllllll11_opy_ times bstack1lllllll1ll_opy_ a new state
            return True
        if (
            bstack11111l1ll1_opy_ == bstack1llllll1l11_opy_.NONE
            or (self.state != bstack1llllll1l11_opy_.NONE and bstack11111l1ll1_opy_ == bstack1llllll1l11_opy_.bstack11111l1l11_opy_)
            or (self.state < bstack1llllll1l11_opy_.bstack11111l1l11_opy_ and bstack11111l1ll1_opy_ == bstack1llllll1l11_opy_.bstack11111l111l_opy_)
            or (self.state < bstack1llllll1l11_opy_.bstack11111l1l11_opy_ and bstack11111l1ll1_opy_ == bstack1llllll1l11_opy_.QUIT)
        ):
            raise ValueError(bstack11l1lll_opy_ (u"ࠦ࡮ࡴࡶࡢ࡮࡬ࡨࠥࡹࡴࡢࡶࡨࠤࡹࡸࡡ࡯ࡵ࡬ࡸ࡮ࡵ࡮࠻ࠢࠥိ") + str(self.state) + bstack11l1lll_opy_ (u"ࠧࠦ࠽࠿ࠢࠥီ") + str(bstack11111l1ll1_opy_))
        self.previous_state = self.state
        self.state = bstack11111l1ll1_opy_
        self.bstack111111l1l1_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1llllll111l_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1lllllll111_opy_: Dict[str, bstack1llllll11ll_opy_] = dict()
    framework_name: str
    framework_version: str
    classes: List[Type]
    def __init__(
        self,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
    ):
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.classes = classes
    @abc.abstractmethod
    def bstack1llllll1111_opy_(self, instance: bstack1llllll11ll_opy_, method_name: str, bstack1111111ll1_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack111111l1ll_opy_(
        self, method_name, previous_state: bstack1llllll1l11_opy_, *args, **kwargs
    ) -> bstack1llllll1l11_opy_:
        return
    @abc.abstractmethod
    def bstack111111ll1l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llllll11ll_opy_, str],
        bstack11111l11l1_opy_: Tuple[bstack1llllll1l11_opy_, bstack11111ll1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack11111111l1_opy_(self, bstack111111l111_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack111111l111_opy_:
                bstack111111111l_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack111111111l_opy_):
                    self.logger.warning(bstack11l1lll_opy_ (u"ࠨࡵ࡯ࡲࡤࡸࡨ࡮ࡥࡥࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࠦု") + str(method_name) + bstack11l1lll_opy_ (u"ࠢࠣူ"))
                    continue
                bstack11111ll1ll_opy_ = self.bstack111111l1ll_opy_(
                    method_name, previous_state=bstack1llllll1l11_opy_.NONE
                )
                bstack1llllllll1l_opy_ = self.bstack1111111lll_opy_(
                    method_name,
                    (bstack11111ll1ll_opy_ if bstack11111ll1ll_opy_ else bstack1llllll1l11_opy_.NONE),
                    bstack111111111l_opy_,
                )
                if not callable(bstack1llllllll1l_opy_):
                    self.logger.warning(bstack11l1lll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠡࡰࡲࡸࠥࡶࡡࡵࡥ࡫ࡩࡩࡀࠠࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࠩࡽࡶࡩࡱ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾ࠼ࠣࠦေ") + str(self.framework_version) + bstack11l1lll_opy_ (u"ࠤࠬࠦဲ"))
                    continue
                setattr(clazz, method_name, bstack1llllllll1l_opy_)
    def bstack1111111lll_opy_(
        self,
        method_name: str,
        bstack11111ll1ll_opy_: bstack1llllll1l11_opy_,
        bstack111111111l_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack11llll111l_opy_ = datetime.now()
            (bstack11111ll1ll_opy_,) = wrapped.__vars__
            bstack11111ll1ll_opy_ = (
                bstack11111ll1ll_opy_
                if bstack11111ll1ll_opy_ and bstack11111ll1ll_opy_ != bstack1llllll1l11_opy_.NONE
                else self.bstack111111l1ll_opy_(method_name, previous_state=bstack11111ll1ll_opy_, *args, **kwargs)
            )
            if bstack11111ll1ll_opy_ == bstack1llllll1l11_opy_.bstack11111l1l11_opy_:
                ctx = bstack11111l1lll_opy_.create_context(self.bstack11111lll11_opy_(target))
                if not self.bstack111111lll1_opy_() or ctx.id not in bstack1llllll111l_opy_.bstack1lllllll111_opy_:
                    bstack1llllll111l_opy_.bstack1lllllll111_opy_[ctx.id] = bstack1llllll11ll_opy_(
                        ctx, self.framework_name, self.framework_version, bstack11111ll1ll_opy_
                    )
                self.logger.debug(bstack11l1lll_opy_ (u"ࠥࡻࡷࡧࡰࡱࡧࡧࠤࡲ࡫ࡴࡩࡱࡧࠤࡨࡸࡥࡢࡶࡨࡨ࠿ࠦࡻࡵࡣࡵ࡫ࡪࡺ࠮ࡠࡡࡦࡰࡦࡹࡳࡠࡡࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡥࡷࡼࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦဳ") + str(bstack1llllll111l_opy_.bstack1lllllll111_opy_.keys()) + bstack11l1lll_opy_ (u"ࠦࠧဴ"))
            else:
                self.logger.debug(bstack11l1lll_opy_ (u"ࠧࡽࡲࡢࡲࡳࡩࡩࠦ࡭ࡦࡶ࡫ࡳࡩࠦࡩ࡯ࡸࡲ࡯ࡪࡪ࠺ࠡࡽࡷࡥࡷ࡭ࡥࡵ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢဵ") + str(bstack1llllll111l_opy_.bstack1lllllll111_opy_.keys()) + bstack11l1lll_opy_ (u"ࠨࠢံ"))
            instance = bstack1llllll111l_opy_.bstack11111l1111_opy_(self.bstack11111lll11_opy_(target))
            if bstack11111ll1ll_opy_ == bstack1llllll1l11_opy_.NONE or not instance:
                ctx = bstack11111l1lll_opy_.create_context(self.bstack11111lll11_opy_(target))
                self.logger.warning(bstack11l1lll_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤࠡࡷࡱࡸࡷࡧࡣ࡬ࡧࡧ࠾ࠥࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡨࡺࡸ࠾ࡽࡦࡸࡽࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀ့ࠦ") + str(bstack1llllll111l_opy_.bstack1lllllll111_opy_.keys()) + bstack11l1lll_opy_ (u"ࠣࠤး"))
                return bstack111111111l_opy_(target, *args, **kwargs)
            bstack1llllll1l1l_opy_ = self.bstack111111ll1l_opy_(
                target,
                (instance, method_name),
                (bstack11111ll1ll_opy_, bstack11111ll1l1_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack111111llll_opy_(bstack11111ll1ll_opy_):
                self.logger.debug(bstack11l1lll_opy_ (u"ࠤࡤࡴࡵࡲࡩࡦࡦࠣࡷࡹࡧࡴࡦ࠯ࡷࡶࡦࡴࡳࡪࡶ࡬ࡳࡳࡀࠠࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡴࡷ࡫ࡶࡪࡱࡸࡷࡤࡹࡴࡢࡶࡨࢁࠥࡃ࠾ࠡࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡸࡺࡡࡵࡧࢀࠤ࠭ࢁࡴࡺࡲࡨࠬࡹࡧࡲࡨࡧࡷ࠭ࢂ࠴ࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡻࡢࡴࡪࡷࢂ࠯ࠠ࡜ࠤ္") + str(instance.ref()) + bstack11l1lll_opy_ (u"ࠥࡡ်ࠧ"))
            result = (
                bstack1llllll1l1l_opy_(target, bstack111111111l_opy_, *args, **kwargs)
                if callable(bstack1llllll1l1l_opy_)
                else bstack111111111l_opy_(target, *args, **kwargs)
            )
            bstack1lllll1llll_opy_ = self.bstack111111ll1l_opy_(
                target,
                (instance, method_name),
                (bstack11111ll1ll_opy_, bstack11111ll1l1_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1llllll1111_opy_(instance, method_name, datetime.now() - bstack11llll111l_opy_, *args, **kwargs)
            return bstack1lllll1llll_opy_ if bstack1lllll1llll_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack11111ll1ll_opy_,)
        return wrapped
    @staticmethod
    def bstack11111l1111_opy_(target: object, strict=True):
        ctx = bstack11111l1lll_opy_.create_context(target)
        instance = bstack1llllll111l_opy_.bstack1lllllll111_opy_.get(ctx.id, None)
        if instance and instance.bstack1llllllllll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack111111l11l_opy_(
        ctx: bstack11111ll11l_opy_, state: bstack1llllll1l11_opy_, reverse=True
    ) -> List[bstack1llllll11ll_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1llllll111l_opy_.bstack1lllllll111_opy_.values(),
            ),
            key=lambda t: t.bstack11111ll111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111l11ll_opy_(instance: bstack1llllll11ll_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llllll11l1_opy_(instance: bstack1llllll11ll_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack111111llll_opy_(instance: bstack1llllll11ll_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1llllll111l_opy_.logger.debug(bstack11l1lll_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦ࡫ࡦࡻࡀࡿࡰ࡫ࡹࡾࠢࡹࡥࡱࡻࡥ࠾ࠤျ") + str(value) + bstack11l1lll_opy_ (u"ࠧࠨြ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1llllll111l_opy_.bstack11111l1111_opy_(target, strict)
        return bstack1llllll111l_opy_.bstack1llllll11l1_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1llllll111l_opy_.bstack11111l1111_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack111111lll1_opy_(self):
        return self.framework_name == bstack11l1lll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪွ")
    def bstack11111lll11_opy_(self, target):
        return target if not self.bstack111111lll1_opy_() else self.bstack11111111ll_opy_()
    @staticmethod
    def bstack11111111ll_opy_():
        return str(os.getpid()) + str(threading.get_ident())