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
import os
from uuid import uuid4
from bstack_utils.helper import bstack1lll11l11_opy_, bstack11l11lll11l_opy_
from bstack_utils.bstack1llll11l1l_opy_ import bstack111l1111lll_opy_
class bstack111ll111l1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1111l1lll11_opy_=None, bstack1111ll11111_opy_=True, bstack1l11l1l1111_opy_=None, bstack1lll1ll1l_opy_=None, result=None, duration=None, bstack111l1l1l1l_opy_=None, meta={}):
        self.bstack111l1l1l1l_opy_ = bstack111l1l1l1l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1111ll11111_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1111l1lll11_opy_ = bstack1111l1lll11_opy_
        self.bstack1l11l1l1111_opy_ = bstack1l11l1l1111_opy_
        self.bstack1lll1ll1l_opy_ = bstack1lll1ll1l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l1l1111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111ll1ll1l_opy_(self, meta):
        self.meta = meta
    def bstack111lll1ll1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1111l1ll111_opy_(self):
        bstack1111ll11l11_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11l1lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩṠ"): bstack1111ll11l11_opy_,
            bstack11l1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩṡ"): bstack1111ll11l11_opy_,
            bstack11l1lll_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭Ṣ"): bstack1111ll11l11_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11l1lll_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥṣ") + key)
            setattr(self, key, val)
    def bstack1111l1ll11l_opy_(self):
        return {
            bstack11l1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨṤ"): self.name,
            bstack11l1lll_opy_ (u"ࠫࡧࡵࡤࡺࠩṥ"): {
                bstack11l1lll_opy_ (u"ࠬࡲࡡ࡯ࡩࠪṦ"): bstack11l1lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ṧ"),
                bstack11l1lll_opy_ (u"ࠧࡤࡱࡧࡩࠬṨ"): self.code
            },
            bstack11l1lll_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨṩ"): self.scope,
            bstack11l1lll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧṪ"): self.tags,
            bstack11l1lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ṫ"): self.framework,
            bstack11l1lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨṬ"): self.started_at
        }
    def bstack1111l1lllll_opy_(self):
        return {
         bstack11l1lll_opy_ (u"ࠬࡳࡥࡵࡣࠪṭ"): self.meta
        }
    def bstack1111l1ll1l1_opy_(self):
        return {
            bstack11l1lll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩṮ"): {
                bstack11l1lll_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫṯ"): self.bstack1111l1lll11_opy_
            }
        }
    def bstack1111ll1111l_opy_(self, bstack1111ll11l1l_opy_, details):
        step = next(filter(lambda st: st[bstack11l1lll_opy_ (u"ࠨ࡫ࡧࠫṰ")] == bstack1111ll11l1l_opy_, self.meta[bstack11l1lll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨṱ")]), None)
        step.update(details)
    def bstack1111ll1l1_opy_(self, bstack1111ll11l1l_opy_):
        step = next(filter(lambda st: st[bstack11l1lll_opy_ (u"ࠪ࡭ࡩ࠭Ṳ")] == bstack1111ll11l1l_opy_, self.meta[bstack11l1lll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪṳ")]), None)
        step.update({
            bstack11l1lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩṴ"): bstack1lll11l11_opy_()
        })
    def bstack11l1111l11_opy_(self, bstack1111ll11l1l_opy_, result, duration=None):
        bstack1l11l1l1111_opy_ = bstack1lll11l11_opy_()
        if bstack1111ll11l1l_opy_ is not None and self.meta.get(bstack11l1lll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬṵ")):
            step = next(filter(lambda st: st[bstack11l1lll_opy_ (u"ࠧࡪࡦࠪṶ")] == bstack1111ll11l1l_opy_, self.meta[bstack11l1lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧṷ")]), None)
            step.update({
                bstack11l1lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧṸ"): bstack1l11l1l1111_opy_,
                bstack11l1lll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬṹ"): duration if duration else bstack11l11lll11l_opy_(step[bstack11l1lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨṺ")], bstack1l11l1l1111_opy_),
                bstack11l1lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬṻ"): result.result,
                bstack11l1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧṼ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1111ll111l1_opy_):
        if self.meta.get(bstack11l1lll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ṽ")):
            self.meta[bstack11l1lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧṾ")].append(bstack1111ll111l1_opy_)
        else:
            self.meta[bstack11l1lll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨṿ")] = [ bstack1111ll111l1_opy_ ]
    def bstack1111ll11ll1_opy_(self):
        return {
            bstack11l1lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨẀ"): self.bstack111l1l1111_opy_(),
            **self.bstack1111l1ll11l_opy_(),
            **self.bstack1111l1ll111_opy_(),
            **self.bstack1111l1lllll_opy_()
        }
    def bstack1111l1lll1l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11l1lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩẁ"): self.bstack1l11l1l1111_opy_,
            bstack11l1lll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭Ẃ"): self.duration,
            bstack11l1lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ẃ"): self.result.result
        }
        if data[bstack11l1lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧẄ")] == bstack11l1lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨẅ"):
            data[bstack11l1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨẆ")] = self.result.bstack1111l111ll_opy_()
            data[bstack11l1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫẇ")] = [{bstack11l1lll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧẈ"): self.result.bstack11l1llllll1_opy_()}]
        return data
    def bstack1111l1l1lll_opy_(self):
        return {
            bstack11l1lll_opy_ (u"ࠬࡻࡵࡪࡦࠪẉ"): self.bstack111l1l1111_opy_(),
            **self.bstack1111l1ll11l_opy_(),
            **self.bstack1111l1ll111_opy_(),
            **self.bstack1111l1lll1l_opy_(),
            **self.bstack1111l1lllll_opy_()
        }
    def bstack111l1ll1l1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11l1lll_opy_ (u"࠭ࡓࡵࡣࡵࡸࡪࡪࠧẊ") in event:
            return self.bstack1111ll11ll1_opy_()
        elif bstack11l1lll_opy_ (u"ࠧࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩẋ") in event:
            return self.bstack1111l1l1lll_opy_()
    def bstack111l1l1lll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l11l1l1111_opy_ = time if time else bstack1lll11l11_opy_()
        self.duration = duration if duration else bstack11l11lll11l_opy_(self.started_at, self.bstack1l11l1l1111_opy_)
        if result:
            self.result = result
class bstack111llllll1_opy_(bstack111ll111l1_opy_):
    def __init__(self, hooks=[], bstack111lllllll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111lllllll_opy_ = bstack111lllllll_opy_
        super().__init__(*args, **kwargs, bstack1lll1ll1l_opy_=bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹ࠭Ẍ"))
    @classmethod
    def bstack1111ll111ll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l1lll_opy_ (u"ࠩ࡬ࡨࠬẍ"): id(step),
                bstack11l1lll_opy_ (u"ࠪࡸࡪࡾࡴࠨẎ"): step.name,
                bstack11l1lll_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬẏ"): step.keyword,
            })
        return bstack111llllll1_opy_(
            **kwargs,
            meta={
                bstack11l1lll_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭Ẑ"): {
                    bstack11l1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫẑ"): feature.name,
                    bstack11l1lll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬẒ"): feature.filename,
                    bstack11l1lll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ẓ"): feature.description
                },
                bstack11l1lll_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫẔ"): {
                    bstack11l1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨẕ"): scenario.name
                },
                bstack11l1lll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪẖ"): steps,
                bstack11l1lll_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧẗ"): bstack111l1111lll_opy_(test)
            }
        )
    def bstack1111l1ll1ll_opy_(self):
        return {
            bstack11l1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬẘ"): self.hooks
        }
    def bstack1111ll11lll_opy_(self):
        if self.bstack111lllllll_opy_:
            return {
                bstack11l1lll_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ẙ"): self.bstack111lllllll_opy_
            }
        return {}
    def bstack1111l1l1lll_opy_(self):
        return {
            **super().bstack1111l1l1lll_opy_(),
            **self.bstack1111l1ll1ll_opy_()
        }
    def bstack1111ll11ll1_opy_(self):
        return {
            **super().bstack1111ll11ll1_opy_(),
            **self.bstack1111ll11lll_opy_()
        }
    def bstack111l1l1lll_opy_(self):
        return bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪẚ")
class bstack111ll1llll_opy_(bstack111ll111l1_opy_):
    def __init__(self, hook_type, *args,bstack111lllllll_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1111ll1l111_opy_ = None
        self.bstack111lllllll_opy_ = bstack111lllllll_opy_
        super().__init__(*args, **kwargs, bstack1lll1ll1l_opy_=bstack11l1lll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧẛ"))
    def bstack111ll111ll_opy_(self):
        return self.hook_type
    def bstack1111l1llll1_opy_(self):
        return {
            bstack11l1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ẜ"): self.hook_type
        }
    def bstack1111l1l1lll_opy_(self):
        return {
            **super().bstack1111l1l1lll_opy_(),
            **self.bstack1111l1llll1_opy_()
        }
    def bstack1111ll11ll1_opy_(self):
        return {
            **super().bstack1111ll11ll1_opy_(),
            bstack11l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩẝ"): self.bstack1111ll1l111_opy_,
            **self.bstack1111l1llll1_opy_()
        }
    def bstack111l1l1lll_opy_(self):
        return bstack11l1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧẞ")
    def bstack111lll1l1l_opy_(self, bstack1111ll1l111_opy_):
        self.bstack1111ll1l111_opy_ = bstack1111ll1l111_opy_