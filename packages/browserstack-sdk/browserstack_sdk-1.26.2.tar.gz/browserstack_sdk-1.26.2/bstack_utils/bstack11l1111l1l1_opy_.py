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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l11l1lll1_opy_
from browserstack_sdk.bstack111lll1l_opy_ import bstack11l1lll11_opy_
def _11l1111llll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l111l11l1_opy_:
    def __init__(self, handler):
        self._11l111l111l_opy_ = {}
        self._11l1111ll1l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11l1lll11_opy_.version()
        if bstack11l11l1lll1_opy_(pytest_version, bstack111l11_opy_ (u"ࠢ࠹࠰࠴࠲࠶ࠨᱩ")) >= 0:
            self._11l111l111l_opy_[bstack111l11_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᱪ")] = Module._register_setup_function_fixture
            self._11l111l111l_opy_[bstack111l11_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᱫ")] = Module._register_setup_module_fixture
            self._11l111l111l_opy_[bstack111l11_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᱬ")] = Class._register_setup_class_fixture
            self._11l111l111l_opy_[bstack111l11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᱭ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11l111ll111_opy_(bstack111l11_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᱮ"))
            Module._register_setup_module_fixture = self.bstack11l111ll111_opy_(bstack111l11_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᱯ"))
            Class._register_setup_class_fixture = self.bstack11l111ll111_opy_(bstack111l11_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᱰ"))
            Class._register_setup_method_fixture = self.bstack11l111ll111_opy_(bstack111l11_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᱱ"))
        else:
            self._11l111l111l_opy_[bstack111l11_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᱲ")] = Module._inject_setup_function_fixture
            self._11l111l111l_opy_[bstack111l11_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᱳ")] = Module._inject_setup_module_fixture
            self._11l111l111l_opy_[bstack111l11_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᱴ")] = Class._inject_setup_class_fixture
            self._11l111l111l_opy_[bstack111l11_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᱵ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11l111ll111_opy_(bstack111l11_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᱶ"))
            Module._inject_setup_module_fixture = self.bstack11l111ll111_opy_(bstack111l11_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᱷ"))
            Class._inject_setup_class_fixture = self.bstack11l111ll111_opy_(bstack111l11_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᱸ"))
            Class._inject_setup_method_fixture = self.bstack11l111ll111_opy_(bstack111l11_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᱹ"))
    def bstack11l111l1lll_opy_(self, bstack11l111l1ll1_opy_, hook_type):
        bstack11l111ll11l_opy_ = id(bstack11l111l1ll1_opy_.__class__)
        if (bstack11l111ll11l_opy_, hook_type) in self._11l1111ll1l_opy_:
            return
        meth = getattr(bstack11l111l1ll1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l1111ll1l_opy_[(bstack11l111ll11l_opy_, hook_type)] = meth
            setattr(bstack11l111l1ll1_opy_, hook_type, self.bstack11l111l1l1l_opy_(hook_type, bstack11l111ll11l_opy_))
    def bstack11l1111lll1_opy_(self, instance, bstack11l1111l1ll_opy_):
        if bstack11l1111l1ll_opy_ == bstack111l11_opy_ (u"ࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᱺ"):
            self.bstack11l111l1lll_opy_(instance.obj, bstack111l11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᱻ"))
            self.bstack11l111l1lll_opy_(instance.obj, bstack111l11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤᱼ"))
        if bstack11l1111l1ll_opy_ == bstack111l11_opy_ (u"ࠨ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᱽ"):
            self.bstack11l111l1lll_opy_(instance.obj, bstack111l11_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࠨ᱾"))
            self.bstack11l111l1lll_opy_(instance.obj, bstack111l11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠥ᱿"))
        if bstack11l1111l1ll_opy_ == bstack111l11_opy_ (u"ࠤࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᲀ"):
            self.bstack11l111l1lll_opy_(instance.obj, bstack111l11_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠣᲁ"))
            self.bstack11l111l1lll_opy_(instance.obj, bstack111l11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠧᲂ"))
        if bstack11l1111l1ll_opy_ == bstack111l11_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᲃ"):
            self.bstack11l111l1lll_opy_(instance.obj, bstack111l11_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠧᲄ"))
            self.bstack11l111l1lll_opy_(instance.obj, bstack111l11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠤᲅ"))
    @staticmethod
    def bstack11l111l1l11_opy_(hook_type, func, args):
        if hook_type in [bstack111l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᲆ"), bstack111l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᲇ")]:
            _11l1111llll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l111l1l1l_opy_(self, hook_type, bstack11l111ll11l_opy_):
        def bstack11l111l11ll_opy_(arg=None):
            self.handler(hook_type, bstack111l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᲈ"))
            result = None
            try:
                bstack1llllll11l1_opy_ = self._11l1111ll1l_opy_[(bstack11l111ll11l_opy_, hook_type)]
                self.bstack11l111l1l11_opy_(hook_type, bstack1llllll11l1_opy_, (arg,))
                result = Result(result=bstack111l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᲉ"))
            except Exception as e:
                result = Result(result=bstack111l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᲊ"), exception=e)
                self.handler(hook_type, bstack111l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬ᲋"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack111l11_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭᲌"), result)
        def bstack11l111l1111_opy_(this, arg=None):
            self.handler(hook_type, bstack111l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ᲍"))
            result = None
            exception = None
            try:
                self.bstack11l111l1l11_opy_(hook_type, self._11l1111ll1l_opy_[hook_type], (this, arg))
                result = Result(result=bstack111l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ᲎"))
            except Exception as e:
                result = Result(result=bstack111l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᲏"), exception=e)
                self.handler(hook_type, bstack111l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᲐ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack111l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᲑ"), result)
        if hook_type in [bstack111l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᲒ"), bstack111l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᲓ")]:
            return bstack11l111l1111_opy_
        return bstack11l111l11ll_opy_
    def bstack11l111ll111_opy_(self, bstack11l1111l1ll_opy_):
        def bstack11l1111ll11_opy_(this, *args, **kwargs):
            self.bstack11l1111lll1_opy_(this, bstack11l1111l1ll_opy_)
            self._11l111l111l_opy_[bstack11l1111l1ll_opy_](this, *args, **kwargs)
        return bstack11l1111ll11_opy_