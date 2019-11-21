from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from kivysec.auth.plain import PlainAuthService
from kivysec.screenmanager import SecureScreenManager


class HomePageScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Welcome'))

        def logout(instance):
            root = self.parent
            root.current = 'logout'

        layout.add_widget(Button(text='LOGOUT',
                                 on_press=logout))

        self.add_widget(layout)


class SecureApp(App):

    def build(self):
        auth_service = PlainAuthService()
        auth_service.useradd('admin', 'pass')
        sm = SecureScreenManager(auth_service)
        screen = HomePageScreen(name='home')
        sm.add_widget(screen)

        login = sm.get_screen('login')

        def set_username(instance, value):
            login.username = value

        user_text = TextInput(text='Username')
        user_text.bind(text=set_username)

        def set_password(instance, value):
            login.password = value

        password_text = TextInput(text='password')
        password_text.bind(text=set_password)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='This is the login page'))
        layout.add_widget(user_text)
        layout.add_widget(password_text)
        layout.add_widget(Button(text='LOGIN',
                                 on_press=login.login(to_screen='home')))

        login.add_widget(layout)

        return sm


if __name__ == '__main__':
    SecureApp().run()
