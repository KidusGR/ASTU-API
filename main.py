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
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget, OneLineListItem
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
        self.database = {}
        self.filepath = ""
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

    def homepage(self):
        layout = self.root.get_screen("Home").ids.boxH
        image = self.root.get_screen("Home").ids.profile
        label = self.root.get_screen("Home").ids.labelH
        label.text = f"Welcome {self.database['Student'][0]['firstName']} {self.database['Student'][0]['fatherName']}"
        Stud = self.database['Student'][0]
        homeList = {
            "Name": f"{Stud['firstName']} {Stud['fatherName']} {Stud['grandFatherName']}",
            "Program": f"{Stud['program']}",
            "Class year": f"{Stud['classYear']}",
            "Section": f"{Stud['section']}",
            "Admission year": f"{Stud['admissionYear']}",
            "Semester": f"{Stud['academicYearSemester']}"
        }
        for line in list(homeList.keys()):
            l = OneLineListItem(
                        id=line,
                        text=f"[size=10][font=appdata/font/neuropol.otf]{line} : {homeList[line]}[/font][/size]",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        _height=dp(35)
                    )
            
            layout.add_widget(l)

        image.source = f"./data/{self.filepath}/info/{Stud['firstName']}_{Stud['fatherName']}_{Stud['grandFatherName']}.jpeg"

    def profilepage(self):
        image = self.root.get_screen("Profile").ids.profile
        card = self.root.get_screen("Profile").ids.card
        cardTwo = self.root.get_screen("Profile").ids.cardTwo
        Stud = self.database['Student'][0]
        image.source = f"./data/{self.filepath}/info/{Stud['firstName']}_{Stud['fatherName']}_{Stud['grandFatherName']}.jpeg"
        profileList = {
            "Name": f"{Stud['firstName']} {Stud['fatherName']} {Stud['grandFatherName']}",
            "ID": f"{Stud['userName']}",
            "Gender": f"{Stud['gender']}"
        }
        for line in list(profileList.keys()):
            l = OneLineListItem(
                id=line,
                text=f"[size=10][font=appdata/font/neuropol.otf]{line} : {profileList[line]}[/font][/size]",
                theme_text_color="Custom",
                text_color=self.theme_cls.primary_color,
                _height=dp(30)
            )
        
            card.add_widget(l)
        profileListTwo = {
            "First name": f"{Stud['firstName']}",
            "Father name": f"{Stud['fatherName']}",
            "Grand F name": f"{Stud['grandFatherName']}",
            "Amharic name": f"{Stud['amharicFirstName']} {Stud['amharicFatherName']} {Stud['amharicGrandFatherName']}",
            "Marital Status": f"{Stud['maritalStatus']}",
            "Nationality": f"{Stud['nationality']}",
            "Region": f"{Stud['region']}",
            "Disability": f"{Stud['disability']}",
            "Birth date": f"{Stud['dateOfBirth']}",
            "Birth place": f"{Stud['placeOfBirth']}",
            "Phone": f"{Stud['mobile']}",
            "Zone": f"{Stud['zone']}"
        }

        for lin in list(profileListTwo.keys()):
            l = l = OneLineListItem(
                id=lin,
                text=f"[size=10][font=appdata/font/neuropol.otf]{lin} : {profileListTwo[lin]}[/font][/size]",
                theme_text_color="Custom",
                text_color=self.theme_cls.primary_color,
                _height=dp(30)
            )
        
            cardTwo.add_widget(l)


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
        self.database = self.inst.Database()
        print(self.database)
        stat = self.status()
        if stat:
            self.create_list()
        self.BLoginStatus = BooleanProperty(stat)
        if stat:
            self.root.current = 'Home'
            self.filepath = login['folder_name']
            self.homepage()
            self.profilepage()

        else:
            error_msg = "Wrong credentials!"
            print(error_msg)


ASTU_APIApp().run()
