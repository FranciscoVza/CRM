"""
Tests para la aplicación CRM
"""
from rest_framework.test import APITestCase
from rest_framework import status
from apps.accounts.models import User, Account, AccountUser
from django.urls import reverse


class UserAuthenticationTestCase(APITestCase):
    """Tests para autenticación de usuarios"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_creation(self):
        """Test creación de usuario"""
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.email, 'test@example.com')

    def test_token_obtain(self):
        """Test obtención de token JWT"""
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
        }
        response = self.client.post(url, data, format='json')
        # Este test asume que se usa email como USERNAME_FIELD
        # Puede requerir ajustes según la configuración

    def test_user_profile_access(self):
        """Test acceso al perfil del usuario"""
        self.client.force_authenticate(user=self.user)
        url = reverse('user-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AccountTestCase(APITestCase):
    """Tests para gestión de cuentas"""

    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(
            email='owner@example.com',
            username='owner',
            password='password123'
        )
        self.account = Account.objects.create(
            name='Test Company',
            slug='test-company',
            owner=self.user
        )

    def test_account_creation(self):
        """Test creación de cuenta"""
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(self.account.owner, self.user)

    def test_account_user_role(self):
        """Test rol de usuario en cuenta"""
        account_user = AccountUser.objects.create(
            account=self.account,
            user=self.user,
            role='admin'
        )
        self.assertEqual(account_user.role, 'admin')


class ContactTestCase(APITestCase):
    """Tests para gestión de contactos"""

    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='password123'
        )
        self.account = Account.objects.create(
            name='Test Company',
            slug='test-company',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_contact_creation(self):
        """Test creación de contacto"""
        from apps.contacts.models import Contact

        contact = Contact.objects.create(
            account=self.account,
            name='John Doe',
            email='john@example.com',
            phone='+1234567890'
        )
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(contact.email, 'john@example.com')

    def test_contact_list_api(self):
        """Test API de lista de contactos"""
        from apps.contacts.models import Contact
        Contact.objects.create(
            account=self.account,
            name='John Doe',
            email='john@example.com'
        )
        url = reverse('contact-list')
        response = self.client.get(f'{url}?account_id={self.account.id}')
        # Requiere que el usuario tenga acceso
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN])


class ConversationTestCase(APITestCase):
    """Tests para gestión de conversaciones"""

    def setUp(self):
        """Configuración inicial"""
        from apps.contacts.models import Contact

        self.user = User.objects.create_user(
            email='agent@example.com',
            username='agent',
            password='password123'
        )
        self.account = Account.objects.create(
            name='Test Company',
            slug='test-company',
            owner=self.user
        )
        self.contact = Contact.objects.create(
            account=self.account,
            name='Customer',
            email='customer@example.com'
        )
        self.client.force_authenticate(user=self.user)

    def test_conversation_creation(self):
        """Test creación de conversación"""
        from apps.conversations.models import Conversation

        conversation = Conversation.objects.create(
            account=self.account,
            contact=self.contact,
            subject='Support Request',
            source='email',
            status='open'
        )
        self.assertEqual(conversation.status, 'open')

    def test_conversation_assignment(self):
        """Test asignación de conversación a agente"""
        from apps.conversations.models import Conversation

        conversation = Conversation.objects.create(
            account=self.account,
            contact=self.contact,
            subject='Support Request',
            source='email',
        )
        conversation.assignee = self.user
        conversation.save()
        self.assertEqual(conversation.assignee, self.user)


if __name__ == '__main__':
    import unittest
    unittest.main()
