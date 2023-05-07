from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from .components import TopBar
from kivy.uix.image import AsyncImage
Builder.load_file("Interface/product.kv")


class ProductDetailScreen(MDScreen):
    laptop = ObjectProperty()
    name = 'product_detail'

    def __init__(self,laptop,**kwargs):
        super(ProductDetailScreen,self).__init__(**kwargs)
        self.laptop = laptop
        self.ids.product_box.add_widget(TopBar(

        ))
        self.ids.product_box.add_widget(
        AsyncImage(source = self.laptop.image)
        )
        self.ids.product_box.add_widget(MDLabel
                                        (
            text = self.laptop.name,
            halign = 'center'
        ))






    def on_enter(self, *args):
        print(self.laptop)





