from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.models import UserProfile

class UserProfileTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone_number='1234567890',
            address='Test Address'
        )

    def test_user_profile_creation(self):
        """Test that a user profile can be created"""
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.phone_number, '1234567890')
        self.assertEqual(self.profile.address, 'Test Address')

    def test_user_profile_str(self):
        """Test the string representation of a user profile"""
        self.assertEqual(str(self.profile), 'testuser Profile') 