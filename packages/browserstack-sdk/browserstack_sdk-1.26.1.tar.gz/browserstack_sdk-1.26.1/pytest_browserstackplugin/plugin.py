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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack11l1lll1l1_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l11l1ll_opy_, bstack1l11l11l1_opy_, update, bstack1l1ll1ll1_opy_,
                                       bstack1ll1lll1l_opy_, bstack1ll1l1llll_opy_, bstack11l11lll11_opy_, bstack11ll1l11l1_opy_,
                                       bstack1llll11ll1_opy_, bstack11l1l1l1l_opy_, bstack1lll1llll1_opy_, bstack1l1ll11l11_opy_,
                                       bstack1ll11l1l1_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1ll11llll_opy_)
from browserstack_sdk.bstack1ll1ll1l11_opy_ import bstack11ll1l111l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l11l1lll_opy_
from bstack_utils.capture import bstack111llll11l_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack11ll11lll_opy_, bstack11l111l111_opy_, bstack1lllll11_opy_, \
    bstack1ll1lll1ll_opy_
from bstack_utils.helper import bstack111l11lll_opy_, bstack11l11l1lll1_opy_, bstack111l1lllll_opy_, bstack1111llll_opy_, bstack1l1ll1l1ll1_opy_, bstack1lll11l11_opy_, \
    bstack11l111lll1l_opy_, \
    bstack11l11ll1lll_opy_, bstack111111111_opy_, bstack1ll1l11ll1_opy_, bstack11l1ll1111l_opy_, bstack1ll11lll_opy_, Notset, \
    bstack11l1ll1l1l_opy_, bstack11l11lll11l_opy_, bstack11l1llll1l1_opy_, Result, bstack11l1lll1111_opy_, bstack11l11l11lll_opy_, bstack111l111111_opy_, \
    bstack11l1lll1l_opy_, bstack1l1111ll_opy_, bstack1llll1l11_opy_, bstack11l1l1l1ll1_opy_
from bstack_utils.bstack11l111ll1ll_opy_ import bstack11l111l1lll_opy_
from bstack_utils.messages import bstack1111l11l_opy_, bstack1l11111ll1_opy_, bstack1l111ll1_opy_, bstack1l1l1111_opy_, bstack1l11111111_opy_, \
    bstack1l1l1l111l_opy_, bstack11lllll1_opy_, bstack1l111l1l11_opy_, bstack1ll11l1lll_opy_, bstack1ll1l11l1l_opy_, \
    bstack11l1llll11_opy_, bstack1l1lll1111_opy_
from bstack_utils.proxy import bstack111ll1lll_opy_, bstack11l111l1_opy_
from bstack_utils.bstack1llll11l1l_opy_ import bstack111l111l1ll_opy_, bstack111l1111l1l_opy_, bstack111l111l1l1_opy_, bstack111l111lll1_opy_, \
    bstack111l111ll1l_opy_, bstack111l1111ll1_opy_, bstack111l111l111_opy_, bstack1llll11111_opy_, bstack111l111ll11_opy_
from bstack_utils.bstack11l1lllll1_opy_ import bstack1111l11l1_opy_
from bstack_utils.bstack111l1111_opy_ import bstack1l111llll_opy_, bstack1l11l111ll_opy_, bstack111ll1l11_opy_, \
    bstack11ll1ll1_opy_, bstack1l1111l1l_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack111llllll1_opy_
from bstack_utils.bstack11l11111ll_opy_ import bstack11l111l11l_opy_
import bstack_utils.accessibility as bstack1l11111lll_opy_
from bstack_utils.bstack11l1111111_opy_ import bstack1lll11111l_opy_
from bstack_utils.bstack1lll11ll11_opy_ import bstack1lll11ll11_opy_
from browserstack_sdk.__init__ import bstack1ll1l111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l11l_opy_ import bstack1llll11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll111111_opy_ import bstack1lll111111_opy_, bstack11lll11lll_opy_, bstack1llll1l111_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l111l11l1l_opy_, bstack1lll11llll1_opy_, bstack1ll1lll1111_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1lll111111_opy_ import bstack1lll111111_opy_, bstack11lll11lll_opy_, bstack1llll1l111_opy_
bstack11l1l11l1l_opy_ = None
bstack1lll11ll1_opy_ = None
bstack1l1llll1l1_opy_ = None
bstack1lll11ll1l_opy_ = None
bstack11l11lllll_opy_ = None
bstack11l1l11ll_opy_ = None
bstack1l1lllll1l_opy_ = None
bstack1111l1l1_opy_ = None
bstack1llll1ll_opy_ = None
bstack1l1111ll1_opy_ = None
bstack1l11l11lll_opy_ = None
bstack1ll111111l_opy_ = None
bstack1lll1lllll_opy_ = None
bstack1l11l1l11l_opy_ = bstack11l1lll_opy_ (u"ࠩࠪ ")
CONFIG = {}
bstack1l111111_opy_ = False
bstack1ll1llll11_opy_ = bstack11l1lll_opy_ (u"ࠪࠫ ")
bstack11ll1l11l_opy_ = bstack11l1lll_opy_ (u"ࠫࠬ ")
bstack1llll1ll1l_opy_ = False
bstack11l111ll_opy_ = []
bstack111llll11_opy_ = bstack11ll11lll_opy_
bstack111111l1lll_opy_ = bstack11l1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ ")
bstack1l1111l1ll_opy_ = {}
bstack1l1l1ll1l1_opy_ = None
bstack111l1l11_opy_ = False
logger = bstack1l11l1lll_opy_.get_logger(__name__, bstack111llll11_opy_)
store = {
    bstack11l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ​"): []
}
bstack111111ll11l_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1111llllll_opy_ = {}
current_test_uuid = None
cli_context = bstack1l111l11l1l_opy_(
    test_framework_name=bstack11ll11ll1l_opy_[bstack11l1lll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࠭ࡃࡆࡇࠫ‌")] if bstack1ll11lll_opy_() else bstack11ll11ll1l_opy_[bstack11l1lll_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࠨ‍")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1lllll111_opy_(page, bstack111l111ll_opy_):
    try:
        page.evaluate(bstack11l1lll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ‎"),
                      bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧ‏") + json.dumps(
                          bstack111l111ll_opy_) + bstack11l1lll_opy_ (u"ࠦࢂࢃࠢ‐"))
    except Exception as e:
        print(bstack11l1lll_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥ‑"), e)
def bstack1llll1llll_opy_(page, message, level):
    try:
        page.evaluate(bstack11l1lll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ‒"), bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ–") + json.dumps(
            message) + bstack11l1lll_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫ—") + json.dumps(level) + bstack11l1lll_opy_ (u"ࠩࢀࢁࠬ―"))
    except Exception as e:
        print(bstack11l1lll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࠨ‖"), e)
def pytest_configure(config):
    global bstack1ll1llll11_opy_
    global CONFIG
    bstack11ll1llll1_opy_ = Config.bstack1ll1l1l1l1_opy_()
    config.args = bstack11l111l11l_opy_.bstack11111l1lll1_opy_(config.args)
    bstack11ll1llll1_opy_.bstack1l11lllll1_opy_(bstack1llll1l11_opy_(config.getoption(bstack11l1lll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ‗"))))
    try:
        bstack1l11l1lll_opy_.bstack11l1111l111_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1lll111111_opy_.invoke(bstack11lll11lll_opy_.CONNECT, bstack1llll1l111_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ‘"), bstack11l1lll_opy_ (u"࠭࠰ࠨ’")))
        config = json.loads(os.environ.get(bstack11l1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࠨ‚"), bstack11l1lll_opy_ (u"ࠣࡽࢀࠦ‛")))
        cli.bstack1ll1llllll1_opy_(bstack1ll1l11ll1_opy_(bstack1ll1llll11_opy_, CONFIG), cli_context.platform_index, bstack1l1ll1ll1_opy_)
    if cli.bstack1lll1llll1l_opy_(bstack1llll11l11l_opy_):
        cli.bstack1ll1llll111_opy_()
        logger.debug(bstack11l1lll_opy_ (u"ࠤࡆࡐࡎࠦࡩࡴࠢࡤࡧࡹ࡯ࡶࡦࠢࡩࡳࡷࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࠣ“") + str(cli_context.platform_index) + bstack11l1lll_opy_ (u"ࠥࠦ”"))
        cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.BEFORE_ALL, bstack1ll1lll1111_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack11l1lll_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤ„"), None)
    if cli.is_running() and when == bstack11l1lll_opy_ (u"ࠧࡩࡡ࡭࡮ࠥ‟"):
        cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.LOG_REPORT, bstack1ll1lll1111_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack11l1lll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧ†"):
            cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.BEFORE_EACH, bstack1ll1lll1111_opy_.POST, item, call, outcome)
        elif when == bstack11l1lll_opy_ (u"ࠢࡤࡣ࡯ࡰࠧ‡"):
            cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.LOG_REPORT, bstack1ll1lll1111_opy_.POST, item, call, outcome)
        elif when == bstack11l1lll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥ•"):
            cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.AFTER_EACH, bstack1ll1lll1111_opy_.POST, item, call, outcome)
        return # skip all existing bstack1111111ll1l_opy_
    skipSessionName = item.config.getoption(bstack11l1lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ‣"))
    plugins = item.config.getoption(bstack11l1lll_opy_ (u"ࠥࡴࡱࡻࡧࡪࡰࡶࠦ․"))
    report = outcome.get_result()
    bstack11111l111l1_opy_(item, call, report)
    if bstack11l1lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠤ‥") not in plugins or bstack1ll11lll_opy_():
        return
    summary = []
    driver = getattr(item, bstack11l1lll_opy_ (u"ࠧࡥࡤࡳ࡫ࡹࡩࡷࠨ…"), None)
    page = getattr(item, bstack11l1lll_opy_ (u"ࠨ࡟ࡱࡣࡪࡩࠧ‧"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack111111lll11_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack11111l1l11l_opy_(item, report, summary, skipSessionName)
def bstack111111lll11_opy_(item, report, summary, skipSessionName):
    if report.when == bstack11l1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ ") and report.skipped:
        bstack111l111ll11_opy_(report)
    if report.when in [bstack11l1lll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢ "), bstack11l1lll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦ‪")]:
        return
    if not bstack1l1ll1l1ll1_opy_():
        return
    try:
        if (str(skipSessionName).lower() != bstack11l1lll_opy_ (u"ࠪࡸࡷࡻࡥࠨ‫") and not cli.is_running()):
            item._driver.execute_script(
                bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ‬") + json.dumps(
                    report.nodeid) + bstack11l1lll_opy_ (u"ࠬࢃࡽࠨ‭"))
        os.environ[bstack11l1lll_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ‮")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11l1lll_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦ࠼ࠣࡿ࠵ࢃࠢ ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1lll_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ‰")))
    bstack1l111111ll_opy_ = bstack11l1lll_opy_ (u"ࠤࠥ‱")
    bstack111l111ll11_opy_(report)
    if not passed:
        try:
            bstack1l111111ll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11l1lll_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥ′").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l111111ll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11l1lll_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ″")))
        bstack1l111111ll_opy_ = bstack11l1lll_opy_ (u"ࠧࠨ‴")
        if not passed:
            try:
                bstack1l111111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1lll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨ‵").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l111111ll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫ‶")
                    + json.dumps(bstack11l1lll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠢࠤ‷"))
                    + bstack11l1lll_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧ‸")
                )
            else:
                item._driver.execute_script(
                    bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨ‹")
                    + json.dumps(str(bstack1l111111ll_opy_))
                    + bstack11l1lll_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢ›")
                )
        except Exception as e:
            summary.append(bstack11l1lll_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡥࡳࡴ࡯ࡵࡣࡷࡩ࠿ࠦࡻ࠱ࡿࠥ※").format(e))
def bstack11111l1l111_opy_(test_name, error_message):
    try:
        bstack111111l11ll_opy_ = []
        bstack1llll11l1_opy_ = os.environ.get(bstack11l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭‼"), bstack11l1lll_opy_ (u"ࠧ࠱ࠩ‽"))
        bstack1l1111ll1l_opy_ = {bstack11l1lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭‾"): test_name, bstack11l1lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ‿"): error_message, bstack11l1lll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ⁀"): bstack1llll11l1_opy_}
        bstack111111ll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1lll_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ⁁"))
        if os.path.exists(bstack111111ll1ll_opy_):
            with open(bstack111111ll1ll_opy_) as f:
                bstack111111l11ll_opy_ = json.load(f)
        bstack111111l11ll_opy_.append(bstack1l1111ll1l_opy_)
        with open(bstack111111ll1ll_opy_, bstack11l1lll_opy_ (u"ࠬࡽࠧ⁂")) as f:
            json.dump(bstack111111l11ll_opy_, f)
    except Exception as e:
        logger.debug(bstack11l1lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡨࡶࡸ࡯ࡳࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡳࡽࡹ࡫ࡳࡵࠢࡨࡶࡷࡵࡲࡴ࠼ࠣࠫ⁃") + str(e))
def bstack11111l1l11l_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack11l1lll_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨ⁄"), bstack11l1lll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥ⁅")]:
        return
    if (str(skipSessionName).lower() != bstack11l1lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⁆")):
        bstack1lllll111_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1lll_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧ⁇")))
    bstack1l111111ll_opy_ = bstack11l1lll_opy_ (u"ࠦࠧ⁈")
    bstack111l111ll11_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l111111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1lll_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧ⁉").format(e)
                )
        try:
            if passed:
                bstack1l1111l1l_opy_(getattr(item, bstack11l1lll_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ⁊"), None), bstack11l1lll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ⁋"))
            else:
                error_message = bstack11l1lll_opy_ (u"ࠨࠩ⁌")
                if bstack1l111111ll_opy_:
                    bstack1llll1llll_opy_(item._page, str(bstack1l111111ll_opy_), bstack11l1lll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ⁍"))
                    bstack1l1111l1l_opy_(getattr(item, bstack11l1lll_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩ⁎"), None), bstack11l1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ⁏"), str(bstack1l111111ll_opy_))
                    error_message = str(bstack1l111111ll_opy_)
                else:
                    bstack1l1111l1l_opy_(getattr(item, bstack11l1lll_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫ⁐"), None), bstack11l1lll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ⁑"))
                bstack11111l1l111_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11l1lll_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼ࠲ࢀࠦ⁒").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack11l1lll_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ⁓"), default=bstack11l1lll_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣ⁔"), help=bstack11l1lll_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤ⁕"))
    parser.addoption(bstack11l1lll_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ⁖"), default=bstack11l1lll_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦ⁗"), help=bstack11l1lll_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧ⁘"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11l1lll_opy_ (u"ࠢ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠤ⁙"), action=bstack11l1lll_opy_ (u"ࠣࡵࡷࡳࡷ࡫ࠢ⁚"), default=bstack11l1lll_opy_ (u"ࠤࡦ࡬ࡷࡵ࡭ࡦࠤ⁛"),
                         help=bstack11l1lll_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴࠤ⁜"))
def bstack111llll111_opy_(log):
    if not (log[bstack11l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⁝")] and log[bstack11l1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⁞")].strip()):
        return
    active = bstack111lll1111_opy_()
    log = {
        bstack11l1lll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ "): log[bstack11l1lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⁠")],
        bstack11l1lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⁡"): bstack111l1lllll_opy_().isoformat() + bstack11l1lll_opy_ (u"ࠩ࡝ࠫ⁢"),
        bstack11l1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⁣"): log[bstack11l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⁤")],
    }
    if active:
        if active[bstack11l1lll_opy_ (u"ࠬࡺࡹࡱࡧࠪ⁥")] == bstack11l1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⁦"):
            log[bstack11l1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⁧")] = active[bstack11l1lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⁨")]
        elif active[bstack11l1lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⁩")] == bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࠨ⁪"):
            log[bstack11l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⁫")] = active[bstack11l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⁬")]
    bstack1lll11111l_opy_.bstack1ll1l1lll_opy_([log])
def bstack111lll1111_opy_():
    if len(store[bstack11l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⁭")]) > 0 and store[bstack11l1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⁮")][-1]:
        return {
            bstack11l1lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭⁯"): bstack11l1lll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⁰"),
            bstack11l1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪⁱ"): store[bstack11l1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⁲")][-1]
        }
    if store.get(bstack11l1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⁳"), None):
        return {
            bstack11l1lll_opy_ (u"࠭ࡴࡺࡲࡨࠫ⁴"): bstack11l1lll_opy_ (u"ࠧࡵࡧࡶࡸࠬ⁵"),
            bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⁶"): store[bstack11l1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⁷")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.INIT_TEST, bstack1ll1lll1111_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.INIT_TEST, bstack1ll1lll1111_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.TEST, bstack1ll1lll1111_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._111111lllll_opy_ = True
        bstack11ll1l111_opy_ = bstack1l11111lll_opy_.bstack1ll1l1l1ll_opy_(bstack11l11ll1lll_opy_(item.own_markers))
        if not cli.bstack1lll1llll1l_opy_(bstack1llll11l11l_opy_):
            item._a11y_test_case = bstack11ll1l111_opy_
            if bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⁸"), None):
                driver = getattr(item, bstack11l1lll_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⁹"), None)
                item._a11y_started = bstack1l11111lll_opy_.bstack1lll1ll11l_opy_(driver, bstack11ll1l111_opy_)
        if not bstack1lll11111l_opy_.on() or bstack111111l1lll_opy_ != bstack11l1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⁺"):
            return
        global current_test_uuid #, bstack111lll111l_opy_
        bstack1111llll1l_opy_ = {
            bstack11l1lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⁻"): uuid4().__str__(),
            bstack11l1lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⁼"): bstack111l1lllll_opy_().isoformat() + bstack11l1lll_opy_ (u"ࠨ࡜ࠪ⁽")
        }
        current_test_uuid = bstack1111llll1l_opy_[bstack11l1lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⁾")]
        store[bstack11l1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧⁿ")] = bstack1111llll1l_opy_[bstack11l1lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ₀")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1111llllll_opy_[item.nodeid] = {**_1111llllll_opy_[item.nodeid], **bstack1111llll1l_opy_}
        bstack11111l11l1l_opy_(item, _1111llllll_opy_[item.nodeid], bstack11l1lll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭₁"))
    except Exception as err:
        print(bstack11l1lll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡣࡢ࡮࡯࠾ࠥࢁࡽࠨ₂"), str(err))
def pytest_runtest_setup(item):
    store[bstack11l1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ₃")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.BEFORE_EACH, bstack1ll1lll1111_opy_.PRE, item, bstack11l1lll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ₄"))
        return # skip all existing bstack1111111ll1l_opy_
    global bstack111111ll11l_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l1ll1111l_opy_():
        atexit.register(bstack1l111l1ll1_opy_)
        if not bstack111111ll11l_opy_:
            try:
                bstack1111111llll_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1l1l1ll1_opy_():
                    bstack1111111llll_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1111111llll_opy_:
                    signal.signal(s, bstack11111l11111_opy_)
                bstack111111ll11l_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11l1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡧࡪࡵࡷࡩࡷࠦࡳࡪࡩࡱࡥࡱࠦࡨࡢࡰࡧࡰࡪࡸࡳ࠻ࠢࠥ₅") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111l111l1ll_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11l1lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ₆")
    try:
        if not bstack1lll11111l_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack1111llll1l_opy_ = {
            bstack11l1lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ₇"): uuid,
            bstack11l1lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ₈"): bstack111l1lllll_opy_().isoformat() + bstack11l1lll_opy_ (u"࡚࠭ࠨ₉"),
            bstack11l1lll_opy_ (u"ࠧࡵࡻࡳࡩࠬ₊"): bstack11l1lll_opy_ (u"ࠨࡪࡲࡳࡰ࠭₋"),
            bstack11l1lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ₌"): bstack11l1lll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ₍"),
            bstack11l1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ₎"): bstack11l1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ₏")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪₐ")] = item
        store[bstack11l1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫₑ")] = [uuid]
        if not _1111llllll_opy_.get(item.nodeid, None):
            _1111llllll_opy_[item.nodeid] = {bstack11l1lll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧₒ"): [], bstack11l1lll_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫₓ"): []}
        _1111llllll_opy_[item.nodeid][bstack11l1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩₔ")].append(bstack1111llll1l_opy_[bstack11l1lll_opy_ (u"ࠫࡺࡻࡩࡥࠩₕ")])
        _1111llllll_opy_[item.nodeid + bstack11l1lll_opy_ (u"ࠬ࠳ࡳࡦࡶࡸࡴࠬₖ")] = bstack1111llll1l_opy_
        bstack11111l11l11_opy_(item, bstack1111llll1l_opy_, bstack11l1lll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧₗ"))
    except Exception as err:
        print(bstack11l1lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪₘ"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.TEST, bstack1ll1lll1111_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.AFTER_EACH, bstack1ll1lll1111_opy_.PRE, item, bstack11l1lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪₙ"))
        return # skip all existing bstack1111111ll1l_opy_
    try:
        global bstack1l1111l1ll_opy_
        bstack1llll11l1_opy_ = 0
        if bstack1llll1ll1l_opy_ is True:
            bstack1llll11l1_opy_ = int(os.environ.get(bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩₚ")))
        if bstack1l11l1ll11_opy_.bstack1lll1l11ll_opy_() == bstack11l1lll_opy_ (u"ࠥࡸࡷࡻࡥࠣₛ"):
            if bstack1l11l1ll11_opy_.bstack1l1lll1ll_opy_() == bstack11l1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨₜ"):
                bstack111111l1ll1_opy_ = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ₝"), None)
                bstack11l1l111ll_opy_ = bstack111111l1ll1_opy_ + bstack11l1lll_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤ₞")
                driver = getattr(item, bstack11l1lll_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ₟"), None)
                bstack11l11l1l11_opy_ = getattr(item, bstack11l1lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭₠"), None)
                bstack1lllll1ll1_opy_ = getattr(item, bstack11l1lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ₡"), None)
                PercySDK.screenshot(driver, bstack11l1l111ll_opy_, bstack11l11l1l11_opy_=bstack11l11l1l11_opy_, bstack1lllll1ll1_opy_=bstack1lllll1ll1_opy_, bstack111l1llll_opy_=bstack1llll11l1_opy_)
        if not cli.bstack1lll1llll1l_opy_(bstack1llll11l11l_opy_):
            if getattr(item, bstack11l1lll_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡶࡸࡦࡸࡴࡦࡦࠪ₢"), False):
                bstack11ll1l111l_opy_.bstack11lll1ll11_opy_(getattr(item, bstack11l1lll_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ₣"), None), bstack1l1111l1ll_opy_, logger, item)
        if not bstack1lll11111l_opy_.on():
            return
        bstack1111llll1l_opy_ = {
            bstack11l1lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ₤"): uuid4().__str__(),
            bstack11l1lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ₥"): bstack111l1lllll_opy_().isoformat() + bstack11l1lll_opy_ (u"࡛ࠧࠩ₦"),
            bstack11l1lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭₧"): bstack11l1lll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ₨"),
            bstack11l1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭₩"): bstack11l1lll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ₪"),
            bstack11l1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ₫"): bstack11l1lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ€")
        }
        _1111llllll_opy_[item.nodeid + bstack11l1lll_opy_ (u"ࠧ࠮ࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ₭")] = bstack1111llll1l_opy_
        bstack11111l11l11_opy_(item, bstack1111llll1l_opy_, bstack11l1lll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ₮"))
    except Exception as err:
        print(bstack11l1lll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱ࠾ࠥࢁࡽࠨ₯"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack111l111lll1_opy_(fixturedef.argname):
        store[bstack11l1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩ₰")] = request.node
    elif bstack111l111ll1l_opy_(fixturedef.argname):
        store[bstack11l1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩ₱")] = request.node
    if not bstack1lll11111l_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.SETUP_FIXTURE, bstack1ll1lll1111_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.SETUP_FIXTURE, bstack1ll1lll1111_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1111111ll1l_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.SETUP_FIXTURE, bstack1ll1lll1111_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.SETUP_FIXTURE, bstack1ll1lll1111_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1111111ll1l_opy_
    try:
        fixture = {
            bstack11l1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ₲"): fixturedef.argname,
            bstack11l1lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭₳"): bstack11l111lll1l_opy_(outcome),
            bstack11l1lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ₴"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11l1lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ₵")]
        if not _1111llllll_opy_.get(current_test_item.nodeid, None):
            _1111llllll_opy_[current_test_item.nodeid] = {bstack11l1lll_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ₶"): []}
        _1111llllll_opy_[current_test_item.nodeid][bstack11l1lll_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ₷")].append(fixture)
    except Exception as err:
        logger.debug(bstack11l1lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧ₸"), str(err))
if bstack1ll11lll_opy_() and bstack1lll11111l_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.STEP, bstack1ll1lll1111_opy_.PRE, request, step)
            return
        try:
            _1111llllll_opy_[request.node.nodeid][bstack11l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ₹")].bstack1111ll1l1_opy_(id(step))
        except Exception as err:
            print(bstack11l1lll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶ࠺ࠡࡽࢀࠫ₺"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.STEP, bstack1ll1lll1111_opy_.POST, request, step, exception)
            return
        try:
            _1111llllll_opy_[request.node.nodeid][bstack11l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ₻")].bstack11l1111l11_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11l1lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ₼"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.STEP, bstack1ll1lll1111_opy_.POST, request, step)
            return
        try:
            bstack111lll11ll_opy_: bstack111llllll1_opy_ = _1111llllll_opy_[request.node.nodeid][bstack11l1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ₽")]
            bstack111lll11ll_opy_.bstack11l1111l11_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11l1lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧ₾"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack111111l1lll_opy_
        try:
            if not bstack1lll11111l_opy_.on() or bstack111111l1lll_opy_ != bstack11l1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ₿"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.TEST, bstack1ll1lll1111_opy_.PRE, request, feature, scenario)
                return
            driver = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ⃀"), None)
            if not _1111llllll_opy_.get(request.node.nodeid, None):
                _1111llllll_opy_[request.node.nodeid] = {}
            bstack111lll11ll_opy_ = bstack111llllll1_opy_.bstack1111ll111ll_opy_(
                scenario, feature, request.node,
                name=bstack111l1111ll1_opy_(request.node, scenario),
                started_at=bstack1lll11l11_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11l1lll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ⃁"),
                tags=bstack111l111l111_opy_(feature, scenario),
                bstack111lllllll_opy_=bstack1lll11111l_opy_.bstack11l111111l_opy_(driver) if driver and driver.session_id else {}
            )
            _1111llllll_opy_[request.node.nodeid][bstack11l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⃂")] = bstack111lll11ll_opy_
            bstack1111111lll1_opy_(bstack111lll11ll_opy_.uuid)
            bstack1lll11111l_opy_.bstack111llll1ll_opy_(bstack11l1lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⃃"), bstack111lll11ll_opy_)
        except Exception as err:
            print(bstack11l1lll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫ⃄"), str(err))
def bstack111111l111l_opy_(bstack111ll1lll1_opy_):
    if bstack111ll1lll1_opy_ in store[bstack11l1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⃅")]:
        store[bstack11l1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⃆")].remove(bstack111ll1lll1_opy_)
def bstack1111111lll1_opy_(test_uuid):
    store[bstack11l1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⃇")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1lll11111l_opy_.bstack11111llll1l_opy_
def bstack11111l111l1_opy_(item, call, report):
    logger.debug(bstack11l1lll_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡸࡴࠨ⃈"))
    global bstack111111l1lll_opy_
    bstack1lll11l1_opy_ = bstack1lll11l11_opy_()
    if hasattr(report, bstack11l1lll_opy_ (u"ࠧࡴࡶࡲࡴࠬ⃉")):
        bstack1lll11l1_opy_ = bstack11l1lll1111_opy_(report.stop)
    elif hasattr(report, bstack11l1lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࠧ⃊")):
        bstack1lll11l1_opy_ = bstack11l1lll1111_opy_(report.start)
    try:
        if getattr(report, bstack11l1lll_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⃋"), bstack11l1lll_opy_ (u"ࠪࠫ⃌")) == bstack11l1lll_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ⃍"):
            logger.debug(bstack11l1lll_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡹ࡫ࠠ࠮ࠢࡾࢁ࠱ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࠰ࠤࢀࢃࠧ⃎").format(getattr(report, bstack11l1lll_opy_ (u"࠭ࡷࡩࡧࡱࠫ⃏"), bstack11l1lll_opy_ (u"ࠧࠨ⃐")).__str__(), bstack111111l1lll_opy_))
            if bstack111111l1lll_opy_ == bstack11l1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⃑"):
                _1111llllll_opy_[item.nodeid][bstack11l1lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺ⃒ࠧ")] = bstack1lll11l1_opy_
                bstack11111l11l1l_opy_(item, _1111llllll_opy_[item.nodeid], bstack11l1lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨ⃓ࠬ"), report, call)
                store[bstack11l1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⃔")] = None
            elif bstack111111l1lll_opy_ == bstack11l1lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤ⃕"):
                bstack111lll11ll_opy_ = _1111llllll_opy_[item.nodeid][bstack11l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⃖")]
                bstack111lll11ll_opy_.set(hooks=_1111llllll_opy_[item.nodeid].get(bstack11l1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⃗"), []))
                exception, bstack111lll1l11_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111lll1l11_opy_ = [call.excinfo.exconly(), getattr(report, bstack11l1lll_opy_ (u"ࠨ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺ⃘ࠧ"), bstack11l1lll_opy_ (u"⃙ࠩࠪ"))]
                bstack111lll11ll_opy_.stop(time=bstack1lll11l1_opy_, result=Result(result=getattr(report, bstack11l1lll_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨ⃚ࠫ"), bstack11l1lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⃛")), exception=exception, bstack111lll1l11_opy_=bstack111lll1l11_opy_))
                bstack1lll11111l_opy_.bstack111llll1ll_opy_(bstack11l1lll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⃜"), _1111llllll_opy_[item.nodeid][bstack11l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⃝")])
        elif getattr(report, bstack11l1lll_opy_ (u"ࠧࡸࡪࡨࡲࠬ⃞"), bstack11l1lll_opy_ (u"ࠨࠩ⃟")) in [bstack11l1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⃠"), bstack11l1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ⃡")]:
            logger.debug(bstack11l1lll_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡸࡪࠦ࠭ࠡࡽࢀ࠰ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࠯ࠣࡿࢂ࠭⃢").format(getattr(report, bstack11l1lll_opy_ (u"ࠬࡽࡨࡦࡰࠪ⃣"), bstack11l1lll_opy_ (u"࠭ࠧ⃤")).__str__(), bstack111111l1lll_opy_))
            bstack11l11111l1_opy_ = item.nodeid + bstack11l1lll_opy_ (u"ࠧ࠮⃥ࠩ") + getattr(report, bstack11l1lll_opy_ (u"ࠨࡹ࡫ࡩࡳ⃦࠭"), bstack11l1lll_opy_ (u"ࠩࠪ⃧"))
            if getattr(report, bstack11l1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧ⃨ࠫ"), False):
                hook_type = bstack11l1lll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ⃩") if getattr(report, bstack11l1lll_opy_ (u"ࠬࡽࡨࡦࡰ⃪ࠪ"), bstack11l1lll_opy_ (u"⃫࠭ࠧ")) == bstack11l1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵ⃬࠭") else bstack11l1lll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌ⃭ࠬ")
                _1111llllll_opy_[bstack11l11111l1_opy_] = {
                    bstack11l1lll_opy_ (u"ࠩࡸࡹ࡮ࡪ⃮ࠧ"): uuid4().__str__(),
                    bstack11l1lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺ⃯ࠧ"): bstack1lll11l1_opy_,
                    bstack11l1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⃰"): hook_type
                }
            _1111llllll_opy_[bstack11l11111l1_opy_][bstack11l1lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⃱")] = bstack1lll11l1_opy_
            bstack111111l111l_opy_(_1111llllll_opy_[bstack11l11111l1_opy_][bstack11l1lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⃲")])
            bstack11111l11l11_opy_(item, _1111llllll_opy_[bstack11l11111l1_opy_], bstack11l1lll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⃳"), report, call)
            if getattr(report, bstack11l1lll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭⃴"), bstack11l1lll_opy_ (u"ࠩࠪ⃵")) == bstack11l1lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⃶"):
                if getattr(report, bstack11l1lll_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ⃷"), bstack11l1lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⃸")) == bstack11l1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⃹"):
                    bstack1111llll1l_opy_ = {
                        bstack11l1lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⃺"): uuid4().__str__(),
                        bstack11l1lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⃻"): bstack1lll11l11_opy_(),
                        bstack11l1lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⃼"): bstack1lll11l11_opy_()
                    }
                    _1111llllll_opy_[item.nodeid] = {**_1111llllll_opy_[item.nodeid], **bstack1111llll1l_opy_}
                    bstack11111l11l1l_opy_(item, _1111llllll_opy_[item.nodeid], bstack11l1lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⃽"))
                    bstack11111l11l1l_opy_(item, _1111llllll_opy_[item.nodeid], bstack11l1lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⃾"), report, call)
    except Exception as err:
        print(bstack11l1lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡼࡿࠪ⃿"), str(err))
def bstack111111l1l11_opy_(test, bstack1111llll1l_opy_, result=None, call=None, bstack1lll1ll1l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111lll11ll_opy_ = {
        bstack11l1lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ℀"): bstack1111llll1l_opy_[bstack11l1lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ℁")],
        bstack11l1lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ℂ"): bstack11l1lll_opy_ (u"ࠩࡷࡩࡸࡺࠧ℃"),
        bstack11l1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨ℄"): test.name,
        bstack11l1lll_opy_ (u"ࠫࡧࡵࡤࡺࠩ℅"): {
            bstack11l1lll_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ℆"): bstack11l1lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ℇ"),
            bstack11l1lll_opy_ (u"ࠧࡤࡱࡧࡩࠬ℈"): inspect.getsource(test.obj)
        },
        bstack11l1lll_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ℉"): test.name,
        bstack11l1lll_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨℊ"): test.name,
        bstack11l1lll_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪℋ"): bstack11l111l11l_opy_.bstack111l1lll1l_opy_(test),
        bstack11l1lll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧℌ"): file_path,
        bstack11l1lll_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧℍ"): file_path,
        bstack11l1lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ℎ"): bstack11l1lll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨℏ"),
        bstack11l1lll_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ℐ"): file_path,
        bstack11l1lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ℑ"): bstack1111llll1l_opy_[bstack11l1lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧℒ")],
        bstack11l1lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧℓ"): bstack11l1lll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ℔"),
        bstack11l1lll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩℕ"): {
            bstack11l1lll_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫ№"): test.nodeid
        },
        bstack11l1lll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭℗"): bstack11l11ll1lll_opy_(test.own_markers)
    }
    if bstack1lll1ll1l_opy_ in [bstack11l1lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ℘"), bstack11l1lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬℙ")]:
        bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠫࡲ࡫ࡴࡢࠩℚ")] = {
            bstack11l1lll_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧℛ"): bstack1111llll1l_opy_.get(bstack11l1lll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨℜ"), [])
        }
    if bstack1lll1ll1l_opy_ == bstack11l1lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨℝ"):
        bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ℞")] = bstack11l1lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ℟")
        bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ℠")] = bstack1111llll1l_opy_[bstack11l1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ℡")]
        bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ™")] = bstack1111llll1l_opy_[bstack11l1lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ℣")]
    if result:
        bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧℤ")] = result.outcome
        bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ℥")] = result.duration * 1000
        bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧΩ")] = bstack1111llll1l_opy_[bstack11l1lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ℧")]
        if result.failed:
            bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪℨ")] = bstack1lll11111l_opy_.bstack1111l111ll_opy_(call.excinfo.typename)
            bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭℩")] = bstack1lll11111l_opy_.bstack1111l111l11_opy_(call.excinfo, result)
        bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬK")] = bstack1111llll1l_opy_[bstack11l1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭Å")]
    if outcome:
        bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨℬ")] = bstack11l111lll1l_opy_(outcome)
        bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪℭ")] = 0
        bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ℮")] = bstack1111llll1l_opy_[bstack11l1lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩℯ")]
        if bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬℰ")] == bstack11l1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ℱ"):
            bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭Ⅎ")] = bstack11l1lll_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩℳ")  # bstack111111l1111_opy_
            bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪℴ")] = [{bstack11l1lll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ℵ"): [bstack11l1lll_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨℶ")]}]
        bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫℷ")] = bstack1111llll1l_opy_[bstack11l1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬℸ")]
    return bstack111lll11ll_opy_
def bstack11111l111ll_opy_(test, bstack111l1llll1_opy_, bstack1lll1ll1l_opy_, result, call, outcome, bstack11111l11lll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l1llll1_opy_[bstack11l1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪℹ")]
    hook_name = bstack111l1llll1_opy_[bstack11l1lll_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ℺")]
    hook_data = {
        bstack11l1lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ℻"): bstack111l1llll1_opy_[bstack11l1lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨℼ")],
        bstack11l1lll_opy_ (u"ࠫࡹࡿࡰࡦࠩℽ"): bstack11l1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪℾ"),
        bstack11l1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫℿ"): bstack11l1lll_opy_ (u"ࠧࡼࡿࠪ⅀").format(bstack111l1111l1l_opy_(hook_name)),
        bstack11l1lll_opy_ (u"ࠨࡤࡲࡨࡾ࠭⅁"): {
            bstack11l1lll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧ⅂"): bstack11l1lll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ⅃"),
            bstack11l1lll_opy_ (u"ࠫࡨࡵࡤࡦࠩ⅄"): None
        },
        bstack11l1lll_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫⅅ"): test.name,
        bstack11l1lll_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ⅆ"): bstack11l111l11l_opy_.bstack111l1lll1l_opy_(test, hook_name),
        bstack11l1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪⅇ"): file_path,
        bstack11l1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪⅈ"): file_path,
        bstack11l1lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩⅉ"): bstack11l1lll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⅊"),
        bstack11l1lll_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩ⅋"): file_path,
        bstack11l1lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⅌"): bstack111l1llll1_opy_[bstack11l1lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⅍")],
        bstack11l1lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪⅎ"): bstack11l1lll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ⅏") if bstack111111l1lll_opy_ == bstack11l1lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭⅐") else bstack11l1lll_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ⅑"),
        bstack11l1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⅒"): hook_type
    }
    bstack1111ll1l111_opy_ = bstack111l111l11_opy_(_1111llllll_opy_.get(test.nodeid, None))
    if bstack1111ll1l111_opy_:
        hook_data[bstack11l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪ⅓")] = bstack1111ll1l111_opy_
    if result:
        hook_data[bstack11l1lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⅔")] = result.outcome
        hook_data[bstack11l1lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⅕")] = result.duration * 1000
        hook_data[bstack11l1lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⅖")] = bstack111l1llll1_opy_[bstack11l1lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⅗")]
        if result.failed:
            hook_data[bstack11l1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⅘")] = bstack1lll11111l_opy_.bstack1111l111ll_opy_(call.excinfo.typename)
            hook_data[bstack11l1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⅙")] = bstack1lll11111l_opy_.bstack1111l111l11_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11l1lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⅚")] = bstack11l111lll1l_opy_(outcome)
        hook_data[bstack11l1lll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⅛")] = 100
        hook_data[bstack11l1lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⅜")] = bstack111l1llll1_opy_[bstack11l1lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⅝")]
        if hook_data[bstack11l1lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⅞")] == bstack11l1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⅟"):
            hook_data[bstack11l1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪⅠ")] = bstack11l1lll_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭Ⅱ")  # bstack111111l1111_opy_
            hook_data[bstack11l1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧⅢ")] = [{bstack11l1lll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪⅣ"): [bstack11l1lll_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬⅤ")]}]
    if bstack11111l11lll_opy_:
        hook_data[bstack11l1lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩⅥ")] = bstack11111l11lll_opy_.result
        hook_data[bstack11l1lll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫⅦ")] = bstack11l11lll11l_opy_(bstack111l1llll1_opy_[bstack11l1lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨⅧ")], bstack111l1llll1_opy_[bstack11l1lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪⅨ")])
        hook_data[bstack11l1lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫⅩ")] = bstack111l1llll1_opy_[bstack11l1lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬⅪ")]
        if hook_data[bstack11l1lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨⅫ")] == bstack11l1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩⅬ"):
            hook_data[bstack11l1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩⅭ")] = bstack1lll11111l_opy_.bstack1111l111ll_opy_(bstack11111l11lll_opy_.exception_type)
            hook_data[bstack11l1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬⅮ")] = [{bstack11l1lll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨⅯ"): bstack11l1llll1l1_opy_(bstack11111l11lll_opy_.exception)}]
    return hook_data
def bstack11111l11l1l_opy_(test, bstack1111llll1l_opy_, bstack1lll1ll1l_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack11l1lll_opy_ (u"࠭ࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡥࡷࡧࡱࡸ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡶࡨࡷࡹࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠥ࠳ࠠࡼࡿࠪⅰ").format(bstack1lll1ll1l_opy_))
    bstack111lll11ll_opy_ = bstack111111l1l11_opy_(test, bstack1111llll1l_opy_, result, call, bstack1lll1ll1l_opy_, outcome)
    driver = getattr(test, bstack11l1lll_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨⅱ"), None)
    if bstack1lll1ll1l_opy_ == bstack11l1lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩⅲ") and driver:
        bstack111lll11ll_opy_[bstack11l1lll_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨⅳ")] = bstack1lll11111l_opy_.bstack11l111111l_opy_(driver)
    if bstack1lll1ll1l_opy_ == bstack11l1lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫⅴ"):
        bstack1lll1ll1l_opy_ = bstack11l1lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ⅵ")
    bstack111l11l1ll_opy_ = {
        bstack11l1lll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩⅶ"): bstack1lll1ll1l_opy_,
        bstack11l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨⅷ"): bstack111lll11ll_opy_
    }
    bstack1lll11111l_opy_.bstack1ll1ll11l_opy_(bstack111l11l1ll_opy_)
    if bstack1lll1ll1l_opy_ == bstack11l1lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨⅸ"):
        threading.current_thread().bstackTestMeta = {bstack11l1lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨⅹ"): bstack11l1lll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪⅺ")}
    elif bstack1lll1ll1l_opy_ == bstack11l1lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬⅻ"):
        threading.current_thread().bstackTestMeta = {bstack11l1lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫⅼ"): getattr(result, bstack11l1lll_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭ⅽ"), bstack11l1lll_opy_ (u"࠭ࠧⅾ"))}
def bstack11111l11l11_opy_(test, bstack1111llll1l_opy_, bstack1lll1ll1l_opy_, result=None, call=None, outcome=None, bstack11111l11lll_opy_=None):
    logger.debug(bstack11l1lll_opy_ (u"ࠧࡴࡧࡱࡨࡤ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡦࡸࡨࡲࡹࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢ࡫ࡳࡴࡱࠠࡥࡣࡷࡥ࠱ࠦࡥࡷࡧࡱࡸ࡙ࡿࡰࡦࠢ࠰ࠤࢀࢃࠧⅿ").format(bstack1lll1ll1l_opy_))
    hook_data = bstack11111l111ll_opy_(test, bstack1111llll1l_opy_, bstack1lll1ll1l_opy_, result, call, outcome, bstack11111l11lll_opy_)
    bstack111l11l1ll_opy_ = {
        bstack11l1lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬↀ"): bstack1lll1ll1l_opy_,
        bstack11l1lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫↁ"): hook_data
    }
    bstack1lll11111l_opy_.bstack1ll1ll11l_opy_(bstack111l11l1ll_opy_)
def bstack111l111l11_opy_(bstack1111llll1l_opy_):
    if not bstack1111llll1l_opy_:
        return None
    if bstack1111llll1l_opy_.get(bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ↂ"), None):
        return getattr(bstack1111llll1l_opy_[bstack11l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧↃ")], bstack11l1lll_opy_ (u"ࠬࡻࡵࡪࡦࠪↄ"), None)
    return bstack1111llll1l_opy_.get(bstack11l1lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫↅ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.LOG, bstack1ll1lll1111_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_.LOG, bstack1ll1lll1111_opy_.POST, request, caplog)
        return # skip all existing bstack1111111ll1l_opy_
    try:
        if not bstack1lll11111l_opy_.on():
            return
        places = [bstack11l1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ↆ"), bstack11l1lll_opy_ (u"ࠨࡥࡤࡰࡱ࠭ↇ"), bstack11l1lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫↈ")]
        logs = []
        for bstack111111ll1l1_opy_ in places:
            records = caplog.get_records(bstack111111ll1l1_opy_)
            bstack111111llll1_opy_ = bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ↉") if bstack111111ll1l1_opy_ == bstack11l1lll_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ↊") else bstack11l1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ↋")
            bstack1111111ll11_opy_ = request.node.nodeid + (bstack11l1lll_opy_ (u"࠭ࠧ↌") if bstack111111ll1l1_opy_ == bstack11l1lll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ↍") else bstack11l1lll_opy_ (u"ࠨ࠯ࠪ↎") + bstack111111ll1l1_opy_)
            test_uuid = bstack111l111l11_opy_(_1111llllll_opy_.get(bstack1111111ll11_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11l11l11lll_opy_(record.message):
                    continue
                logs.append({
                    bstack11l1lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ↏"): bstack11l11l1lll1_opy_(record.created).isoformat() + bstack11l1lll_opy_ (u"ࠪ࡞ࠬ←"),
                    bstack11l1lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ↑"): record.levelname,
                    bstack11l1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭→"): record.message,
                    bstack111111llll1_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1lll11111l_opy_.bstack1ll1l1lll_opy_(logs)
    except Exception as err:
        print(bstack11l1lll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡤࡱࡱࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡀࠠࡼࡿࠪ↓"), str(err))
def bstack11lll11l11_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack111l1l11_opy_
    bstack1l11l11ll_opy_ = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ↔"), None) and bstack111l11lll_opy_(
            threading.current_thread(), bstack11l1lll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ↕"), None)
    bstack1l111lllll_opy_ = getattr(driver, bstack11l1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ↖"), None) != None and getattr(driver, bstack11l1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ↗"), None) == True
    if sequence == bstack11l1lll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ↘") and driver != None:
      if not bstack111l1l11_opy_ and bstack1l1ll1l1ll1_opy_() and bstack11l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ↙") in CONFIG and CONFIG[bstack11l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭↚")] == True and bstack1lll11ll11_opy_.bstack1l1ll1ll11_opy_(driver_command) and (bstack1l111lllll_opy_ or bstack1l11l11ll_opy_) and not bstack1ll11llll_opy_(args):
        try:
          bstack111l1l11_opy_ = True
          logger.debug(bstack11l1lll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡻࡾࠩ↛").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11l1lll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡹࡣࡢࡰࠣࡿࢂ࠭↜").format(str(err)))
        bstack111l1l11_opy_ = False
    if sequence == bstack11l1lll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ↝"):
        if driver_command == bstack11l1lll_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ↞"):
            bstack1lll11111l_opy_.bstack1111lll1_opy_({
                bstack11l1lll_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ↟"): response[bstack11l1lll_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ↠")],
                bstack11l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭↡"): store[bstack11l1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ↢")]
            })
def bstack1l111l1ll1_opy_():
    global bstack11l111ll_opy_
    bstack1l11l1lll_opy_.bstack1ll1l111l_opy_()
    logging.shutdown()
    bstack1lll11111l_opy_.bstack111ll11l1l_opy_()
    for driver in bstack11l111ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11111l11111_opy_(*args):
    global bstack11l111ll_opy_
    bstack1lll11111l_opy_.bstack111ll11l1l_opy_()
    for driver in bstack11l111ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11111l1l1_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1l11111l11_opy_(self, *args, **kwargs):
    bstack1l1l1l1l1_opy_ = bstack11l1l11l1l_opy_(self, *args, **kwargs)
    bstack1l1l1l1l1l_opy_ = getattr(threading.current_thread(), bstack11l1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩ↣"), None)
    if bstack1l1l1l1l1l_opy_ and bstack1l1l1l1l1l_opy_.get(bstack11l1lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ↤"), bstack11l1lll_opy_ (u"ࠪࠫ↥")) == bstack11l1lll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ↦"):
        bstack1lll11111l_opy_.bstack111l1ll11_opy_(self)
    return bstack1l1l1l1l1_opy_
@measure(event_name=EVENTS.bstack1111l11ll_opy_, stage=STAGE.bstack1l1l1l11_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1llll1ll1_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11ll1llll1_opy_ = Config.bstack1ll1l1l1l1_opy_()
    if bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ↧")):
        return
    bstack11ll1llll1_opy_.bstack11l1l11lll_opy_(bstack11l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ↨"), True)
    global bstack1l11l1l11l_opy_
    global bstack11l1ll1l1_opy_
    bstack1l11l1l11l_opy_ = framework_name
    logger.info(bstack1l1lll1111_opy_.format(bstack1l11l1l11l_opy_.split(bstack11l1lll_opy_ (u"ࠧ࠮ࠩ↩"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1ll1l1ll1_opy_():
            Service.start = bstack11l11lll11_opy_
            Service.stop = bstack11ll1l11l1_opy_
            webdriver.Remote.get = bstack1l11lll1l_opy_
            webdriver.Remote.__init__ = bstack11l11l1111_opy_
            if not isinstance(os.getenv(bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩ↪")), str):
                return
            WebDriver.close = bstack1llll11ll1_opy_
            WebDriver.quit = bstack11llll1111_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1lll11111l_opy_.on():
            webdriver.Remote.__init__ = bstack1l11111l11_opy_
        bstack11l1ll1l1_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack11l1lll_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ↫")):
        bstack11l1ll1l1_opy_ = eval(os.environ.get(bstack11l1lll_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨ↬")))
    if not bstack11l1ll1l1_opy_:
        bstack1lll1llll1_opy_(bstack11l1lll_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨ↭"), bstack11l1llll11_opy_)
    if bstack1llll1l1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._11l1ll1l_opy_ = bstack1llll11ll_opy_
        except Exception as e:
            logger.error(bstack1l1l1l111l_opy_.format(str(e)))
    if bstack11l1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ↮") in str(framework_name).lower():
        if not bstack1l1ll1l1ll1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll1lll1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1ll1l1llll_opy_
            Config.getoption = bstack11l1l11l1_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1111llll1_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1l1ll11_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack11llll1111_opy_(self):
    global bstack1l11l1l11l_opy_
    global bstack111l111l1_opy_
    global bstack1lll11ll1_opy_
    try:
        if bstack11l1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭↯") in bstack1l11l1l11l_opy_ and self.session_id != None and bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ↰"), bstack11l1lll_opy_ (u"ࠨࠩ↱")) != bstack11l1lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ↲"):
            bstack1l1llllll_opy_ = bstack11l1lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ↳") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ↴")
            bstack1l1111ll_opy_(logger, True)
            if self != None:
                bstack11ll1ll1_opy_(self, bstack1l1llllll_opy_, bstack11l1lll_opy_ (u"ࠬ࠲ࠠࠨ↵").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1lll1llll1l_opy_(bstack1llll11l11l_opy_):
            item = store.get(bstack11l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ↶"), None)
            if item is not None and bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭↷"), None):
                bstack11ll1l111l_opy_.bstack11lll1ll11_opy_(self, bstack1l1111l1ll_opy_, logger, item)
        threading.current_thread().testStatus = bstack11l1lll_opy_ (u"ࠨࠩ↸")
    except Exception as e:
        logger.debug(bstack11l1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥ↹") + str(e))
    bstack1lll11ll1_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11ll11l1ll_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack11l11l1111_opy_(self, command_executor,
             desired_capabilities=None, bstack11l1llll_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack111l111l1_opy_
    global bstack1l1l1ll1l1_opy_
    global bstack1llll1ll1l_opy_
    global bstack1l11l1l11l_opy_
    global bstack11l1l11l1l_opy_
    global bstack11l111ll_opy_
    global bstack1ll1llll11_opy_
    global bstack11ll1l11l_opy_
    global bstack1l1111l1ll_opy_
    CONFIG[bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ↺")] = str(bstack1l11l1l11l_opy_) + str(__version__)
    command_executor = bstack1ll1l11ll1_opy_(bstack1ll1llll11_opy_, CONFIG)
    logger.debug(bstack1l1l1111_opy_.format(command_executor))
    proxy = bstack1ll11l1l1_opy_(CONFIG, proxy)
    bstack1llll11l1_opy_ = 0
    try:
        if bstack1llll1ll1l_opy_ is True:
            bstack1llll11l1_opy_ = int(os.environ.get(bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ↻")))
    except:
        bstack1llll11l1_opy_ = 0
    bstack11lll1l1ll_opy_ = bstack1l11l1ll_opy_(CONFIG, bstack1llll11l1_opy_)
    logger.debug(bstack1l111l1l11_opy_.format(str(bstack11lll1l1ll_opy_)))
    bstack1l1111l1ll_opy_ = CONFIG.get(bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ↼"))[bstack1llll11l1_opy_]
    if bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ↽") in CONFIG and CONFIG[bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ↾")]:
        bstack111ll1l11_opy_(bstack11lll1l1ll_opy_, bstack11ll1l11l_opy_)
    if bstack1l11111lll_opy_.bstack1l111l11ll_opy_(CONFIG, bstack1llll11l1_opy_) and bstack1l11111lll_opy_.bstack11lll111_opy_(bstack11lll1l1ll_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1lll1llll1l_opy_(bstack1llll11l11l_opy_):
            bstack1l11111lll_opy_.set_capabilities(bstack11lll1l1ll_opy_, CONFIG)
    if desired_capabilities:
        bstack111l11l1_opy_ = bstack1l11l11l1_opy_(desired_capabilities)
        bstack111l11l1_opy_[bstack11l1lll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ↿")] = bstack11l1ll1l1l_opy_(CONFIG)
        bstack111ll1l1_opy_ = bstack1l11l1ll_opy_(bstack111l11l1_opy_)
        if bstack111ll1l1_opy_:
            bstack11lll1l1ll_opy_ = update(bstack111ll1l1_opy_, bstack11lll1l1ll_opy_)
        desired_capabilities = None
    if options:
        bstack11l1l1l1l_opy_(options, bstack11lll1l1ll_opy_)
    if not options:
        options = bstack1l1ll1ll1_opy_(bstack11lll1l1ll_opy_)
    if proxy and bstack111111111_opy_() >= version.parse(bstack11l1lll_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ⇀")):
        options.proxy(proxy)
    if options and bstack111111111_opy_() >= version.parse(bstack11l1lll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ⇁")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack111111111_opy_() < version.parse(bstack11l1lll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ⇂")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11lll1l1ll_opy_)
    logger.info(bstack1l111ll1_opy_)
    bstack11l1lll1l1_opy_.end(EVENTS.bstack1111l11ll_opy_.value, EVENTS.bstack1111l11ll_opy_.value + bstack11l1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ⇃"),
                               EVENTS.bstack1111l11ll_opy_.value + bstack11l1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ⇄"), True, None)
    if bstack111111111_opy_() >= version.parse(bstack11l1lll_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ⇅")):
        bstack11l1l11l1l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111111111_opy_() >= version.parse(bstack11l1lll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ⇆")):
        bstack11l1l11l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack11l1llll_opy_=bstack11l1llll_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111111111_opy_() >= version.parse(bstack11l1lll_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ⇇")):
        bstack11l1l11l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11l1llll_opy_=bstack11l1llll_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack11l1l11l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11l1llll_opy_=bstack11l1llll_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack11llll1lll_opy_ = bstack11l1lll_opy_ (u"ࠪࠫ⇈")
        if bstack111111111_opy_() >= version.parse(bstack11l1lll_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ⇉")):
            bstack11llll1lll_opy_ = self.caps.get(bstack11l1lll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ⇊"))
        else:
            bstack11llll1lll_opy_ = self.capabilities.get(bstack11l1lll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ⇋"))
        if bstack11llll1lll_opy_:
            bstack11l1lll1l_opy_(bstack11llll1lll_opy_)
            if bstack111111111_opy_() <= version.parse(bstack11l1lll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ⇌")):
                self.command_executor._url = bstack11l1lll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ⇍") + bstack1ll1llll11_opy_ + bstack11l1lll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ⇎")
            else:
                self.command_executor._url = bstack11l1lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ⇏") + bstack11llll1lll_opy_ + bstack11l1lll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ⇐")
            logger.debug(bstack1l11111ll1_opy_.format(bstack11llll1lll_opy_))
        else:
            logger.debug(bstack1111l11l_opy_.format(bstack11l1lll_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨ⇑")))
    except Exception as e:
        logger.debug(bstack1111l11l_opy_.format(e))
    bstack111l111l1_opy_ = self.session_id
    if bstack11l1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⇒") in bstack1l11l1l11l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11l1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⇓"), None)
        if item:
            bstack111111l1l1l_opy_ = getattr(item, bstack11l1lll_opy_ (u"ࠨࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࡤࡹࡴࡢࡴࡷࡩࡩ࠭⇔"), False)
            if not getattr(item, bstack11l1lll_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⇕"), None) and bstack111111l1l1l_opy_:
                setattr(store[bstack11l1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⇖")], bstack11l1lll_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⇗"), self)
        bstack1l1l1l1l1l_opy_ = getattr(threading.current_thread(), bstack11l1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭⇘"), None)
        if bstack1l1l1l1l1l_opy_ and bstack1l1l1l1l1l_opy_.get(bstack11l1lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⇙"), bstack11l1lll_opy_ (u"ࠧࠨ⇚")) == bstack11l1lll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⇛"):
            bstack1lll11111l_opy_.bstack111l1ll11_opy_(self)
    bstack11l111ll_opy_.append(self)
    if bstack11l1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⇜") in CONFIG and bstack11l1lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⇝") in CONFIG[bstack11l1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⇞")][bstack1llll11l1_opy_]:
        bstack1l1l1ll1l1_opy_ = CONFIG[bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⇟")][bstack1llll11l1_opy_][bstack11l1lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⇠")]
    logger.debug(bstack1ll1l11l1l_opy_.format(bstack111l111l1_opy_))
@measure(event_name=EVENTS.bstack1lll111ll1_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1l11lll1l_opy_(self, url):
    global bstack1llll1ll_opy_
    global CONFIG
    try:
        bstack1l11l111ll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1ll11l1lll_opy_.format(str(err)))
    try:
        bstack1llll1ll_opy_(self, url)
    except Exception as e:
        try:
            bstack11l1ll1111_opy_ = str(e)
            if any(err_msg in bstack11l1ll1111_opy_ for err_msg in bstack1lllll11_opy_):
                bstack1l11l111ll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1ll11l1lll_opy_.format(str(err)))
        raise e
def bstack1l11llll_opy_(item, when):
    global bstack1ll111111l_opy_
    try:
        bstack1ll111111l_opy_(item, when)
    except Exception as e:
        pass
def bstack1111llll1_opy_(item, call, rep):
    global bstack1lll1lllll_opy_
    global bstack11l111ll_opy_
    name = bstack11l1lll_opy_ (u"ࠧࠨ⇡")
    try:
        if rep.when == bstack11l1lll_opy_ (u"ࠨࡥࡤࡰࡱ࠭⇢"):
            bstack111l111l1_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack11l1lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⇣"))
            try:
                if (str(skipSessionName).lower() != bstack11l1lll_opy_ (u"ࠪࡸࡷࡻࡥࠨ⇤")):
                    name = str(rep.nodeid)
                    bstack11lll1l111_opy_ = bstack1l111llll_opy_(bstack11l1lll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⇥"), name, bstack11l1lll_opy_ (u"ࠬ࠭⇦"), bstack11l1lll_opy_ (u"࠭ࠧ⇧"), bstack11l1lll_opy_ (u"ࠧࠨ⇨"), bstack11l1lll_opy_ (u"ࠨࠩ⇩"))
                    os.environ[bstack11l1lll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ⇪")] = name
                    for driver in bstack11l111ll_opy_:
                        if bstack111l111l1_opy_ == driver.session_id:
                            driver.execute_script(bstack11lll1l111_opy_)
            except Exception as e:
                logger.debug(bstack11l1lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ⇫").format(str(e)))
            try:
                bstack1llll11111_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11l1lll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⇬"):
                    status = bstack11l1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⇭") if rep.outcome.lower() == bstack11l1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⇮") else bstack11l1lll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⇯")
                    reason = bstack11l1lll_opy_ (u"ࠨࠩ⇰")
                    if status == bstack11l1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⇱"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11l1lll_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨ⇲") if status == bstack11l1lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⇳") else bstack11l1lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⇴")
                    data = name + bstack11l1lll_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨ⇵") if status == bstack11l1lll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⇶") else name + bstack11l1lll_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫ⇷") + reason
                    bstack1ll1lllll_opy_ = bstack1l111llll_opy_(bstack11l1lll_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ⇸"), bstack11l1lll_opy_ (u"ࠪࠫ⇹"), bstack11l1lll_opy_ (u"ࠫࠬ⇺"), bstack11l1lll_opy_ (u"ࠬ࠭⇻"), level, data)
                    for driver in bstack11l111ll_opy_:
                        if bstack111l111l1_opy_ == driver.session_id:
                            driver.execute_script(bstack1ll1lllll_opy_)
            except Exception as e:
                logger.debug(bstack11l1lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ⇼").format(str(e)))
    except Exception as e:
        logger.debug(bstack11l1lll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫ⇽").format(str(e)))
    bstack1lll1lllll_opy_(item, call, rep)
notset = Notset()
def bstack11l1l11l1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l11l11lll_opy_
    if str(name).lower() == bstack11l1lll_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨ⇾"):
        return bstack11l1lll_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣ⇿")
    else:
        return bstack1l11l11lll_opy_(self, name, default, skip)
def bstack1llll11ll_opy_(self):
    global CONFIG
    global bstack1l1lllll1l_opy_
    try:
        proxy = bstack111ll1lll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11l1lll_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ∀")):
                proxies = bstack11l111l1_opy_(proxy, bstack1ll1l11ll1_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll1lll11_opy_ = proxies.popitem()
                    if bstack11l1lll_opy_ (u"ࠦ࠿࠵࠯ࠣ∁") in bstack1ll1lll11_opy_:
                        return bstack1ll1lll11_opy_
                    else:
                        return bstack11l1lll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ∂") + bstack1ll1lll11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11l1lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥ∃").format(str(e)))
    return bstack1l1lllll1l_opy_(self)
def bstack1llll1l1_opy_():
    return (bstack11l1lll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ∄") in CONFIG or bstack11l1lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ∅") in CONFIG) and bstack1111llll_opy_() and bstack111111111_opy_() >= version.parse(
        bstack11l111l111_opy_)
def bstack11ll11111_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l1l1ll1l1_opy_
    global bstack1llll1ll1l_opy_
    global bstack1l11l1l11l_opy_
    CONFIG[bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ∆")] = str(bstack1l11l1l11l_opy_) + str(__version__)
    bstack1llll11l1_opy_ = 0
    try:
        if bstack1llll1ll1l_opy_ is True:
            bstack1llll11l1_opy_ = int(os.environ.get(bstack11l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ∇")))
    except:
        bstack1llll11l1_opy_ = 0
    CONFIG[bstack11l1lll_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ∈")] = True
    bstack11lll1l1ll_opy_ = bstack1l11l1ll_opy_(CONFIG, bstack1llll11l1_opy_)
    logger.debug(bstack1l111l1l11_opy_.format(str(bstack11lll1l1ll_opy_)))
    if CONFIG.get(bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ∉")):
        bstack111ll1l11_opy_(bstack11lll1l1ll_opy_, bstack11ll1l11l_opy_)
    if bstack11l1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ∊") in CONFIG and bstack11l1lll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ∋") in CONFIG[bstack11l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ∌")][bstack1llll11l1_opy_]:
        bstack1l1l1ll1l1_opy_ = CONFIG[bstack11l1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ∍")][bstack1llll11l1_opy_][bstack11l1lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ∎")]
    import urllib
    import json
    if bstack11l1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ∏") in CONFIG and str(CONFIG[bstack11l1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ∐")]).lower() != bstack11l1lll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ∑"):
        bstack1l11ll11l1_opy_ = bstack1ll1l111_opy_()
        bstack111ll11ll_opy_ = bstack1l11ll11l1_opy_ + urllib.parse.quote(json.dumps(bstack11lll1l1ll_opy_))
    else:
        bstack111ll11ll_opy_ = bstack11l1lll_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩ−") + urllib.parse.quote(json.dumps(bstack11lll1l1ll_opy_))
    browser = self.connect(bstack111ll11ll_opy_)
    return browser
def bstack11l1l11ll1_opy_():
    global bstack11l1ll1l1_opy_
    global bstack1l11l1l11l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1lllll11ll_opy_
        if not bstack1l1ll1l1ll1_opy_():
            global bstack1lll1l11_opy_
            if not bstack1lll1l11_opy_:
                from bstack_utils.helper import bstack1l1l11ll1_opy_, bstack11ll1l1l1l_opy_
                bstack1lll1l11_opy_ = bstack1l1l11ll1_opy_()
                bstack11ll1l1l1l_opy_(bstack1l11l1l11l_opy_)
            BrowserType.connect = bstack1lllll11ll_opy_
            return
        BrowserType.launch = bstack11ll11111_opy_
        bstack11l1ll1l1_opy_ = True
    except Exception as e:
        pass
def bstack11111l1111l_opy_():
    global CONFIG
    global bstack1l111111_opy_
    global bstack1ll1llll11_opy_
    global bstack11ll1l11l_opy_
    global bstack1llll1ll1l_opy_
    global bstack111llll11_opy_
    CONFIG = json.loads(os.environ.get(bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧ∓")))
    bstack1l111111_opy_ = eval(os.environ.get(bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ∔")))
    bstack1ll1llll11_opy_ = os.environ.get(bstack11l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪ∕"))
    bstack1l1ll11l11_opy_(CONFIG, bstack1l111111_opy_)
    bstack111llll11_opy_ = bstack1l11l1lll_opy_.bstack1lllll1l11_opy_(CONFIG, bstack111llll11_opy_)
    if cli.bstack1l1l11lll_opy_():
        bstack1lll111111_opy_.invoke(bstack11lll11lll_opy_.CONNECT, bstack1llll1l111_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ∖"), bstack11l1lll_opy_ (u"ࠬ࠶ࠧ∗")))
        cli.bstack1lllll111ll_opy_(cli_context.platform_index)
        cli.bstack1ll1llllll1_opy_(bstack1ll1l11ll1_opy_(bstack1ll1llll11_opy_, CONFIG), cli_context.platform_index, bstack1l1ll1ll1_opy_)
        cli.bstack1ll1llll111_opy_()
        logger.debug(bstack11l1lll_opy_ (u"ࠨࡃࡍࡋࠣ࡭ࡸࠦࡡࡤࡶ࡬ࡺࡪࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧ∘") + str(cli_context.platform_index) + bstack11l1lll_opy_ (u"ࠢࠣ∙"))
        return # skip all existing bstack1111111ll1l_opy_
    global bstack11l1l11l1l_opy_
    global bstack1lll11ll1_opy_
    global bstack1l1llll1l1_opy_
    global bstack1lll11ll1l_opy_
    global bstack11l11lllll_opy_
    global bstack11l1l11ll_opy_
    global bstack1111l1l1_opy_
    global bstack1llll1ll_opy_
    global bstack1l1lllll1l_opy_
    global bstack1l11l11lll_opy_
    global bstack1ll111111l_opy_
    global bstack1lll1lllll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack11l1l11l1l_opy_ = webdriver.Remote.__init__
        bstack1lll11ll1_opy_ = WebDriver.quit
        bstack1111l1l1_opy_ = WebDriver.close
        bstack1llll1ll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11l1lll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ√") in CONFIG or bstack11l1lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭∛") in CONFIG) and bstack1111llll_opy_():
        if bstack111111111_opy_() < version.parse(bstack11l111l111_opy_):
            logger.error(bstack11lllll1_opy_.format(bstack111111111_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1l1lllll1l_opy_ = RemoteConnection._11l1ll1l_opy_
            except Exception as e:
                logger.error(bstack1l1l1l111l_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l11l11lll_opy_ = Config.getoption
        from _pytest import runner
        bstack1ll111111l_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l11111111_opy_)
    try:
        from pytest_bdd import reporting
        bstack1lll1lllll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11l1lll_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫ∜"))
    bstack11ll1l11l_opy_ = CONFIG.get(bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ∝"), {}).get(bstack11l1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ∞"))
    bstack1llll1ll1l_opy_ = True
    bstack1llll1ll1_opy_(bstack1ll1lll1ll_opy_)
if (bstack11l1ll1111l_opy_()):
    bstack11111l1111l_opy_()
@bstack111l111111_opy_(class_method=False)
def bstack111111lll1l_opy_(hook_name, event, bstack1l11ll11l1l_opy_=None):
    if hook_name not in [bstack11l1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ∟"), bstack11l1lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ∠"), bstack11l1lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ∡"), bstack11l1lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ∢"), bstack11l1lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ∣"), bstack11l1lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬ∤"), bstack11l1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫ∥"), bstack11l1lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨ∦")]:
        return
    node = store[bstack11l1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ∧")]
    if hook_name in [bstack11l1lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ∨"), bstack11l1lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ∩")]:
        node = store[bstack11l1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩ∪")]
    elif hook_name in [bstack11l1lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩ∫"), bstack11l1lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭∬")]:
        node = store[bstack11l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫ∭")]
    hook_type = bstack111l111l1l1_opy_(hook_name)
    if event == bstack11l1lll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ∮"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_[hook_type], bstack1ll1lll1111_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l1llll1_opy_ = {
            bstack11l1lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭∯"): uuid,
            bstack11l1lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭∰"): bstack1lll11l11_opy_(),
            bstack11l1lll_opy_ (u"ࠪࡸࡾࡶࡥࠨ∱"): bstack11l1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ∲"),
            bstack11l1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ∳"): hook_type,
            bstack11l1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ∴"): hook_name
        }
        store[bstack11l1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ∵")].append(uuid)
        bstack111111ll111_opy_ = node.nodeid
        if hook_type == bstack11l1lll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭∶"):
            if not _1111llllll_opy_.get(bstack111111ll111_opy_, None):
                _1111llllll_opy_[bstack111111ll111_opy_] = {bstack11l1lll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ∷"): []}
            _1111llllll_opy_[bstack111111ll111_opy_][bstack11l1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ∸")].append(bstack111l1llll1_opy_[bstack11l1lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ∹")])
        _1111llllll_opy_[bstack111111ll111_opy_ + bstack11l1lll_opy_ (u"ࠬ࠳ࠧ∺") + hook_name] = bstack111l1llll1_opy_
        bstack11111l11l11_opy_(node, bstack111l1llll1_opy_, bstack11l1lll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ∻"))
    elif event == bstack11l1lll_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭∼"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11llll1_opy_[hook_type], bstack1ll1lll1111_opy_.POST, node, None, bstack1l11ll11l1l_opy_)
            return
        bstack11l11111l1_opy_ = node.nodeid + bstack11l1lll_opy_ (u"ࠨ࠯ࠪ∽") + hook_name
        _1111llllll_opy_[bstack11l11111l1_opy_][bstack11l1lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ∾")] = bstack1lll11l11_opy_()
        bstack111111l111l_opy_(_1111llllll_opy_[bstack11l11111l1_opy_][bstack11l1lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ∿")])
        bstack11111l11l11_opy_(node, _1111llllll_opy_[bstack11l11111l1_opy_], bstack11l1lll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭≀"), bstack11111l11lll_opy_=bstack1l11ll11l1l_opy_)
def bstack11111l11ll1_opy_():
    global bstack111111l1lll_opy_
    if bstack1ll11lll_opy_():
        bstack111111l1lll_opy_ = bstack11l1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩ≁")
    else:
        bstack111111l1lll_opy_ = bstack11l1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭≂")
@bstack1lll11111l_opy_.bstack11111llll1l_opy_
def bstack111111l11l1_opy_():
    bstack11111l11ll1_opy_()
    if cli.is_running():
        try:
            bstack11l111l1lll_opy_(bstack111111lll1l_opy_)
        except Exception as e:
            logger.debug(bstack11l1lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡷࠥࡶࡡࡵࡥ࡫࠾ࠥࢁࡽࠣ≃").format(e))
        return
    if bstack1111llll_opy_():
        bstack11ll1llll1_opy_ = Config.bstack1ll1l1l1l1_opy_()
        bstack11l1lll_opy_ (u"ࠨࠩࠪࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡉࡳࡷࠦࡰࡱࡲࠣࡁࠥ࠷ࠬࠡ࡯ࡲࡨࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡧࡦࡶࡶࠤࡺࡹࡥࡥࠢࡩࡳࡷࠦࡡ࠲࠳ࡼࠤࡨࡵ࡭࡮ࡣࡱࡨࡸ࠳ࡷࡳࡣࡳࡴ࡮ࡴࡧࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡴࡵࡶࠠ࠿ࠢ࠴࠰ࠥࡳ࡯ࡥࡡࡨࡼࡪࡩࡵࡵࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡥࡩࡨࡧࡵࡴࡧࠣ࡭ࡹࠦࡩࡴࠢࡳࡥࡹࡩࡨࡦࡦࠣ࡭ࡳࠦࡡࠡࡦ࡬ࡪ࡫࡫ࡲࡦࡰࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࠥ࡯ࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩࡷࡶࠤࡼ࡫ࠠ࡯ࡧࡨࡨࠥࡺ࡯ࠡࡷࡶࡩ࡙ࠥࡥ࡭ࡧࡱ࡭ࡺࡳࡐࡢࡶࡦ࡬࠭ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡩࡣࡱࡨࡱ࡫ࡲࠪࠢࡩࡳࡷࠦࡰࡱࡲࠣࡂࠥ࠷ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠩࠪࠫ≄")
        if bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭≅")):
            if CONFIG.get(bstack11l1lll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ≆")) is not None and int(CONFIG[bstack11l1lll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ≇")]) > 1:
                bstack1111l11l1_opy_(bstack11lll11l11_opy_)
            return
        bstack1111l11l1_opy_(bstack11lll11l11_opy_)
    try:
        bstack11l111l1lll_opy_(bstack111111lll1l_opy_)
    except Exception as e:
        logger.debug(bstack11l1lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡵࠣࡴࡦࡺࡣࡩ࠼ࠣࡿࢂࠨ≈").format(e))
bstack111111l11l1_opy_()