import pytest
from django.contrib.auth.models import User
from django.core import mail

from site_config.models import SiteConfiguration


@pytest.mark.django_db
@pytest.mark.slow
class TestSignup:
    def test_sign_up(self, live_server, browser, users):
        """
        Tests the sign up form and checks that the appropriate emails
        have been sent afterwards.
        """
        # signup
        uri = '/accounts/signup'
        browser.get(live_server + uri)
        email_box = browser.find_elements_by_name('email')[0]
        email_box.send_keys('testsignupemail@example.com')
        password_box1 = browser.find_elements_by_name('password1')[0]
        password_box1.send_keys('top_secret')
        password_box2 = browser.find_elements_by_name('password2')[0]
        password_box2.send_keys('top_secret')
        login_button = browser.find_elements_by_xpath(
            'html/body/div/div/form/button'
        )[0]
        login_button.click()
        # check we have been redirected
        assert '/accounts/confirm-email/' in browser.current_url
        assert len(mail.outbox) == 1
        # assert '[apostello] New User' in mail.outbox[0].subject # not sent
        # when we have no office email set
        assert 'Please Confirm Your E-mail Address' in mail.outbox[0].subject
        for x in mail.outbox[0].body.split():
            if x.startswith('http'):
                confirm_url = x
        browser.get(confirm_url)
        confirm_button = browser.find_element_by_class_name('button')
        confirm_button.click()
        user = User.objects.get(email='testsignupemail@example.com')
        assert not user.is_staff
        assert not user.is_superuser

    def test_first_user_sign_up(self, live_server, browser):
        """
        Tests the sign up form and checks that the appropriate emails
        have been sent afterwards.
        Then we confirm the email and verify the user has been made an admin.
        """
        # add an office email to test correct email is sent on sign up
        config = SiteConfiguration.get_solo()
        config.office_email = 'test@apostello.ninja'
        config.save()
        # signup
        uri = '/accounts/signup'
        browser.get(live_server + uri)
        email_box = browser.find_elements_by_name('email')[0]
        email_box.send_keys('testsignupemail@example.com')
        password_box1 = browser.find_elements_by_name('password1')[0]
        password_box1.send_keys('top_secret')
        password_box2 = browser.find_elements_by_name('password2')[0]
        password_box2.send_keys('top_secret')
        login_button = browser.find_elements_by_xpath(
            'html/body/div/div/form/button'
        )[0]
        login_button.click()
        # check we have been redirected
        assert '/accounts/confirm-email/' in browser.current_url
        assert len(mail.outbox) == 2
        assert '[apostello] New User' in mail.outbox[0].subject
        assert 'Please Confirm Your E-mail Address' in mail.outbox[1].subject
        for x in mail.outbox[1].body.split():
            if x.startswith('http'):
                confirm_url = x
        browser.get(confirm_url)
        confirm_button = browser.find_element_by_class_name('button')
        confirm_button.click()
        user = User.objects.get(email='testsignupemail@example.com')
        assert user.is_staff
        assert user.is_superuser
