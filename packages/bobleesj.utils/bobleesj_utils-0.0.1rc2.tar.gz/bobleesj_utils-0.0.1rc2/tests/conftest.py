import pytest

from bobleesj.utils.sources.oliynyk import Oliynyk


@pytest.fixture
def oliynyk() -> Oliynyk:
    # 20250516 - deleted Tc, Pm and Hg since some properties are not available
    return Oliynyk()
