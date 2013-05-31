# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestEverythingMe(GaiaTestCase):

    # Everything.Me locators
    _shortcut_items_locator = ('css selector', '#shortcuts-items li')
    _app_icon_locator = ('css selector', 'div.evme-apps li.cloud')

    # Homescreen locators
    _homescreen_frame_locator = ('css selector', 'div.homescreen > iframe')
    _homescreen_landing_locator = ('id', 'landing-page')

    # Facebook app locator
    _facebook_iframe_locator = ('css selector', "iframe[data-url*='facebook.com']")
    _facebook_app_locator = ('xpath', "//li[@data-name='Facebook']")

    def setUp(self):
        GaiaTestCase.setUp(self)

        # Turn off geolocation prompt
        self.apps.set_permission('Homescreen', 'geolocation', 'deny')

        self.connect_to_network()

    def test_launch_everything_me_app(self):
        # https://github.com/mozilla/gaia-ui-tests/issues/69

        # Swipe to Everything.Me
        hs_frame = self.marionette.find_element(*self._homescreen_frame_locator)
        self.marionette.switch_to_frame(hs_frame)

        # We'll use js to flick pages for reliability/Touch is unreliable
        self.marionette.execute_script("window.wrappedJSObject.GridManager.goToPreviousPage();")

        # Check for the available application shortcut categories
        self.wait_for_element_displayed(*self._shortcut_items_locator)

        # Check that there are shortcut application categories available
        shortcuts = self.marionette.find_elements(*self._shortcut_items_locator)
        self.assertGreater(len(shortcuts), 0, 'No shortcut categories found')

        # Tap on the first category of shortcuts
        # TODO: Had to revert back to using the first shortcut as v1.0.1 still uses canvas
        shortcuts[0].tap()

        self.wait_for_element_displayed(*self._app_icon_locator)

        # Due to everythingme HTML we cannot locate by the text...
        app_icons = self.marionette.find_elements(*self._app_icon_locator)
        # ... so we'll just get the first one.
        app_icons[0].tap()

        # Switch to top level frame then look for the Facebook app
        self.marionette.switch_to_frame()

        # Find the frame and switch to it
        app_iframe = self.wait_for_element_present(*self._facebook_iframe_locator)
        self.marionette.switch_to_frame(app_iframe)

        self.assertIn("Facebook", self.marionette.title)

    def tearDown(self):
        # This will take us back to Everything.Me 'Social' category, from whence cleanUp can return to the home page
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")

        GaiaTestCase.tearDown(self)
