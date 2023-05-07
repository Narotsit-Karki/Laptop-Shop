from .home import HomeScreen
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

# Builder.load_file("Interface/main.kv")
Window.size = [428,614]



class AppScreens(MDScreenManager):
	def __init__(self,**kwargs):
		super(AppScreens,self).__init__(**kwargs)
		self.add_widget(HomeScreen())
		

class App(MDApp):
	def build(self):
		self.title = "Byte Boulevard"
		self.theme_cls.primary_palette = "Purple"
		self.icon = "assets/images/logo-32x32.png"
		self.theme_cls.material_style = "M3"
		self.app_screens = AppScreens()
		return self.app_screens





