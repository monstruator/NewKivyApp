from kaki.app import App 
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.screen import MDScreen
from mydb import *
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)



class SectionScreen(MDScreen):
    id = None
    current_record = None

    def on_enter(self):
        name =  App.get_running_app().current_record
        self.current_record = search_record(name)
        self.id = self.current_record[0]
        self.ids.proba_name_bar.text = self.current_record[1]
        print("Edit meas for item:",self.current_record) 
        measures = fetch_records_by_record_id(self.id)
        