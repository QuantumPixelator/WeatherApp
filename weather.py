import json
import requests
import customtkinter as ctk
import datetime as dt
from PIL import Image
from io import BytesIO
from customtkinter import CTkImage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.iconbitmap('weather.ico')
        self.title("Weather App")
        self.geometry("280x280")
        
        with open('config.json') as f:
            config = json.load(f)
            self.api_key = config['api_key']
            self.zip_code = config.get('zip_code', '')
        self.last_update_time = None
        self.alerts_window = None
        self.has_alerts = False
        self.alert_text = ""
        self.current_headlines = set()  # Track headlines currently being shown
        self.acknowledged_alerts = set()  # Store alert headlines that have been acknowledged
        self.has_unread_alerts = False  # Track if there are new/unread alerts
        # Load temperature icon from file
        self.temp_img = Image.open('thermometer.png')
        self.temp_icon = CTkImage(light_image=self.temp_img, size=(32, 32))
        # Load wind icon from file
        self.wind_img = Image.open('wind.png')
        self.wind_icon = CTkImage(light_image=self.wind_img, size=(32, 32))
        self.create_widgets()
        self.update_weather()
    
    def create_widgets(self):
        # Input frame for zip and button
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10)
        self.zip_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter Zip Code")
        self.zip_entry.pack(side="left", padx=5)
        if self.zip_code:
            self.zip_entry.insert(0, self.zip_code)
        self.fetch_button = ctk.CTkButton(self.input_frame, text="Go", command=self.fetch_weather, width=50)
        self.fetch_button.pack(side="left")

        # Location
        self.name_frame = ctk.CTkFrame(self)
        self.name_frame.pack(pady=2)
        self.name_prefix = ctk.CTkLabel(self.name_frame, text="", text_color="white")
        self.name_prefix.pack(side="left")
        self.name_label = ctk.CTkLabel(self.name_frame, text="", font=("Arial", 28, "bold"), text_color="#FFD700")
        self.name_label.pack(side="left")
        
        # Temperature
        self.temp_frame = ctk.CTkFrame(self)
        self.temp_frame.pack(pady=2)
        self.temp_icon_label = ctk.CTkLabel(self.temp_frame, text="", image=self.temp_icon)
        self.temp_icon_label.pack(side="left", padx=5)
        self.temp_prefix = ctk.CTkLabel(self.temp_frame, text="Temperature: ", text_color="#008CFF")
        self.temp_prefix.pack(side="left")
        self.temp_label = ctk.CTkLabel(self.temp_frame, text="")
        self.temp_label.pack(side="left")
        
        # Condition
        self.weather_frame = ctk.CTkFrame(self)
        self.weather_frame.pack(pady=2)
        self.icon_label = ctk.CTkLabel(self.weather_frame, text="", image=None)
        self.icon_label.pack(side="left", padx=5)
        self.weather_prefix = ctk.CTkLabel(self.weather_frame, text="Condition: ", text_color="#008CFF")
        self.weather_prefix.pack(side="left")
        self.weather_label = ctk.CTkLabel(self.weather_frame, text="", text_color="white")
        self.weather_label.pack(side="left")
        
        # Wind
        self.wind_frame = ctk.CTkFrame(self)
        self.wind_frame.pack(pady=2)
        self.wind_icon_label = ctk.CTkLabel(self.wind_frame, text="", image=self.wind_icon)
        self.wind_icon_label.pack(side="left", padx=5)
        self.wind_prefix = ctk.CTkLabel(self.wind_frame, text="Wind: ", text_color="#008CFF")
        self.wind_prefix.pack(side="left")
        self.wind_label = ctk.CTkLabel(self.wind_frame, text="", text_color="white")
        self.wind_label.pack(side="left")
        
        # Moon Phase
        self.moon_frame = ctk.CTkFrame(self)
        self.moon_frame.pack(pady=2)
        self.moon_prefix = ctk.CTkLabel(self.moon_frame, text="Moon Phase: ", text_color="#008CFF")
        self.moon_prefix.pack(side="left")
        self.moon_label = ctk.CTkLabel(self.moon_frame, text="", text_color="white")
        self.moon_label.pack(side="left")

        # Alert button
        self.alert_button = ctk.CTkButton(self, text="ALERT", command=lambda: self.show_alerts_window(self.alert_text), state="disabled", fg_color="transparent", text_color="gray", border_color="gray")
        self.alert_button.pack(pady=5)

        # Last update
        self.last_update_label = ctk.CTkLabel(self, text="", font=("Arial", 10))
        self.last_update_label.pack(pady=5)
        
    def fetch_weather(self):
        self.zip_code = self.zip_entry.get()
        if self.zip_code:
            self.update_weather()
    
    def fetch_alerts(self):
        if self.zip_code:
            url = f"http://api.weatherapi.com/v1/alerts.json?key={self.api_key}&q={self.zip_code}"
            try:
                response = requests.get(url)
                data = response.json()
                if 'alerts' in data and 'alert' in data['alerts'] and data['alerts']['alert']:
                    alerts = data['alerts']['alert']
                    alert_texts = []
                    self.current_headlines = set()
                    
                    for alert in alerts:
                        headline = alert.get('headline', 'Alert').strip()
                        msgtype = alert.get('msgtype', '')
                        severity = alert.get('severity', '')
                        urgency = alert.get('urgency', '')
                        areas = alert.get('areas', '')
                        alert_text = f"{headline}\nType: {msgtype}\nSeverity: {severity}\nUrgency: {urgency}\nAreas: {areas}\n"
                        alert_texts.append(alert_text)
                        self.current_headlines.add(headline)
                    
                    self.alert_text = "\n\n".join(alert_texts)
                    self.has_alerts = True
                    
                    # Check if there are any new alerts that haven't been acknowledged
                    new_alerts = self.current_headlines - self.acknowledged_alerts
                    self.has_unread_alerts = len(new_alerts) > 0
                    
                    # Remove acknowledged alerts that are no longer active
                    self.acknowledged_alerts = self.acknowledged_alerts & self.current_headlines
                    
                    # Configure button based on whether there are unread alerts
                    if self.has_unread_alerts:
                        self.alert_button.configure(state="normal", fg_color="red", text_color="white", border_color="red")
                    else:
                        # Still has alerts but they've been acknowledged
                        self.alert_button.configure(state="normal", fg_color="orange", text_color="white", border_color="orange")
                else:
                    # No alerts - clear everything
                    self.alert_text = ""
                    self.has_alerts = False
                    self.has_unread_alerts = False
                    self.current_headlines.clear()
                    self.acknowledged_alerts.clear()
                    self.alert_button.configure(state="disabled", fg_color="transparent", text_color="gray", border_color="gray")
            except Exception as e:
                # On error, don't clear existing alert data - just disable button if no alerts
                if not self.has_alerts:
                    self.alert_text = ""
                    self.has_alerts = False
                    self.has_unread_alerts = False
                    self.current_headlines.clear()
                    self.acknowledged_alerts.clear()
                    self.alert_button.configure(state="disabled", fg_color="transparent", text_color="gray", border_color="gray")
    
    def show_alerts_window(self, alert_text):
        if self.alerts_window is None or not self.alerts_window.winfo_exists():
            self.alerts_window = ctk.CTkToplevel(self)
            self.alerts_window.title("Weather Alerts")
            self.alerts_window.geometry(f"400x300+{self.winfo_x()}+{self.winfo_y()}")
            self.alerts_window.attributes('-topmost', True)
            self.alerts_window.grab_set()  # Make it modal
            
            # Alerts text
            self.alerts_textbox = ctk.CTkTextbox(self.alerts_window, wrap="word")
            self.alerts_textbox.pack(pady=10, padx=10, fill="both", expand=True)
            
            # Close button
            close_button = ctk.CTkButton(self.alerts_window, text="Close", command=self.close_alerts_window)
            close_button.pack(pady=5)
            
            # Handle window close
            self.alerts_window.protocol("WM_DELETE_WINDOW", self.close_alerts_window)
        
        self.alerts_textbox.delete("1.0", "end")
        self.alerts_textbox.insert("1.0", alert_text)
        self.alerts_window.lift()  # Bring to front
    
    def close_alerts_window(self):
        if self.alerts_window and self.alerts_window.winfo_exists():
            self.alerts_window.grab_release()
            self.alerts_window.destroy()
            self.alerts_window = None
        
        # Mark all current alerts as acknowledged
        if self.has_alerts:
            # Add all current headlines to acknowledged set
            self.acknowledged_alerts.update(self.current_headlines)
            
            # Mark as no longer having unread alerts
            self.has_unread_alerts = False
            
            # Change button to orange (acknowledged but still active)
            self.alert_button.configure(state="normal", fg_color="orange", text_color="white", border_color="orange")
    
    def update_weather(self):
        if self.zip_code:
            url = f"http://api.weatherapi.com/v1/current.json?key={self.api_key}&q={self.zip_code}"
            try:
                response = requests.get(url)
                data = response.json()
                if 'current' in data:
                    current = data['current']
                    temp = current['temp_f']
                    condition = current['condition']['text']
                    wind = current['wind_mph']
                    self.temp_label.configure(text=f"{temp}°F", text_color="white")
                    self.weather_label.configure(text=f"{condition}", text_color="white")
                    self.wind_label.configure(text=f"{wind} mph", text_color="white")
                    self.name_label.configure(text=f"{data['location']['name']}", text_color="#FFD700")
                    self.last_update_time = dt.datetime.now()
                    self.last_update_label.configure(text=f"Updated: {self.last_update_time.strftime('%I:%M %p').upper()}", text_color="gray")
                    
                    # Load weather icon
                    icon_url = "https:" + current['condition']['icon']
                    icon_response = requests.get(icon_url)
                    img = Image.open(BytesIO(icon_response.content))
                    photo = CTkImage(light_image=img, size=(32, 32))
                    self.icon_label.configure(image=photo)
                    
                                        # Fetch moon phase
                    moon_url = f"http://api.weatherapi.com/v1/astronomy.json?key={self.api_key}&q={self.zip_code}"
                    moon_response = requests.get(moon_url)
                    moon_data = moon_response.json()
                    moon_phase = ""
                    if 'astronomy' in moon_data and 'astro' in moon_data['astronomy']:
                        moon_phase = moon_data['astronomy']['astro'].get('moon_phase', "")
                    self.moon_label.configure(text=moon_phase, text_color="white")
                    
                    # Fetch alerts
                    self.fetch_alerts()
                    
                else:
                    self.temp_label.configure(text="Invalid zip code", text_color="white")
                    self.weather_label.configure(text="", text_color="white")
                    self.wind_label.configure(text="", text_color="white")
                    self.name_label.configure(text="", text_color="#FFD700")
                    self.last_update_label.configure(text="", text_color="gray")
                    self.icon_label.configure(image=None)
                    # Don't clear alerts on invalid zip - let them persist
            except Exception as e:
                self.temp_label.configure(text=f"{str(e)}", text_color="white")
                self.weather_label.configure(text="", text_color="white")
                self.wind_label.configure(text="", text_color="white")
                self.name_label.configure(text="", text_color="#FFD700")
                self.last_update_label.configure(text="", text_color="gray")
                self.icon_label.configure(image=None)
                # Don't clear alerts on error - let them persist
        # Schedule next update in 10 minutes
        self.after(600000, self.update_weather)

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()