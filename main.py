#!/usr/bin/python3
import json
import os
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.navigationdrawer import MDNavigationDrawer

import API

Window.size = (300, 600)


class LoginScreen(Screen):
    pass


class HomeScreen(Screen):
    pass


class ProfileScreen(Screen):
    pass


class EnrollmentScreen(Screen):
    pass


class HistoryScreen(Screen):
    pass


class EventsScreen(Screen):
    pass


class AssessmentsScreen(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class NavWidget(MDNavigationDrawer):
    pass


sm = ScreenManager()
sm.add_widget(LoginScreen(name="Login"))
sm.add_widget(HistoryScreen(name='Home'))
sm.add_widget(EventsScreen(name='Events'))
sm.add_widget(ProfileScreen(name="Profile"))
sm.add_widget(AssessmentsScreen(name='Assessments'))


class ASTU_APIApp(MDApp):

    def build(self):
        screen = Builder.load_file("appdata/kvs/main.kv")
        self.theme_cls.primary_palette = "LightGreen"
        self.theme_cls.primary_hue = "A700"
        self.theme_cls.theme_style = "Dark"
        Clock.schedule_once(self.create_list)
        self.inst = API.Stalker()
        self.BLoginStatus = BooleanProperty(False)
        return screen

    def create_list(self, *args):
        lists = [
            'Home home hom',
            'Profile identifier pro',
            'Events calendar eve',
            'Assessments check asses',
            "Logout logout logu"
        ]
        pages = ['Home', 'Profile', 'Events', 'Assessments']
        
        if self.status():
            for p in pages:
                for l in lists:
                    text = l.split(" ")
                    button = self.root.get_screen(p).ids.list
                    textline = f"[size=12][font=appdata/font/neuropol.otf]{text[0]}[/font][/size]"
                    list1 = OneLineIconListItem(
                        id=text[2],
                        text=textline,
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    )

                    list1.add_widget(IconLeftWidget(
                        icon=text[1],
                        theme_icon_color="Custom",
                        icon_color=self.theme_cls.primary_color,
                        icon_size=15
                    )
                    )
                    if text[0] == "Logout":
                        # self.inst.logout()
                        list1.bind(on_release=lambda i="Login": self.page("Login"))
                    else:
                        list1.bind(on_release=lambda i=text[0]: self.page(i.text.split(']')[2].split('[')[0]))
                    if any(child.id == text[2] for child in button.children):
                        pass
                    else:
                        button.add_widget(list1)

    def header_data(self, filepath):

        field = ['dormitoryView', 'section', 'idNumber', 'classYear', 'name', 'fullName', 'admissionYear']
        with open(f"./data/{filepath}/info/headerProfile.json") as head:
            data = json.load(head)
            head.close()

        def get_recursively(search_dict, fields):
            fields_found = []
            for key, value in search_dict.items():
                if key in field:
                    fields_found.append(value)
                elif isinstance(value, dict):
                    results = get_recursively(value, field)
                    for result in results:
                        fields_found.append(result)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            more_results = get_recursively(item, field)
                            for another_result in more_results:
                                fields_found.append(another_result)

            return fields_found

        return get_recursively(data, field)

    def homepage(self, filepath, filename):
        layout = self.root.get_screen("Home").ids.float
        image = self.root.get_screen("Home").ids.profile
        data = self.header_data(filepath)
        # [size=24] ... [/size]
        self.root.get_screen("Home").ids.fullname.text = f"[font=appdata/font/Paul-le1V.ttf]Full Name\
        : {data[5]}[/font]"
        self.root.get_screen("Home").ids.idnum.text = f"[font=appdata/font/Paul-le1V.ttf]ID\
        : {data[0]}[/font]"
        self.root.get_screen("Home").ids.program.text = f"[font=appdata/font/Paul-le1V.ttf]Program\
        : {data[4]}[/font]"
        self.root.get_screen("Home").ids.classyear.text = f"[font=appdata/font/Paul-le1V.ttf]Class Year\
        : {data[1]}[/font]"
        self.root.get_screen("Home").ids.section.text = f"[font=appdata/font/Paul-le1V.ttf]Section\
        : {data[3]}[/font]"
        self.root.get_screen("Home").ids.dorm.text = f"[font=appdata/font/Paul-le1V.ttf]Dormitory\
        : {data[2]}[/font]"
        self.root.get_screen("Home").ids.admission.text = f"[font=appdata/font/Paul-le1V.ttf]Admission\
        : {data[7]}[/font]"
        self.root.get_screen("Home").ids.admissiony.text = f"[font=appdata/font/Paul-le1V.ttf]Admission Year\
        : {data[6]}[/font]"
        image.source = f"./data/{filepath}/info/{filename}.jpeg"

    def page(self, text):
        self.root.current = text
        self.root.get_screen(self.root.current).ids.nav_drawer.set_state('close')

    def status(self):
        login_status = self.inst.LoginStatus
        return login_status

    def login(self):
        username = self.root.get_screen('Login').ids.id_field.text
        password = self.root.get_screen('Login').ids.pass_field.text
        login = self.inst.login(username, password)
        fetch = self.inst.fetch()
        stat = self.status()
        if stat:
            self.create_list()
        self.BLoginStatus = BooleanProperty(stat)
        if stat:
            self.root.current = 'Home'
            #self.homepage(login['folder_name'], fetch)

        else:
            error_msg = "Wrong credentials!"
            print(error_msg)


ASTU_APIApp().run()
