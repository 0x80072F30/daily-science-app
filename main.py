from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.pickers import MDTimePicker
from kivy.uix.screenmanager import ScreenManager
from db_manager import DBManager

class FirstTimeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        title = MDLabel(
            text="Welcome to Daily Science!",
            font_style="H4",
            halign="center"
        )
        subtitle = MDLabel(
            text="Set your daily notification time for NDA science facts.",
            font_style="Body1",
            halign="center"
        )
        
        self.time_btn = MDRaisedButton(
            text="Select Time (Default 07:00 AM)",
            pos_hint={'center_x': 0.5},
            on_release=self.show_time_picker
        )
        
        self.selected_time = "07:00"
        
        save_btn = MDRaisedButton(
            text="Get Started",
            pos_hint={'center_x': 0.5},
            on_release=self.save_and_continue
        )
        
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(self.time_btn)
        layout.add_widget(save_btn)
        self.add_widget(layout)

    def show_time_picker(self, instance):
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.on_time_save)
        time_dialog.open()

    def on_time_save(self, instance, time_obj):
        self.selected_time = time_obj.strftime("%H:%M")
        self.time_btn.text = f"Selected Time: {self.selected_time}"

    def save_and_continue(self, instance):
        app = MDApp.get_running_app()
        app.db.update_setup(self.selected_time)
        app.sm.current = 'home'

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15)
        self.add_widget(self.layout)

    def on_enter(self):
        self.layout.clear_widgets()
        app = MDApp.get_running_app()
        
        streak = app.db.update_streak()
        fact_data = app.db.get_daily_fact()

        streak_label = MDLabel(
            text=f"🔥 Daily Streak: {streak} Days",
            font_style="H6",
            halign="center",
            size_hint_y=None,
            height=40
        )
        self.layout.add_widget(streak_label)

        if fact_data:
            card = MDCard(orientation='vertical', padding=15, spacing=10, elevation=4)
            
            category = MDLabel(text=f"[{fact_data[3]} - {fact_data[5]}]", font_style="Subtitle2", theme_text_color="Secondary")
            fact = MDLabel(text=fact_data[1], font_style="H6")
            explanation = MDLabel(text=fact_data[2], font_style="Body1")
            nda_note = MDLabel(text=f"📌 NDA Exam Tip: {fact_data[4]}", font_style="Caption", theme_text_color="Hint")

            card.add_widget(category)
            card.add_widget(fact)
            card.add_widget(explanation)
            card.add_widget(nda_note)
            self.layout.add_widget(card)

        refresh_btn = MDFlatButton(
            text="Next Fact",
            pos_hint={'center_x': 0.5},
            on_release=lambda x: self.on_enter()
        )
        self.layout.add_widget(refresh_btn)

class DailyScienceApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.db = DBManager()
        self.sm = ScreenManager()

        user_data = self.db.get_user_data()
        setup_completed = user_data[1] if user_data else 0

        self.sm.add_widget(FirstTimeScreen(name='first_time'))
        self.sm.add_widget(HomeScreen(name='home'))

        if setup_completed:
            self.sm.current = 'home'
        else:
            self.sm.current = 'first_time'

        return self.sm

    def on_stop(self):
        self.db.close()

if __name__ == '__main__':
    DailyScienceApp().run()
