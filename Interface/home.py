from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.effects.fadingedge.fadingedge import FadingEdgeEffect
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from Models.models import Laptop
from kivy.properties import ObjectProperty, BooleanProperty
from kivymd.uix.behaviors import HoverBehavior
from kivy.animation import Animation
from .components import TopBar,SearchBar

from .product import ProductDetailScreen


Builder.load_file("Interface/home.kv")



class FadeScrollView(FadingEdgeEffect, ScrollView):
	pass


class CartButton(MDRoundFlatIconButton):
	checked = BooleanProperty(False)
	def __init__(self,**kwargs):
		super().__init__(**kwargs)

	def on_enter(self,*args):
		print("Cart")
		self.md_bg_color = "red"
		self.text_color = "white"

	def on_press(self):
		if not self.checked:
			self.line_color = "green"
			self.text = "added"
			self.icon = "cart-check"
			self.icon_color = "green"
			self.text_color = "green"
			self.checked = True
		else:
			self.checked = False
			self.line_color = "red"
			self.text = "Cart"
			self.icon = "cart-plus"
			self.icon_color = "red"
			self.text_color = "red"





class HomeScreen(MDScreen):
	name = 'home_screen'
	badge_labels = []
	def __init__(self,**kwargs):
		super(HomeScreen,self).__init__(**kwargs)
		self.display_laptops()


	def display_laptops(self):
		Laptops = []
		with open(Laptop.file_path['Sales']) as file:
			for index,line in enumerate(file,start=0):
				laptop = Laptop.create_laptop(line,index)
				Laptops.append(laptop)
		
		for laptop in Laptops:
			self.ids.laptop_grid.add_widget(
				MD3Card(
					laptop = laptop)
				)

class MD3Card(MDCard,HoverBehavior):
	laptop = ObjectProperty(None)
	def __init__(self,**kwargs):
		super(MD3Card,self).__init__(**kwargs)

	def on_enter(self):
		Animation(size=(dp(195),dp(325)), duration=0.2, t='linear').start(self)

	def click(self,app,laptop):
		product_screen = ProductDetailScreen(laptop=laptop)
		app.app_screens.add_widget(product_screen)
		self.parent.parent.parent.parent.manager.current = 'product_detail'


	def on_leave(self):
		Animation(size=(dp(190),dp(320)), duration=0.2, t='out_quad').start(self)



