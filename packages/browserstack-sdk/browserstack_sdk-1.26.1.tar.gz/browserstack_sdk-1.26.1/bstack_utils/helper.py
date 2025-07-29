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
from bstack_utils.constants import (bstack11ll11ll111_opy_, bstack11ll1l1111_opy_, bstack111lllll1_opy_, bstack11llllll1l_opy_,
                                    bstack11ll1l11ll1_opy_, bstack11ll11lllll_opy_, bstack11ll11l111l_opy_, bstack11ll1l11111_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11llll1ll_opy_, bstack1l1l1l111l_opy_
from bstack_utils.proxy import bstack1ll111l1_opy_, bstack111ll1lll_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l11l1lll_opy_
from browserstack_sdk._version import __version__
bstack11ll1llll1_opy_ = Config.bstack1ll1l1l1l1_opy_()
logger = bstack1l11l1lll_opy_.get_logger(__name__, bstack1l11l1lll_opy_.bstack1lllll11ll1_opy_())
def bstack11lll11l111_opy_(config):
    return config[bstack11l1lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᨨ")]
def bstack11lll111111_opy_(config):
    return config[bstack11l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᨩ")]
def bstack11l1l1l1l1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1l1l111l_opy_(obj):
    values = []
    bstack11l111lll11_opy_ = re.compile(bstack11l1lll_opy_ (u"ࡸࠢ࡟ࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤࡢࡤࠬࠦࠥᨪ"), re.I)
    for key in obj.keys():
        if bstack11l111lll11_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l1ll11l1l_opy_(config):
    tags = []
    tags.extend(bstack11l1l1l111l_opy_(os.environ))
    tags.extend(bstack11l1l1l111l_opy_(config))
    return tags
def bstack11l11ll1lll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l11l1111l_opy_(bstack11l1l111111_opy_):
    if not bstack11l1l111111_opy_:
        return bstack11l1lll_opy_ (u"ࠧࠨᨫ")
    return bstack11l1lll_opy_ (u"ࠣࡽࢀࠤ࠭ࢁࡽࠪࠤᨬ").format(bstack11l1l111111_opy_.name, bstack11l1l111111_opy_.email)
def bstack11lll1l1lll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1ll1lll1_opy_ = repo.common_dir
        info = {
            bstack11l1lll_opy_ (u"ࠤࡶ࡬ࡦࠨᨭ"): repo.head.commit.hexsha,
            bstack11l1lll_opy_ (u"ࠥࡷ࡭ࡵࡲࡵࡡࡶ࡬ࡦࠨᨮ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11l1lll_opy_ (u"ࠦࡧࡸࡡ࡯ࡥ࡫ࠦᨯ"): repo.active_branch.name,
            bstack11l1lll_opy_ (u"ࠧࡺࡡࡨࠤᨰ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11l1lll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࠤᨱ"): bstack11l11l1111l_opy_(repo.head.commit.committer),
            bstack11l1lll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࡢࡨࡦࡺࡥࠣᨲ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11l1lll_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࠣᨳ"): bstack11l11l1111l_opy_(repo.head.commit.author),
            bstack11l1lll_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡡࡧࡥࡹ࡫ࠢᨴ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11l1lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦᨵ"): repo.head.commit.message,
            bstack11l1lll_opy_ (u"ࠦࡷࡵ࡯ࡵࠤᨶ"): repo.git.rev_parse(bstack11l1lll_opy_ (u"ࠧ࠳࠭ࡴࡪࡲࡻ࠲ࡺ࡯ࡱ࡮ࡨࡺࡪࡲࠢᨷ")),
            bstack11l1lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡳࡳࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᨸ"): bstack11l1ll1lll1_opy_,
            bstack11l1lll_opy_ (u"ࠢࡸࡱࡵ࡯ࡹࡸࡥࡦࡡࡪ࡭ࡹࡥࡤࡪࡴࠥᨹ"): subprocess.check_output([bstack11l1lll_opy_ (u"ࠣࡩ࡬ࡸࠧᨺ"), bstack11l1lll_opy_ (u"ࠤࡵࡩࡻ࠳ࡰࡢࡴࡶࡩࠧᨻ"), bstack11l1lll_opy_ (u"ࠥ࠱࠲࡭ࡩࡵ࠯ࡦࡳࡲࡳ࡯࡯࠯ࡧ࡭ࡷࠨᨼ")]).strip().decode(
                bstack11l1lll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᨽ")),
            bstack11l1lll_opy_ (u"ࠧࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᨾ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11l1lll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡹ࡟ࡴ࡫ࡱࡧࡪࡥ࡬ࡢࡵࡷࡣࡹࡧࡧࠣᨿ"): repo.git.rev_list(
                bstack11l1lll_opy_ (u"ࠢࡼࡿ࠱࠲ࢀࢃࠢᩀ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l1l11ll11_opy_ = []
        for remote in remotes:
            bstack11l1ll11lll_opy_ = {
                bstack11l1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨᩁ"): remote.name,
                bstack11l1lll_opy_ (u"ࠤࡸࡶࡱࠨᩂ"): remote.url,
            }
            bstack11l1l11ll11_opy_.append(bstack11l1ll11lll_opy_)
        bstack11l1l11l1l1_opy_ = {
            bstack11l1lll_opy_ (u"ࠥࡲࡦࡳࡥࠣᩃ"): bstack11l1lll_opy_ (u"ࠦ࡬࡯ࡴࠣᩄ"),
            **info,
            bstack11l1lll_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡸࠨᩅ"): bstack11l1l11ll11_opy_
        }
        bstack11l1l11l1l1_opy_ = bstack11l11lllll1_opy_(bstack11l1l11l1l1_opy_)
        return bstack11l1l11l1l1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11l1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᩆ").format(err))
        return {}
def bstack11l11lllll1_opy_(bstack11l1l11l1l1_opy_):
    bstack11l11l1ll11_opy_ = bstack11l1lll11l1_opy_(bstack11l1l11l1l1_opy_)
    if bstack11l11l1ll11_opy_ and bstack11l11l1ll11_opy_ > bstack11ll1l11ll1_opy_:
        bstack11l1l11ll1l_opy_ = bstack11l11l1ll11_opy_ - bstack11ll1l11ll1_opy_
        bstack11l111llll1_opy_ = bstack11l1l1l1111_opy_(bstack11l1l11l1l1_opy_[bstack11l1lll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣᩇ")], bstack11l1l11ll1l_opy_)
        bstack11l1l11l1l1_opy_[bstack11l1lll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᩈ")] = bstack11l111llll1_opy_
        logger.info(bstack11l1lll_opy_ (u"ࠤࡗ࡬ࡪࠦࡣࡰ࡯ࡰ࡭ࡹࠦࡨࡢࡵࠣࡦࡪ࡫࡮ࠡࡶࡵࡹࡳࡩࡡࡵࡧࡧ࠲࡙ࠥࡩࡻࡧࠣࡳ࡫ࠦࡣࡰ࡯ࡰ࡭ࡹࠦࡡࡧࡶࡨࡶࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥࢁࡽࠡࡍࡅࠦᩉ")
                    .format(bstack11l1lll11l1_opy_(bstack11l1l11l1l1_opy_) / 1024))
    return bstack11l1l11l1l1_opy_
def bstack11l1lll11l1_opy_(bstack1l1ll1l11_opy_):
    try:
        if bstack1l1ll1l11_opy_:
            bstack11l1l111lll_opy_ = json.dumps(bstack1l1ll1l11_opy_)
            bstack11l1lll1ll1_opy_ = sys.getsizeof(bstack11l1l111lll_opy_)
            return bstack11l1lll1ll1_opy_
    except Exception as e:
        logger.debug(bstack11l1lll_opy_ (u"ࠥࡗࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡦࡥࡱࡩࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡴ࡫ࡽࡩࠥࡵࡦࠡࡌࡖࡓࡓࠦ࡯ࡣ࡬ࡨࡧࡹࡀࠠࡼࡿࠥᩊ").format(e))
    return -1
def bstack11l1l1l1111_opy_(field, bstack11l11lll1l1_opy_):
    try:
        bstack11l1lllll1l_opy_ = len(bytes(bstack11ll11lllll_opy_, bstack11l1lll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᩋ")))
        bstack11l11ll1111_opy_ = bytes(field, bstack11l1lll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᩌ"))
        bstack11l11l111ll_opy_ = len(bstack11l11ll1111_opy_)
        bstack11l11llll1l_opy_ = ceil(bstack11l11l111ll_opy_ - bstack11l11lll1l1_opy_ - bstack11l1lllll1l_opy_)
        if bstack11l11llll1l_opy_ > 0:
            bstack11l1l1l1l11_opy_ = bstack11l11ll1111_opy_[:bstack11l11llll1l_opy_].decode(bstack11l1lll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᩍ"), errors=bstack11l1lll_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࠧᩎ")) + bstack11ll11lllll_opy_
            return bstack11l1l1l1l11_opy_
    except Exception as e:
        logger.debug(bstack11l1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡴࡳࡷࡱࡧࡦࡺࡩ࡯ࡩࠣࡪ࡮࡫࡬ࡥ࠮ࠣࡲࡴࡺࡨࡪࡰࡪࠤࡼࡧࡳࠡࡶࡵࡹࡳࡩࡡࡵࡧࡧࠤ࡭࡫ࡲࡦ࠼ࠣࡿࢂࠨᩏ").format(e))
    return field
def bstack11ll1lllll_opy_():
    env = os.environ
    if (bstack11l1lll_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢᩐ") in env and len(env[bstack11l1lll_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣᩑ")]) > 0) or (
            bstack11l1lll_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥᩒ") in env and len(env[bstack11l1lll_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦᩓ")]) > 0):
        return {
            bstack11l1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᩔ"): bstack11l1lll_opy_ (u"ࠢࡋࡧࡱ࡯࡮ࡴࡳࠣᩕ"),
            bstack11l1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᩖ"): env.get(bstack11l1lll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᩗ")),
            bstack11l1lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᩘ"): env.get(bstack11l1lll_opy_ (u"ࠦࡏࡕࡂࡠࡐࡄࡑࡊࠨᩙ")),
            bstack11l1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᩚ"): env.get(bstack11l1lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᩛ"))
        }
    if env.get(bstack11l1lll_opy_ (u"ࠢࡄࡋࠥᩜ")) == bstack11l1lll_opy_ (u"ࠣࡶࡵࡹࡪࠨᩝ") and bstack1llll1l11_opy_(env.get(bstack11l1lll_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡅࡌࠦᩞ"))):
        return {
            bstack11l1lll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᩟"): bstack11l1lll_opy_ (u"ࠦࡈ࡯ࡲࡤ࡮ࡨࡇࡎࠨ᩠"),
            bstack11l1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᩡ"): env.get(bstack11l1lll_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᩢ")),
            bstack11l1lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᩣ"): env.get(bstack11l1lll_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡌࡒࡆࠧᩤ")),
            bstack11l1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᩥ"): env.get(bstack11l1lll_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࠨᩦ"))
        }
    if env.get(bstack11l1lll_opy_ (u"ࠦࡈࡏࠢᩧ")) == bstack11l1lll_opy_ (u"ࠧࡺࡲࡶࡧࠥᩨ") and bstack1llll1l11_opy_(env.get(bstack11l1lll_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࠨᩩ"))):
        return {
            bstack11l1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩪ"): bstack11l1lll_opy_ (u"ࠣࡖࡵࡥࡻ࡯ࡳࠡࡅࡌࠦᩫ"),
            bstack11l1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᩬ"): env.get(bstack11l1lll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡ࡚ࡉࡇࡥࡕࡓࡎࠥᩭ")),
            bstack11l1lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᩮ"): env.get(bstack11l1lll_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᩯ")),
            bstack11l1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᩰ"): env.get(bstack11l1lll_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᩱ"))
        }
    if env.get(bstack11l1lll_opy_ (u"ࠣࡅࡌࠦᩲ")) == bstack11l1lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᩳ") and env.get(bstack11l1lll_opy_ (u"ࠥࡇࡎࡥࡎࡂࡏࡈࠦᩴ")) == bstack11l1lll_opy_ (u"ࠦࡨࡵࡤࡦࡵ࡫࡭ࡵࠨ᩵"):
        return {
            bstack11l1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᩶"): bstack11l1lll_opy_ (u"ࠨࡃࡰࡦࡨࡷ࡭࡯ࡰࠣ᩷"),
            bstack11l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᩸"): None,
            bstack11l1lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᩹"): None,
            bstack11l1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᩺"): None
        }
    if env.get(bstack11l1lll_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡓࡃࡑࡇࡍࠨ᩻")) and env.get(bstack11l1lll_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢ᩼")):
        return {
            bstack11l1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᩽"): bstack11l1lll_opy_ (u"ࠨࡂࡪࡶࡥࡹࡨࡱࡥࡵࠤ᩾"),
            bstack11l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮᩿ࠥ"): env.get(bstack11l1lll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡌࡏࡔࡠࡊࡗࡘࡕࡥࡏࡓࡋࡊࡍࡓࠨ᪀")),
            bstack11l1lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᪁"): None,
            bstack11l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᪂"): env.get(bstack11l1lll_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᪃"))
        }
    if env.get(bstack11l1lll_opy_ (u"ࠧࡉࡉࠣ᪄")) == bstack11l1lll_opy_ (u"ࠨࡴࡳࡷࡨࠦ᪅") and bstack1llll1l11_opy_(env.get(bstack11l1lll_opy_ (u"ࠢࡅࡔࡒࡒࡊࠨ᪆"))):
        return {
            bstack11l1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪇"): bstack11l1lll_opy_ (u"ࠤࡇࡶࡴࡴࡥࠣ᪈"),
            bstack11l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᪉"): env.get(bstack11l1lll_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡏࡍࡓࡑࠢ᪊")),
            bstack11l1lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᪋"): None,
            bstack11l1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᪌"): env.get(bstack11l1lll_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᪍"))
        }
    if env.get(bstack11l1lll_opy_ (u"ࠣࡅࡌࠦ᪎")) == bstack11l1lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᪏") and bstack1llll1l11_opy_(env.get(bstack11l1lll_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࠨ᪐"))):
        return {
            bstack11l1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪑"): bstack11l1lll_opy_ (u"࡙ࠧࡥ࡮ࡣࡳ࡬ࡴࡸࡥࠣ᪒"),
            bstack11l1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᪓"): env.get(bstack11l1lll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡓࡗࡍࡁࡏࡋ࡝ࡅ࡙ࡏࡏࡏࡡࡘࡖࡑࠨ᪔")),
            bstack11l1lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᪕"): env.get(bstack11l1lll_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ᪖")),
            bstack11l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᪗"): env.get(bstack11l1lll_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡎࡊࠢ᪘"))
        }
    if env.get(bstack11l1lll_opy_ (u"ࠧࡉࡉࠣ᪙")) == bstack11l1lll_opy_ (u"ࠨࡴࡳࡷࡨࠦ᪚") and bstack1llll1l11_opy_(env.get(bstack11l1lll_opy_ (u"ࠢࡈࡋࡗࡐࡆࡈ࡟ࡄࡋࠥ᪛"))):
        return {
            bstack11l1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪜"): bstack11l1lll_opy_ (u"ࠤࡊ࡭ࡹࡒࡡࡣࠤ᪝"),
            bstack11l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᪞"): env.get(bstack11l1lll_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣ࡚ࡘࡌࠣ᪟")),
            bstack11l1lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᪠"): env.get(bstack11l1lll_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᪡")),
            bstack11l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪢"): env.get(bstack11l1lll_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡋࡇࠦ᪣"))
        }
    if env.get(bstack11l1lll_opy_ (u"ࠤࡆࡍࠧ᪤")) == bstack11l1lll_opy_ (u"ࠥࡸࡷࡻࡥࠣ᪥") and bstack1llll1l11_opy_(env.get(bstack11l1lll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋࠢ᪦"))):
        return {
            bstack11l1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᪧ"): bstack11l1lll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡰ࡯ࡴࡦࠤ᪨"),
            bstack11l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᪩"): env.get(bstack11l1lll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ᪪")),
            bstack11l1lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᪫"): env.get(bstack11l1lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡌࡂࡄࡈࡐࠧ᪬")) or env.get(bstack11l1lll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢ᪭")),
            bstack11l1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᪮"): env.get(bstack11l1lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ᪯"))
        }
    if bstack1llll1l11_opy_(env.get(bstack11l1lll_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤ᪰"))):
        return {
            bstack11l1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪱"): bstack11l1lll_opy_ (u"ࠤ࡙࡭ࡸࡻࡡ࡭ࠢࡖࡸࡺࡪࡩࡰࠢࡗࡩࡦࡳࠠࡔࡧࡵࡺ࡮ࡩࡥࡴࠤ᪲"),
            bstack11l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᪳"): bstack11l1lll_opy_ (u"ࠦࢀࢃࡻࡾࠤ᪴").format(env.get(bstack11l1lll_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨ᪵")), env.get(bstack11l1lll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࡍࡉ᪶࠭"))),
            bstack11l1lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪷"): env.get(bstack11l1lll_opy_ (u"ࠣࡕ࡜ࡗ࡙ࡋࡍࡠࡆࡈࡊࡎࡔࡉࡕࡋࡒࡒࡎࡊ᪸ࠢ")),
            bstack11l1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲ᪹ࠣ"): env.get(bstack11l1lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆ᪺ࠥ"))
        }
    if bstack1llll1l11_opy_(env.get(bstack11l1lll_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࠨ᪻"))):
        return {
            bstack11l1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᪼"): bstack11l1lll_opy_ (u"ࠨࡁࡱࡲࡹࡩࡾࡵࡲ᪽ࠣ"),
            bstack11l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᪾"): bstack11l1lll_opy_ (u"ࠣࡽࢀ࠳ࡵࡸ࡯࡫ࡧࡦࡸ࠴ࢁࡽ࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃᪿࠢ").format(env.get(bstack11l1lll_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣ࡚ࡘࡌࠨᫀ")), env.get(bstack11l1lll_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡇࡃࡄࡑࡘࡒ࡙ࡥࡎࡂࡏࡈࠫ᫁")), env.get(bstack11l1lll_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡔࡎࡘࡋࠬ᫂")), env.get(bstack11l1lll_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡉࡅ᫃ࠩ"))),
            bstack11l1lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥ᫄ࠣ"): env.get(bstack11l1lll_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᫅")),
            bstack11l1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᫆"): env.get(bstack11l1lll_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᫇"))
        }
    if env.get(bstack11l1lll_opy_ (u"ࠥࡅ࡟࡛ࡒࡆࡡࡋࡘ࡙ࡖ࡟ࡖࡕࡈࡖࡤࡇࡇࡆࡐࡗࠦ᫈")) and env.get(bstack11l1lll_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨ᫉")):
        return {
            bstack11l1lll_opy_ (u"ࠧࡴࡡ࡮ࡧ᫊ࠥ"): bstack11l1lll_opy_ (u"ࠨࡁࡻࡷࡵࡩࠥࡉࡉࠣ᫋"),
            bstack11l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᫌ"): bstack11l1lll_opy_ (u"ࠣࡽࢀࡿࢂ࠵࡟ࡣࡷ࡬ࡰࡩ࠵ࡲࡦࡵࡸࡰࡹࡹ࠿ࡣࡷ࡬ࡰࡩࡏࡤ࠾ࡽࢀࠦᫍ").format(env.get(bstack11l1lll_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬᫎ")), env.get(bstack11l1lll_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࠨ᫏")), env.get(bstack11l1lll_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠫ᫐"))),
            bstack11l1lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᫑"): env.get(bstack11l1lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨ᫒")),
            bstack11l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᫓"): env.get(bstack11l1lll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣ᫔"))
        }
    if any([env.get(bstack11l1lll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ᫕")), env.get(bstack11l1lll_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤ᫖")), env.get(bstack11l1lll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣ᫗"))]):
        return {
            bstack11l1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᫘"): bstack11l1lll_opy_ (u"ࠨࡁࡘࡕࠣࡇࡴࡪࡥࡃࡷ࡬ࡰࡩࠨ᫙"),
            bstack11l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᫚"): env.get(bstack11l1lll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡕ࡛ࡂࡍࡋࡆࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ᫛")),
            bstack11l1lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᫜"): env.get(bstack11l1lll_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ᫝")),
            bstack11l1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᫞"): env.get(bstack11l1lll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ᫟"))
        }
    if env.get(bstack11l1lll_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦ᫠")):
        return {
            bstack11l1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᫡"): bstack11l1lll_opy_ (u"ࠣࡄࡤࡱࡧࡵ࡯ࠣ᫢"),
            bstack11l1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᫣"): env.get(bstack11l1lll_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡔࡨࡷࡺࡲࡴࡴࡗࡵࡰࠧ᫤")),
            bstack11l1lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᫥"): env.get(bstack11l1lll_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡹࡨࡰࡴࡷࡎࡴࡨࡎࡢ࡯ࡨࠦ᫦")),
            bstack11l1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᫧"): env.get(bstack11l1lll_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧ᫨"))
        }
    if env.get(bstack11l1lll_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࠤ᫩")) or env.get(bstack11l1lll_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦ᫪")):
        return {
            bstack11l1lll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᫫"): bstack11l1lll_opy_ (u"ࠦ࡜࡫ࡲࡤ࡭ࡨࡶࠧ᫬"),
            bstack11l1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᫭"): env.get(bstack11l1lll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᫮")),
            bstack11l1lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᫯"): bstack11l1lll_opy_ (u"ࠣࡏࡤ࡭ࡳࠦࡐࡪࡲࡨࡰ࡮ࡴࡥࠣ᫰") if env.get(bstack11l1lll_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦ᫱")) else None,
            bstack11l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᫲"): env.get(bstack11l1lll_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡍࡉࡕࡡࡆࡓࡒࡓࡉࡕࠤ᫳"))
        }
    if any([env.get(bstack11l1lll_opy_ (u"ࠧࡍࡃࡑࡡࡓࡖࡔࡐࡅࡄࡖࠥ᫴")), env.get(bstack11l1lll_opy_ (u"ࠨࡇࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ᫵")), env.get(bstack11l1lll_opy_ (u"ࠢࡈࡑࡒࡋࡑࡋ࡟ࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ᫶"))]):
        return {
            bstack11l1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨ᫷"): bstack11l1lll_opy_ (u"ࠤࡊࡳࡴ࡭࡬ࡦࠢࡆࡰࡴࡻࡤࠣ᫸"),
            bstack11l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᫹"): None,
            bstack11l1lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᫺"): env.get(bstack11l1lll_opy_ (u"ࠧࡖࡒࡐࡌࡈࡇ࡙ࡥࡉࡅࠤ᫻")),
            bstack11l1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᫼"): env.get(bstack11l1lll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤ᫽"))
        }
    if env.get(bstack11l1lll_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࠦ᫾")):
        return {
            bstack11l1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᫿"): bstack11l1lll_opy_ (u"ࠥࡗ࡭࡯ࡰࡱࡣࡥࡰࡪࠨᬀ"),
            bstack11l1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᬁ"): env.get(bstack11l1lll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᬂ")),
            bstack11l1lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᬃ"): bstack11l1lll_opy_ (u"ࠢࡋࡱࡥࠤࠨࢁࡽࠣᬄ").format(env.get(bstack11l1lll_opy_ (u"ࠨࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠫᬅ"))) if env.get(bstack11l1lll_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠧᬆ")) else None,
            bstack11l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᬇ"): env.get(bstack11l1lll_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᬈ"))
        }
    if bstack1llll1l11_opy_(env.get(bstack11l1lll_opy_ (u"ࠧࡔࡅࡕࡎࡌࡊ࡞ࠨᬉ"))):
        return {
            bstack11l1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᬊ"): bstack11l1lll_opy_ (u"ࠢࡏࡧࡷࡰ࡮࡬ࡹࠣᬋ"),
            bstack11l1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᬌ"): env.get(bstack11l1lll_opy_ (u"ࠤࡇࡉࡕࡒࡏ࡚ࡡࡘࡖࡑࠨᬍ")),
            bstack11l1lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᬎ"): env.get(bstack11l1lll_opy_ (u"ࠦࡘࡏࡔࡆࡡࡑࡅࡒࡋࠢᬏ")),
            bstack11l1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᬐ"): env.get(bstack11l1lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣᬑ"))
        }
    if bstack1llll1l11_opy_(env.get(bstack11l1lll_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡂࡅࡗࡍࡔࡔࡓࠣᬒ"))):
        return {
            bstack11l1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨᬓ"): bstack11l1lll_opy_ (u"ࠤࡊ࡭ࡹࡎࡵࡣࠢࡄࡧࡹ࡯࡯࡯ࡵࠥᬔ"),
            bstack11l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᬕ"): bstack11l1lll_opy_ (u"ࠦࢀࢃ࠯ࡼࡿ࠲ࡥࡨࡺࡩࡰࡰࡶ࠳ࡷࡻ࡮ࡴ࠱ࡾࢁࠧᬖ").format(env.get(bstack11l1lll_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤ࡙ࡅࡓࡘࡈࡖࡤ࡛ࡒࡍࠩᬗ")), env.get(bstack11l1lll_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡆࡒࡒࡗࡎ࡚ࡏࡓ࡛ࠪᬘ")), env.get(bstack11l1lll_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠧᬙ"))),
            bstack11l1lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᬚ"): env.get(bstack11l1lll_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡ࡚ࡓࡗࡑࡆࡍࡑ࡚ࠦᬛ")),
            bstack11l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᬜ"): env.get(bstack11l1lll_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠦᬝ"))
        }
    if env.get(bstack11l1lll_opy_ (u"ࠧࡉࡉࠣᬞ")) == bstack11l1lll_opy_ (u"ࠨࡴࡳࡷࡨࠦᬟ") and env.get(bstack11l1lll_opy_ (u"ࠢࡗࡇࡕࡇࡊࡒࠢᬠ")) == bstack11l1lll_opy_ (u"ࠣ࠳ࠥᬡ"):
        return {
            bstack11l1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᬢ"): bstack11l1lll_opy_ (u"࡚ࠥࡪࡸࡣࡦ࡮ࠥᬣ"),
            bstack11l1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᬤ"): bstack11l1lll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࢁࡽࠣᬥ").format(env.get(bstack11l1lll_opy_ (u"࠭ࡖࡆࡔࡆࡉࡑࡥࡕࡓࡎࠪᬦ"))),
            bstack11l1lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᬧ"): None,
            bstack11l1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᬨ"): None,
        }
    if env.get(bstack11l1lll_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣ࡛ࡋࡒࡔࡋࡒࡒࠧᬩ")):
        return {
            bstack11l1lll_opy_ (u"ࠥࡲࡦࡳࡥࠣᬪ"): bstack11l1lll_opy_ (u"࡙ࠦ࡫ࡡ࡮ࡥ࡬ࡸࡾࠨᬫ"),
            bstack11l1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᬬ"): None,
            bstack11l1lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᬭ"): env.get(bstack11l1lll_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡࡓࡖࡔࡐࡅࡄࡖࡢࡒࡆࡓࡅࠣᬮ")),
            bstack11l1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᬯ"): env.get(bstack11l1lll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᬰ"))
        }
    if any([env.get(bstack11l1lll_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࠨᬱ")), env.get(bstack11l1lll_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡔࡏࠦᬲ")), env.get(bstack11l1lll_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡖࡉࡗࡔࡁࡎࡇࠥᬳ")), env.get(bstack11l1lll_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡗࡉࡆࡓ᬴ࠢ"))]):
        return {
            bstack11l1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᬵ"): bstack11l1lll_opy_ (u"ࠣࡅࡲࡲࡨࡵࡵࡳࡵࡨࠦᬶ"),
            bstack11l1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᬷ"): None,
            bstack11l1lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᬸ"): env.get(bstack11l1lll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᬹ")) or None,
            bstack11l1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᬺ"): env.get(bstack11l1lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣᬻ"), 0)
        }
    if env.get(bstack11l1lll_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᬼ")):
        return {
            bstack11l1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨᬽ"): bstack11l1lll_opy_ (u"ࠤࡊࡳࡈࡊࠢᬾ"),
            bstack11l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᬿ"): None,
            bstack11l1lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᭀ"): env.get(bstack11l1lll_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᭁ")),
            bstack11l1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᭂ"): env.get(bstack11l1lll_opy_ (u"ࠢࡈࡑࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡉࡏࡖࡐࡗࡉࡗࠨᭃ"))
        }
    if env.get(bstack11l1lll_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᭄")):
        return {
            bstack11l1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᭅ"): bstack11l1lll_opy_ (u"ࠥࡇࡴࡪࡥࡇࡴࡨࡷ࡭ࠨᭆ"),
            bstack11l1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᭇ"): env.get(bstack11l1lll_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᭈ")),
            bstack11l1lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᭉ"): env.get(bstack11l1lll_opy_ (u"ࠢࡄࡈࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥᭊ")),
            bstack11l1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᭋ"): env.get(bstack11l1lll_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᭌ"))
        }
    return {bstack11l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᭍"): None}
def get_host_info():
    return {
        bstack11l1lll_opy_ (u"ࠦ࡭ࡵࡳࡵࡰࡤࡱࡪࠨ᭎"): platform.node(),
        bstack11l1lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢ᭏"): platform.system(),
        bstack11l1lll_opy_ (u"ࠨࡴࡺࡲࡨࠦ᭐"): platform.machine(),
        bstack11l1lll_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣ᭑"): platform.version(),
        bstack11l1lll_opy_ (u"ࠣࡣࡵࡧ࡭ࠨ᭒"): platform.architecture()[0]
    }
def bstack1111llll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1lll1l1l_opy_():
    if bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ᭓")):
        return bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ᭔")
    return bstack11l1lll_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠪ᭕")
def bstack11l1ll111ll_opy_(driver):
    info = {
        bstack11l1lll_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ᭖"): driver.capabilities,
        bstack11l1lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪ᭗"): driver.session_id,
        bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ᭘"): driver.capabilities.get(bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭᭙"), None),
        bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ᭚"): driver.capabilities.get(bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᭛"), None),
        bstack11l1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࠭᭜"): driver.capabilities.get(bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫ᭝"), None),
        bstack11l1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᭞"):driver.capabilities.get(bstack11l1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ᭟"), None),
    }
    if bstack11l1lll1l1l_opy_() == bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ᭠"):
        if bstack11ll1l11ll_opy_():
            info[bstack11l1lll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪ᭡")] = bstack11l1lll_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ᭢")
        elif driver.capabilities.get(bstack11l1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᭣"), {}).get(bstack11l1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ᭤"), False):
            info[bstack11l1lll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ᭥")] = bstack11l1lll_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ᭦")
        else:
            info[bstack11l1lll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ᭧")] = bstack11l1lll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᭨")
    return info
def bstack11ll1l11ll_opy_():
    if bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ᭩")):
        return True
    if bstack1llll1l11_opy_(os.environ.get(bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ᭪"), None)):
        return True
    return False
def bstack11lll1lll_opy_(bstack11l1lll1l11_opy_, url, data, config):
    headers = config.get(bstack11l1lll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭᭫"), None)
    proxies = bstack1ll111l1_opy_(config, url)
    auth = config.get(bstack11l1lll_opy_ (u"࠭ࡡࡶࡶ࡫᭬ࠫ"), None)
    response = requests.request(
            bstack11l1lll1l11_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1l1ll1ll_opy_(bstack1l11l1ll1_opy_, size):
    bstack1l1l1ll11l_opy_ = []
    while len(bstack1l11l1ll1_opy_) > size:
        bstack11l11111l_opy_ = bstack1l11l1ll1_opy_[:size]
        bstack1l1l1ll11l_opy_.append(bstack11l11111l_opy_)
        bstack1l11l1ll1_opy_ = bstack1l11l1ll1_opy_[size:]
    bstack1l1l1ll11l_opy_.append(bstack1l11l1ll1_opy_)
    return bstack1l1l1ll11l_opy_
def bstack11l1l1lll11_opy_(message, bstack11l1l111l1l_opy_=False):
    os.write(1, bytes(message, bstack11l1lll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭᭭")))
    os.write(1, bytes(bstack11l1lll_opy_ (u"ࠨ࡞ࡱࠫ᭮"), bstack11l1lll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᭯")))
    if bstack11l1l111l1l_opy_:
        with open(bstack11l1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡳ࠶࠷ࡹ࠮ࠩ᭰") + os.environ[bstack11l1lll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪ᭱")] + bstack11l1lll_opy_ (u"ࠬ࠴࡬ࡰࡩࠪ᭲"), bstack11l1lll_opy_ (u"࠭ࡡࠨ᭳")) as f:
            f.write(message + bstack11l1lll_opy_ (u"ࠧ࡝ࡰࠪ᭴"))
def bstack1l1ll1l1ll1_opy_():
    return os.environ[bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ᭵")].lower() == bstack11l1lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ᭶")
def bstack1ll1ll11_opy_(bstack11l1l1l1lll_opy_):
    return bstack11l1lll_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩ᭷").format(bstack11ll11ll111_opy_, bstack11l1l1l1lll_opy_)
def bstack1lll11l11_opy_():
    return bstack111l1lllll_opy_().replace(tzinfo=None).isoformat() + bstack11l1lll_opy_ (u"ࠫ࡟࠭᭸")
def bstack11l11lll11l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11l1lll_opy_ (u"ࠬࡠࠧ᭹"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11l1lll_opy_ (u"࡚࠭ࠨ᭺")))).total_seconds() * 1000
def bstack11l1lll1111_opy_(timestamp):
    return bstack11l11l1lll1_opy_(timestamp).isoformat() + bstack11l1lll_opy_ (u"࡛ࠧࠩ᭻")
def bstack11l11l1llll_opy_(bstack11l11lll1ll_opy_):
    date_format = bstack11l1lll_opy_ (u"ࠨࠧ࡜ࠩࡲࠫࡤࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࠱ࠩ࡫࠭᭼")
    bstack11l1ll11111_opy_ = datetime.datetime.strptime(bstack11l11lll1ll_opy_, date_format)
    return bstack11l1ll11111_opy_.isoformat() + bstack11l1lll_opy_ (u"ࠩ࡝ࠫ᭽")
def bstack11l111lll1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11l1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᭾")
    else:
        return bstack11l1lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ᭿")
def bstack1llll1l11_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11l1lll_opy_ (u"ࠬࡺࡲࡶࡧࠪᮀ")
def bstack11l11l11l11_opy_(val):
    return val.__str__().lower() == bstack11l1lll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬᮁ")
def bstack111l111111_opy_(bstack11l1llll1ll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1llll1ll_opy_ as e:
                print(bstack11l1lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢᮂ").format(func.__name__, bstack11l1llll1ll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l11ll11l1_opy_(bstack11l1ll1ll11_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1ll1ll11_opy_(cls, *args, **kwargs)
            except bstack11l1llll1ll_opy_ as e:
                print(bstack11l1lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣᮃ").format(bstack11l1ll1ll11_opy_.__name__, bstack11l1llll1ll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l11ll11l1_opy_
    else:
        return decorator
def bstack1lll11l1l_opy_(bstack1111lll1ll_opy_):
    if os.getenv(bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬᮄ")) is not None:
        return bstack1llll1l11_opy_(os.getenv(bstack11l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ᮅ")))
    if bstack11l1lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᮆ") in bstack1111lll1ll_opy_ and bstack11l11l11l11_opy_(bstack1111lll1ll_opy_[bstack11l1lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᮇ")]):
        return False
    if bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᮈ") in bstack1111lll1ll_opy_ and bstack11l11l11l11_opy_(bstack1111lll1ll_opy_[bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᮉ")]):
        return False
    return True
def bstack1ll11lll_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l1llll111_opy_ = os.environ.get(bstack11l1lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠣᮊ"), None)
        return bstack11l1llll111_opy_ is None or bstack11l1llll111_opy_ == bstack11l1lll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᮋ")
    except Exception as e:
        return False
def bstack1ll1l11ll1_opy_(hub_url, CONFIG):
    if bstack111111111_opy_() <= version.parse(bstack11l1lll_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪᮌ")):
        if hub_url:
            return bstack11l1lll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᮍ") + hub_url + bstack11l1lll_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤᮎ")
        return bstack111lllll1_opy_
    if hub_url:
        return bstack11l1lll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣᮏ") + hub_url + bstack11l1lll_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣᮐ")
    return bstack11llllll1l_opy_
def bstack11l1ll1111l_opy_():
    return isinstance(os.getenv(bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧᮑ")), str)
def bstack1l11111l1_opy_(url):
    return urlparse(url).hostname
def bstack1l11l111l1_opy_(hostname):
    for bstack11llll1l1l_opy_ in bstack11ll1l1111_opy_:
        regex = re.compile(bstack11llll1l1l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1lllll11_opy_(bstack11l11llll11_opy_, file_name, logger):
    bstack1lll11l11l_opy_ = os.path.join(os.path.expanduser(bstack11l1lll_opy_ (u"ࠩࢁࠫᮒ")), bstack11l11llll11_opy_)
    try:
        if not os.path.exists(bstack1lll11l11l_opy_):
            os.makedirs(bstack1lll11l11l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11l1lll_opy_ (u"ࠪࢂࠬᮓ")), bstack11l11llll11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11l1lll_opy_ (u"ࠫࡼ࠭ᮔ")):
                pass
            with open(file_path, bstack11l1lll_opy_ (u"ࠧࡽࠫࠣᮕ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11llll1ll_opy_.format(str(e)))
def bstack11l1l1ll11l_opy_(file_name, key, value, logger):
    file_path = bstack11l1lllll11_opy_(bstack11l1lll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᮖ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll1llll1_opy_ = json.load(open(file_path, bstack11l1lll_opy_ (u"ࠧࡳࡤࠪᮗ")))
        else:
            bstack1ll1llll1_opy_ = {}
        bstack1ll1llll1_opy_[key] = value
        with open(file_path, bstack11l1lll_opy_ (u"ࠣࡹ࠮ࠦᮘ")) as outfile:
            json.dump(bstack1ll1llll1_opy_, outfile)
def bstack1ll1l11l1_opy_(file_name, logger):
    file_path = bstack11l1lllll11_opy_(bstack11l1lll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᮙ"), file_name, logger)
    bstack1ll1llll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11l1lll_opy_ (u"ࠪࡶࠬᮚ")) as bstack1llllll1ll_opy_:
            bstack1ll1llll1_opy_ = json.load(bstack1llllll1ll_opy_)
    return bstack1ll1llll1_opy_
def bstack1ll11l1l1l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11l1lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡨ࡬ࡰࡪࡀࠠࠨᮛ") + file_path + bstack11l1lll_opy_ (u"ࠬࠦࠧᮜ") + str(e))
def bstack111111111_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11l1lll_opy_ (u"ࠨ࠼ࡏࡑࡗࡗࡊ࡚࠾ࠣᮝ")
def bstack11l1ll1l1l_opy_(config):
    if bstack11l1lll_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᮞ") in config:
        del (config[bstack11l1lll_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᮟ")])
        return False
    if bstack111111111_opy_() < version.parse(bstack11l1lll_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨᮠ")):
        return False
    if bstack111111111_opy_() >= version.parse(bstack11l1lll_opy_ (u"ࠪ࠸࠳࠷࠮࠶ࠩᮡ")):
        return True
    if bstack11l1lll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᮢ") in config and config[bstack11l1lll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᮣ")] is False:
        return False
    else:
        return True
def bstack1l1lll11_opy_(args_list, bstack11l1lll1lll_opy_):
    index = -1
    for value in bstack11l1lll1lll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11lll1lll1l_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11lll1lll1l_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111lll1l11_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111lll1l11_opy_ = bstack111lll1l11_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11l1lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᮤ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11l1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᮥ"), exception=exception)
    def bstack1111l111ll_opy_(self):
        if self.result != bstack11l1lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᮦ"):
            return None
        if isinstance(self.exception_type, str) and bstack11l1lll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᮧ") in self.exception_type:
            return bstack11l1lll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᮨ")
        return bstack11l1lll_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᮩ")
    def bstack11l1llllll1_opy_(self):
        if self.result != bstack11l1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨ᮪ࠬ"):
            return None
        if self.bstack111lll1l11_opy_:
            return self.bstack111lll1l11_opy_
        return bstack11l1llll1l1_opy_(self.exception)
def bstack11l1llll1l1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l11l11lll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack111l11lll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11l111ll1l_opy_(config, logger):
    try:
        import playwright
        bstack11l1l1ll1ll_opy_ = playwright.__file__
        bstack11l1l1ll111_opy_ = os.path.split(bstack11l1l1ll1ll_opy_)
        bstack11l1l11llll_opy_ = bstack11l1l1ll111_opy_[0] + bstack11l1lll_opy_ (u"࠭࠯ࡥࡴ࡬ࡺࡪࡸ࠯ࡱࡣࡦ࡯ࡦ࡭ࡥ࠰࡮࡬ࡦ࠴ࡩ࡬ࡪ࠱ࡦࡰ࡮࠴ࡪࡴ᮫ࠩ")
        os.environ[bstack11l1lll_opy_ (u"ࠧࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠪᮬ")] = bstack111ll1lll_opy_(config)
        with open(bstack11l1l11llll_opy_, bstack11l1lll_opy_ (u"ࠨࡴࠪᮭ")) as f:
            bstack1lll1lll11_opy_ = f.read()
            bstack11l1l1llll1_opy_ = bstack11l1lll_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨᮮ")
            bstack11l1ll1llll_opy_ = bstack1lll1lll11_opy_.find(bstack11l1l1llll1_opy_)
            if bstack11l1ll1llll_opy_ == -1:
              process = subprocess.Popen(bstack11l1lll_opy_ (u"ࠥࡲࡵࡳࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠢᮯ"), shell=True, cwd=bstack11l1l1ll111_opy_[0])
              process.wait()
              bstack11l1ll1l1l1_opy_ = bstack11l1lll_opy_ (u"ࠫࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵࠤ࠾ࠫ᮰")
              bstack11l1l11l1ll_opy_ = bstack11l1lll_opy_ (u"ࠧࠨࠢࠡ࡞ࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺ࡜ࠣ࠽ࠣࡧࡴࡴࡳࡵࠢࡾࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠠࡾࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ࠯࠻ࠡ࡫ࡩࠤ࠭ࡶࡲࡰࡥࡨࡷࡸ࠴ࡥ࡯ࡸ࠱ࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠯ࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠫ࠭ࡀࠦࠢࠣࠤ᮱")
              bstack11l1l1ll1l1_opy_ = bstack1lll1lll11_opy_.replace(bstack11l1ll1l1l1_opy_, bstack11l1l11l1ll_opy_)
              with open(bstack11l1l11llll_opy_, bstack11l1lll_opy_ (u"࠭ࡷࠨ᮲")) as f:
                f.write(bstack11l1l1ll1l1_opy_)
    except Exception as e:
        logger.error(bstack1l1l1l111l_opy_.format(str(e)))
def bstack111l11l11_opy_():
  try:
    bstack11l1ll1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1lll_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧ᮳"))
    bstack11l1l111ll1_opy_ = []
    if os.path.exists(bstack11l1ll1l11l_opy_):
      with open(bstack11l1ll1l11l_opy_) as f:
        bstack11l1l111ll1_opy_ = json.load(f)
      os.remove(bstack11l1ll1l11l_opy_)
    return bstack11l1l111ll1_opy_
  except:
    pass
  return []
def bstack11l1lll1l_opy_(bstack11llll1lll_opy_):
  try:
    bstack11l1l111ll1_opy_ = []
    bstack11l1ll1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1lll_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨ᮴"))
    if os.path.exists(bstack11l1ll1l11l_opy_):
      with open(bstack11l1ll1l11l_opy_) as f:
        bstack11l1l111ll1_opy_ = json.load(f)
    bstack11l1l111ll1_opy_.append(bstack11llll1lll_opy_)
    with open(bstack11l1ll1l11l_opy_, bstack11l1lll_opy_ (u"ࠩࡺࠫ᮵")) as f:
        json.dump(bstack11l1l111ll1_opy_, f)
  except:
    pass
def bstack1l1111ll_opy_(logger, bstack11l1l11l111_opy_ = False):
  try:
    test_name = os.environ.get(bstack11l1lll_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭᮶"), bstack11l1lll_opy_ (u"ࠫࠬ᮷"))
    if test_name == bstack11l1lll_opy_ (u"ࠬ࠭᮸"):
        test_name = threading.current_thread().__dict__.get(bstack11l1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡈࡤࡥࡡࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠬ᮹"), bstack11l1lll_opy_ (u"ࠧࠨᮺ"))
    bstack11l1l1l1l1l_opy_ = bstack11l1lll_opy_ (u"ࠨ࠮ࠣࠫᮻ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l1l11l111_opy_:
        bstack1llll11l1_opy_ = os.environ.get(bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᮼ"), bstack11l1lll_opy_ (u"ࠪ࠴ࠬᮽ"))
        bstack1l1111ll1l_opy_ = {bstack11l1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᮾ"): test_name, bstack11l1lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᮿ"): bstack11l1l1l1l1l_opy_, bstack11l1lll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᯀ"): bstack1llll11l1_opy_}
        bstack11l11ll1l11_opy_ = []
        bstack11l11l111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ᯁ"))
        if os.path.exists(bstack11l11l111l1_opy_):
            with open(bstack11l11l111l1_opy_) as f:
                bstack11l11ll1l11_opy_ = json.load(f)
        bstack11l11ll1l11_opy_.append(bstack1l1111ll1l_opy_)
        with open(bstack11l11l111l1_opy_, bstack11l1lll_opy_ (u"ࠨࡹࠪᯂ")) as f:
            json.dump(bstack11l11ll1l11_opy_, f)
    else:
        bstack1l1111ll1l_opy_ = {bstack11l1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᯃ"): test_name, bstack11l1lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᯄ"): bstack11l1l1l1l1l_opy_, bstack11l1lll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᯅ"): str(multiprocessing.current_process().name)}
        if bstack11l1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩᯆ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1111ll1l_opy_)
  except Exception as e:
      logger.warn(bstack11l1lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡲࡼࡸࡪࡹࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥᯇ").format(e))
def bstack1lll111ll_opy_(error_message, test_name, index, logger):
  try:
    bstack11l11l11ll1_opy_ = []
    bstack1l1111ll1l_opy_ = {bstack11l1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᯈ"): test_name, bstack11l1lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᯉ"): error_message, bstack11l1lll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᯊ"): index}
    bstack11ll1111111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫᯋ"))
    if os.path.exists(bstack11ll1111111_opy_):
        with open(bstack11ll1111111_opy_) as f:
            bstack11l11l11ll1_opy_ = json.load(f)
    bstack11l11l11ll1_opy_.append(bstack1l1111ll1l_opy_)
    with open(bstack11ll1111111_opy_, bstack11l1lll_opy_ (u"ࠫࡼ࠭ᯌ")) as f:
        json.dump(bstack11l11l11ll1_opy_, f)
  except Exception as e:
    logger.warn(bstack11l1lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡳࡱࡥࡳࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣᯍ").format(e))
def bstack11llll11ll_opy_(bstack1l1lll1l_opy_, name, logger):
  try:
    bstack1l1111ll1l_opy_ = {bstack11l1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᯎ"): name, bstack11l1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᯏ"): bstack1l1lll1l_opy_, bstack11l1lll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᯐ"): str(threading.current_thread()._name)}
    return bstack1l1111ll1l_opy_
  except Exception as e:
    logger.warn(bstack11l1lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡧ࡫ࡨࡢࡸࡨࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨᯑ").format(e))
  return
def bstack11l1l1l1ll1_opy_():
    return platform.system() == bstack11l1lll_opy_ (u"࡛ࠪ࡮ࡴࡤࡰࡹࡶࠫᯒ")
def bstack1ll11ll1l1_opy_(bstack11l11l1ll1l_opy_, config, logger):
    bstack11l1l11l11l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l11l1ll1l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11l1lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫࡯ࡸࡪࡸࠠࡤࡱࡱࡪ࡮࡭ࠠ࡬ࡧࡼࡷࠥࡨࡹࠡࡴࡨ࡫ࡪࡾࠠ࡮ࡣࡷࡧ࡭ࡀࠠࡼࡿࠥᯓ").format(e))
    return bstack11l1l11l11l_opy_
def bstack11l11l1l11l_opy_(bstack11l11l1l1ll_opy_, bstack11l1ll1ll1l_opy_):
    bstack11l1ll11ll1_opy_ = version.parse(bstack11l11l1l1ll_opy_)
    bstack11l1ll1l111_opy_ = version.parse(bstack11l1ll1ll1l_opy_)
    if bstack11l1ll11ll1_opy_ > bstack11l1ll1l111_opy_:
        return 1
    elif bstack11l1ll11ll1_opy_ < bstack11l1ll1l111_opy_:
        return -1
    else:
        return 0
def bstack111l1lllll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l11l1lll1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1l1111ll_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1lll1l11l1_opy_(options, framework, config, bstack1ll1111l11_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11l1lll_opy_ (u"ࠬ࡭ࡥࡵࠩᯔ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1ll11lll11_opy_ = caps.get(bstack11l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᯕ"))
    bstack11l1lll11ll_opy_ = True
    bstack1lllll111l_opy_ = os.environ[bstack11l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᯖ")]
    bstack1ll11l1ll11_opy_ = config.get(bstack11l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᯗ"), False)
    if bstack1ll11l1ll11_opy_:
        bstack1ll1lll1ll1_opy_ = config.get(bstack11l1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᯘ"), {})
        bstack1ll1lll1ll1_opy_[bstack11l1lll_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭ᯙ")] = os.getenv(bstack11l1lll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᯚ"))
        bstack11llll11l1l_opy_ = json.loads(os.getenv(bstack11l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᯛ"), bstack11l1lll_opy_ (u"࠭ࡻࡾࠩᯜ"))).get(bstack11l1lll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᯝ"))
    if bstack11l11l11l11_opy_(caps.get(bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨ࡛࠸ࡉࠧᯞ"))) or bstack11l11l11l11_opy_(caps.get(bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩᯟ"))):
        bstack11l1lll11ll_opy_ = False
    if bstack11l1ll1l1l_opy_({bstack11l1lll_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥᯠ"): bstack11l1lll11ll_opy_}):
        bstack1ll11lll11_opy_ = bstack1ll11lll11_opy_ or {}
        bstack1ll11lll11_opy_[bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᯡ")] = bstack11l1l1111ll_opy_(framework)
        bstack1ll11lll11_opy_[bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᯢ")] = bstack1l1ll1l1ll1_opy_()
        bstack1ll11lll11_opy_[bstack11l1lll_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᯣ")] = bstack1lllll111l_opy_
        bstack1ll11lll11_opy_[bstack11l1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᯤ")] = bstack1ll1111l11_opy_
        if bstack1ll11l1ll11_opy_:
            bstack1ll11lll11_opy_[bstack11l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᯥ")] = bstack1ll11l1ll11_opy_
            bstack1ll11lll11_opy_[bstack11l1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴ᯦ࠩ")] = bstack1ll1lll1ll1_opy_
            bstack1ll11lll11_opy_[bstack11l1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᯧ")][bstack11l1lll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᯨ")] = bstack11llll11l1l_opy_
        if getattr(options, bstack11l1lll_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ᯩ"), None):
            options.set_capability(bstack11l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᯪ"), bstack1ll11lll11_opy_)
        else:
            options[bstack11l1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᯫ")] = bstack1ll11lll11_opy_
    else:
        if getattr(options, bstack11l1lll_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩᯬ"), None):
            options.set_capability(bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᯭ"), bstack11l1l1111ll_opy_(framework))
            options.set_capability(bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᯮ"), bstack1l1ll1l1ll1_opy_())
            options.set_capability(bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᯯ"), bstack1lllll111l_opy_)
            options.set_capability(bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᯰ"), bstack1ll1111l11_opy_)
            if bstack1ll11l1ll11_opy_:
                options.set_capability(bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᯱ"), bstack1ll11l1ll11_opy_)
                options.set_capability(bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ᯲࠭"), bstack1ll1lll1ll1_opy_)
                options.set_capability(bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹ࠮ࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᯳"), bstack11llll11l1l_opy_)
        else:
            options[bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᯴")] = bstack11l1l1111ll_opy_(framework)
            options[bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᯵")] = bstack1l1ll1l1ll1_opy_()
            options[bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭᯶")] = bstack1lllll111l_opy_
            options[bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭᯷")] = bstack1ll1111l11_opy_
            if bstack1ll11l1ll11_opy_:
                options[bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᯸")] = bstack1ll11l1ll11_opy_
                options[bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᯹")] = bstack1ll1lll1ll1_opy_
                options[bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ᯺")][bstack11l1lll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᯻")] = bstack11llll11l1l_opy_
    return options
def bstack11l1l11111l_opy_(bstack11l11ll1ll1_opy_, framework):
    bstack1ll1111l11_opy_ = bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"ࠥࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡑࡔࡒࡈ࡚ࡉࡔࡠࡏࡄࡔࠧ᯼"))
    if bstack11l11ll1ll1_opy_ and len(bstack11l11ll1ll1_opy_.split(bstack11l1lll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ᯽"))) > 1:
        ws_url = bstack11l11ll1ll1_opy_.split(bstack11l1lll_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ᯾"))[0]
        if bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ᯿") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l1ll11l11_opy_ = json.loads(urllib.parse.unquote(bstack11l11ll1ll1_opy_.split(bstack11l1lll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᰀ"))[1]))
            bstack11l1ll11l11_opy_ = bstack11l1ll11l11_opy_ or {}
            bstack1lllll111l_opy_ = os.environ[bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᰁ")]
            bstack11l1ll11l11_opy_[bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᰂ")] = str(framework) + str(__version__)
            bstack11l1ll11l11_opy_[bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᰃ")] = bstack1l1ll1l1ll1_opy_()
            bstack11l1ll11l11_opy_[bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᰄ")] = bstack1lllll111l_opy_
            bstack11l1ll11l11_opy_[bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᰅ")] = bstack1ll1111l11_opy_
            bstack11l11ll1ll1_opy_ = bstack11l11ll1ll1_opy_.split(bstack11l1lll_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᰆ"))[0] + bstack11l1lll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᰇ") + urllib.parse.quote(json.dumps(bstack11l1ll11l11_opy_))
    return bstack11l11ll1ll1_opy_
def bstack1l1l11ll1_opy_():
    global bstack1lll1l11_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1lll1l11_opy_ = BrowserType.connect
    return bstack1lll1l11_opy_
def bstack11ll1l1l1l_opy_(framework_name):
    global bstack1l11l1l11l_opy_
    bstack1l11l1l11l_opy_ = framework_name
    return framework_name
def bstack1lllll11ll_opy_(self, *args, **kwargs):
    global bstack1lll1l11_opy_
    try:
        global bstack1l11l1l11l_opy_
        if bstack11l1lll_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᰈ") in kwargs:
            kwargs[bstack11l1lll_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᰉ")] = bstack11l1l11111l_opy_(
                kwargs.get(bstack11l1lll_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧᰊ"), None),
                bstack1l11l1l11l_opy_
            )
    except Exception as e:
        logger.error(bstack11l1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦᰋ").format(str(e)))
    return bstack1lll1l11_opy_(self, *args, **kwargs)
def bstack11l1llll11l_opy_(bstack11l11ll11ll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1ll111l1_opy_(bstack11l11ll11ll_opy_, bstack11l1lll_opy_ (u"ࠧࠨᰌ"))
        if proxies and proxies.get(bstack11l1lll_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᰍ")):
            parsed_url = urlparse(proxies.get(bstack11l1lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᰎ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11l1lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫᰏ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11l1lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬᰐ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11l1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᰑ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11l1lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᰒ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l111111l1_opy_(bstack11l11ll11ll_opy_):
    bstack11l1lllllll_opy_ = {
        bstack11ll1l11111_opy_[bstack11l1l11lll1_opy_]: bstack11l11ll11ll_opy_[bstack11l1l11lll1_opy_]
        for bstack11l1l11lll1_opy_ in bstack11l11ll11ll_opy_
        if bstack11l1l11lll1_opy_ in bstack11ll1l11111_opy_
    }
    bstack11l1lllllll_opy_[bstack11l1lll_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᰓ")] = bstack11l1llll11l_opy_(bstack11l11ll11ll_opy_, bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨᰔ")))
    bstack11l1l1lllll_opy_ = [element.lower() for element in bstack11ll11l111l_opy_]
    bstack11l1l111l11_opy_(bstack11l1lllllll_opy_, bstack11l1l1lllll_opy_)
    return bstack11l1lllllll_opy_
def bstack11l1l111l11_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11l1lll_opy_ (u"ࠢࠫࠬ࠭࠮ࠧᰕ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11l1l111l11_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11l1l111l11_opy_(item, keys)
def bstack1ll11111l1l_opy_():
    bstack11l11ll111l_opy_ = [os.environ.get(bstack11l1lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡋࡏࡉࡘࡥࡄࡊࡔࠥᰖ")), os.path.join(os.path.expanduser(bstack11l1lll_opy_ (u"ࠤࢁࠦᰗ")), bstack11l1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᰘ")), os.path.join(bstack11l1lll_opy_ (u"ࠫ࠴ࡺ࡭ࡱࠩᰙ"), bstack11l1lll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᰚ"))]
    for path in bstack11l11ll111l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11l1lll_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࠬࠨᰛ") + str(path) + bstack11l1lll_opy_ (u"ࠢࠨࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠥᰜ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11l1lll_opy_ (u"ࠣࡉ࡬ࡺ࡮ࡴࡧࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸࠦࡦࡰࡴࠣࠫࠧᰝ") + str(path) + bstack11l1lll_opy_ (u"ࠤࠪࠦᰞ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11l1lll_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥᰟ") + str(path) + bstack11l1lll_opy_ (u"ࠦࠬࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡩࡣࡶࠤࡹ࡮ࡥࠡࡴࡨࡵࡺ࡯ࡲࡦࡦࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳ࠯ࠤᰠ"))
            else:
                logger.debug(bstack11l1lll_opy_ (u"ࠧࡉࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩࠥ࠭ࠢᰡ") + str(path) + bstack11l1lll_opy_ (u"ࠨࠧࠡࡹ࡬ࡸ࡭ࠦࡷࡳ࡫ࡷࡩࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯࠰ࠥᰢ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11l1lll_opy_ (u"ࠢࡐࡲࡨࡶࡦࡺࡩࡰࡰࠣࡷࡺࡩࡣࡦࡧࡧࡩࡩࠦࡦࡰࡴࠣࠫࠧᰣ") + str(path) + bstack11l1lll_opy_ (u"ࠣࠩ࠱ࠦᰤ"))
            return path
        except Exception as e:
            logger.debug(bstack11l1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡸࡴࠥ࡬ࡩ࡭ࡧࠣࠫࢀࡶࡡࡵࡪࢀࠫ࠿ࠦࠢᰥ") + str(e) + bstack11l1lll_opy_ (u"ࠥࠦᰦ"))
    logger.debug(bstack11l1lll_opy_ (u"ࠦࡆࡲ࡬ࠡࡲࡤࡸ࡭ࡹࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠣᰧ"))
    return None
@measure(event_name=EVENTS.bstack11ll111l1l1_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
def bstack1lllll111l1_opy_(binary_path, bstack1llll1llll1_opy_, bs_config):
    logger.debug(bstack11l1lll_opy_ (u"ࠧࡉࡵࡳࡴࡨࡲࡹࠦࡃࡍࡋࠣࡔࡦࡺࡨࠡࡨࡲࡹࡳࡪ࠺ࠡࡽࢀࠦᰨ").format(binary_path))
    bstack11l11l1l111_opy_ = bstack11l1lll_opy_ (u"࠭ࠧᰩ")
    bstack11l11l1l1l1_opy_ = {
        bstack11l1lll_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᰪ"): __version__,
        bstack11l1lll_opy_ (u"ࠣࡱࡶࠦᰫ"): platform.system(),
        bstack11l1lll_opy_ (u"ࠤࡲࡷࡤࡧࡲࡤࡪࠥᰬ"): platform.machine(),
        bstack11l1lll_opy_ (u"ࠥࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᰭ"): bstack11l1lll_opy_ (u"ࠫ࠵࠭ᰮ"),
        bstack11l1lll_opy_ (u"ࠧࡹࡤ࡬ࡡ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠦᰯ"): bstack11l1lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᰰ")
    }
    bstack11l1l1111l1_opy_(bstack11l11l1l1l1_opy_)
    try:
        if binary_path:
            bstack11l11l1l1l1_opy_[bstack11l1lll_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᰱ")] = subprocess.check_output([binary_path, bstack11l1lll_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤᰲ")]).strip().decode(bstack11l1lll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᰳ"))
        response = requests.request(
            bstack11l1lll_opy_ (u"ࠪࡋࡊ࡚ࠧᰴ"),
            url=bstack1ll1ll11_opy_(bstack11ll11l1ll1_opy_),
            headers=None,
            auth=(bs_config[bstack11l1lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᰵ")], bs_config[bstack11l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᰶ")]),
            json=None,
            params=bstack11l11l1l1l1_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11l1lll_opy_ (u"࠭ࡵࡳ࡮᰷ࠪ") in data.keys() and bstack11l1lll_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡠࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᰸") in data.keys():
            logger.debug(bstack11l1lll_opy_ (u"ࠣࡐࡨࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡥ࡭ࡳࡧࡲࡺ࠮ࠣࡧࡺࡸࡲࡦࡰࡷࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠤ᰹").format(bstack11l11l1l1l1_opy_[bstack11l1lll_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ᰺")]))
            if bstack11l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑ࠭᰻") in os.environ:
                logger.debug(bstack11l1lll_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡢࡪࡰࡤࡶࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡣࡶࠤࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡗࡉࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠤ࡮ࡹࠠࡴࡧࡷࠦ᰼"))
                data[bstack11l1lll_opy_ (u"ࠬࡻࡲ࡭ࠩ᰽")] = os.environ[bstack11l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠩ᰾")]
            bstack11l1ll1l1ll_opy_ = bstack11l11llllll_opy_(data[bstack11l1lll_opy_ (u"ࠧࡶࡴ࡯ࠫ᰿")], bstack1llll1llll1_opy_)
            bstack11l11l1l111_opy_ = os.path.join(bstack1llll1llll1_opy_, bstack11l1ll1l1ll_opy_)
            os.chmod(bstack11l11l1l111_opy_, 0o777) # bstack11l11lll111_opy_ permission
            return bstack11l11l1l111_opy_
    except Exception as e:
        logger.debug(bstack11l1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡳ࡫ࡷࠡࡕࡇࡏࠥࢁࡽࠣ᱀").format(e))
    return binary_path
def bstack11l1l1111l1_opy_(bstack11l11l1l1l1_opy_):
    try:
        if bstack11l1lll_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨ᱁") not in bstack11l11l1l1l1_opy_[bstack11l1lll_opy_ (u"ࠪࡳࡸ࠭᱂")].lower():
            return
        if os.path.exists(bstack11l1lll_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡲࡷ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨ᱃")):
            with open(bstack11l1lll_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡳࡸ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢ᱄"), bstack11l1lll_opy_ (u"ࠨࡲࠣ᱅")) as f:
                bstack11l11l11111_opy_ = {}
                for line in f:
                    if bstack11l1lll_opy_ (u"ࠢ࠾ࠤ᱆") in line:
                        key, value = line.rstrip().split(bstack11l1lll_opy_ (u"ࠣ࠿ࠥ᱇"), 1)
                        bstack11l11l11111_opy_[key] = value.strip(bstack11l1lll_opy_ (u"ࠩࠥࡠࠬ࠭᱈"))
                bstack11l11l1l1l1_opy_[bstack11l1lll_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱࠪ᱉")] = bstack11l11l11111_opy_.get(bstack11l1lll_opy_ (u"ࠦࡎࡊࠢ᱊"), bstack11l1lll_opy_ (u"ࠧࠨ᱋"))
        elif os.path.exists(bstack11l1lll_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡦࡲࡰࡪࡰࡨ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧ᱌")):
            bstack11l11l1l1l1_opy_[bstack11l1lll_opy_ (u"ࠧࡥ࡫ࡶࡸࡷࡵࠧᱍ")] = bstack11l1lll_opy_ (u"ࠨࡣ࡯ࡴ࡮ࡴࡥࠨᱎ")
    except Exception as e:
        logger.debug(bstack11l1lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡧ࡭ࡸࡺࡲࡰࠢࡲࡪࠥࡲࡩ࡯ࡷࡻࠦᱏ") + e)
@measure(event_name=EVENTS.bstack11ll11ll11l_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
def bstack11l11llllll_opy_(bstack11l1l1l11l1_opy_, bstack11l1l1lll1l_opy_):
    logger.debug(bstack11l1lll_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯࠽ࠤࠧ᱐") + str(bstack11l1l1l11l1_opy_) + bstack11l1lll_opy_ (u"ࠦࠧ᱑"))
    zip_path = os.path.join(bstack11l1l1lll1l_opy_, bstack11l1lll_opy_ (u"ࠧࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࡡࡩ࡭ࡱ࡫࠮ࡻ࡫ࡳࠦ᱒"))
    bstack11l1ll1l1ll_opy_ = bstack11l1lll_opy_ (u"࠭ࠧ᱓")
    with requests.get(bstack11l1l1l11l1_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11l1lll_opy_ (u"ࠢࡸࡤࠥ᱔")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11l1lll_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺ࠰ࠥ᱕"))
    with zipfile.ZipFile(zip_path, bstack11l1lll_opy_ (u"ࠩࡵࠫ᱖")) as zip_ref:
        bstack11l1lll111l_opy_ = zip_ref.namelist()
        if len(bstack11l1lll111l_opy_) > 0:
            bstack11l1ll1l1ll_opy_ = bstack11l1lll111l_opy_[0] # bstack11l1l1l11ll_opy_ bstack11ll11l1l11_opy_ will be bstack11l111lllll_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l1l1lll1l_opy_)
        logger.debug(bstack11l1lll_opy_ (u"ࠥࡊ࡮ࡲࡥࡴࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡧࡻࡸࡷࡧࡣࡵࡧࡧࠤࡹࡵࠠࠨࠤ᱗") + str(bstack11l1l1lll1l_opy_) + bstack11l1lll_opy_ (u"ࠦࠬࠨ᱘"))
    os.remove(zip_path)
    return bstack11l1ll1l1ll_opy_
def get_cli_dir():
    bstack11l11ll1l1l_opy_ = bstack1ll11111l1l_opy_()
    if bstack11l11ll1l1l_opy_:
        bstack1llll1llll1_opy_ = os.path.join(bstack11l11ll1l1l_opy_, bstack11l1lll_opy_ (u"ࠧࡩ࡬ࡪࠤ᱙"))
        if not os.path.exists(bstack1llll1llll1_opy_):
            os.makedirs(bstack1llll1llll1_opy_, mode=0o777, exist_ok=True)
        return bstack1llll1llll1_opy_
    else:
        raise FileNotFoundError(bstack11l1lll_opy_ (u"ࠨࡎࡰࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡪࡴࡸࠠࡵࡪࡨࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹ࠯ࠤᱚ"))
def bstack1lll11l1ll1_opy_(bstack1llll1llll1_opy_):
    bstack11l1lll_opy_ (u"ࠢࠣࠤࡊࡩࡹࠦࡴࡩࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯࡮ࠡࡣࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠯ࠤࠥࠦᱛ")
    bstack11l11l11l1l_opy_ = [
        os.path.join(bstack1llll1llll1_opy_, f)
        for f in os.listdir(bstack1llll1llll1_opy_)
        if os.path.isfile(os.path.join(bstack1llll1llll1_opy_, f)) and f.startswith(bstack11l1lll_opy_ (u"ࠣࡤ࡬ࡲࡦࡸࡹ࠮ࠤᱜ"))
    ]
    if len(bstack11l11l11l1l_opy_) > 0:
        return max(bstack11l11l11l1l_opy_, key=os.path.getmtime) # get bstack11l1ll111l1_opy_ binary
    return bstack11l1lll_opy_ (u"ࠤࠥᱝ")
def bstack11llll11l11_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll1l1l111l_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll1l1l111l_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d