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
import collections
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11ll1l11111_opy_, bstack1llll1l1ll_opy_, bstack111lllll_opy_, bstack1ll1ll1111_opy_,
                                    bstack11ll11l1lll_opy_, bstack11ll11ll111_opy_, bstack11ll11ll1ll_opy_, bstack11ll111ll11_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1111l11l_opy_, bstack11llll11l_opy_
from bstack_utils.proxy import bstack1l1l11ll1l_opy_, bstack11lllllll_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1lll111lll_opy_
from browserstack_sdk._version import __version__
bstack111l111ll_opy_ = Config.bstack11l11lll1l_opy_()
logger = bstack1lll111lll_opy_.get_logger(__name__, bstack1lll111lll_opy_.bstack1lll1111111_opy_())
def bstack11ll1lllll1_opy_(config):
    return config[bstack111l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᨳ")]
def bstack11lll11l1l1_opy_(config):
    return config[bstack111l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᨴ")]
def bstack1ll1ll11ll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1llll111_opy_(obj):
    values = []
    bstack11l11l11l1l_opy_ = re.compile(bstack111l11_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢᨵ"), re.I)
    for key in obj.keys():
        if bstack11l11l11l1l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l1lll1l1l_opy_(config):
    tags = []
    tags.extend(bstack11l1llll111_opy_(os.environ))
    tags.extend(bstack11l1llll111_opy_(config))
    return tags
def bstack11l1ll1111l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l111lll1l_opy_(bstack11l1l1l1l1l_opy_):
    if not bstack11l1l1l1l1l_opy_:
        return bstack111l11_opy_ (u"ࠫࠬᨶ")
    return bstack111l11_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨᨷ").format(bstack11l1l1l1l1l_opy_.name, bstack11l1l1l1l1l_opy_.email)
def bstack11ll1llllll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1l1ll11l_opy_ = repo.common_dir
        info = {
            bstack111l11_opy_ (u"ࠨࡳࡩࡣࠥᨸ"): repo.head.commit.hexsha,
            bstack111l11_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣࠥᨹ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack111l11_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨࠣᨺ"): repo.active_branch.name,
            bstack111l11_opy_ (u"ࠤࡷࡥ࡬ࠨᨻ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack111l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨᨼ"): bstack11l111lll1l_opy_(repo.head.commit.committer),
            bstack111l11_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧᨽ"): repo.head.commit.committed_datetime.isoformat(),
            bstack111l11_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧᨾ"): bstack11l111lll1l_opy_(repo.head.commit.author),
            bstack111l11_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨࠦᨿ"): repo.head.commit.authored_datetime.isoformat(),
            bstack111l11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣᩀ"): repo.head.commit.message,
            bstack111l11_opy_ (u"ࠣࡴࡲࡳࡹࠨᩁ"): repo.git.rev_parse(bstack111l11_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ࠦᩂ")),
            bstack111l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦᩃ"): bstack11l1l1ll11l_opy_,
            bstack111l11_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᩄ"): subprocess.check_output([bstack111l11_opy_ (u"ࠧ࡭ࡩࡵࠤᩅ"), bstack111l11_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤᩆ"), bstack111l11_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴࠥᩇ")]).strip().decode(
                bstack111l11_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᩈ")),
            bstack111l11_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᩉ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack111l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫ࠧᩊ"): repo.git.rev_list(
                bstack111l11_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦᩋ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l1lllll11_opy_ = []
        for remote in remotes:
            bstack11l1l1l1lll_opy_ = {
                bstack111l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᩌ"): remote.name,
                bstack111l11_opy_ (u"ࠨࡵࡳ࡮ࠥᩍ"): remote.url,
            }
            bstack11l1lllll11_opy_.append(bstack11l1l1l1lll_opy_)
        bstack11l11ll11ll_opy_ = {
            bstack111l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩎ"): bstack111l11_opy_ (u"ࠣࡩ࡬ࡸࠧᩏ"),
            **info,
            bstack111l11_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥᩐ"): bstack11l1lllll11_opy_
        }
        bstack11l11ll11ll_opy_ = bstack11l11ll1ll1_opy_(bstack11l11ll11ll_opy_)
        return bstack11l11ll11ll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack111l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᩑ").format(err))
        return {}
def bstack11l11ll1ll1_opy_(bstack11l11ll11ll_opy_):
    bstack11l1lll1111_opy_ = bstack11l11llll11_opy_(bstack11l11ll11ll_opy_)
    if bstack11l1lll1111_opy_ and bstack11l1lll1111_opy_ > bstack11ll11l1lll_opy_:
        bstack11l11ll1111_opy_ = bstack11l1lll1111_opy_ - bstack11ll11l1lll_opy_
        bstack11l1l11lll1_opy_ = bstack11l11ll1lll_opy_(bstack11l11ll11ll_opy_[bstack111l11_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧᩒ")], bstack11l11ll1111_opy_)
        bstack11l11ll11ll_opy_[bstack111l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨᩓ")] = bstack11l1l11lll1_opy_
        logger.info(bstack111l11_opy_ (u"ࠨࡔࡩࡧࠣࡧࡴࡳ࡭ࡪࡶࠣ࡬ࡦࡹࠠࡣࡧࡨࡲࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤ࠯ࠢࡖ࡭ࡿ࡫ࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࠣࡥ࡫ࡺࡥࡳࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡾࢁࠥࡑࡂࠣᩔ")
                    .format(bstack11l11llll11_opy_(bstack11l11ll11ll_opy_) / 1024))
    return bstack11l11ll11ll_opy_
def bstack11l11llll11_opy_(bstack111l11111_opy_):
    try:
        if bstack111l11111_opy_:
            bstack11l11ll11l1_opy_ = json.dumps(bstack111l11111_opy_)
            bstack11l11lllll1_opy_ = sys.getsizeof(bstack11l11ll11l1_opy_)
            return bstack11l11lllll1_opy_
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠢࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡣࡢ࡮ࡦࡹࡱࡧࡴࡪࡰࡪࠤࡸ࡯ࡺࡦࠢࡲࡪࠥࡐࡓࡐࡐࠣࡳࡧࡰࡥࡤࡶ࠽ࠤࢀࢃࠢᩕ").format(e))
    return -1
def bstack11l11ll1lll_opy_(field, bstack11l11l111ll_opy_):
    try:
        bstack11l11l1llll_opy_ = len(bytes(bstack11ll11ll111_opy_, bstack111l11_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᩖ")))
        bstack11l1lll11ll_opy_ = bytes(field, bstack111l11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᩗ"))
        bstack11l1l1llll1_opy_ = len(bstack11l1lll11ll_opy_)
        bstack11l1l1lll1l_opy_ = ceil(bstack11l1l1llll1_opy_ - bstack11l11l111ll_opy_ - bstack11l11l1llll_opy_)
        if bstack11l1l1lll1l_opy_ > 0:
            bstack11l1l111lll_opy_ = bstack11l1lll11ll_opy_[:bstack11l1l1lll1l_opy_].decode(bstack111l11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᩘ"), errors=bstack111l11_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࠫᩙ")) + bstack11ll11ll111_opy_
            return bstack11l1l111lll_opy_
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡳ࡭ࠠࡧ࡫ࡨࡰࡩ࠲ࠠ࡯ࡱࡷ࡬࡮ࡴࡧࠡࡹࡤࡷࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤࠡࡪࡨࡶࡪࡀࠠࡼࡿࠥᩚ").format(e))
    return field
def bstack11l1ll11ll_opy_():
    env = os.environ
    if (bstack111l11_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦᩛ") in env and len(env[bstack111l11_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧᩜ")]) > 0) or (
            bstack111l11_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢᩝ") in env and len(env[bstack111l11_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣᩞ")]) > 0):
        return {
            bstack111l11_opy_ (u"ࠥࡲࡦࡳࡥࠣ᩟"): bstack111l11_opy_ (u"ࠦࡏ࡫࡮࡬࡫ࡱࡷ᩠ࠧ"),
            bstack111l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᩡ"): env.get(bstack111l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᩢ")),
            bstack111l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᩣ"): env.get(bstack111l11_opy_ (u"ࠣࡌࡒࡆࡤࡔࡁࡎࡇࠥᩤ")),
            bstack111l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᩥ"): env.get(bstack111l11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᩦ"))
        }
    if env.get(bstack111l11_opy_ (u"ࠦࡈࡏࠢᩧ")) == bstack111l11_opy_ (u"ࠧࡺࡲࡶࡧࠥᩨ") and bstack1l1llll1_opy_(env.get(bstack111l11_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡉࡉࠣᩩ"))):
        return {
            bstack111l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩪ"): bstack111l11_opy_ (u"ࠣࡅ࡬ࡶࡨࡲࡥࡄࡋࠥᩫ"),
            bstack111l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᩬ"): env.get(bstack111l11_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᩭ")),
            bstack111l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᩮ"): env.get(bstack111l11_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡐࡏࡃࠤᩯ")),
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᩰ"): env.get(bstack111l11_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠥᩱ"))
        }
    if env.get(bstack111l11_opy_ (u"ࠣࡅࡌࠦᩲ")) == bstack111l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᩳ") and bstack1l1llll1_opy_(env.get(bstack111l11_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࠥᩴ"))):
        return {
            bstack111l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᩵"): bstack111l11_opy_ (u"࡚ࠧࡲࡢࡸ࡬ࡷࠥࡉࡉࠣ᩶"),
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᩷"): env.get(bstack111l11_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡗࡆࡄࡢ࡙ࡗࡒࠢ᩸")),
            bstack111l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᩹"): env.get(bstack111l11_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᩺")),
            bstack111l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᩻"): env.get(bstack111l11_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᩼"))
        }
    if env.get(bstack111l11_opy_ (u"ࠧࡉࡉࠣ᩽")) == bstack111l11_opy_ (u"ࠨࡴࡳࡷࡨࠦ᩾") and env.get(bstack111l11_opy_ (u"ࠢࡄࡋࡢࡒࡆࡓࡅ᩿ࠣ")) == bstack111l11_opy_ (u"ࠣࡥࡲࡨࡪࡹࡨࡪࡲࠥ᪀"):
        return {
            bstack111l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᪁"): bstack111l11_opy_ (u"ࠥࡇࡴࡪࡥࡴࡪ࡬ࡴࠧ᪂"),
            bstack111l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᪃"): None,
            bstack111l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᪄"): None,
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᪅"): None
        }
    if env.get(bstack111l11_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠥ᪆")) and env.get(bstack111l11_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠦ᪇")):
        return {
            bstack111l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᪈"): bstack111l11_opy_ (u"ࠥࡆ࡮ࡺࡢࡶࡥ࡮ࡩࡹࠨ᪉"),
            bstack111l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᪊"): env.get(bstack111l11_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡉࡌࡘࡤࡎࡔࡕࡒࡢࡓࡗࡏࡇࡊࡐࠥ᪋")),
            bstack111l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᪌"): None,
            bstack111l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪍"): env.get(bstack111l11_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᪎"))
        }
    if env.get(bstack111l11_opy_ (u"ࠤࡆࡍࠧ᪏")) == bstack111l11_opy_ (u"ࠥࡸࡷࡻࡥࠣ᪐") and bstack1l1llll1_opy_(env.get(bstack111l11_opy_ (u"ࠦࡉࡘࡏࡏࡇࠥ᪑"))):
        return {
            bstack111l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᪒"): bstack111l11_opy_ (u"ࠨࡄࡳࡱࡱࡩࠧ᪓"),
            bstack111l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᪔"): env.get(bstack111l11_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡌࡊࡐࡎࠦ᪕")),
            bstack111l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᪖"): None,
            bstack111l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᪗"): env.get(bstack111l11_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᪘"))
        }
    if env.get(bstack111l11_opy_ (u"ࠧࡉࡉࠣ᪙")) == bstack111l11_opy_ (u"ࠨࡴࡳࡷࡨࠦ᪚") and bstack1l1llll1_opy_(env.get(bstack111l11_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࠥ᪛"))):
        return {
            bstack111l11_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪜"): bstack111l11_opy_ (u"ࠤࡖࡩࡲࡧࡰࡩࡱࡵࡩࠧ᪝"),
            bstack111l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᪞"): env.get(bstack111l11_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡐࡔࡊࡅࡓࡏ࡚ࡂࡖࡌࡓࡓࡥࡕࡓࡎࠥ᪟")),
            bstack111l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᪠"): env.get(bstack111l11_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᪡")),
            bstack111l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪢"): env.get(bstack111l11_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠦ᪣"))
        }
    if env.get(bstack111l11_opy_ (u"ࠤࡆࡍࠧ᪤")) == bstack111l11_opy_ (u"ࠥࡸࡷࡻࡥࠣ᪥") and bstack1l1llll1_opy_(env.get(bstack111l11_opy_ (u"ࠦࡌࡏࡔࡍࡃࡅࡣࡈࡏࠢ᪦"))):
        return {
            bstack111l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᪧ"): bstack111l11_opy_ (u"ࠨࡇࡪࡶࡏࡥࡧࠨ᪨"),
            bstack111l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᪩"): env.get(bstack111l11_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡗࡕࡐࠧ᪪")),
            bstack111l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᪫"): env.get(bstack111l11_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ᪬")),
            bstack111l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᪭"): env.get(bstack111l11_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡏࡄࠣ᪮"))
        }
    if env.get(bstack111l11_opy_ (u"ࠨࡃࡊࠤ᪯")) == bstack111l11_opy_ (u"ࠢࡵࡴࡸࡩࠧ᪰") and bstack1l1llll1_opy_(env.get(bstack111l11_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࠦ᪱"))):
        return {
            bstack111l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᪲"): bstack111l11_opy_ (u"ࠥࡆࡺ࡯࡬ࡥ࡭࡬ࡸࡪࠨ᪳"),
            bstack111l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᪴"): env.get(bstack111l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏ᪵ࠦ")),
            bstack111l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥ᪶ࠣ"): env.get(bstack111l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡐࡆࡈࡅࡍࠤ᪷")) or env.get(bstack111l11_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈ᪸ࠦ")),
            bstack111l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲ᪹ࠣ"): env.get(bstack111l11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖ᪺ࠧ"))
        }
    if bstack1l1llll1_opy_(env.get(bstack111l11_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨ᪻"))):
        return {
            bstack111l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᪼"): bstack111l11_opy_ (u"ࠨࡖࡪࡵࡸࡥࡱࠦࡓࡵࡷࡧ࡭ࡴࠦࡔࡦࡣࡰࠤࡘ࡫ࡲࡷ࡫ࡦࡩࡸࠨ᪽"),
            bstack111l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᪾"): bstack111l11_opy_ (u"ࠣࡽࢀࡿࢂࠨᪿ").format(env.get(bstack111l11_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍᫀࠬ")), env.get(bstack111l11_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࡊࡆࠪ᫁"))),
            bstack111l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᫂"): env.get(bstack111l11_opy_ (u"࡙࡙ࠧࡔࡖࡈࡑࡤࡊࡅࡇࡋࡑࡍ࡙ࡏࡏࡏࡋࡇ᫃ࠦ")),
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶ᫄ࠧ"): env.get(bstack111l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢ᫅"))
        }
    if bstack1l1llll1_opy_(env.get(bstack111l11_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࠥ᫆"))):
        return {
            bstack111l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᫇"): bstack111l11_opy_ (u"ࠥࡅࡵࡶࡶࡦࡻࡲࡶࠧ᫈"),
            bstack111l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᫉"): bstack111l11_opy_ (u"ࠧࢁࡽ࠰ࡲࡵࡳ࡯࡫ࡣࡵ࠱ࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ᫊ࠦ").format(env.get(bstack111l11_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡗࡕࡐࠬ᫋")), env.get(bstack111l11_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡄࡇࡈࡕࡕࡏࡖࡢࡒࡆࡓࡅࠨᫌ")), env.get(bstack111l11_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡔࡗࡕࡊࡆࡅࡗࡣࡘࡒࡕࡈࠩᫍ")), env.get(bstack111l11_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ᫎ"))),
            bstack111l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᫏"): env.get(bstack111l11_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ᫐")),
            bstack111l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᫑"): env.get(bstack111l11_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᫒"))
        }
    if env.get(bstack111l11_opy_ (u"ࠢࡂ࡜ࡘࡖࡊࡥࡈࡕࡖࡓࡣ࡚࡙ࡅࡓࡡࡄࡋࡊࡔࡔࠣ᫓")) and env.get(bstack111l11_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥ᫔")):
        return {
            bstack111l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᫕"): bstack111l11_opy_ (u"ࠥࡅࡿࡻࡲࡦࠢࡆࡍࠧ᫖"),
            bstack111l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᫗"): bstack111l11_opy_ (u"ࠧࢁࡽࡼࡿ࠲ࡣࡧࡻࡩ࡭ࡦ࠲ࡶࡪࡹࡵ࡭ࡶࡶࡃࡧࡻࡩ࡭ࡦࡌࡨࡂࢁࡽࠣ᫘").format(env.get(bstack111l11_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩ᫙")), env.get(bstack111l11_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࠬ᫚")), env.get(bstack111l11_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨ᫛"))),
            bstack111l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᫜"): env.get(bstack111l11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥ᫝")),
            bstack111l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᫞"): env.get(bstack111l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧ᫟"))
        }
    if any([env.get(bstack111l11_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ᫠")), env.get(bstack111l11_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ᫡")), env.get(bstack111l11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧ᫢"))]):
        return {
            bstack111l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᫣"): bstack111l11_opy_ (u"ࠥࡅ࡜࡙ࠠࡄࡱࡧࡩࡇࡻࡩ࡭ࡦࠥ᫤"),
            bstack111l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᫥"): env.get(bstack111l11_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡒࡘࡆࡑࡏࡃࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᫦")),
            bstack111l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᫧"): env.get(bstack111l11_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᫨")),
            bstack111l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᫩"): env.get(bstack111l11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ᫪"))
        }
    if env.get(bstack111l11_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣ᫫")):
        return {
            bstack111l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᫬"): bstack111l11_opy_ (u"ࠧࡈࡡ࡮ࡤࡲࡳࠧ᫭"),
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᫮"): env.get(bstack111l11_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡘࡥࡴࡷ࡯ࡸࡸ࡛ࡲ࡭ࠤ᫯")),
            bstack111l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᫰"): env.get(bstack111l11_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡶ࡬ࡴࡸࡴࡋࡱࡥࡒࡦࡳࡥࠣ᫱")),
            bstack111l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᫲"): env.get(bstack111l11_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤ᫳"))
        }
    if env.get(bstack111l11_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࠨ᫴")) or env.get(bstack111l11_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣ᫵")):
        return {
            bstack111l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᫶"): bstack111l11_opy_ (u"࡙ࠣࡨࡶࡨࡱࡥࡳࠤ᫷"),
            bstack111l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᫸"): env.get(bstack111l11_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ᫹")),
            bstack111l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᫺"): bstack111l11_opy_ (u"ࠧࡓࡡࡪࡰࠣࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠧ᫻") if env.get(bstack111l11_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣ᫼")) else None,
            bstack111l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᫽"): env.get(bstack111l11_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡊࡍ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨ᫾"))
        }
    if any([env.get(bstack111l11_opy_ (u"ࠤࡊࡇࡕࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ᫿")), env.get(bstack111l11_opy_ (u"ࠥࡋࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦᬀ")), env.get(bstack111l11_opy_ (u"ࠦࡌࡕࡏࡈࡎࡈࡣࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦᬁ"))]):
        return {
            bstack111l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᬂ"): bstack111l11_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡃ࡭ࡱࡸࡨࠧᬃ"),
            bstack111l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᬄ"): None,
            bstack111l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᬅ"): env.get(bstack111l11_opy_ (u"ࠤࡓࡖࡔࡐࡅࡄࡖࡢࡍࡉࠨᬆ")),
            bstack111l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᬇ"): env.get(bstack111l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᬈ"))
        }
    if env.get(bstack111l11_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࠣᬉ")):
        return {
            bstack111l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᬊ"): bstack111l11_opy_ (u"ࠢࡔࡪ࡬ࡴࡵࡧࡢ࡭ࡧࠥᬋ"),
            bstack111l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᬌ"): env.get(bstack111l11_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᬍ")),
            bstack111l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᬎ"): bstack111l11_opy_ (u"ࠦࡏࡵࡢࠡࠥࡾࢁࠧᬏ").format(env.get(bstack111l11_opy_ (u"࡙ࠬࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠨᬐ"))) if env.get(bstack111l11_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠤᬑ")) else None,
            bstack111l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᬒ"): env.get(bstack111l11_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᬓ"))
        }
    if bstack1l1llll1_opy_(env.get(bstack111l11_opy_ (u"ࠤࡑࡉ࡙ࡒࡉࡇ࡛ࠥᬔ"))):
        return {
            bstack111l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᬕ"): bstack111l11_opy_ (u"ࠦࡓ࡫ࡴ࡭࡫ࡩࡽࠧᬖ"),
            bstack111l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᬗ"): env.get(bstack111l11_opy_ (u"ࠨࡄࡆࡒࡏࡓ࡞ࡥࡕࡓࡎࠥᬘ")),
            bstack111l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᬙ"): env.get(bstack111l11_opy_ (u"ࠣࡕࡌࡘࡊࡥࡎࡂࡏࡈࠦᬚ")),
            bstack111l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᬛ"): env.get(bstack111l11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᬜ"))
        }
    if bstack1l1llll1_opy_(env.get(bstack111l11_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡆࡉࡔࡊࡑࡑࡗࠧᬝ"))):
        return {
            bstack111l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᬞ"): bstack111l11_opy_ (u"ࠨࡇࡪࡶࡋࡹࡧࠦࡁࡤࡶ࡬ࡳࡳࡹࠢᬟ"),
            bstack111l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᬠ"): bstack111l11_opy_ (u"ࠣࡽࢀ࠳ࢀࢃ࠯ࡢࡥࡷ࡭ࡴࡴࡳ࠰ࡴࡸࡲࡸ࠵ࡻࡾࠤᬡ").format(env.get(bstack111l11_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡖࡉࡗ࡜ࡅࡓࡡࡘࡖࡑ࠭ᬢ")), env.get(bstack111l11_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖࡊࡖࡏࡔࡋࡗࡓࡗ࡟ࠧᬣ")), env.get(bstack111l11_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠫᬤ"))),
            bstack111l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᬥ"): env.get(bstack111l11_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡗࡐࡔࡎࡊࡑࡕࡗࠣᬦ")),
            bstack111l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᬧ"): env.get(bstack111l11_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠣᬨ"))
        }
    if env.get(bstack111l11_opy_ (u"ࠤࡆࡍࠧᬩ")) == bstack111l11_opy_ (u"ࠥࡸࡷࡻࡥࠣᬪ") and env.get(bstack111l11_opy_ (u"࡛ࠦࡋࡒࡄࡇࡏࠦᬫ")) == bstack111l11_opy_ (u"ࠧ࠷ࠢᬬ"):
        return {
            bstack111l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᬭ"): bstack111l11_opy_ (u"ࠢࡗࡧࡵࡧࡪࡲࠢᬮ"),
            bstack111l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᬯ"): bstack111l11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡾࢁࠧᬰ").format(env.get(bstack111l11_opy_ (u"࡚ࠪࡊࡘࡃࡆࡎࡢ࡙ࡗࡒࠧᬱ"))),
            bstack111l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᬲ"): None,
            bstack111l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᬳ"): None,
        }
    if env.get(bstack111l11_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠤ᬴")):
        return {
            bstack111l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᬵ"): bstack111l11_opy_ (u"ࠣࡖࡨࡥࡲࡩࡩࡵࡻࠥᬶ"),
            bstack111l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᬷ"): None,
            bstack111l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᬸ"): env.get(bstack111l11_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠧᬹ")),
            bstack111l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᬺ"): env.get(bstack111l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᬻ"))
        }
    if any([env.get(bstack111l11_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࠥᬼ")), env.get(bstack111l11_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚ࡘࡌࠣᬽ")), env.get(bstack111l11_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠢᬾ")), env.get(bstack111l11_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡔࡆࡃࡐࠦᬿ"))]):
        return {
            bstack111l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᭀ"): bstack111l11_opy_ (u"ࠧࡉ࡯࡯ࡥࡲࡹࡷࡹࡥࠣᭁ"),
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᭂ"): None,
            bstack111l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᭃ"): env.get(bstack111l11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᭄")) or None,
            bstack111l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᭅ"): env.get(bstack111l11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᭆ"), 0)
        }
    if env.get(bstack111l11_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᭇ")):
        return {
            bstack111l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᭈ"): bstack111l11_opy_ (u"ࠨࡇࡰࡅࡇࠦᭉ"),
            bstack111l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᭊ"): None,
            bstack111l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᭋ"): env.get(bstack111l11_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᭌ")),
            bstack111l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᭍"): env.get(bstack111l11_opy_ (u"ࠦࡌࡕ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡆࡓ࡚ࡔࡔࡆࡔࠥ᭎"))
        }
    if env.get(bstack111l11_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ᭏")):
        return {
            bstack111l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᭐"): bstack111l11_opy_ (u"ࠢࡄࡱࡧࡩࡋࡸࡥࡴࡪࠥ᭑"),
            bstack111l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᭒"): env.get(bstack111l11_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ᭓")),
            bstack111l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᭔"): env.get(bstack111l11_opy_ (u"ࠦࡈࡌ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢ᭕")),
            bstack111l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᭖"): env.get(bstack111l11_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ᭗"))
        }
    return {bstack111l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᭘"): None}
def get_host_info():
    return {
        bstack111l11_opy_ (u"ࠣࡪࡲࡷࡹࡴࡡ࡮ࡧࠥ᭙"): platform.node(),
        bstack111l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ᭚"): platform.system(),
        bstack111l11_opy_ (u"ࠥࡸࡾࡶࡥࠣ᭛"): platform.machine(),
        bstack111l11_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧ᭜"): platform.version(),
        bstack111l11_opy_ (u"ࠧࡧࡲࡤࡪࠥ᭝"): platform.architecture()[0]
    }
def bstack11l11ll11_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1lll1lll_opy_():
    if bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ᭞")):
        return bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭᭟")
    return bstack111l11_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠧ᭠")
def bstack11l11l1l1ll_opy_(driver):
    info = {
        bstack111l11_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᭡"): driver.capabilities,
        bstack111l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧ᭢"): driver.session_id,
        bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ᭣"): driver.capabilities.get(bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ᭤"), None),
        bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᭥"): driver.capabilities.get(bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᭦"), None),
        bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᭧"): driver.capabilities.get(bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨ᭨"), None),
        bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᭩"):driver.capabilities.get(bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᭪"), None),
    }
    if bstack11l1lll1lll_opy_() == bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ᭫"):
        if bstack11lllll1l_opy_():
            info[bstack111l11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ᭬ࠧ")] = bstack111l11_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᭭")
        elif driver.capabilities.get(bstack111l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᭮"), {}).get(bstack111l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭᭯"), False):
            info[bstack111l11_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ᭰")] = bstack111l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ᭱")
        else:
            info[bstack111l11_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭᭲")] = bstack111l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ᭳")
    return info
def bstack11lllll1l_opy_():
    if bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᭴")):
        return True
    if bstack1l1llll1_opy_(os.environ.get(bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ᭵"), None)):
        return True
    return False
def bstack11l1111l_opy_(bstack11l1l1ll1ll_opy_, url, data, config):
    headers = config.get(bstack111l11_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ᭶"), None)
    proxies = bstack1l1l11ll1l_opy_(config, url)
    auth = config.get(bstack111l11_opy_ (u"ࠪࡥࡺࡺࡨࠨ᭷"), None)
    response = requests.request(
            bstack11l1l1ll1ll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11ll1ll111_opy_(bstack1lllll1l11_opy_, size):
    bstack11ll11ll1l_opy_ = []
    while len(bstack1lllll1l11_opy_) > size:
        bstack1ll1l1ll1_opy_ = bstack1lllll1l11_opy_[:size]
        bstack11ll11ll1l_opy_.append(bstack1ll1l1ll1_opy_)
        bstack1lllll1l11_opy_ = bstack1lllll1l11_opy_[size:]
    bstack11ll11ll1l_opy_.append(bstack1lllll1l11_opy_)
    return bstack11ll11ll1l_opy_
def bstack11l11l1l111_opy_(message, bstack11l1l11ll11_opy_=False):
    os.write(1, bytes(message, bstack111l11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᭸")))
    os.write(1, bytes(bstack111l11_opy_ (u"ࠬࡢ࡮ࠨ᭹"), bstack111l11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᭺")))
    if bstack11l1l11ll11_opy_:
        with open(bstack111l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭ࡰ࠳࠴ࡽ࠲࠭᭻") + os.environ[bstack111l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧ᭼")] + bstack111l11_opy_ (u"ࠩ࠱ࡰࡴ࡭ࠧ᭽"), bstack111l11_opy_ (u"ࠪࡥࠬ᭾")) as f:
            f.write(message + bstack111l11_opy_ (u"ࠫࡡࡴࠧ᭿"))
def bstack1ll1111llll_opy_():
    return os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨᮀ")].lower() == bstack111l11_opy_ (u"࠭ࡴࡳࡷࡨࠫᮁ")
def bstack1l1lll1ll_opy_(bstack11l1ll11l11_opy_):
    return bstack111l11_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ᮂ").format(bstack11ll1l11111_opy_, bstack11l1ll11l11_opy_)
def bstack11l11ll11l_opy_():
    return bstack111l1l1111_opy_().replace(tzinfo=None).isoformat() + bstack111l11_opy_ (u"ࠨ࡜ࠪᮃ")
def bstack11l11l1ll1l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack111l11_opy_ (u"ࠩ࡝ࠫᮄ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack111l11_opy_ (u"ࠪ࡞ࠬᮅ")))).total_seconds() * 1000
def bstack11l1ll1l111_opy_(timestamp):
    return bstack11l1l1l1111_opy_(timestamp).isoformat() + bstack111l11_opy_ (u"ࠫ࡟࠭ᮆ")
def bstack11l1l111l1l_opy_(bstack11l1l11l1ll_opy_):
    date_format = bstack111l11_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪᮇ")
    bstack11l11ll1l11_opy_ = datetime.datetime.strptime(bstack11l1l11l1ll_opy_, date_format)
    return bstack11l11ll1l11_opy_.isoformat() + bstack111l11_opy_ (u"࡚࠭ࠨᮈ")
def bstack11l1lll111l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack111l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᮉ")
    else:
        return bstack111l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᮊ")
def bstack1l1llll1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack111l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᮋ")
def bstack11l1ll11ll1_opy_(val):
    return val.__str__().lower() == bstack111l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᮌ")
def bstack111l11111l_opy_(bstack11l1l1l111l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1l1l111l_opy_ as e:
                print(bstack111l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᮍ").format(func.__name__, bstack11l1l1l111l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1l11l111_opy_(bstack11l11ll111l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l11ll111l_opy_(cls, *args, **kwargs)
            except bstack11l1l1l111l_opy_ as e:
                print(bstack111l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧᮎ").format(bstack11l11ll111l_opy_.__name__, bstack11l1l1l111l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1l11l111_opy_
    else:
        return decorator
def bstack1l11111l1_opy_(bstack1111l1l11l_opy_):
    if os.getenv(bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᮏ")) is not None:
        return bstack1l1llll1_opy_(os.getenv(bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᮐ")))
    if bstack111l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᮑ") in bstack1111l1l11l_opy_ and bstack11l1ll11ll1_opy_(bstack1111l1l11l_opy_[bstack111l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᮒ")]):
        return False
    if bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᮓ") in bstack1111l1l11l_opy_ and bstack11l1ll11ll1_opy_(bstack1111l1l11l_opy_[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᮔ")]):
        return False
    return True
def bstack11l11l11_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l1ll11111_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧᮕ"), None)
        return bstack11l1ll11111_opy_ is None or bstack11l1ll11111_opy_ == bstack111l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᮖ")
    except Exception as e:
        return False
def bstack1l1ll11l11_opy_(hub_url, CONFIG):
    if bstack11l1lll1l_opy_() <= version.parse(bstack111l11_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᮗ")):
        if hub_url:
            return bstack111l11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᮘ") + hub_url + bstack111l11_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨᮙ")
        return bstack111lllll_opy_
    if hub_url:
        return bstack111l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᮚ") + hub_url + bstack111l11_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧᮛ")
    return bstack1ll1ll1111_opy_
def bstack11l1llll1l1_opy_():
    return isinstance(os.getenv(bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫᮜ")), str)
def bstack1l1111ll1_opy_(url):
    return urlparse(url).hostname
def bstack11ll11ll1_opy_(hostname):
    for bstack11ll111ll_opy_ in bstack1llll1l1ll_opy_:
        regex = re.compile(bstack11ll111ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1l11l11l_opy_(bstack11l1ll111l1_opy_, file_name, logger):
    bstack1l1l111l1_opy_ = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"࠭ࡾࠨᮝ")), bstack11l1ll111l1_opy_)
    try:
        if not os.path.exists(bstack1l1l111l1_opy_):
            os.makedirs(bstack1l1l111l1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠧࡿࠩᮞ")), bstack11l1ll111l1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack111l11_opy_ (u"ࠨࡹࠪᮟ")):
                pass
            with open(file_path, bstack111l11_opy_ (u"ࠤࡺ࠯ࠧᮠ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1111l11l_opy_.format(str(e)))
def bstack11l111lll11_opy_(file_name, key, value, logger):
    file_path = bstack11l1l11l11l_opy_(bstack111l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᮡ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1lll1ll1_opy_ = json.load(open(file_path, bstack111l11_opy_ (u"ࠫࡷࡨࠧᮢ")))
        else:
            bstack1lll1ll1_opy_ = {}
        bstack1lll1ll1_opy_[key] = value
        with open(file_path, bstack111l11_opy_ (u"ࠧࡽࠫࠣᮣ")) as outfile:
            json.dump(bstack1lll1ll1_opy_, outfile)
def bstack1llllll1l_opy_(file_name, logger):
    file_path = bstack11l1l11l11l_opy_(bstack111l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᮤ"), file_name, logger)
    bstack1lll1ll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack111l11_opy_ (u"ࠧࡳࠩᮥ")) as bstack11l11lll_opy_:
            bstack1lll1ll1_opy_ = json.load(bstack11l11lll_opy_)
    return bstack1lll1ll1_opy_
def bstack1lll11l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬᮦ") + file_path + bstack111l11_opy_ (u"ࠩࠣࠫᮧ") + str(e))
def bstack11l1lll1l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack111l11_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧᮨ")
def bstack1l1l1llll1_opy_(config):
    if bstack111l11_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᮩ") in config:
        del (config[bstack111l11_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ᮪ࠫ")])
        return False
    if bstack11l1lll1l_opy_() < version.parse(bstack111l11_opy_ (u"࠭࠳࠯࠶࠱࠴᮫ࠬ")):
        return False
    if bstack11l1lll1l_opy_() >= version.parse(bstack111l11_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭ᮬ")):
        return True
    if bstack111l11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᮭ") in config and config[bstack111l11_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᮮ")] is False:
        return False
    else:
        return True
def bstack1l1l1ll1l_opy_(args_list, bstack11l1l11111l_opy_):
    index = -1
    for value in bstack11l1l11111l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11lll1l1l1l_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11lll1l1l1l_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111llll1ll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111llll1ll_opy_ = bstack111llll1ll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack111l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᮯ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack111l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᮰"), exception=exception)
    def bstack1111l11ll1_opy_(self):
        if self.result != bstack111l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᮱"):
            return None
        if isinstance(self.exception_type, str) and bstack111l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤ᮲") in self.exception_type:
            return bstack111l11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣ᮳")
        return bstack111l11_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤ᮴")
    def bstack11l11llll1l_opy_(self):
        if self.result != bstack111l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᮵"):
            return None
        if self.bstack111llll1ll_opy_:
            return self.bstack111llll1ll_opy_
        return bstack11l111llll1_opy_(self.exception)
def bstack11l111llll1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l111ll1l1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l1lllll1l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11llll1l1_opy_(config, logger):
    try:
        import playwright
        bstack11l1l1ll111_opy_ = playwright.__file__
        bstack11l1ll1l11l_opy_ = os.path.split(bstack11l1l1ll111_opy_)
        bstack11l11llllll_opy_ = bstack11l1ll1l11l_opy_[0] + bstack111l11_opy_ (u"ࠪ࠳ࡩࡸࡩࡷࡧࡵ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠴ࡲࡩࡣ࠱ࡦࡰ࡮࠵ࡣ࡭࡫࠱࡮ࡸ࠭᮶")
        os.environ[bstack111l11_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠧ᮷")] = bstack11lllllll_opy_(config)
        with open(bstack11l11llllll_opy_, bstack111l11_opy_ (u"ࠬࡸࠧ᮸")) as f:
            bstack1ll1ll1l11_opy_ = f.read()
            bstack11l1l111111_opy_ = bstack111l11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ᮹")
            bstack11l11lll1l1_opy_ = bstack1ll1ll1l11_opy_.find(bstack11l1l111111_opy_)
            if bstack11l11lll1l1_opy_ == -1:
              process = subprocess.Popen(bstack111l11_opy_ (u"ࠢ࡯ࡲࡰࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠦᮺ"), shell=True, cwd=bstack11l1ll1l11l_opy_[0])
              process.wait()
              bstack11l1ll1l1l1_opy_ = bstack111l11_opy_ (u"ࠨࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࠨ࠻ࠨᮻ")
              bstack11l1l11llll_opy_ = bstack111l11_opy_ (u"ࠤࠥࠦࠥࡢࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࡠࠧࡁࠠࡤࡱࡱࡷࡹࠦࡻࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤࢂࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩࠬ࠿ࠥ࡯ࡦࠡࠪࡳࡶࡴࡩࡥࡴࡵ࠱ࡩࡳࡼ࠮ࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠬࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠨࠪ࠽ࠣࠦࠧࠨᮼ")
              bstack11l1ll111ll_opy_ = bstack1ll1ll1l11_opy_.replace(bstack11l1ll1l1l1_opy_, bstack11l1l11llll_opy_)
              with open(bstack11l11llllll_opy_, bstack111l11_opy_ (u"ࠪࡻࠬᮽ")) as f:
                f.write(bstack11l1ll111ll_opy_)
    except Exception as e:
        logger.error(bstack11llll11l_opy_.format(str(e)))
def bstack11ll1ll1l1_opy_():
  try:
    bstack11l1l1l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack111l11_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫᮾ"))
    bstack11l111lllll_opy_ = []
    if os.path.exists(bstack11l1l1l1l11_opy_):
      with open(bstack11l1l1l1l11_opy_) as f:
        bstack11l111lllll_opy_ = json.load(f)
      os.remove(bstack11l1l1l1l11_opy_)
    return bstack11l111lllll_opy_
  except:
    pass
  return []
def bstack1lll11l11l_opy_(bstack1l1lll11l1_opy_):
  try:
    bstack11l111lllll_opy_ = []
    bstack11l1l1l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack111l11_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬᮿ"))
    if os.path.exists(bstack11l1l1l1l11_opy_):
      with open(bstack11l1l1l1l11_opy_) as f:
        bstack11l111lllll_opy_ = json.load(f)
    bstack11l111lllll_opy_.append(bstack1l1lll11l1_opy_)
    with open(bstack11l1l1l1l11_opy_, bstack111l11_opy_ (u"࠭ࡷࠨᯀ")) as f:
        json.dump(bstack11l111lllll_opy_, f)
  except:
    pass
def bstack11111llll_opy_(logger, bstack11l1l1lllll_opy_ = False):
  try:
    test_name = os.environ.get(bstack111l11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᯁ"), bstack111l11_opy_ (u"ࠨࠩᯂ"))
    if test_name == bstack111l11_opy_ (u"ࠩࠪᯃ"):
        test_name = threading.current_thread().__dict__.get(bstack111l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡅࡨࡩࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩᯄ"), bstack111l11_opy_ (u"ࠫࠬᯅ"))
    bstack11l1lll1l11_opy_ = bstack111l11_opy_ (u"ࠬ࠲ࠠࠨᯆ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l1l1lllll_opy_:
        bstack1lll11lll1_opy_ = os.environ.get(bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᯇ"), bstack111l11_opy_ (u"ࠧ࠱ࠩᯈ"))
        bstack11lll1l1_opy_ = {bstack111l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᯉ"): test_name, bstack111l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᯊ"): bstack11l1lll1l11_opy_, bstack111l11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᯋ"): bstack1lll11lll1_opy_}
        bstack11l11l111l1_opy_ = []
        bstack11l1l111l11_opy_ = os.path.join(tempfile.gettempdir(), bstack111l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᯌ"))
        if os.path.exists(bstack11l1l111l11_opy_):
            with open(bstack11l1l111l11_opy_) as f:
                bstack11l11l111l1_opy_ = json.load(f)
        bstack11l11l111l1_opy_.append(bstack11lll1l1_opy_)
        with open(bstack11l1l111l11_opy_, bstack111l11_opy_ (u"ࠬࡽࠧᯍ")) as f:
            json.dump(bstack11l11l111l1_opy_, f)
    else:
        bstack11lll1l1_opy_ = {bstack111l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᯎ"): test_name, bstack111l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᯏ"): bstack11l1lll1l11_opy_, bstack111l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᯐ"): str(multiprocessing.current_process().name)}
        if bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭ᯑ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11lll1l1_opy_)
  except Exception as e:
      logger.warn(bstack111l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᯒ").format(e))
def bstack1ll111ll11_opy_(error_message, test_name, index, logger):
  try:
    bstack11l111ll1ll_opy_ = []
    bstack11lll1l1_opy_ = {bstack111l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᯓ"): test_name, bstack111l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᯔ"): error_message, bstack111l11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᯕ"): index}
    bstack11l1l1lll11_opy_ = os.path.join(tempfile.gettempdir(), bstack111l11_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᯖ"))
    if os.path.exists(bstack11l1l1lll11_opy_):
        with open(bstack11l1l1lll11_opy_) as f:
            bstack11l111ll1ll_opy_ = json.load(f)
    bstack11l111ll1ll_opy_.append(bstack11lll1l1_opy_)
    with open(bstack11l1l1lll11_opy_, bstack111l11_opy_ (u"ࠨࡹࠪᯗ")) as f:
        json.dump(bstack11l111ll1ll_opy_, f)
  except Exception as e:
    logger.warn(bstack111l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧᯘ").format(e))
def bstack11l1llllll_opy_(bstack11111l1l1_opy_, name, logger):
  try:
    bstack11lll1l1_opy_ = {bstack111l11_opy_ (u"ࠪࡲࡦࡳࡥࠨᯙ"): name, bstack111l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᯚ"): bstack11111l1l1_opy_, bstack111l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᯛ"): str(threading.current_thread()._name)}
    return bstack11lll1l1_opy_
  except Exception as e:
    logger.warn(bstack111l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡤࡨ࡬ࡦࡼࡥࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥᯜ").format(e))
  return
def bstack11l1l1l1ll1_opy_():
    return platform.system() == bstack111l11_opy_ (u"ࠧࡘ࡫ࡱࡨࡴࡽࡳࠨᯝ")
def bstack1lll1l1l_opy_(bstack11l1ll11lll_opy_, config, logger):
    bstack11l1ll1llll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l1ll11lll_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡬ࡵࡧࡵࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡰ࡫ࡹࡴࠢࡥࡽࠥࡸࡥࡨࡧࡻࠤࡲࡧࡴࡤࡪ࠽ࠤࢀࢃࠢᯞ").format(e))
    return bstack11l1ll1llll_opy_
def bstack11l11l1lll1_opy_(bstack11l1l111ll1_opy_, bstack11l1l1l11ll_opy_):
    bstack11l11l11111_opy_ = version.parse(bstack11l1l111ll1_opy_)
    bstack11l11ll1l1l_opy_ = version.parse(bstack11l1l1l11ll_opy_)
    if bstack11l11l11111_opy_ > bstack11l11ll1l1l_opy_:
        return 1
    elif bstack11l11l11111_opy_ < bstack11l11ll1l1l_opy_:
        return -1
    else:
        return 0
def bstack111l1l1111_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1l1l1111_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1ll11l1l_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l1ll1llll_opy_(options, framework, config, bstack1l1ll111l_opy_={}):
    if options is None:
        return
    if getattr(options, bstack111l11_opy_ (u"ࠩࡪࡩࡹ࠭ᯟ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1lll1lll11_opy_ = caps.get(bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᯠ"))
    bstack11l11l11l11_opy_ = True
    bstack1ll11l111l_opy_ = os.environ[bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᯡ")]
    bstack1ll1ll11111_opy_ = config.get(bstack111l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᯢ"), False)
    if bstack1ll1ll11111_opy_:
        bstack1llll11l111_opy_ = config.get(bstack111l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᯣ"), {})
        bstack1llll11l111_opy_[bstack111l11_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪᯤ")] = os.getenv(bstack111l11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᯥ"))
        bstack11lll11l111_opy_ = json.loads(os.getenv(bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎ᯦ࠪ"), bstack111l11_opy_ (u"ࠪࡿࢂ࠭ᯧ"))).get(bstack111l11_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᯨ"))
    if bstack11l1ll11ll1_opy_(caps.get(bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡘ࠵ࡆࠫᯩ"))) or bstack11l1ll11ll1_opy_(caps.get(bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡡࡺ࠷ࡨ࠭ᯪ"))):
        bstack11l11l11l11_opy_ = False
    if bstack1l1l1llll1_opy_({bstack111l11_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢᯫ"): bstack11l11l11l11_opy_}):
        bstack1lll1lll11_opy_ = bstack1lll1lll11_opy_ or {}
        bstack1lll1lll11_opy_[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᯬ")] = bstack11l1ll11l1l_opy_(framework)
        bstack1lll1lll11_opy_[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᯭ")] = bstack1ll1111llll_opy_()
        bstack1lll1lll11_opy_[bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᯮ")] = bstack1ll11l111l_opy_
        bstack1lll1lll11_opy_[bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᯯ")] = bstack1l1ll111l_opy_
        if bstack1ll1ll11111_opy_:
            bstack1lll1lll11_opy_[bstack111l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᯰ")] = bstack1ll1ll11111_opy_
            bstack1lll1lll11_opy_[bstack111l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᯱ")] = bstack1llll11l111_opy_
            bstack1lll1lll11_opy_[bstack111l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹ᯲ࠧ")][bstack111l11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯᯳ࠩ")] = bstack11lll11l111_opy_
        if getattr(options, bstack111l11_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪ᯴"), None):
            options.set_capability(bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᯵"), bstack1lll1lll11_opy_)
        else:
            options[bstack111l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᯶")] = bstack1lll1lll11_opy_
    else:
        if getattr(options, bstack111l11_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭᯷"), None):
            options.set_capability(bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᯸"), bstack11l1ll11l1l_opy_(framework))
            options.set_capability(bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᯹"), bstack1ll1111llll_opy_())
            options.set_capability(bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ᯺"), bstack1ll11l111l_opy_)
            options.set_capability(bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᯻"), bstack1l1ll111l_opy_)
            if bstack1ll1ll11111_opy_:
                options.set_capability(bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᯼"), bstack1ll1ll11111_opy_)
                options.set_capability(bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᯽"), bstack1llll11l111_opy_)
                options.set_capability(bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ࠲ࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᯾"), bstack11lll11l111_opy_)
        else:
            options[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᯿")] = bstack11l1ll11l1l_opy_(framework)
            options[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᰀ")] = bstack1ll1111llll_opy_()
            options[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᰁ")] = bstack1ll11l111l_opy_
            options[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᰂ")] = bstack1l1ll111l_opy_
            if bstack1ll1ll11111_opy_:
                options[bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᰃ")] = bstack1ll1ll11111_opy_
                options[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᰄ")] = bstack1llll11l111_opy_
                options[bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᰅ")][bstack111l11_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᰆ")] = bstack11lll11l111_opy_
    return options
def bstack11l1llllll1_opy_(bstack11l1l1111ll_opy_, framework):
    bstack1l1ll111l_opy_ = bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤᰇ"))
    if bstack11l1l1111ll_opy_ and len(bstack11l1l1111ll_opy_.split(bstack111l11_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᰈ"))) > 1:
        ws_url = bstack11l1l1111ll_opy_.split(bstack111l11_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᰉ"))[0]
        if bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᰊ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l11l11lll_opy_ = json.loads(urllib.parse.unquote(bstack11l1l1111ll_opy_.split(bstack111l11_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᰋ"))[1]))
            bstack11l11l11lll_opy_ = bstack11l11l11lll_opy_ or {}
            bstack1ll11l111l_opy_ = os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᰌ")]
            bstack11l11l11lll_opy_[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᰍ")] = str(framework) + str(__version__)
            bstack11l11l11lll_opy_[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᰎ")] = bstack1ll1111llll_opy_()
            bstack11l11l11lll_opy_[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᰏ")] = bstack1ll11l111l_opy_
            bstack11l11l11lll_opy_[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᰐ")] = bstack1l1ll111l_opy_
            bstack11l1l1111ll_opy_ = bstack11l1l1111ll_opy_.split(bstack111l11_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᰑ"))[0] + bstack111l11_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᰒ") + urllib.parse.quote(json.dumps(bstack11l11l11lll_opy_))
    return bstack11l1l1111ll_opy_
def bstack1l11l1lll1_opy_():
    global bstack11ll11l1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11ll11l1_opy_ = BrowserType.connect
    return bstack11ll11l1_opy_
def bstack1l1llllll_opy_(framework_name):
    global bstack11llllllll_opy_
    bstack11llllllll_opy_ = framework_name
    return framework_name
def bstack11ll11llll_opy_(self, *args, **kwargs):
    global bstack11ll11l1_opy_
    try:
        global bstack11llllllll_opy_
        if bstack111l11_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩᰓ") in kwargs:
            kwargs[bstack111l11_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪᰔ")] = bstack11l1llllll1_opy_(
                kwargs.get(bstack111l11_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᰕ"), None),
                bstack11llllllll_opy_
            )
    except Exception as e:
        logger.error(bstack111l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡖࡈࡐࠦࡣࡢࡲࡶ࠾ࠥࢁࡽࠣᰖ").format(str(e)))
    return bstack11ll11l1_opy_(self, *args, **kwargs)
def bstack11l1ll1l1ll_opy_(bstack11l1lll11l1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1l1l11ll1l_opy_(bstack11l1lll11l1_opy_, bstack111l11_opy_ (u"ࠤࠥᰗ"))
        if proxies and proxies.get(bstack111l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤᰘ")):
            parsed_url = urlparse(proxies.get(bstack111l11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥᰙ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack111l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨᰚ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack111l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩᰛ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack111l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᰜ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack111l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫᰝ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1111llll1_opy_(bstack11l1lll11l1_opy_):
    bstack11l1ll1lll1_opy_ = {
        bstack11ll111ll11_opy_[bstack11l11lll111_opy_]: bstack11l1lll11l1_opy_[bstack11l11lll111_opy_]
        for bstack11l11lll111_opy_ in bstack11l1lll11l1_opy_
        if bstack11l11lll111_opy_ in bstack11ll111ll11_opy_
    }
    bstack11l1ll1lll1_opy_[bstack111l11_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤᰞ")] = bstack11l1ll1l1ll_opy_(bstack11l1lll11l1_opy_, bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥᰟ")))
    bstack11l1lllll1l_opy_ = [element.lower() for element in bstack11ll11ll1ll_opy_]
    bstack11l1llll1ll_opy_(bstack11l1ll1lll1_opy_, bstack11l1lllll1l_opy_)
    return bstack11l1ll1lll1_opy_
def bstack11l1llll1ll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack111l11_opy_ (u"ࠦ࠯࠰ࠪࠫࠤᰠ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11l1llll1ll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11l1llll1ll_opy_(item, keys)
def bstack1l1lll11l1l_opy_():
    bstack11l11l1ll11_opy_ = [os.environ.get(bstack111l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡏࡌࡆࡕࡢࡈࡎࡘࠢᰡ")), os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠨࡾࠣᰢ")), bstack111l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᰣ")), os.path.join(bstack111l11_opy_ (u"ࠨ࠱ࡷࡱࡵ࠭ᰤ"), bstack111l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᰥ"))]
    for path in bstack11l11l1ll11_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack111l11_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥᰦ") + str(path) + bstack111l11_opy_ (u"ࠦࠬࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠢᰧ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack111l11_opy_ (u"ࠧࡍࡩࡷ࡫ࡱ࡫ࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠣࡪࡴࡸࠠࠨࠤᰨ") + str(path) + bstack111l11_opy_ (u"ࠨࠧࠣᰩ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack111l11_opy_ (u"ࠢࡇ࡫࡯ࡩࠥ࠭ࠢᰪ") + str(path) + bstack111l11_opy_ (u"ࠣࠩࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡭ࡧࡳࠡࡶ࡫ࡩࠥࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷ࠳ࠨᰫ"))
            else:
                logger.debug(bstack111l11_opy_ (u"ࠤࡆࡶࡪࡧࡴࡪࡰࡪࠤ࡫࡯࡬ࡦࠢࠪࠦᰬ") + str(path) + bstack111l11_opy_ (u"ࠥࠫࠥࡽࡩࡵࡪࠣࡻࡷ࡯ࡴࡦࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳ࠴ࠢᰭ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack111l11_opy_ (u"ࠦࡔࡶࡥࡳࡣࡷ࡭ࡴࡴࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦࠣࡪࡴࡸࠠࠨࠤᰮ") + str(path) + bstack111l11_opy_ (u"ࠧ࠭࠮ࠣᰯ"))
            return path
        except Exception as e:
            logger.debug(bstack111l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡵࡱࠢࡩ࡭ࡱ࡫ࠠࠨࡽࡳࡥࡹ࡮ࡽࠨ࠼ࠣࠦᰰ") + str(e) + bstack111l11_opy_ (u"ࠢࠣᰱ"))
    logger.debug(bstack111l11_opy_ (u"ࠣࡃ࡯ࡰࠥࡶࡡࡵࡪࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠧᰲ"))
    return None
@measure(event_name=EVENTS.bstack11ll1111l1l_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
def bstack1lll111l11l_opy_(binary_path, bstack1llll111111_opy_, bs_config):
    logger.debug(bstack111l11_opy_ (u"ࠤࡆࡹࡷࡸࡥ࡯ࡶࠣࡇࡑࡏࠠࡑࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧ࠾ࠥࢁࡽࠣᰳ").format(binary_path))
    bstack11l11lll1ll_opy_ = bstack111l11_opy_ (u"ࠪࠫᰴ")
    bstack11l1ll1ll1l_opy_ = {
        bstack111l11_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᰵ"): __version__,
        bstack111l11_opy_ (u"ࠧࡵࡳࠣᰶ"): platform.system(),
        bstack111l11_opy_ (u"ࠨ࡯ࡴࡡࡤࡶࡨ࡮᰷ࠢ"): platform.machine(),
        bstack111l11_opy_ (u"ࠢࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ᰸"): bstack111l11_opy_ (u"ࠨ࠲ࠪ᰹"),
        bstack111l11_opy_ (u"ࠤࡶࡨࡰࡥ࡬ࡢࡰࡪࡹࡦ࡭ࡥࠣ᰺"): bstack111l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ᰻")
    }
    bstack11l1l1111l1_opy_(bstack11l1ll1ll1l_opy_)
    try:
        if binary_path:
            bstack11l1ll1ll1l_opy_[bstack111l11_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᰼")] = subprocess.check_output([binary_path, bstack111l11_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨ᰽")]).strip().decode(bstack111l11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᰾"))
        response = requests.request(
            bstack111l11_opy_ (u"ࠧࡈࡇࡗࠫ᰿"),
            url=bstack1l1lll1ll_opy_(bstack11ll11l1111_opy_),
            headers=None,
            auth=(bs_config[bstack111l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ᱀")], bs_config[bstack111l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ᱁")]),
            json=None,
            params=bstack11l1ll1ll1l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack111l11_opy_ (u"ࠪࡹࡷࡲࠧ᱂") in data.keys() and bstack111l11_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡨࡤࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪ᱃") in data.keys():
            logger.debug(bstack111l11_opy_ (u"ࠧࡔࡥࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡢࡪࡰࡤࡶࡾ࠲ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡤ࡬ࡲࡦࡸࡹࠡࡸࡨࡶࡸ࡯࡯࡯࠼ࠣࡿࢂࠨ᱄").format(bstack11l1ll1ll1l_opy_[bstack111l11_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫ᱅")]))
            if bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠪ᱆") in os.environ:
                logger.debug(bstack111l11_opy_ (u"ࠣࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡦ࡮ࡴࡡࡳࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡧࡳࠡࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡔࡆࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠡ࡫ࡶࠤࡸ࡫ࡴࠣ᱇"))
                data[bstack111l11_opy_ (u"ࠩࡸࡶࡱ࠭᱈")] = os.environ[bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑ࠭᱉")]
            bstack11l11l1l11l_opy_ = bstack11l11l11ll1_opy_(data[bstack111l11_opy_ (u"ࠫࡺࡸ࡬ࠨ᱊")], bstack1llll111111_opy_)
            bstack11l11lll1ll_opy_ = os.path.join(bstack1llll111111_opy_, bstack11l11l1l11l_opy_)
            os.chmod(bstack11l11lll1ll_opy_, 0o777) # bstack11l1lll1ll1_opy_ permission
            return bstack11l11lll1ll_opy_
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡰࡨࡻ࡙ࠥࡄࡌࠢࡾࢁࠧ᱋").format(e))
    return binary_path
def bstack11l1l1111l1_opy_(bstack11l1ll1ll1l_opy_):
    try:
        if bstack111l11_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬ᱌") not in bstack11l1ll1ll1l_opy_[bstack111l11_opy_ (u"ࠧࡰࡵࠪᱍ")].lower():
            return
        if os.path.exists(bstack111l11_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵࡯ࡴ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥᱎ")):
            with open(bstack111l11_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡰࡵ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᱏ"), bstack111l11_opy_ (u"ࠥࡶࠧ᱐")) as f:
                bstack11l11lll11l_opy_ = {}
                for line in f:
                    if bstack111l11_opy_ (u"ࠦࡂࠨ᱑") in line:
                        key, value = line.rstrip().split(bstack111l11_opy_ (u"ࠧࡃࠢ᱒"), 1)
                        bstack11l11lll11l_opy_[key] = value.strip(bstack111l11_opy_ (u"࠭ࠢ࡝ࠩࠪ᱓"))
                bstack11l1ll1ll1l_opy_[bstack111l11_opy_ (u"ࠧࡥ࡫ࡶࡸࡷࡵࠧ᱔")] = bstack11l11lll11l_opy_.get(bstack111l11_opy_ (u"ࠣࡋࡇࠦ᱕"), bstack111l11_opy_ (u"ࠤࠥ᱖"))
        elif os.path.exists(bstack111l11_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡣ࡯ࡴ࡮ࡴࡥ࠮ࡴࡨࡰࡪࡧࡳࡦࠤ᱗")):
            bstack11l1ll1ll1l_opy_[bstack111l11_opy_ (u"ࠫࡩ࡯ࡳࡵࡴࡲࠫ᱘")] = bstack111l11_opy_ (u"ࠬࡧ࡬ࡱ࡫ࡱࡩࠬ᱙")
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡤࡪࡵࡷࡶࡴࠦ࡯ࡧࠢ࡯࡭ࡳࡻࡸࠣᱚ") + e)
@measure(event_name=EVENTS.bstack11ll11111l1_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
def bstack11l11l11ll1_opy_(bstack11l11l1l1l1_opy_, bstack11l1ll1ll11_opy_):
    logger.debug(bstack111l11_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳ࠺ࠡࠤᱛ") + str(bstack11l11l1l1l1_opy_) + bstack111l11_opy_ (u"ࠣࠤᱜ"))
    zip_path = os.path.join(bstack11l1ll1ll11_opy_, bstack111l11_opy_ (u"ࠤࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࡥࡦࡪ࡮ࡨ࠲ࡿ࡯ࡰࠣᱝ"))
    bstack11l11l1l11l_opy_ = bstack111l11_opy_ (u"ࠪࠫᱞ")
    with requests.get(bstack11l11l1l1l1_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack111l11_opy_ (u"ࠦࡼࡨࠢᱟ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack111l11_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾ࠴ࠢᱠ"))
    with zipfile.ZipFile(zip_path, bstack111l11_opy_ (u"࠭ࡲࠨᱡ")) as zip_ref:
        bstack11l1l1l11l1_opy_ = zip_ref.namelist()
        if len(bstack11l1l1l11l1_opy_) > 0:
            bstack11l11l1l11l_opy_ = bstack11l1l1l11l1_opy_[0] # bstack11l11l1111l_opy_ bstack11ll1l111l1_opy_ will be bstack11l1l11l1l1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l1ll1ll11_opy_)
        logger.debug(bstack111l11_opy_ (u"ࠢࡇ࡫࡯ࡩࡸࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥ࡫ࡸࡵࡴࡤࡧࡹ࡫ࡤࠡࡶࡲࠤࠬࠨᱢ") + str(bstack11l1ll1ll11_opy_) + bstack111l11_opy_ (u"ࠣࠩࠥᱣ"))
    os.remove(zip_path)
    return bstack11l11l1l11l_opy_
def get_cli_dir():
    bstack11l1l1ll1l1_opy_ = bstack1l1lll11l1l_opy_()
    if bstack11l1l1ll1l1_opy_:
        bstack1llll111111_opy_ = os.path.join(bstack11l1l1ll1l1_opy_, bstack111l11_opy_ (u"ࠤࡦࡰ࡮ࠨᱤ"))
        if not os.path.exists(bstack1llll111111_opy_):
            os.makedirs(bstack1llll111111_opy_, mode=0o777, exist_ok=True)
        return bstack1llll111111_opy_
    else:
        raise FileNotFoundError(bstack111l11_opy_ (u"ࠥࡒࡴࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽ࠳ࠨᱥ"))
def bstack1llll111lll_opy_(bstack1llll111111_opy_):
    bstack111l11_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡲࠥࡧࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠳ࠨࠢࠣᱦ")
    bstack11l1l11ll1l_opy_ = [
        os.path.join(bstack1llll111111_opy_, f)
        for f in os.listdir(bstack1llll111111_opy_)
        if os.path.isfile(os.path.join(bstack1llll111111_opy_, f)) and f.startswith(bstack111l11_opy_ (u"ࠧࡨࡩ࡯ࡣࡵࡽ࠲ࠨᱧ"))
    ]
    if len(bstack11l1l11ll1l_opy_) > 0:
        return max(bstack11l1l11ll1l_opy_, key=os.path.getmtime) # get bstack11l1llll11l_opy_ binary
    return bstack111l11_opy_ (u"ࠨࠢᱨ")
def bstack11lll111111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll1l1l1l11_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll1l1l1l11_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d