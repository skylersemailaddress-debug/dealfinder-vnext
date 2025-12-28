from app.services.pricing_service import _aggregate
from app.models import PriceObs

def test_aggregate_median():
    obs = [
        PriceObs(provider="x", title="a", url="u", item_price=10, shipping=0, all_in=10),
        PriceObs(provider="x", title="b", url="u", item_price=20, shipping=0, all_in=20),
        PriceObs(provider="x", title="c", url="u", item_price=30, shipping=0, all_in=30),
    ]
    med, lo, hi, conf = _aggregate(obs)
    assert med == 20.0
    assert lo <= med <= hi
    assert 0.0 <= conf <= 1.0
