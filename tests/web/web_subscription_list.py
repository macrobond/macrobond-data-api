from datetime import datetime, timezone

from macrobond_data_api.web import WebApi


def test_subscription_list(web: WebApi) -> None:
    subscription_list = web.subscription_list(datetime.now(timezone.utc))

    subscription_list.set(["sek", "nok"])
    assert set(subscription_list.list()) == {"sek", "nok"}

    subscription_list.add(["dkk"])
    assert set(subscription_list.list()) == {"sek", "nok", "dkk"}

    subscription_list.remove(["nok"])
    assert set(subscription_list.list()) == {"sek", "dkk"}

    assert subscription_list.poll() == {}
