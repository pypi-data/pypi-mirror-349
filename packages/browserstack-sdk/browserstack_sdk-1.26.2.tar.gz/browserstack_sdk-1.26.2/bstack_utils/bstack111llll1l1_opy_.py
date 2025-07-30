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
from uuid import uuid4
from bstack_utils.helper import bstack11l11ll11l_opy_, bstack11l11l1ll1l_opy_
from bstack_utils.bstack1l1l1111ll_opy_ import bstack111l1111111_opy_
class bstack1111llllll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1111l1lll11_opy_=None, bstack1111ll111ll_opy_=True, bstack1l111l1l111_opy_=None, bstack1111l1l1_opy_=None, result=None, duration=None, bstack111l111111_opy_=None, meta={}):
        self.bstack111l111111_opy_ = bstack111l111111_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1111ll111ll_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1111l1lll11_opy_ = bstack1111l1lll11_opy_
        self.bstack1l111l1l111_opy_ = bstack1l111l1l111_opy_
        self.bstack1111l1l1_opy_ = bstack1111l1l1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l1lllll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111lllll1l_opy_(self, meta):
        self.meta = meta
    def bstack11l11111ll_opy_(self, hooks):
        self.hooks = hooks
    def bstack1111l1l1l11_opy_(self):
        bstack1111l1ll11l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack111l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ṫ"): bstack1111l1ll11l_opy_,
            bstack111l11_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭Ṭ"): bstack1111l1ll11l_opy_,
            bstack111l11_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪṭ"): bstack1111l1ll11l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack111l11_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠿ࠦࠢṮ") + key)
            setattr(self, key, val)
    def bstack1111ll11111_opy_(self):
        return {
            bstack111l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬṯ"): self.name,
            bstack111l11_opy_ (u"ࠨࡤࡲࡨࡾ࠭Ṱ"): {
                bstack111l11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧṱ"): bstack111l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪṲ"),
                bstack111l11_opy_ (u"ࠫࡨࡵࡤࡦࠩṳ"): self.code
            },
            bstack111l11_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬṴ"): self.scope,
            bstack111l11_opy_ (u"࠭ࡴࡢࡩࡶࠫṵ"): self.tags,
            bstack111l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪṶ"): self.framework,
            bstack111l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬṷ"): self.started_at
        }
    def bstack1111l1ll1ll_opy_(self):
        return {
         bstack111l11_opy_ (u"ࠩࡰࡩࡹࡧࠧṸ"): self.meta
        }
    def bstack1111l1l1lll_opy_(self):
        return {
            bstack111l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ṹ"): {
                bstack111l11_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨṺ"): self.bstack1111l1lll11_opy_
            }
        }
    def bstack1111l1ll111_opy_(self, bstack1111l1l1ll1_opy_, details):
        step = next(filter(lambda st: st[bstack111l11_opy_ (u"ࠬ࡯ࡤࠨṻ")] == bstack1111l1l1ll1_opy_, self.meta[bstack111l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬṼ")]), None)
        step.update(details)
    def bstack1l1lll1l1l_opy_(self, bstack1111l1l1ll1_opy_):
        step = next(filter(lambda st: st[bstack111l11_opy_ (u"ࠧࡪࡦࠪṽ")] == bstack1111l1l1ll1_opy_, self.meta[bstack111l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧṾ")]), None)
        step.update({
            bstack111l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ṿ"): bstack11l11ll11l_opy_()
        })
    def bstack111lll1lll_opy_(self, bstack1111l1l1ll1_opy_, result, duration=None):
        bstack1l111l1l111_opy_ = bstack11l11ll11l_opy_()
        if bstack1111l1l1ll1_opy_ is not None and self.meta.get(bstack111l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩẀ")):
            step = next(filter(lambda st: st[bstack111l11_opy_ (u"ࠫ࡮ࡪࠧẁ")] == bstack1111l1l1ll1_opy_, self.meta[bstack111l11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫẂ")]), None)
            step.update({
                bstack111l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫẃ"): bstack1l111l1l111_opy_,
                bstack111l11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩẄ"): duration if duration else bstack11l11l1ll1l_opy_(step[bstack111l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬẅ")], bstack1l111l1l111_opy_),
                bstack111l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩẆ"): result.result,
                bstack111l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫẇ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1111l1ll1l1_opy_):
        if self.meta.get(bstack111l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪẈ")):
            self.meta[bstack111l11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫẉ")].append(bstack1111l1ll1l1_opy_)
        else:
            self.meta[bstack111l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬẊ")] = [ bstack1111l1ll1l1_opy_ ]
    def bstack1111ll11l11_opy_(self):
        return {
            bstack111l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬẋ"): self.bstack111l1lllll_opy_(),
            **self.bstack1111ll11111_opy_(),
            **self.bstack1111l1l1l11_opy_(),
            **self.bstack1111l1ll1ll_opy_()
        }
    def bstack1111l1l11ll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack111l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭Ẍ"): self.bstack1l111l1l111_opy_,
            bstack111l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪẍ"): self.duration,
            bstack111l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪẎ"): self.result.result
        }
        if data[bstack111l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫẏ")] == bstack111l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬẐ"):
            data[bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬẑ")] = self.result.bstack1111l11ll1_opy_()
            data[bstack111l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨẒ")] = [{bstack111l11_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫẓ"): self.result.bstack11l11llll1l_opy_()}]
        return data
    def bstack1111l1llll1_opy_(self):
        return {
            bstack111l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧẔ"): self.bstack111l1lllll_opy_(),
            **self.bstack1111ll11111_opy_(),
            **self.bstack1111l1l1l11_opy_(),
            **self.bstack1111l1l11ll_opy_(),
            **self.bstack1111l1ll1ll_opy_()
        }
    def bstack111l11lll1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack111l11_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫẕ") in event:
            return self.bstack1111ll11l11_opy_()
        elif bstack111l11_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ẖ") in event:
            return self.bstack1111l1llll1_opy_()
    def bstack1111lllll1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l111l1l111_opy_ = time if time else bstack11l11ll11l_opy_()
        self.duration = duration if duration else bstack11l11l1ll1l_opy_(self.started_at, self.bstack1l111l1l111_opy_)
        if result:
            self.result = result
class bstack111lll1l11_opy_(bstack1111llllll_opy_):
    def __init__(self, hooks=[], bstack111lll111l_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111lll111l_opy_ = bstack111lll111l_opy_
        super().__init__(*args, **kwargs, bstack1111l1l1_opy_=bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࠪẗ"))
    @classmethod
    def bstack1111ll1111l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111l11_opy_ (u"࠭ࡩࡥࠩẘ"): id(step),
                bstack111l11_opy_ (u"ࠧࡵࡧࡻࡸࠬẙ"): step.name,
                bstack111l11_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩẚ"): step.keyword,
            })
        return bstack111lll1l11_opy_(
            **kwargs,
            meta={
                bstack111l11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪẛ"): {
                    bstack111l11_opy_ (u"ࠪࡲࡦࡳࡥࠨẜ"): feature.name,
                    bstack111l11_opy_ (u"ࠫࡵࡧࡴࡩࠩẝ"): feature.filename,
                    bstack111l11_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪẞ"): feature.description
                },
                bstack111l11_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨẟ"): {
                    bstack111l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬẠ"): scenario.name
                },
                bstack111l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧạ"): steps,
                bstack111l11_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫẢ"): bstack111l1111111_opy_(test)
            }
        )
    def bstack1111l1l1l1l_opy_(self):
        return {
            bstack111l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩả"): self.hooks
        }
    def bstack1111ll111l1_opy_(self):
        if self.bstack111lll111l_opy_:
            return {
                bstack111l11_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪẤ"): self.bstack111lll111l_opy_
            }
        return {}
    def bstack1111l1llll1_opy_(self):
        return {
            **super().bstack1111l1llll1_opy_(),
            **self.bstack1111l1l1l1l_opy_()
        }
    def bstack1111ll11l11_opy_(self):
        return {
            **super().bstack1111ll11l11_opy_(),
            **self.bstack1111ll111l1_opy_()
        }
    def bstack1111lllll1_opy_(self):
        return bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧấ")
class bstack111lll1ll1_opy_(bstack1111llllll_opy_):
    def __init__(self, hook_type, *args,bstack111lll111l_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1111l1lllll_opy_ = None
        self.bstack111lll111l_opy_ = bstack111lll111l_opy_
        super().__init__(*args, **kwargs, bstack1111l1l1_opy_=bstack111l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫẦ"))
    def bstack111ll11111_opy_(self):
        return self.hook_type
    def bstack1111l1lll1l_opy_(self):
        return {
            bstack111l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪầ"): self.hook_type
        }
    def bstack1111l1llll1_opy_(self):
        return {
            **super().bstack1111l1llll1_opy_(),
            **self.bstack1111l1lll1l_opy_()
        }
    def bstack1111ll11l11_opy_(self):
        return {
            **super().bstack1111ll11l11_opy_(),
            bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭Ẩ"): self.bstack1111l1lllll_opy_,
            **self.bstack1111l1lll1l_opy_()
        }
    def bstack1111lllll1_opy_(self):
        return bstack111l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫẩ")
    def bstack11l1111l1l_opy_(self, bstack1111l1lllll_opy_):
        self.bstack1111l1lllll_opy_ = bstack1111l1lllll_opy_