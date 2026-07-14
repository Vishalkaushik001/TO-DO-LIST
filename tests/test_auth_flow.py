import unittest

from app import create_app, db, seed_default_data


class AuthFlowTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
            WTF_CSRF_ENABLED=False,
        )
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            seed_default_data(self.app)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_and_login_flow(self):
        register_response = self.client.post('/register', data={
            'username': 'jane',
            'email': 'jane@example.com',
            'password': 'secret123',
            'confirm_password': 'secret123',
        }, follow_redirects=True)

        self.assertEqual(register_response.status_code, 200)
        self.assertIn(b'Login', register_response.data)

        login_response = self.client.post('/login', data={
            'username': 'jane',
            'password': 'secret123',
        }, follow_redirects=True)

        self.assertEqual(login_response.status_code, 200)
        self.assertIn(b'Welcome', login_response.data)
        self.assertIn(b'Tasks', login_response.data)

    def test_dashboard_shows_task_summary(self):
        self.client.post('/register', data={
            'username': 'jane',
            'email': 'jane@example.com',
            'password': 'secret123',
            'confirm_password': 'secret123',
        })

        self.client.post('/login', data={
            'username': 'jane',
            'password': 'secret123',
        })

        self.client.post('/tasks', data={
            'title': 'Buy milk',
            'description': 'From the store'
        }, follow_redirects=True)

        dashboard_response = self.client.get('/tasks')

        self.assertEqual(dashboard_response.status_code, 200)
        self.assertIn(b'1 task total', dashboard_response.data)

    def test_admin_login_and_header_update(self):
        login_response = self.client.post('/admin/login', data={
            'username': 'admin',
            'password': 'admin123',
        }, follow_redirects=True)

        self.assertEqual(login_response.status_code, 200)
        self.assertIn(b'Admin Dashboard', login_response.data)

        settings_response = self.client.post('/admin/settings', data={
            'header_title': 'FocusFlow Admin',
            'header_subtitle': 'Admin control center',
        }, follow_redirects=True)

        self.assertEqual(settings_response.status_code, 200)
        self.assertIn(b'FocusFlow Admin', settings_response.data)


if __name__ == '__main__':
    unittest.main()
