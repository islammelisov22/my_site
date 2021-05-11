from django.test import TestCase

from shop.forms import RegisterForm, EditForm


class RegisterFormTestSuccess(TestCase):
    def test_register_success(self):
        form_data = {
            'email': '324243@fds.mail.ru',
            'password': '1231waeaw123',
            'password2': '123waeaw123',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())


class RegisterFormTest(TestCase):
    def test_register_email_fail(self):
        form_data = {
            'email': '1234fs@fasf.ru' * 25,
            'password1': '12345',
            'password2': '123456',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())


class EditFormTest(TestCase):
    def test_edit_form_email_success(self):
        form_data = {
            'email': '123212@mail.ru',
            'password': '123123',
        }
        form = EditForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_edit_form_first_name(self):
        form_data = {
            'first_name1': 'misha',
            'first_name2': 'sasha'
        }
        form = EditForm(data=form_data)
        self.assertFalse(form.is_valid())
