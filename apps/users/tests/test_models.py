import test_utils

from django.core import mail
from nose.tools import eq_

from users.models import RegisterProfile


class RegisterProfileTests(test_utils.TestCase):
    fixtures = ['registration_profiles.json']

    def setUp(self):
        self.p = RegisterProfile.objects.create_profile('TestUser',
                                                        'test@example.com',
                                                        'asdfasdf')

    def test_email_activation_code(self):
        """Creating a RegisterProfile sends an activation email."""
        eq_(len(mail.outbox), 1)
        assert ('activate/%s' % self.p.activation_key) in mail.outbox[0].body

    def test_password_hash(self):
        """Passwords in RegisterProfile are hashed with sha512."""
        assert self.p.password.startswith('sha512')

    def test_activation(self):
        """Activating a RegisterProfile creates a valid user."""
        p = RegisterProfile.objects.all()[0]
        RegisterProfile.objects.activate_profile(p.activation_key)

        assert p.user is not None
        assert p.user.check_password('asdfasdf')