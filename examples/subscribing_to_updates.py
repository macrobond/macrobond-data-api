from datetime import datetime, timedelta, timezone
from typing import Dict, List

from macrobond_data_api.common.types import Series
from macrobond_data_api.web import WebApi, WebClient
from macrobond_data_api.web.subscription_list import SubscriptionList


def poll_for_updates(api: WebApi, subscription_list: SubscriptionList, dbmock: Dict[str, Series]) -> None:
    # Poll for updates
    while True:
        result = subscription_list.poll()
        updated = List[str]()

        for name, update_time in result.items():
            print(f'Series "{name}", last_modified "{update_time}"')
            # Here we should compare with the last_modified we have stored and ignore it if it the same or older since
            # we might see updates we have already stored. In the real world, we would read from our database.
            series = dbmock[name]
            if series is not None and update_time > series.last_modified:
                # The series was updated
                updated.append(name)

        if updated:
            for series in api.get_many_series(updated):
                # Store the updated series in our database
                if not series.is_error:  # Error handling omitted
                    dbmock[series.primary_name] = series

        # We should store the last_modified timestamp of the susbscription list so that we can resume polling in
        # case it is interupted or aborted.
        list_modified = subscription_list.last_modified
        print(f"List last updated {list_modified}")


def set_and_poll() -> None:
    # Example how to define a list and then poll for updates
    with WebClient() as api:
        # This is the set of series we want to subscribe to
        myseries = ["sek", "nok"]

        # Since we are replacing any existing list, we should use "now" as the starting point polling
        list_modified = datetime.now(timezone.utc)
        subscription_list = api.subscription_list(list_modified)

        # Add to the list first so that we capture all updates
        subscription_list.set(myseries)

        # Get the current version of the series and put it in our in-memory "database". This replaces the content.
        # In the real world, this is where we should store the series in the DB

        dbmock: Dict[str, Series] = Dict()

        for series in api.get_many_series(myseries):
            if not series.is_error:  # Error handling omitted
                dbmock[series.primary_name] = series

        for name, series in dbmock.items():
            print(f'Store series "{name}" in DB, last_modified "{series.last_modified}"')

        poll_for_updates(api, subscription_list, dbmock)


def add_and_poll(dbmock: Dict[str, Series]) -> None:
    # Example how to modify a list and then poll for updates
    with WebClient() as api:
        # This is the set of additional series we want to subscribe to
        new_series = ["gbp"]

        # A fictional timestamp. This should be a value stored while polling in the past.
        list_modified = datetime.now(timezone.utc) - timedelta(hours=10)

        # Since we are replacing any existing list, we should use "now" as the starting point polling
        subscription_list = api.subscription_list(list_modified)

        # Add to the list first so that we capture all updates
        subscription_list.add(new_series)

        # Get the current version of the series and add to our in-memory "database".
        # In the real world, this is where we should store the series in the DB

        for series in api.get_many_series(new_series):
            if not series.is_error:  # Error handling omitted
                dbmock[series.primary_name] = series
                print(f'Store series "{series.primary_name}" in DB, last_modified "{series.last_modified}"')

        poll_for_updates(api, subscription_list, dbmock)


set_and_poll()
# add_and_poll(Dict[str, Series]())
