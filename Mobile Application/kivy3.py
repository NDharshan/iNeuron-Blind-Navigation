"""from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.list import OneLineListItem

KV = '''
<DrawerClickableItem@MDNavigationDrawerItem>
    focus_color: "#e7e4c0"
    text_color: "#4a4939"
    icon_color: "#4a4939"
    ripple_color: "#c5bdd2"
    selected_color: "#0c6c4d"


<DrawerLabelItem@MDNavigationDrawerItem>
    text_color: "#4a4939"
    icon_color: "#4a4939"
    focus_behavior: False
    selected_color: "#4a4939"
    _no_ripple_effect: True


MDScreen:

    MDNavigationLayout:

        MDScreenManager:

            MDScreen:

                MDTopAppBar:
                    title: "Navigation Drawer"
                    elevation: 4
                    pos_hint: {"top": 1}
                    md_bg_color: "#e7e4c0"
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                MDNavigationLayout:
                    MDScreenManager:
                        id: "screen_manager"

                        MDScreen:
                            name: "Travel Diary"
                            MDBoxLayout:
                                orientation: "vertical"


                                MDScrollView:
                                    scroll_timeout : 100

                                    MDList:
                                        id: md_list
                                        padding: 0


                        MDScreen:
                            name: "Current Location"
                            MDLabel:
                                text: "Screen 2"
                                halign: "center"




        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)

            MDNavigationDrawerMenu:

                MDNavigationDrawerHeader:
                    title: "NavigateMe"
                    title_color: "#4a4939"
                    text: "Eye of Horus"
                    spacing: "4dp"
                    padding: "12dp", 0, 0, "56dp"

                MDNavigationDrawerLabel:
                    text: "Srinivas"

                MDNavigationDrawerLabel:
                    text: "#1621, 50 Ft Main Road, RR Nagar"



                MDNavigationDrawerDivider:

                MDNavigationDrawerLabel:
                    text: "Actions"

                DrawerLabelItem:
                    icon: "information-outline"
                    text: "Travel Diary"

                DrawerLabelItem:
                    icon: "information-outline"
                    text: "Current Location"

'''

class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()

class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        from kivy.uix.button import Button
        from kivy.uix.slider import Slider
        from kivy.uix.widget import Widget

        root = Widget()
        root.add_widget(Button())
        slider = Slider()

        root.add_widget(slider)
        return Builder.load_string(KV)

    def on_start(self):
        '''Creates a list of cards.'''

        for i in range(4):
            self.root.ids.md_list.add_widget(
                SwipeToDeleteItem(text=f"One-line item {i}")
            )

    def switch_screen(self, instance_list_item: OneLineListItem):
        self.root.ids.screen_manager.ids.nav_drawer.current = {
            "Current Location": "Current Location", "Travel Diary": "Travel Diary"
        }[instance_list_item.text]
        self.root.children[0].ids.nav_drawer_close()

Example().run()"""
import json

# import geolocator
import pyrebase
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar


def data_gen():
    firebaseConfig = {
          "apiKey": "AIzaSyCqWpqh7mzrO0puVvlXGJdNSUgzSuc9H6A",
          "authDomain": "taarkshya.firebaseapp.com",
          "projectId": "taarkshya",
          "storageBucket": "taarkshya.appspot.com",
          "messagingSenderId": "1088440610226",
          "appId": "1:1088440610226:web:298bd6bda042373b0bc8ab",
          "databaseURL": ""
    };
    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()

    def download_firebase():
        filename = "jason_parser.json"
        storage.child(filename).download("", "downloaded.txt")
        return filename
        # upload_firebase()


def data_gen():
    import json
    import pyrebase
    firebaseConfig = {
        "apiKey": "AIzaSyArKFFDqMwXZR1QCCJvBmcOUn0ajIISs3Y",
        "authDomain": "suparna-7dd6e.firebaseapp.com",
        "databaseURL": "https://suparna-7dd6e-default-rtdb.firebaseio.com",
        "projectId": "suparna-7dd6e",
        "storageBucket": "suparna-7dd6e.appspot.com",
        "messagingSenderId": "292555253504",
        "appId": "1:292555253504:web:63ad4c6273dffd7f6eb5e5",
        "databaseURL": ""
    };

import geocoder
g = geocoder.ip('me')
print(g.latlng)
# import module
from geopy.geocoders import Nominatim
# initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")

# location = geolocator.reverse(str(g.latlng[0])+","+str(g.latlng[1])).raw["address"]['suburb']
# currently_at = location
currently_at = 'Nagarbhavi'
with open('locations.json') as f:
    data = [i['streetAdd'] for i in json.load(f)]
currently_at = "Srinivas\nis at Nagarbhavi"
data = data[:5]
travels = "Past Travels were in:\n\n"+"\n\n".join(data)

class Example(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Brown"
        self.theme_cls.theme_style = "Light"
        return (
            MDScreen(
                MDTopAppBar(
                    pos_hint={"top": 1},
                    elevation=4,
                    title="NavigateMe",
                    left_action_items=[["menu", lambda x: self.nav_drawer_open()]],
                ),
                MDNavigationLayout(
                    MDScreenManager(
                        MDScreen(
                            MDLabel(
                                text=currently_at,
                                halign="center",
                            ),
                            name="scr 1",
                        ),
                        MDScreen(
                            MDLabel(
                                text=travels,
                                halign="center",
                            ),
                            name="scr 2",
                        ),
                        id="screen_manager",
                    ),
                    MDNavigationDrawer(
                        MDScrollView(
                            MDList(
                                OneLineListItem(
                                    text="Bio and Current Location",
                                    on_press=self.switch_screen,
                                ),
                                OneLineListItem(
                                    text="Past Travels",
                                    on_press=self.switch_screen,
                                ),
                            ),
                        ),
                        id="nav_drawer",
                        radius=(0, 16, 16, 0),
                    ),
                    id="navigation_layout",
                )
            )
        )

    def switch_screen(self, instance_list_item: OneLineListItem):
        self.root.ids.navigation_layout.ids.screen_manager.current = {
            "Bio and Current Location": "scr 1", "Past Travels": "scr 2"
        }[instance_list_item.text]
        self.root.children[0].ids.nav_drawer.set_state("close")

    def nav_drawer_open(self):
        nav_drawer = self.root.children[0].ids.nav_drawer
        nav_drawer.set_state("open")




Example().run()