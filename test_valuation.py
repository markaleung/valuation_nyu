from classes import manager

def test_valuation():
    manager_ = manager.Manager()
    manager_.main()
    price = manager_.final.share_price
    assert round(price) == 130, price