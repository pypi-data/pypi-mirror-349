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
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111l111l11_opy_ import RobotHandler
from bstack_utils.capture import bstack111llllll1_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack1111llllll_opy_, bstack111lll1ll1_opy_, bstack111lll1l11_opy_
from bstack_utils.bstack111lllllll_opy_ import bstack1lllll1l1l_opy_
from bstack_utils.bstack111lll11l1_opy_ import bstack1l11l1l1ll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l1lllll1l_opy_, bstack11l11ll11l_opy_, Result, \
    bstack111l11111l_opy_, bstack111l1l1111_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack111l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ༬"): [],
        bstack111l11_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭༭"): [],
        bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ༮"): []
    }
    bstack111ll1111l_opy_ = []
    bstack111l111ll1_opy_ = []
    @staticmethod
    def bstack11l1111111_opy_(log):
        if not ((isinstance(log[bstack111l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༯")], list) or (isinstance(log[bstack111l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༰")], dict)) and len(log[bstack111l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༱")])>0) or (isinstance(log[bstack111l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭༲")], str) and log[bstack111l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ༳")].strip())):
            return
        active = bstack1lllll1l1l_opy_.bstack11l1111l11_opy_()
        log = {
            bstack111l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭༴"): log[bstack111l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲ༵ࠧ")],
            bstack111l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ༶"): bstack111l1l1111_opy_().isoformat() + bstack111l11_opy_ (u"ࠪ࡞༷ࠬ"),
            bstack111l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༸"): log[bstack111l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ༹࠭")],
        }
        if active:
            if active[bstack111l11_opy_ (u"࠭ࡴࡺࡲࡨࠫ༺")] == bstack111l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ༻"):
                log[bstack111l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ༼")] = active[bstack111l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ༽")]
            elif active[bstack111l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ༾")] == bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ༿"):
                log[bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬཀ")] = active[bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ཁ")]
        bstack1l11l1l1ll_opy_.bstack1ll1llll_opy_([log])
    def __init__(self):
        self.messages = bstack111l1ll1ll_opy_()
        self._111ll11l1l_opy_ = None
        self._111ll1l11l_opy_ = None
        self._111ll1l1ll_opy_ = OrderedDict()
        self.bstack111lll1111_opy_ = bstack111llllll1_opy_(self.bstack11l1111111_opy_)
    @bstack111l11111l_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111l1lll11_opy_()
        if not self._111ll1l1ll_opy_.get(attrs.get(bstack111l11_opy_ (u"ࠧࡪࡦࠪག")), None):
            self._111ll1l1ll_opy_[attrs.get(bstack111l11_opy_ (u"ࠨ࡫ࡧࠫགྷ"))] = {}
        bstack111ll111l1_opy_ = bstack111lll1l11_opy_(
                bstack111l111111_opy_=attrs.get(bstack111l11_opy_ (u"ࠩ࡬ࡨࠬང")),
                name=name,
                started_at=bstack11l11ll11l_opy_(),
                file_path=os.path.relpath(attrs[bstack111l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪཅ")], start=os.getcwd()) if attrs.get(bstack111l11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫཆ")) != bstack111l11_opy_ (u"ࠬ࠭ཇ") else bstack111l11_opy_ (u"࠭ࠧ཈"),
                framework=bstack111l11_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ཉ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack111l11_opy_ (u"ࠨ࡫ࡧࠫཊ"), None)
        self._111ll1l1ll_opy_[attrs.get(bstack111l11_opy_ (u"ࠩ࡬ࡨࠬཋ"))][bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ཌ")] = bstack111ll111l1_opy_
    @bstack111l11111l_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111l11l111_opy_()
        self._111l1l11ll_opy_(messages)
        for bstack111l1l1lll_opy_ in self.bstack111ll1111l_opy_:
            bstack111l1l1lll_opy_[bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ཌྷ")][bstack111l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫཎ")].extend(self.store[bstack111l11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬཏ")])
            bstack1l11l1l1ll_opy_.bstack111l1l1ll_opy_(bstack111l1l1lll_opy_)
        self.bstack111ll1111l_opy_ = []
        self.store[bstack111l11_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ཐ")] = []
    @bstack111l11111l_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack111lll1111_opy_.start()
        if not self._111ll1l1ll_opy_.get(attrs.get(bstack111l11_opy_ (u"ࠨ࡫ࡧࠫད")), None):
            self._111ll1l1ll_opy_[attrs.get(bstack111l11_opy_ (u"ࠩ࡬ࡨࠬདྷ"))] = {}
        driver = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩན"), None)
        bstack111llll1l1_opy_ = bstack111lll1l11_opy_(
            bstack111l111111_opy_=attrs.get(bstack111l11_opy_ (u"ࠫ࡮ࡪࠧཔ")),
            name=name,
            started_at=bstack11l11ll11l_opy_(),
            file_path=os.path.relpath(attrs[bstack111l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬཕ")], start=os.getcwd()),
            scope=RobotHandler.bstack111l11llll_opy_(attrs.get(bstack111l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭བ"), None)),
            framework=bstack111l11_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭བྷ"),
            tags=attrs[bstack111l11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭མ")],
            hooks=self.store[bstack111l11_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨཙ")],
            bstack111lll111l_opy_=bstack1l11l1l1ll_opy_.bstack111ll1ll1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack111l11_opy_ (u"ࠥࡿࢂࠦ࡜࡯ࠢࡾࢁࠧཚ").format(bstack111l11_opy_ (u"ࠦࠥࠨཛ").join(attrs[bstack111l11_opy_ (u"ࠬࡺࡡࡨࡵࠪཛྷ")]), name) if attrs[bstack111l11_opy_ (u"࠭ࡴࡢࡩࡶࠫཝ")] else name
        )
        self._111ll1l1ll_opy_[attrs.get(bstack111l11_opy_ (u"ࠧࡪࡦࠪཞ"))][bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫཟ")] = bstack111llll1l1_opy_
        threading.current_thread().current_test_uuid = bstack111llll1l1_opy_.bstack111l1lllll_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack111l11_opy_ (u"ࠩ࡬ࡨࠬའ"), None)
        self.bstack111llll11l_opy_(bstack111l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫཡ"), bstack111llll1l1_opy_)
    @bstack111l11111l_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack111lll1111_opy_.reset()
        bstack111ll11ll1_opy_ = bstack111l1ll111_opy_.get(attrs.get(bstack111l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫར")), bstack111l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ལ"))
        self._111ll1l1ll_opy_[attrs.get(bstack111l11_opy_ (u"࠭ࡩࡥࠩཤ"))][bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪཥ")].stop(time=bstack11l11ll11l_opy_(), duration=int(attrs.get(bstack111l11_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ས"), bstack111l11_opy_ (u"ࠩ࠳ࠫཧ"))), result=Result(result=bstack111ll11ll1_opy_, exception=attrs.get(bstack111l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫཨ")), bstack111llll1ll_opy_=[attrs.get(bstack111l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཀྵ"))]))
        self.bstack111llll11l_opy_(bstack111l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧཪ"), self._111ll1l1ll_opy_[attrs.get(bstack111l11_opy_ (u"࠭ࡩࡥࠩཫ"))][bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪཬ")], True)
        self.store[bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ཭")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack111l11111l_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111l1lll11_opy_()
        current_test_id = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ཮"), None)
        bstack111l11l1l1_opy_ = current_test_id if bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬ཯"), None) else bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧ཰"), None)
        if attrs.get(bstack111l11_opy_ (u"ࠬࡺࡹࡱࡧཱࠪ"), bstack111l11_opy_ (u"ི࠭ࠧ")).lower() in [bstack111l11_opy_ (u"ࠧࡴࡧࡷࡹࡵཱི࠭"), bstack111l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰུࠪ")]:
            hook_type = bstack111l111l1l_opy_(attrs.get(bstack111l11_opy_ (u"ࠩࡷࡽࡵ࡫ཱུࠧ")), bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧྲྀ"), None))
            hook_name = bstack111l11_opy_ (u"ࠫࢀࢃࠧཷ").format(attrs.get(bstack111l11_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬླྀ"), bstack111l11_opy_ (u"࠭ࠧཹ")))
            if hook_type in [bstack111l11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏེࠫ"), bstack111l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏཻࠫ")]:
                hook_name = bstack111l11_opy_ (u"ࠩ࡞ࡿࢂࡣࠠࡼࡿོࠪ").format(bstack111l111lll_opy_.get(hook_type), attrs.get(bstack111l11_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧཽࠪ"), bstack111l11_opy_ (u"ࠫࠬཾ")))
            bstack111l1l1ll1_opy_ = bstack111lll1ll1_opy_(
                bstack111l111111_opy_=bstack111l11l1l1_opy_ + bstack111l11_opy_ (u"ࠬ࠳ࠧཿ") + attrs.get(bstack111l11_opy_ (u"࠭ࡴࡺࡲࡨྀࠫ"), bstack111l11_opy_ (u"ࠧࠨཱྀ")).lower(),
                name=hook_name,
                started_at=bstack11l11ll11l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack111l11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨྂ")), start=os.getcwd()),
                framework=bstack111l11_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨྃ"),
                tags=attrs[bstack111l11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ྄")],
                scope=RobotHandler.bstack111l11llll_opy_(attrs.get(bstack111l11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ྅"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111l1l1ll1_opy_.bstack111l1lllll_opy_()
            threading.current_thread().current_hook_id = bstack111l11l1l1_opy_ + bstack111l11_opy_ (u"ࠬ࠳ࠧ྆") + attrs.get(bstack111l11_opy_ (u"࠭ࡴࡺࡲࡨࠫ྇"), bstack111l11_opy_ (u"ࠧࠨྈ")).lower()
            self.store[bstack111l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬྉ")] = [bstack111l1l1ll1_opy_.bstack111l1lllll_opy_()]
            if bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ྊ"), None):
                self.store[bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧྋ")].append(bstack111l1l1ll1_opy_.bstack111l1lllll_opy_())
            else:
                self.store[bstack111l11_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪྌ")].append(bstack111l1l1ll1_opy_.bstack111l1lllll_opy_())
            if bstack111l11l1l1_opy_:
                self._111ll1l1ll_opy_[bstack111l11l1l1_opy_ + bstack111l11_opy_ (u"ࠬ࠳ࠧྍ") + attrs.get(bstack111l11_opy_ (u"࠭ࡴࡺࡲࡨࠫྎ"), bstack111l11_opy_ (u"ࠧࠨྏ")).lower()] = { bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫྐ"): bstack111l1l1ll1_opy_ }
            bstack1l11l1l1ll_opy_.bstack111llll11l_opy_(bstack111l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪྑ"), bstack111l1l1ll1_opy_)
        else:
            bstack111ll1llll_opy_ = {
                bstack111l11_opy_ (u"ࠪ࡭ࡩ࠭ྒ"): uuid4().__str__(),
                bstack111l11_opy_ (u"ࠫࡹ࡫ࡸࡵࠩྒྷ"): bstack111l11_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫྔ").format(attrs.get(bstack111l11_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ྕ")), attrs.get(bstack111l11_opy_ (u"ࠧࡢࡴࡪࡷࠬྖ"), bstack111l11_opy_ (u"ࠨࠩྗ"))) if attrs.get(bstack111l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ྘"), []) else attrs.get(bstack111l11_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪྙ")),
                bstack111l11_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫྚ"): attrs.get(bstack111l11_opy_ (u"ࠬࡧࡲࡨࡵࠪྛ"), []),
                bstack111l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪྜ"): bstack11l11ll11l_opy_(),
                bstack111l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧྜྷ"): bstack111l11_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩྞ"),
                bstack111l11_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧྟ"): attrs.get(bstack111l11_opy_ (u"ࠪࡨࡴࡩࠧྠ"), bstack111l11_opy_ (u"ࠫࠬྡ"))
            }
            if attrs.get(bstack111l11_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭ྡྷ"), bstack111l11_opy_ (u"࠭ࠧྣ")) != bstack111l11_opy_ (u"ࠧࠨྤ"):
                bstack111ll1llll_opy_[bstack111l11_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩྥ")] = attrs.get(bstack111l11_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪྦ"))
            if not self.bstack111l111ll1_opy_:
                self._111ll1l1ll_opy_[self._111l1111ll_opy_()][bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྦྷ")].add_step(bstack111ll1llll_opy_)
                threading.current_thread().current_step_uuid = bstack111ll1llll_opy_[bstack111l11_opy_ (u"ࠫ࡮ࡪࠧྨ")]
            self.bstack111l111ll1_opy_.append(bstack111ll1llll_opy_)
    @bstack111l11111l_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111l11l111_opy_()
        self._111l1l11ll_opy_(messages)
        current_test_id = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧྩ"), None)
        bstack111l11l1l1_opy_ = current_test_id if current_test_id else bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩྪ"), None)
        bstack1111llll1l_opy_ = bstack111l1ll111_opy_.get(attrs.get(bstack111l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧྫ")), bstack111l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩྫྷ"))
        bstack111l1l1l11_opy_ = attrs.get(bstack111l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪྭ"))
        if bstack1111llll1l_opy_ != bstack111l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫྮ") and not attrs.get(bstack111l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬྯ")) and self._111ll11l1l_opy_:
            bstack111l1l1l11_opy_ = self._111ll11l1l_opy_
        bstack111ll1lll1_opy_ = Result(result=bstack1111llll1l_opy_, exception=bstack111l1l1l11_opy_, bstack111llll1ll_opy_=[bstack111l1l1l11_opy_])
        if attrs.get(bstack111l11_opy_ (u"ࠬࡺࡹࡱࡧࠪྰ"), bstack111l11_opy_ (u"࠭ࠧྱ")).lower() in [bstack111l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ྲ"), bstack111l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪླ")]:
            bstack111l11l1l1_opy_ = current_test_id if current_test_id else bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬྴ"), None)
            if bstack111l11l1l1_opy_:
                bstack11l111111l_opy_ = bstack111l11l1l1_opy_ + bstack111l11_opy_ (u"ࠥ࠱ࠧྵ") + attrs.get(bstack111l11_opy_ (u"ࠫࡹࡿࡰࡦࠩྶ"), bstack111l11_opy_ (u"ࠬ࠭ྷ")).lower()
                self._111ll1l1ll_opy_[bstack11l111111l_opy_][bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩྸ")].stop(time=bstack11l11ll11l_opy_(), duration=int(attrs.get(bstack111l11_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬྐྵ"), bstack111l11_opy_ (u"ࠨ࠲ࠪྺ"))), result=bstack111ll1lll1_opy_)
                bstack1l11l1l1ll_opy_.bstack111llll11l_opy_(bstack111l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫྻ"), self._111ll1l1ll_opy_[bstack11l111111l_opy_][bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྼ")])
        else:
            bstack111l11l1l1_opy_ = current_test_id if current_test_id else bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢ࡭ࡩ࠭྽"), None)
            if bstack111l11l1l1_opy_ and len(self.bstack111l111ll1_opy_) == 1:
                current_step_uuid = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩ྾"), None)
                self._111ll1l1ll_opy_[bstack111l11l1l1_opy_][bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ྿")].bstack111lll1lll_opy_(current_step_uuid, duration=int(attrs.get(bstack111l11_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬ࿀"), bstack111l11_opy_ (u"ࠨ࠲ࠪ࿁"))), result=bstack111ll1lll1_opy_)
            else:
                self.bstack111l1l111l_opy_(attrs)
            self.bstack111l111ll1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack111l11_opy_ (u"ࠩ࡫ࡸࡲࡲࠧ࿂"), bstack111l11_opy_ (u"ࠪࡲࡴ࠭࿃")) == bstack111l11_opy_ (u"ࠫࡾ࡫ࡳࠨ࿄"):
                return
            self.messages.push(message)
            logs = []
            if bstack1lllll1l1l_opy_.bstack11l1111l11_opy_():
                logs.append({
                    bstack111l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ࿅"): bstack11l11ll11l_opy_(),
                    bstack111l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫࿆ࠧ"): message.get(bstack111l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿇")),
                    bstack111l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ࿈"): message.get(bstack111l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ࿉")),
                    **bstack1lllll1l1l_opy_.bstack11l1111l11_opy_()
                })
                if len(logs) > 0:
                    bstack1l11l1l1ll_opy_.bstack1ll1llll_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack1l11l1l1ll_opy_.bstack111ll111ll_opy_()
    def bstack111l1l111l_opy_(self, bstack111ll11l11_opy_):
        if not bstack1lllll1l1l_opy_.bstack11l1111l11_opy_():
            return
        kwname = bstack111l11_opy_ (u"ࠪࡿࢂࠦࡻࡾࠩ࿊").format(bstack111ll11l11_opy_.get(bstack111l11_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ࿋")), bstack111ll11l11_opy_.get(bstack111l11_opy_ (u"ࠬࡧࡲࡨࡵࠪ࿌"), bstack111l11_opy_ (u"࠭ࠧ࿍"))) if bstack111ll11l11_opy_.get(bstack111l11_opy_ (u"ࠧࡢࡴࡪࡷࠬ࿎"), []) else bstack111ll11l11_opy_.get(bstack111l11_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ࿏"))
        error_message = bstack111l11_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠡࡾࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠ࡝ࠤࡾ࠶ࢂࡢࠢࠣ࿐").format(kwname, bstack111ll11l11_opy_.get(bstack111l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ࿑")), str(bstack111ll11l11_opy_.get(bstack111l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ࿒"))))
        bstack111l1lll1l_opy_ = bstack111l11_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠦ࿓").format(kwname, bstack111ll11l11_opy_.get(bstack111l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭࿔")))
        bstack111ll1ll11_opy_ = error_message if bstack111ll11l11_opy_.get(bstack111l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿕")) else bstack111l1lll1l_opy_
        bstack111l1ll11l_opy_ = {
            bstack111l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ࿖"): self.bstack111l111ll1_opy_[-1].get(bstack111l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭࿗"), bstack11l11ll11l_opy_()),
            bstack111l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿘"): bstack111ll1ll11_opy_,
            bstack111l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ࿙"): bstack111l11_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫ࿚") if bstack111ll11l11_opy_.get(bstack111l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭࿛")) == bstack111l11_opy_ (u"ࠧࡇࡃࡌࡐࠬ࿜") else bstack111l11_opy_ (u"ࠨࡋࡑࡊࡔ࠭࿝"),
            **bstack1lllll1l1l_opy_.bstack11l1111l11_opy_()
        }
        bstack1l11l1l1ll_opy_.bstack1ll1llll_opy_([bstack111l1ll11l_opy_])
    def _111l1111ll_opy_(self):
        for bstack111l111111_opy_ in reversed(self._111ll1l1ll_opy_):
            bstack111l1llll1_opy_ = bstack111l111111_opy_
            data = self._111ll1l1ll_opy_[bstack111l111111_opy_][bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ࿞")]
            if isinstance(data, bstack111lll1ll1_opy_):
                if not bstack111l11_opy_ (u"ࠪࡉࡆࡉࡈࠨ࿟") in data.bstack111ll11111_opy_():
                    return bstack111l1llll1_opy_
            else:
                return bstack111l1llll1_opy_
    def _111l1l11ll_opy_(self, messages):
        try:
            bstack111l11l11l_opy_ = BuiltIn().get_variable_value(bstack111l11_opy_ (u"ࠦࠩࢁࡌࡐࡉࠣࡐࡊ࡜ࡅࡍࡿࠥ࿠")) in (bstack111l11ll1l_opy_.DEBUG, bstack111l11ll1l_opy_.TRACE)
            for message, bstack111l1l11l1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack111l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿡"))
                level = message.get(bstack111l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ࿢"))
                if level == bstack111l11ll1l_opy_.FAIL:
                    self._111ll11l1l_opy_ = name or self._111ll11l1l_opy_
                    self._111ll1l11l_opy_ = bstack111l1l11l1_opy_.get(bstack111l11_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣ࿣")) if bstack111l11l11l_opy_ and bstack111l1l11l1_opy_ else self._111ll1l11l_opy_
        except:
            pass
    @classmethod
    def bstack111llll11l_opy_(self, event: str, bstack111l11ll11_opy_: bstack1111llllll_opy_, bstack111ll1l111_opy_=False):
        if event == bstack111l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ࿤"):
            bstack111l11ll11_opy_.set(hooks=self.store[bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭࿥")])
        if event == bstack111l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ࿦"):
            event = bstack111l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭࿧")
        if bstack111ll1l111_opy_:
            bstack111ll1l1l1_opy_ = {
                bstack111l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ࿨"): event,
                bstack111l11ll11_opy_.bstack1111lllll1_opy_(): bstack111l11ll11_opy_.bstack111l11lll1_opy_(event)
            }
            self.bstack111ll1111l_opy_.append(bstack111ll1l1l1_opy_)
        else:
            bstack1l11l1l1ll_opy_.bstack111llll11l_opy_(event, bstack111l11ll11_opy_)
class bstack111l1ll1ll_opy_:
    def __init__(self):
        self._111ll11lll_opy_ = []
    def bstack111l1lll11_opy_(self):
        self._111ll11lll_opy_.append([])
    def bstack111l11l111_opy_(self):
        return self._111ll11lll_opy_.pop() if self._111ll11lll_opy_ else list()
    def push(self, message):
        self._111ll11lll_opy_[-1].append(message) if self._111ll11lll_opy_ else self._111ll11lll_opy_.append([message])
class bstack111l11ll1l_opy_:
    FAIL = bstack111l11_opy_ (u"࠭ࡆࡂࡋࡏࠫ࿩")
    ERROR = bstack111l11_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭࿪")
    WARNING = bstack111l11_opy_ (u"ࠨ࡙ࡄࡖࡓ࠭࿫")
    bstack111l11l1ll_opy_ = bstack111l11_opy_ (u"ࠩࡌࡒࡋࡕࠧ࿬")
    DEBUG = bstack111l11_opy_ (u"ࠪࡈࡊࡈࡕࡈࠩ࿭")
    TRACE = bstack111l11_opy_ (u"࡙ࠫࡘࡁࡄࡇࠪ࿮")
    bstack111l1ll1l1_opy_ = [FAIL, ERROR]
def bstack111l1l1l1l_opy_(bstack111l1111l1_opy_):
    if not bstack111l1111l1_opy_:
        return None
    if bstack111l1111l1_opy_.get(bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿯"), None):
        return getattr(bstack111l1111l1_opy_[bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿰")], bstack111l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ࿱"), None)
    return bstack111l1111l1_opy_.get(bstack111l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭࿲"), None)
def bstack111l111l1l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack111l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ࿳"), bstack111l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ࿴")]:
        return
    if hook_type.lower() == bstack111l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ࿵"):
        if current_test_uuid is None:
            return bstack111l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ࿶")
        else:
            return bstack111l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ࿷")
    elif hook_type.lower() == bstack111l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ࿸"):
        if current_test_uuid is None:
            return bstack111l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ࿹")
        else:
            return bstack111l11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭࿺")