import unittest
from unittest.mock import MagicMock, AsyncMock, Mock
from sqlalchemy.ext.asyncio import AsyncSession
from src.entity.models import Contact, User, Role
from src.schemas.todo import ContactSchema, ContactUpdateSchema
from src.schemas.user import UserSchema
from src.repository.todos import create_contact, get_contacts, get_contact, update_contact, delete_contact
from src.repository.users import get_user_by_email, create_user, confirmed_email, update_avatar_url


class TestAsyncRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.user = User(id=1, username='test_user', password="qwerty", confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [Contact(id=1, first_name='John', last_name='Doe', email='john@example.com', phone_number='123456789'),
                    Contact(id=2, first_name='Jane', last_name='Doe', email='jane@example.com', phone_number='987654321')]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact_id = 1
        contact = Contact(id=contact_id, first_name='John', last_name='Doe', email='john@example.com', phone_number='123456789')
        mocked_contact = Mock()
        mocked_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mocked_contact
        result = await get_contact(contact_id, self.session)
        self.assertEqual(result, contact)

    async def test_create_contact(self):
        contact_data = ContactSchema(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone_number='123456789',
            birthday=None,
            additional_data=None  
        )
        result = await create_contact(contact_data, self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name, contact_data.first_name)
        self.assertEqual(result.last_name, contact_data.last_name)
        self.assertEqual(result.email, contact_data.email)
        self.assertEqual(result.phone_number, contact_data.phone_number)
        self.assertEqual(result.birthday, contact_data.birthday)
        self.assertEqual(result.additional_data, contact_data.additional_data)

    async def test_update_contact(self):
        contact_id = 1
        contact_data = ContactUpdateSchema(
            first_name='Jane',
            last_name='Doe',
            email='jane@example.com',
            phone_number='987654321',
            birthday=None,
            additional_data=None  
        )
        result = await update_contact(contact_id, contact_data, self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name, contact_data.first_name)
        self.assertEqual(result.last_name, contact_data.last_name)
        self.assertEqual(result.email, contact_data.email)
        self.assertEqual(result.phone_number, contact_data.phone_number)
        self.assertEqual(result.birthday, contact_data.birthday)
        self.assertEqual(result.additional_data, contact_data.additional_data)

    async def test_delete_contact(self):
        contact_id = 1
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=contact_id, first_name='John', last_name='Doe', email='john@example.com', phone_number='123456789')
        self.session.execute.return_value = mocked_contact
        result = await delete_contact(contact_id, self.session)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertIsInstance(result, Contact)

    async def test_get_user_by_email(self):
        email = "test@example.com"
        user = User(id=1, username="test_user", email=email, password="password", confirmed=False)
        mocked_user = Mock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        result = await get_user_by_email(email, self.session)
        self.assertEqual(result, user)

    async def test_create_user(self):
        user_data = UserSchema(username="test_user", email="test@example.com", password="password")
        result = await create_user(user_data, self.session)
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, user_data.username)
        self.assertEqual(result.email, user_data.email)
        self.assertEqual(result.password, user_data.password)

    async def test_confirmed_email(self):
        email = "test@example.com"
        user = User(id=1, username="test_user", email=email, password="password", confirmed=False)
        mocked_get_user = Mock(return_value=user)
        mocked_get_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_get_user
        result = await confirmed_email(email, self.session)
        self.assertEqual(user.confirmed, True)

    async def test_update_avatar_url(self):
        email = "test@example.com"
        url = "https://example.com/avatar.jpg"
        user = User(id=1, username="test_user", email=email, password="password", confirmed=True, avatar=None)
        mocked_get_user = Mock(return_value=user)
        self.session.execute.return_value = mocked_get_user
        result = await update_avatar_url(email, url, self.session)
        self.assertEqual(result.avatar, url)