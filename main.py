# set DEBUG=1 && c:\Projects\NewKivyApp\venv\Scripts\python.exe C:\Projects\NewKivyApp\main.py
from kaki.app import App 
from kivy.metrics import dp
from kivy.factory import Factory
from kivy.core.window import Window
from kivymd.uix.menu import MDDropdownMenu
import datetime
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.utils import get_color_from_hex
from kivymd.uix.pickers import MDTimePickerInput, MDTimePickerDialVertical
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import  MDListItemSupportingText, MDListItemTertiaryText, MDListItemTrailingIcon, MDListItemHeadlineText
from kivymd.uix.pickers import MDModalDatePicker
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.base import EventLoop
from meas_record_screen import MeasRecordScreen
from section_screen import SectionScreen
from enter_data import EnterDataScreen
from calc_dry import CalcDryScreen
from view_result import ResultScreen
from gost_result import GostScreen
from tube_result import TubeScreen
from bt_screen import   BtScreen
#!!!
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.utils import platform

from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
)
from kivymd.uix.list import (
    MDListItem,
    MDListItemSupportingText,
)
import os
from mydb import *


class MyCardMD1(MDCard):
    text1 = StringProperty('')
    text2 = StringProperty('')
    text3 = StringProperty('')
    color = ListProperty([1, 1, 1, 1])  # Default color is white
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'color' in kwargs:
            self.color = kwargs['color']

class MeasCard(RelativeLayout):
    pass

class ManagerScreens(MDScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        screens = [
                LoginScreen(name='login'), 
                RecordScreen(name='record'),
                NewRecordScreen(name='new_record'),
                ObjRecordScreen(name='obj_record'),
                FolderRecordScreen(name='folder_record'),
                MeasRecordScreen(name='meas_record'),
                SectionScreen(name='section_screen'),
                EnterDataScreen(name='enter_data_screen'),
                CalcDryScreen(name='calc_dry_screen'),
                ResultScreen(name='view_result'),
                GostScreen(name='gost_screen'),
                TubeScreen(name='tube_screen'),
                BtScreen(name='bt_screen'),
                #!!!
            ]
        for screen in screens:
            self.add_widget(screen)
        self.current = "record"
        
class MyCard(MDCard):
    text = StringProperty()

#-------------------------------------------------- ObjRecordScreen ------------------------------------------------
class ObjRecordScreen(MDScreen):
    dialog = None
    warning =None
    date = ""
    time = ""
    current_record = None
    id = None

    def on_enter(self):
        name =  App.get_running_app().current_record
        print("Edit item:", )
        current_record = search_record(name)
        self.ids.proba_name_bar.text = current_record[1]
        self.id = current_record[0]
        self.text_date =  current_record[8]
        self.text_time1 =  current_record[9]
        self.text_time2 =  current_record[10]
        self.text_description = current_record[2]
        print(current_record)
        self.text_name = self.ids.name_field.text = current_record[1]
        
        self.presure = current_record[4]
        self.ids.presure_field.text = str(current_record[4])
        self.temp = current_record[5]
        self.ids.temp_field.text = str(current_record[5])
        self.hum = current_record[6]
        self.ids.hum_field.text = str(current_record[6])
        self.ids.total_points.text = "Всего рабочих точек: " + str(current_record[17])

        measures = fetch_records_by_record_id(self.id)
        if measures:
            self.ids.total_meas.text = "Всего измерений: " + str(len(measures))
        else:
            self.ids.total_meas.text = "Всего измерений: 0"
        

    def open_date_picker(self, focus):
        if not focus:
            return
        print("OPEN")
        if not self.dialog:
            self.dialog = MDModalDatePicker
            if self.dialog:
                self.date_picker = self.dialog(mode="picker", mark_today=True,)
                self.date_picker.bind(on_ok=self.on_ok, on_cancel=self.on_cancel, on_dismiss=self.on_dialog_dismiss)
                self.date_picker.pos = [
                    self.ids.date_field.center_x - self.date_picker.width / 2,
                    self.ids.date_field.y - (self.date_picker.height + dp(32)),
                ]
                
            self.date_picker.open() 

    def on_ok(self, *args):
        date_object_list = self.date_picker.get_date()
        date_object = date_object_list[0]
        formatted_date = date_object.strftime("%d.%m.%Y")
        print(formatted_date)
        self.text_date = formatted_date
        self.on_cancel()

    def on_cancel(self, *args):
        if self.date_picker:
            self.date_picker.dismiss()
      
    def on_dialog_dismiss(self, obj):
        self.dialog = None       

    def open_time_picker1(self, focus):
        if not focus:
            return
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        print("open_time_picker1")
        dialog = MDTimePickerDialVertical
        if dialog:
            self.time_picker1 = dialog(hour=str(hour),minute=str(minute),)
            self.time_picker1.bind(on_ok=self.time_ok1,on_cancel=self.time_cancel1,)
            self.time_picker1.open()

    def open_time_picker2(self, focus):
        if not focus:
            return
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        print("open_time_picker2")
        dialog = MDTimePickerDialVertical
        if dialog:
            self.time_picker2 = dialog(
                hour=str(hour),
                minute=str(minute),
            )
            self.time_picker2.bind(
                on_ok=self.time_ok2,
                on_cancel=self.time_cancel2,
            )
            self.time_picker2.open()

    def time_ok1(self, *args):
        time_str1 = self.time_picker1.time.strftime('%H:%M:%S')
        print(time_str1)
        self.text_time1 = time_str1
        self.time_cancel1()

    def time_ok2(self, *args):
        time_str2 = self.time_picker2.time.strftime('%H:%M:%S')
        print(time_str2)
        self.text_time2 = time_str2
        self.time_cancel2()

    def time_cancel1(self, *args):
        if self.time_picker1:
            self.time_picker1.dismiss()

    def time_cancel2(self, *args):
        if self.time_picker2:
            self.time_picker2.dismiss()

    def on_text_change(self, text):
        self.text_name = text
    def on_descr_change(self, text):
        self.text_description = text
    def on_presure_change(self, text):
        self.presure = text
    def on_temp_change(self, text):
        self.temp = text
    def on_hum_change(self, text):
        self.hum = text

    def save_record(self):
        text_err = ""
        if not self.text_time2:
            text_err = "Введите время окончания измерения"  
        if not self.text_time1:
            text_err = "Введите время начала измерения"
        if not self.text_date:
            text_err = "Введите дату измерения" 
        if not self.text_name:
            text_err = "Введите имя пробы" 
        if not self.text_description:
            text_err = "Введите описание объекта измерений"     
           
        if len(self.text_name) > 20:
            text_err = "Имя пробы превышает 20 символов"
        try:
            self.hum = float(self.hum)
        except:
            text_err = "Введено неправильное значение влажности"
        try:
            self.temp = float(self.temp)
        except:
            text_err = "Введено неправильное значение температуры"
        try:
            self.presure = float(self.presure)
        except:
            text_err = "Введено неправильное значение давления"
        print(self.presure, self.temp, self.hum)
        if text_err:
            MDDialog(
                MDDialogHeadlineText(text="Ошибка сохранения записи",),
                MDDialogSupportingText(text=text_err,),
            ).open()
            return
        print(self.text_name, self.text_description, 0, self.presure, self.temp, self.hum, self.text_date, self.text_time1, self.text_time2)
        update_record(self.id, self.text_name, self.text_description, 0, self.presure, self.temp, self.hum, 1, self.text_date, self.text_time1, self.text_time2)
        print(load_data()) 
        screen_manager = self.manager
        screen_manager.current = 'record'
#-------------------------------------------------- FolderRecordScreen ------------------------------------------------
class FolderRecordScreen(MDScreen):
    def on_enter(self):
        self.ids.custom_widget_box.clear_widgets()
        records = load_data()
        num_cards = 0
        if records:
            for card in records:
                if card[7] == 0: #is_active
                    date_txt = "Дата: " +  card[8] + "   Время: с " + card[9][:-3] + " по " + card[10][:-3]
                    self.add_card(card[1], date_txt, str(card[3]) + " измерений", get_color_from_hex("#70F490"))
            num_cards = len(self.ids.custom_widget_box.children)
        print("Number of cards:", num_cards)
                   
    def add_card(self, text1, text2, text3, color):
        print( text1, text2, text3)
        grid_layout = self.ids.custom_widget_box  # Accessing the MDGridLayout
        list_item = MDListItem()
        list_item.text1 = text1
        icon_btn = MDIconButton(icon="file-plus-outline",
                                pos_hint={'center_y': .5},
                                on_release=lambda x: self.icon_add_click(list_item))
        # MDListItemLeadingIcon(icon="information-outline", on_release=lambda x: self.icon_click(list_item))    
        headlineText = MDListItemHeadlineText(text=text1,)
        supportingText  = MDListItemSupportingText(text=text2,)
        TertiaryText = MDListItemTertiaryText(text=text3,)
        icon_btn1 = MDIconButton(icon="trash-can-outline",
                                pos_hint={'center_y': .5},
                                on_release=lambda x: self.icon_del_click(list_item))
        container = MDBoxLayout(size_hint_x = 0.1) #md_bg_color = get_color_from_hex("#70F490"),
        list_item.add_widget(icon_btn)
        list_item.add_widget(headlineText)
        list_item.add_widget(supportingText)
        list_item.add_widget(TertiaryText)
        list_item.add_widget(container)
        list_item.add_widget(icon_btn1)
        grid_layout.add_widget(list_item)

    def icon_del_click(self, list_item):
        if list_item:
            text1 = list_item.text1
            print("Deleted item:", text1)
            res = update_is_active(text1,0)
            if res:
                grid_layout = self.ids.custom_widget_box 
                grid_layout.remove_widget(list_item) 
    
    def icon_add_click(self, list_item):
        if list_item:
            text1 = list_item.text1
            print("Deleted item:", text1)
            res = update_is_active(text1, 1)
            if res:
                grid_layout = self.ids.custom_widget_box 
                grid_layout.remove_widget(list_item) 
#-------------------------------------------------- NewRecordScreen ------------------------------------------------
class NewRecordScreen(MDScreen):
    dialog = None
    warning =None
    date = ""
    time = ""

    def on_enter(self):
        self.text_date =  "Введите дату"
        self.text_time1 =  "Введите время"
        self.text_time2 =  "Введите время"
        self.text_name = ""
        self.text_description = ""
        
        self.entered_date = ""
        self.entered_time1 = ""
        self.entered_time2 = ""
        self.presure = None
        self.temp = None
        self.hum = None

    def open_date_picker(self, focus):
        if not focus:
            return
        print("OPEN")
        if not self.dialog:
            self.dialog = MDModalDatePicker
            if self.dialog:
                self.date_picker = self.dialog(
                    mode="picker",
                    mark_today=True,
                )
                self.date_picker.bind(
                    on_ok=self.on_ok,
                    on_cancel=self.on_cancel,
                    on_dismiss=self.on_dialog_dismiss
                )
                self.date_picker.pos = [
                    self.ids.date_field.center_x - self.date_picker.width / 2,
                    self.ids.date_field.y - (self.date_picker.height + dp(32)),
                ]
                
            self.date_picker.open() 

    def on_ok(self, *args):
        date_object_list = self.date_picker.get_date()
        date_object = date_object_list[0]
        formatted_date = date_object.strftime("%d.%m.%Y")
        print(formatted_date)
        self.text_date = formatted_date
        self.entered_date = date_object
        self.on_cancel()

    def on_cancel(self, *args):
        if self.date_picker:
            self.date_picker.dismiss()
      
    def on_dialog_dismiss(self, obj):
        self.dialog = None       

    def open_time_picker1(self, focus):
        if not focus:
            return
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        print("open_time_picker1")
        # dialog = MDTimePickerInput
        dialog = MDTimePickerDialVertical
        if dialog:
            self.time_picker1 = dialog(
                hour=str(hour),
                minute=str(minute),
            )
            self.time_picker1.bind(
                on_ok=self.time_ok1,
                on_cancel=self.time_cancel1,
            )
            self.time_picker1.open()

    def open_time_picker2(self, focus):
        if not focus:
            return
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        print("open_time_picker2")
        # dialog = MDTimePickerInput
        dialog = MDTimePickerDialVertical
        if dialog:
            self.time_picker2 = dialog(
                hour=str(hour),
                minute=str(minute),
            )
            self.time_picker2.bind(
                on_ok=self.time_ok2,
                on_cancel=self.time_cancel2,
            )
            self.time_picker2.open()

    def time_ok1(self, *args):
        time_str1 = self.time_picker1.time.strftime('%H:%M:%S')
        print(time_str1)
        self.text_time1 = time_str1
        self.entered_time1 = self.time_picker1.time
        self.time_cancel1()

    def time_ok2(self, *args):
        time_str2 = self.time_picker2.time.strftime('%H:%M:%S')
        print(time_str2)
        self.text_time2 = time_str2
        self.entered_time2 = self.time_picker2.time
        self.time_cancel2()

    def time_cancel1(self, *args):
        if self.time_picker1:
            self.time_picker1.dismiss()

    def time_cancel2(self, *args):
        if self.time_picker2:
            self.time_picker2.dismiss()

    def on_text_change(self, text):
        self.text_name = text
    def on_descr_change(self, text):
        self.text_description = text
    def on_presure_change(self, text):
        self.presure = text
    def on_temp_change(self, text):
        self.temp = text
    def on_hum_change(self, text):
        self.hum = text

    def save_record(self):
        text_err = ""
        if not self.entered_time2:
            text_err = "Введите время окончания измерения"  
        if not self.entered_time1:
            text_err = "Введите время начала измерения"
        if not self.entered_date:
            text_err = "Введите дату измерения" 
        if not self.text_name:
            text_err = "Введите имя пробы" 
        if not self.text_description:
            text_err = "Введите описание объекта измерений"     
           
        if len(self.text_name) > 20:
            text_err = "Имя пробы превышает 20 символов"
        try:
            self.hum = float(self.hum)
        except:
            text_err = "Введено неправильное значение влажности"
        try:
            self.temp = float(self.temp)
        except:
            text_err = "Введено неправильное значение температуры"
        try:
            self.presure = float(self.presure)
        except:
            text_err = "Введено неправильное значение давления"
        print(self.presure, self.temp, self.hum)
        if text_err:
            MDDialog(
                MDDialogHeadlineText(text="Ошибка сохранения записи",),
                MDDialogSupportingText(text=text_err,),
            ).open()
            return
        print(self.text_name, self.text_description, 0, self.presure, self.temp, self.hum, type(self.text_date), self.text_time1, self.text_time2)
        id = insert_record(self.text_name, self.text_description, 0, self.presure, self.temp, self.hum, self.text_date, self.text_time1, self.text_time2)
        if id == 0:
            MDDialog(
                MDDialogHeadlineText(text="Ошибка создания записи",),
                MDDialogSupportingText(text="Обратитесь к разработчику",),
            ).open()
        # insert_data(self.text_name, 0, file_name)
        print(load_data()) 
        screen_manager = self.manager
        screen_manager.current = 'record'
#-------------------------------------------------- RecordScreen ------------------------------------------------
class RecordScreen(MDScreen):
    def on_enter(self):
        self.ids.custom_widget_box.clear_widgets()
        records = load_data()
        num_cards = 0
        if records:
            for card in records:
                print(0,card[0], type(card[0]))
                if card[7] == 1: #is_active
                    date_txt = "Дата: " +  card[8] + "   Время: с " + card[9][:-3] + " по " + card[10][:-3]
                    measures = fetch_records_by_record_id(card[0])
                    if measures:
                        count = len(measures)
                    else:
                        count = 0
                    self.add_card(card[1], date_txt, str(count) + " измерений", get_color_from_hex("#70F490"))
            num_cards = len(self.ids.custom_widget_box.children)
        print("Number of cards:", num_cards)
            
    def add_card(self, text1, text2, text3, color):
        grid_layout = self.ids.custom_widget_box  # Accessing the MDGridLayout

        list_item = MDListItem()
        list_item.text1 = text1
        icon_btn = MDIconButton(icon="file-edit",
                                pos_hint={'center_y': .5},
                                on_release=lambda x: self.icon_edit_click(list_item))
        # MDListItemLeadingIcon(icon="information-outline", on_release=lambda x: self.icon_click(list_item))    
        headlineText = MDListItemHeadlineText(text=text1,)
        supportingText  = MDListItemSupportingText(text=text2,)
        TertiaryText = MDListItemTertiaryText(text=text3,)
        icon_btn1 = MDIconButton(icon="trash-can-outline",
                                pos_hint={'center_y': .5},
                                on_release=lambda x: self.icon_del_click(list_item))
        container = MDBoxLayout(size_hint_x = 0.1) #md_bg_color = get_color_from_hex("#70F490"),
        list_item.add_widget(icon_btn)
        list_item.add_widget(headlineText)
        list_item.add_widget(supportingText)
        list_item.add_widget(TertiaryText)
        list_item.add_widget(container)
        list_item.add_widget(icon_btn1)
        grid_layout.add_widget(list_item)
        

    def icon_del_click(self, list_item):
        if list_item:
            text1 = list_item.text1
            print("Deleted item:", text1)
            res = update_is_active(text1,0)
            if res:
                grid_layout = self.ids.custom_widget_box 
                grid_layout.remove_widget(list_item) 
    
    def icon_edit_click(self, list_item):
        if list_item:
            
            App.get_running_app().current_record = list_item.text1
            App.get_running_app().go_to_obj()
    
class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label1 = "Какой-то текст"

left_menu = [
    "Объект измерений", "Измерения", "Рабочее сечение и точки", "Ввод первичных данных",
    "Расчет плотности газа","Расчет влажности газа","Просмотр результатов",
    "Изокинетический отбор"
]
right_menu = [
    "Сохранить", "Сформировать отчет", "ОТправить", "Настройки"
]

#------------------------------------------------------------ APP -----------------------------------------
class Live(App, MDApp):
    current_record = None
    KV_FILES = {
        os.path.join(os.getcwd(), "login_screen.kv"),
        os.path.join(os.getcwd(), "record_screen.kv"),
        os.path.join(os.getcwd(), "new_record_screen.kv"),
        os.path.join(os.getcwd(), "folder_record_screen.kv"),
        os.path.join(os.getcwd(), "obj_record_screen.kv"),
        os.path.join(os.getcwd(), "meas_record_screen.kv"),
        os.path.join(os.getcwd(), "section_screen.kv"),
        os.path.join(os.getcwd(), "enter_data.kv"),
        os.path.join(os.getcwd(), "calc_dry.kv"),
        os.path.join(os.getcwd(), "view_result.kv"),
        os.path.join(os.getcwd(), "gost_result.kv"),
        os.path.join(os.getcwd(), "tube_result.kv"),
        os.path.join(os.getcwd(), "bt_screen.kv"),
        # os.path.join(os.getcwd(), "manager_screens.kv"),
        #!!!
    }

    CLASSES = {
        "ManagerScreens":"manager_screens",
        "LoginScreen":"login_screen",
        "RecordScreen":"record_screen",
        "NewRecordScreen":"new_record_screen",
        "ObjRecordScreen":"obj_record_screen",
        "MeasRecordScreen":"meas_record_screen",
        "SectionRecordScreen":"section_screen",
        "EnterDataScreen":"enter_data_screen",
        "CalcDryScreen":"calc_dry_screen", 
        "ResultScreen":"view_result", 
        "BtScreen":"bt_screen",
        #!!!
    }
    AUTORELOADER_PATHS = [(os.getcwd(), {"recursive": False})]

    AUTORELOADER_IGNORE_PATTERNS = ["*.pyc", "*__pycache__*", "*.pkl", "*.txt",]

    def build_app(self):
        create_table()
        # self.icon = 'icon.png'
        self.manager_screens = ManagerScreens()
        Window.bind(on_reyboard=self._rebuild)
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
        if not platform == 'android':
            Window.size = [1050, 1800]
        return self.manager_screens
    
    def _rebuild(self, *args):
        if args[1] == 32:
            self.rebuild()

    def open_left_menu(self, item, exclude):
        filtered_menu = left_menu#[i for idx, i in enumerate(left_menu) if idx != exclude]

        menu_items = [
            {
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.menu_l_callback(x),
            } for i in filtered_menu
        ]
        MDDropdownMenu(caller=item, items=menu_items).open()

    def open_right_menu(self, item):
        menu_items = [
            {
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.menu_r_callback(x),
            } for i in right_menu
        ]
        MDDropdownMenu(caller=item, items=menu_items).open()
    
    def menu_r_callback(self, text_item):
        # self.root.ids.drop_text.text = text_item
        print(text_item)
    
    def menu_l_callback(self, text_item):
        print(text_item) #!!!
        if text_item == left_menu[0]:
            self.go_to_obj()
        if text_item == left_menu[1]:
            self.go_to_meas()
        if text_item == left_menu[2]:
            self.go_to_section()
        if text_item == left_menu[3]:
            self.go_to_enter_data()
        if text_item == left_menu[4]:
            self.go_to_calc_dry()
        if text_item == left_menu[6]:
            self.go_to_result()
        
            
    def go_to_enter_data(self):
        self.manager_screens.current = 'enter_data_screen'

    def go_to_folder_recods(self):
        self.manager_screens.current = 'folder_record'
        screen2 = self.manager_screens.get_screen('folder_record')
        print(screen2)

    def go_to_recods(self):
        self.manager_screens.current = 'record'
        screen2 = self.manager_screens.get_screen('record')
        print(screen2)

    def go_to_newrecods(self):
        self.manager_screens.current = 'new_record'
        screen2 = self.manager_screens.get_screen('new_record')
        print(screen2)

    def go_to_login(self):
        self.manager_screens.current = 'login'
        screen2 = self.manager_screens.get_screen('login')
        print(screen2)
    def go_to_obj(self):
        self.manager_screens.current = 'obj_record'
    def go_to_meas(self):
        self.manager_screens.current = 'meas_record'
    def go_to_section(self):
        self.manager_screens.current = 'section_screen'
    def go_to_calc_dry(self):
        self.manager_screens.current = 'calc_dry_screen'
    def go_to_result(self):
        self.manager_screens.current = 'view_result'
    def go_to_gost(self):
        self.manager_screens.current = 'gost_screen'
    def go_to_tube(self):
        self.manager_screens.current = 'tube_screen'
    def go_to_bt(self):
        self.manager_screens.current = 'bt_screen'

    #!!!

    def hook_keyboard(self, window, key, *largs):
        go_to_obj_scr = ['meas_record', 'view_result', 'section_screen', 'enter_data_record', 'calc_dry_screen']
        go_to_rec_scr = ['new_record', 'folder_record', 'obj_record']
        go_to_res_scr = ['gost_screen', 'tube_screen']
        if key == 27:
            if self.manager_screens.current in go_to_rec_scr:
                self.go_to_recods()
            if self.manager_screens.current in go_to_obj_scr:
                self.go_to_obj()
            if self.manager_screens.current in go_to_res_scr:
                self.go_to_result()
            if self.manager_screens.current == 'bt_screen':
                self.go_to_meas()
        return True


Live().run()