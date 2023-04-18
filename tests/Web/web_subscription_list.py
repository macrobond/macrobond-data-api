from datetime import datetime, timezone

import pytest

from macrobond_data_api.web import WebApi, WebClient


def test_subscription_list() -> None:
    with WebClient(api_url="https://szctwebapi0.i.mbnd.eu/", authorization_url="https://auth.test.macrobond.net/mbauth/") as web:
        subscription_list = web.subscription_list(datetime.now(timezone.utc))
        subscription_list.set(['sek', 'nok'])
        assert set(subscription_list.list()) == {'sek', 'nok'}
        subscription_list.add(['dkk'])
        assert set(subscription_list.list()) == {'sek', 'nok', 'dkk'}
        subscription_list.remove(['nok'])
        assert set(subscription_list.list()) == {'sek', 'dkk'}
        
        result = subscription_list.poll()
        assert result == {}