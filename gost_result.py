from kaki.app import App 
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from mydb import *
from kivy.utils import platform
import math

if platform == 'android':
    try:
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        context = PythonActivity.mActivity
    except:
        print('Error11')

class GostScreen(MDScreen):
    check_box_choise = 0
    id = 0

    def on_enter(self):
        self.screen_width = MDApp.get_running_app().root.width
        self.screen_height = MDApp.get_running_app().root.height

        name =  App.get_running_app().current_record
        self.current_record = list(search_record(name))
        self.id = self.current_record[0]
        measures = fetch_records_by_record_id(self.id)

        # print(measures)
        Pdk = 0
        Ppoln = 0
        Pct = 0
        Alfa = 0
        count_meas = 0
        try:
            for meas in measures:
                if meas[8] == 1: #in_calc
                    Pdk += math.sqrt(meas[3] * self.current_record[18])
                    Ppoln += meas[4]
                    Pct += meas[4] - (meas[2] * self.current_record[19])
                    if not self.current_record[18] == 0 and not meas[3] == 0:
                        Alfa += math.sqrt((meas[2]*self.current_record[19])/(meas[3]*self.current_record[18]))
                    count_meas += 1
            Pdk = (Pdk / count_meas) ** 2
            Ppoln = Ppoln / count_meas
            Pct = Pct / count_meas
            Alfa = Alfa / count_meas

            self.ids.box1.text2 = str(int(Pdk)) + " Па"
            self.ids.box2.text2 = str(int(Ppoln)) + " Па"
            self.ids.box3.text2 = str(int(Pct)) + " Па"
            self.ids.box4.text2 = f"{Alfa:.2f}"


        except:
            print("Math error")
        Pgsnu = 0
        if self.current_record[23] == 0:
            Pgsnu = 1.293
        elif self.current_record[23] == 1:
            Pgsnu = self.current_record[21]
        elif self.current_record[23] == 2:
            Pgsnu = self.current_record[25]
        self.ids.box5.text2 = f"{self.current_record[25]:.2f}" + " г/м³"

        F = 0
        if self.current_record[24] == 0:
            F = 0
        elif self.current_record[24] == 1:
            F = self.current_record[22]
        elif self.current_record[24] == 2:
            F = self.current_record[26]

        Pgvlnu = (Pgsnu + F/1000)*0.804 / (0.804 + F/1000)
        self.ids.box6.text2 = f"{Pgvlnu:.2f}" + " г/м³"

        Pgvlru = Pgvlnu * 273 * (self.current_record[4] + Pct/1000) / (101.3 * (273 + self.current_record[5]))
        self.ids.box7.text2 = f"{Pgvlru:.2f}" + " кг/м³"

        Usr = Alfa * math.sqrt(2*Pdk/Pgvlru)
        self.ids.box8.text2 = f"{Usr:.2f}" + " м/с"

        if self.current_record[12] == 0:
            area = math.pi * (self.current_record[13] ** 2) / 4
        else:
            area = self.current_record[14] * self.current_record[15]
        Vgvlru = Usr * area
        self.ids.box9.text2 = f"{Vgvlru:.2f}" + " м³/с"

        Vgsru = Vgvlru * 0.804 / (0.804 + F/1000)
        self.ids.box10.text2 = f"{Vgsru:.2f}" + " м³/с"

        Vgsnu = Vgsru *273 * (self.current_record[4] + Pct/1000) / (101.3* (273 + self.current_record[5]))
        self.ids.box11.text2 = f"{Vgsnu:.2f}" + " м³/с"

        if platform == 'android':
            try:
                configuration = context.getResources().getConfiguration()
                font_scale = configuration.fontScale
                
                print("font_scale ", font_scale)
                if font_scale > 1.5:
                    self.ids.label_top.role = "small"
                    self.ids.label_top.font_style =  "Title"
                elif font_scale > 1.2:
                    self.ids.label_top.role = "medium"
                    self.ids.label_top.font_style =  "Hedline"
                else:
                    self.ids.label_top.role = "large"
                    self.ids.label_top.font_style = "Hedline"

            except Exception as e:
                print('Error get font_scale')

        
        
        


        # self.ids.proba_name_bar.text = self.current_record[1]
        # self.ids.part_len.text = str(self.current_record[11]) #part_len
        # print("switch active = ", self.current_record[16])
        # self.ids.double_poins_id.active = self.current_record[16]
        # #print("Form1: ",self.current_record[12]) 
        # # measures = fetch_records_by_record_id(self.id)
        
        # if self.current_record[12] == 0:
        #     self.ids.circle_checkbox.active = True
        #     self.ids.rectangle_checkbox.active = False
        #     self.add_circle_main_layout()
        # else:
        #     self.ids.circle_checkbox.active = False
        #     self.ids.rectangle_checkbox.active = True
        #     self.add_rectangle_main_layout()

    def on_checkbox_active(self, checkbox):
        if not self.check_box_choise == checkbox:
            self.check_box_choise = checkbox
            print(self.check_box_choise)
                
    

