from kivy.app import App

from kivysec.auth.plain import PlainAuthService
from kivysec.auth.user import anonymous_user
from kivysec.screenmanager import SecureScreenManager, AuthorizedScreen

from kivy.lang import Builder

anonymous_user.name = 'Anonymous'

Builder.load_file('plain.kv')


class HomePageScreen(AuthorizedScreen):

    def update_user(self, user):
        self.ids["user_label"].text = 'Welcome ' + user.name


auth_service = PlainAuthService()
auth_service.useradd('admin', 'pass', {'name': 'Administrator'})

sm = SecureScreenManager(auth_service)
sm.add_widget(HomePageScreen(name='home'))


class PlainApp(App):

    def build(self):
        return sm


if __name__ == '__main__':
    PlainApp().run()
