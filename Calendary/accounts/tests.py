from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view(self):
        # Utiliza reverse para obtener la URL de la vista
        url = reverse('register')

        # Realiza una solicitud POST simulada con datos de formulario
        response = self.client.post(url, {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
        })

        # Verifica que la respuesta sea un código de redirección (302)
        self.assertEqual(response.status_code, 302)

        # Verifica que el usuario haya sido creado y esté logueado
        user = get_user_model().objects.get(username='testuser')
        self.assertTrue(user.is_authenticated)

        # Puedes agregar más aserciones según las necesidades de tu aplicación

        # Verifica que el redireccionamiento sea al URL esperado
        self.assertRedirects(response, reverse('home'))

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_login_view(self):
        # Utiliza reverse para obtener la URL de la vista
        url = reverse('login')

        # Realiza una solicitud POST simulada con datos de formulario
        response = self.client.post(url, self.user_data)

        # Verifica que la respuesta sea un código de redirección (302)
        self.assertEqual(response.status_code, 302)

        # Verifica que el usuario esté autenticado
        user = get_user_model().objects.get(username='testuser')
        self.assertTrue(user.is_authenticated)

        # Puedes agregar más aserciones según las necesidades de tu aplicación

        # Verifica que el redireccionamiento sea al URL esperado (por ejemplo, el dashboard)
        self.assertRedirects(response, reverse('home'))