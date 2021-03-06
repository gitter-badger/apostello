from time import sleep

import pytest


@pytest.mark.django_db
@pytest.mark.slow
@pytest.mark.parametrize("uri", ['/users/profiles/', ])
class TestUserProfiles:
    def test_page_and_submit(
        self, uri, live_server, browser_in, users, driver_wait_time
    ):
        # load page
        browser_in.get(live_server + uri)
        assert uri in browser_in.current_url
        # check table is there
        sleep(driver_wait_time)
        tables = browser_in.find_elements_by_class_name('table')
        assert len(tables) == 1
        table = tables[0]
        assert 'Approved' in table.text
        assert 'Incoming' in table.text
        assert 'test@example.com' in table.text
        # toggle a permission
        toggle_button = browser_in.find_elements_by_class_name('minus')[0]
        toggle_button.click()
        assert users['staff'].profile.approved
