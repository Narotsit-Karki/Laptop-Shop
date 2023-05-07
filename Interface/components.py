from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar
from kivy.lang import Builder

Builder.load_file("Interface/components.kv")

class TopBar(MDTopAppBar):
	pass

class SearchBar(MDTextField):
    pass
