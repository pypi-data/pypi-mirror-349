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
from browserstack_sdk.bstack1ll1ll1l11_opy_ import bstack11ll1l111l_opy_
from browserstack_sdk.bstack111ll11lll_opy_ import RobotHandler
def bstack1ll11l1ll_opy_(framework):
    if framework.lower() == bstack11l1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭᨜"):
        return bstack11ll1l111l_opy_.version()
    elif framework.lower() == bstack11l1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭᨝"):
        return RobotHandler.version()
    elif framework.lower() == bstack11l1lll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ᨞"):
        import behave
        return behave.__version__
    else:
        return bstack11l1lll_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࠪ᨟")
def bstack1l1l11l1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11l1lll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᨠ"))
        framework_version.append(importlib.metadata.version(bstack11l1lll_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᨡ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᨢ"))
        framework_version.append(importlib.metadata.version(bstack11l1lll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᨣ")))
    except:
        pass
    return {
        bstack11l1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᨤ"): bstack11l1lll_opy_ (u"ࠨࡡࠪᨥ").join(framework_name),
        bstack11l1lll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪᨦ"): bstack11l1lll_opy_ (u"ࠪࡣࠬᨧ").join(framework_version)
    }