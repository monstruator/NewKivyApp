from kaki.app import App 
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from mydb import *
from kivy.utils import platform
import math
from kivymd.uix.list import MDListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from threading import Thread
from kivymd.uix.button import MDIconButton
import struct
from kivy.clock import Clock
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)

if platform == 'android':
    try:
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        context = PythonActivity.mActivity
        BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
        BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
        BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
        UUID = autoclass('java.util.UUID')

    except:
        print('Error11')

class BtScreen(MDScreen):
    check_box_choise = 0
    id = 0
    thread_flag = False

    def on_enter(self):
        self.devs = []
        self.screen_width = MDApp.get_running_app().root.width
        self.screen_height = MDApp.get_running_app().root.height

        name =  App.get_running_app().current_record
        self.current_record = list(search_record(name))
        self.id = self.current_record[0]
        self.record_name = name
        print(self.record_name)
        self.esp32_devices = None
        if platform == 'android':
            try:
                bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
                if bluetooth_adapter:
                    paired_devices = bluetooth_adapter.getBondedDevices().toArray()
                    self.esp32_devices = [device for device in paired_devices if "SB-1" in device.getName()]
                    for widget in self.ids.custom_widget_box.children[:]:
                        if hasattr(widget, 'id') and "table_item" in widget.id:
                            self.ids.custom_widget_box.remove_widget(widget)
                    for device in self.esp32_devices:
                        self.devs.append(device.getName())
                        print(device.getName())
                        self.add_card(device.getName())
                else:
                    print("Bluetooth is not available on this device.")
            except Exception as e:
                print("Error:", e)
        else:
            for widget in self.ids.custom_widget_box.children[:]:
                if hasattr(widget, 'id') and "table_item" in widget.id:
                    self.ids.custom_widget_box.remove_widget(widget)
            self.esp32_devices = ["SB1 №122", "SB1 №123", "SB1 №124", "SB1 №125"]
            for device in self.esp32_devices:
                        # self.devs.append(device.getName())
                        # print(device.getName())
                        self.add_card(device)

        print("esp32_devices ", self.esp32_devices)               
#-----------------------------------------------------------------------------------------------------     
#-----------------------------------------------------------------------------------------------------
    def add_card(self, name):
        list_item = MDBoxLayout(
            id = "table_item" + name,
            md_bg_color = get_color_from_hex("#C4C4FF"), 
            adaptive_height=True,  
            spacing="2dp", padding=["0dp", "20dp", "0dp", "20dp"]) 
        
        container = MDBoxLayout(
            # md_bg_color=get_color_from_hex("#F00490"),
            size_hint_x=None,
            width=self.screen_width / 2,  # Adjust the width as needed
            # theme_bg_color="Custom",
            # padding=["15dp", "20dp", "0dp", "20dp"]
        )
        label = MDLabel(text=name, markup = True, font_style="Body", role="small", halign='center')  # Adjust the width as needed
        container.add_widget(label)
        list_item.add_widget(container)

        icon_btn1 = MDIconButton(icon="cloud-download",
                            pos_hint={'center_x': .1, 'center_y': .5},
                            on_release=lambda x: self.icon_del_click(name),
                            size_hint_x=None, width=self.screen_width / 3,
                            )
        
        widget_center = Widget()
        widget_center1 = Widget()
        container1 = MDBoxLayout(
            # md_bg_color=get_color_from_hex("#F00490"),
            size_hint_x=None,
            width=self.screen_width / 3,  # Adjust the width as needed
            # theme_bg_color="Custom",
            # padding=["15dp", "20dp", "0dp", "20dp"]
        )
        container1.add_widget(widget_center)
        container1.add_widget(icon_btn1)
        container1.add_widget(widget_center1)
        list_item.add_widget(container1)
        self.ids.custom_widget_box.add_widget(list_item)

#----------------------------------------------------------------------------------------------------
    def icon_del_click(self, name):
        # print(name, self.esp32_devices)
        # index = self.esp32_devices.index(name)
        # print(name, index)

        self.dev = name
        self.thread_flag = True
        # for widget in self.ids.custom_widget_box.children[:]:
        #     if hasattr(widget, 'id') and name in widget.id:
        #         self.widget_tabed = widget
        #         self.widget_tabed.md_bg_color = get_color_from_hex("#84C48F")
        #         print(self.widget_tabed.id, name)
        #         break 
        Thread(target=self.receive_data).start()
#----------------------------------------------------------------------------------------------------
    def receive_data(self):
        if platform == 'android':
            data_size = 4541
            data_size_mini = 1041
            packet_size = 0
            received_data = bytearray(data_size)
            received_packet = bytearray()
            format_string = '<25si3i' + '5f' * 225
            format_string_mini = '<25si3i' + '5f' * 50
            try:
                bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
                if bluetooth_adapter:
                    paired_devices = bluetooth_adapter.getBondedDevices().toArray()
                    for device in paired_devices:
                        if self.dev == device.getName(): #совпало имя из файла и из списка
                            print("TRY CONNECT TO ", device.getName()) 
                            self.socket = device.createRfcommSocketToServiceRecord(UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
                            self.socket.connect()
                            print("Connected to device:", device.getName())
                            Clock.schedule_once(lambda dt: self.update_screen2()) 
                            while self.thread_flag:
                                bytes_read = self.socket.getInputStream().read(received_data)
                                if bytes_read > 20:
                                    packet_size = packet_size + bytes_read
                                    received_packet += received_data[:bytes_read]
                                    print(bytes_read, packet_size)
                                    if packet_size > data_size:
                                        packet_size = 0
                                        received_packet = b'' 
                                    if packet_size == data_size:
                                        print("received_packet in format_string")
                                        data = struct.unpack(format_string, received_packet)
                                        Clock.schedule_once(lambda dt: self.update_screen3(data))
                                        packet_size = 0
                                        received_packet = b'' 
                                    if packet_size == data_size_mini:
                                        print("received_packet in format_string_mini")
                                        data = struct.unpack(format_string_mini, received_packet)
                                        Clock.schedule_once(lambda dt: self.update_screen3(data))
                                        received_packet = b'' 
                                        packet_size = 0

            except Exception as e:
                print("Error receiving data:", e)
                Clock.schedule_once(lambda dt: self.update_screen1())

    def update_screen1(self):
        name = self.dev
        for widget in self.ids.custom_widget_box.children[:]:
            if hasattr(widget, 'id') and name in widget.id:
                self.widget_tabed = widget
                self.widget_tabed.md_bg_color = get_color_from_hex("#C4848F")
                print(self.widget_tabed.id, name)
                break 

    def update_screen2(self):
        name = self.dev
        for widget in self.ids.custom_widget_box.children[:]:
            if hasattr(widget, 'id') and name in widget.id:
                self.widget_tabed = widget
                self.widget_tabed.md_bg_color = get_color_from_hex("#84C48F")
                print(self.widget_tabed.id, name)
                break 

    def update_screen3(self, data):
    # def update_screen3(self):
        f_name = data[0].decode().strip()
        count_mes = data[1]
        # f_name = '/2024/02/09/17_11_39'
        # count_mes = 15
        print(f_name, count_mes)
        float_data = data[5:]
        errores1= 0
        for i in range(0,count_mes):
            group_float_data = float_data[i*5:(i+1)*5]
            p1 = group_float_data[0]
            p2 = group_float_data[1]
            p3 = group_float_data[2]
            p4 = 0 #float(self.ids.p4n.text)
            p5 = 0 #float(self.ids.p5n.text)
            n_point = 0
            in_calc = 1
            measurement_details = (p1, p2, p3, p4, p5, n_point, in_calc)
            
            if not add_measurement(self.id, measurement_details):
                errores1 = errores1 + 1
                
        if errores1==0:
            MDDialog(
                MDDialogHeadlineText(text="Данные получены и сохранены",),
                MDDialogSupportingText(text="Успешно",),
            ).open()  
        
        else:
            MDDialog(
                MDDialogHeadlineText(text="Данные получены",),
                MDDialogSupportingText(text="Во время добавления данных произошла ошибка",),
            ).open()
            
            

            print(f"Group {i+1}:", group_float_data)
        # Clock.schedule_once(lambda dt: self.add_seria_card(f_name, count_mes))
            
    def on_stop(self):
        self.thread_flag = False