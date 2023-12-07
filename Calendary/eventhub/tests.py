import email
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Task, Tag
from .forms import TaskForm
from accounts.models import User

class CreateTasksViewTest(TestCase):
    def setUp(self):
        # Crear datos de prueba, por ejemplo, un usuario y una etiqueta
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.tag = Tag.objects.create(name='Test Tag', color='#00FF00')

    def test_create_task(self):
        # Loguear al usuario
        self.client.login(username='testuser', password='testpassword')

        # Datos de prueba para la tarea
        task_data = {
            'title': 'Test Task',
            'description': 'This is a test task.',
            'due_date': timezone.now(),
            'tags': [self.tag.id],  # Usar el ID de la etiqueta creada en setUp
            'users': [self.user.id],  # Usar el ID del usuario creado en setUp
            'has_frequency': False,
        }

        # Enviar solicitud POST para crear la tarea
        response = self.client.post(reverse('create task'), data=task_data)

        # Verificar que se redirige a la página de lista de tareas después de crear una tarea exitosamente
        self.assertRedirects(response, reverse('list tasks'))

        # Verificar que la tarea se ha creado correctamente en la base de datos
        self.assertEqual(Task.objects.count(), 1)
        new_task = Task.objects.first()
        self.assertEqual(new_task.title, 'Test Task')

    def test_invalid_form_submission(self):
        # Loguear al usuario
        self.client.login(username='testuser', password='testpassword')

        # Datos inválidos para la tarea (sin título)
        invalid_task_data = {
            'description': 'This is an invalid task.',
            'due_date': timezone.now(),
            'tags': [self.tag.id],
            'users': [self.user.id],
            'has_frequency': False,
        }

        # Enviar solicitud POST con datos inválidos
        response = self.client.post(reverse('create task'), data=invalid_task_data)

        # Verificar que la página de creación de tareas se vuelve a renderizar
        self.assertEqual(response.status_code, 200)

        # Verificar que no se ha creado ninguna tarea en la base de datos
        self.assertEqual(Task.objects.count(), 0)

        # Verificar que el formulario en el contexto contiene errores
        form = response.context['form']
        self.assertTrue(form.errors)

# Agrega más casos de prueba según tus necesidades
class TaskListViewTest(TestCase):
    def setUp(self):
        # Crear usuarios de prueba
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password1')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password2')

        # Crear etiquetas de prueba
        self.tag1 = Tag.objects.create(name='Tag 1', color='#00FF00')
        self.tag2 = Tag.objects.create(name='Tag 2', color='#0000FF')

        # Crear tareas de prueba asociadas a usuarios específicos
        self.task_user1 = Task.objects.create(
            title='Task User 1',
            description='Description for User 1',
            due_date=timezone.now(),
            has_frequency=False
        )
        self.task_user1.users.add(self.user1)
        self.task_user1.tags.add(self.tag1)

        self.task_user2 = Task.objects.create(
            title='Task User 2',
            description='Description for User 2',
            due_date=timezone.now(),
            has_frequency=False
        )
        self.task_user2.users.add(self.user2)
        self.task_user2.tags.add(self.tag2)

    def test_task_list_view_for_user(self):
        # Loguear al usuario1
        self.client.login(username='user1', password='password1')

        # Obtener la URL de la lista de tareas filtrada por usuario1
        url = reverse('list tasks')

        # Hacer una solicitud GET a la vista de lista de tareas
        response = self.client.get(url)

        # Verificar que la respuesta tenga el código de estado 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verificar que la tarea de user1 esté presente en la lista
        self.assertContains(response, 'Task User 1')

        # Verificar que la tarea de user2 no esté presente en la lista
        self.assertNotContains(response, 'Task User 2')

        # Asegurarse de que se esté utilizando el template correcto
        self.assertTemplateUsed(response, 'eventhub/list.html')


class UpdateTasksViewTest(TestCase):
    def setUp(self):
        # Crear datos de prueba, por ejemplo, un usuario y una etiqueta
        self.user = User.objects.create_user(username='testuser', password='testpassword', email="user1@example.com")
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword', email="user2@example.com")
        self.tag = Tag.objects.create(name='Test Tag', color='#00FF00')

        # Crear una tarea de prueba
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task.',
            due_date=timezone.now(),
            has_frequency=False
        )
        self.task.tags.add(self.tag)
        self.task.users.add(self.user)

    def test_update_task(self):
        # Loguear al usuario propietario de la tarea
        self.client.force_login(self.user)

        # Datos de prueba actualizados para la tarea
        updated_task_data = {
            'title': 'Updated Test Task',
            'description': 'This is the updated test task.',
            'due_date': timezone.now(),
            'tags': [self.tag.id],
            'users': [self.user.id],
            'has_frequency': False,
        }

        # Enviar solicitud POST para actualizar la tarea
        response = self.client.post(reverse('update task', kwargs={'pk': self.task.pk}), data=updated_task_data)

        # Verificar que se redirige a la página de detalles de la tarea después de actualizar
        self.assertRedirects(response, reverse('list tasks'))

        # Recargar la tarea desde la base de datos para obtener los cambios
        updated_task = Task.objects.get(pk=self.task.pk)

        # Verificar que la tarea se ha actualizado correctamente en la base de datos
        self.assertEqual(updated_task.title, 'Updated Test Task')
        self.assertEqual(updated_task.description, 'This is the updated test task.')

    def test_update_task_unauthorized_user(self):
        # Loguear a otro usuario que no es propietario de la tarea
        self.client.force_login(self.other_user)

        # Datos de prueba actualizados para la tarea
        updated_task_data = {
            'title': 'Updated Test Task',
            'description': 'This is the updated test task.',
            'due_date': timezone.now(),
            'tags': [self.tag.id],
            'users': [self.other_user.id],
            'has_frequency': False,
        }

        # Enviar solicitud POST para actualizar la tarea
        response = self.client.post(reverse('update task', kwargs={'pk': self.task.pk}), data=updated_task_data)

        # Verificar que se recibe un código de estado 403 (Forbidden) ya que el usuario no es propietario
        self.assertEqual(response.status_code, 403)

        # Recargar la tarea desde la base de datos para verificar que no se ha actualizado
        updated_task = Task.objects.get(pk=self.task.pk)
        self.assertNotEqual(updated_task.title, 'Updated Test Task')
        self.assertNotEqual(updated_task.description, 'This is the updated test task.')

class DeleteTasksViewTest(TestCase):
    def setUp(self):
        # Crear datos de prueba, por ejemplo, un usuario y una etiqueta
        self.user = User.objects.create_user(username='testuser', password='testpassword', email="user1@example.com")
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword', email="user2@example.com")
        self.tag = Tag.objects.create(name='Test Tag', color='#00FF00')

        # Crear una tarea de prueba
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task.',
            due_date=timezone.now(),
            has_frequency=False
        )
        self.task.tags.add(self.tag)
        self.task.users.add(self.user)

    def test_delete_task(self):
        # Loguear al usuario propietario de la tarea
        self.client.force_login(self.user)

        # Enviar solicitud POST para eliminar la tarea
        response = self.client.post(reverse('delete task', kwargs={'pk': self.task.pk}))

        # Verificar que se redirige a la página de lista de tareas después de eliminar
        self.assertRedirects(response, reverse('list tasks'))

        # Verificar que la tarea se ha eliminado correctamente de la base de datos
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.task.pk)

    def test_delete_task_unauthorized_user(self):
        # Loguear a otro usuario que no es propietario de la tarea
        self.client.force_login(self.other_user)

        # Enviar solicitud POST para eliminar la tarea
        response = self.client.post(reverse('delete task', kwargs={'pk': self.task.pk}))

        # Verificar que se recibe un código de estado 403 (Forbidden) ya que el usuario no es propietario
        self.assertEqual(response.status_code, 403)

        # Verificar que la tarea no se ha eliminado de la base de datos
        self.assertIsNotNone(Task.objects.get(pk=self.task.pk))