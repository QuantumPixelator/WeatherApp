import json
import requests
import customtkinter as ctk
import datetime as dt

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.iconbitmap('weather.ico')
        self.title("Weather App")
        self.geometry("280x240")
        
        with open('config.json') as f:
            self.api_key = json.load(f)['api_key']
        
        self.zip_code = ""
        self.last_update_time = None
        self.create_widgets()
        self.update_weather()
    
    def create_widgets(self):
        # Input frame for zip and button
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10)
        self.zip_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter Zip Code")
        self.zip_entry.pack(side="left", padx=5)
        self.fetch_button = ctk.CTkButton(self.input_frame, text="Go", command=self.fetch_weather, width=50)
        self.fetch_button.pack(side="left")

        # Location
        self.name_frame = ctk.CTkFrame(self)
        self.name_frame.pack(pady=2)
        self.name_prefix = ctk.CTkLabel(self.name_frame, text="")
        self.name_prefix.pack(side="left")
        self.name_label = ctk.CTkLabel(self.name_frame, text="", font=("Arial", 28, "bold"))
        self.name_label.pack(side="left")
        
        # Temperature
        self.temp_frame = ctk.CTkFrame(self)
        self.temp_frame.pack(pady=2)
        self.temp_prefix = ctk.CTkLabel(self.temp_frame, text="Temperature: ")
        self.temp_prefix.pack(side="left")
        self.temp_label = ctk.CTkLabel(self.temp_frame, text="")
        self.temp_label.pack(side="left")
        
        # Condition
        self.weather_frame = ctk.CTkFrame(self)
        self.weather_frame.pack(pady=2)
        self.weather_prefix = ctk.CTkLabel(self.weather_frame, text="Condition: ")
        self.weather_prefix.pack(side="left")
        self.weather_label = ctk.CTkLabel(self.weather_frame, text="")
        self.weather_label.pack(side="left")
        
        # Humidity
        self.humidity_frame = ctk.CTkFrame(self)
        self.humidity_frame.pack(pady=2)
        self.humidity_prefix = ctk.CTkLabel(self.humidity_frame, text="Humidity: ")
        self.humidity_prefix.pack(side="left")
        self.humidity_label = ctk.CTkLabel(self.humidity_frame, text="")
        self.humidity_label.pack(side="left")
        
        # Wind
        self.wind_frame = ctk.CTkFrame(self)
        self.wind_frame.pack(pady=2)
        self.wind_prefix = ctk.CTkLabel(self.wind_frame, text="Wind: ")
        self.wind_prefix.pack(side="left")
        self.wind_label = ctk.CTkLabel(self.wind_frame, text="")
        self.wind_label.pack(side="left")

        # Last update
        self.last_update_label = ctk.CTkLabel(self, text="", font=("Arial", 10))
        self.last_update_label.pack(pady=5)

        
    
    def fetch_weather(self):
        self.zip_code = self.zip_entry.get()
        if self.zip_code:
            self.update_weather()
    
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
                    humidity = current['humidity']
                    wind = current['wind_mph']
                    if temp <= 32:
                        color = "#155EE7"
                    elif temp >= 85:
                        color = "#FF0000"
                    else:
                        color = "#90EE90"
                    self.temp_label.configure(text=f"{temp}°F", text_color=color)
                    self.weather_label.configure(text=f"{condition}", text_color="#FFA500")
                    self.humidity_label.configure(text=f"{humidity}%", text_color="#00FFFF")
                    self.wind_label.configure(text=f"{wind} mph", text_color="#FF00FF")
                    self.name_label.configure(text=f"{data['location']['name']}", text_color="#F6FA00")
                    self.last_update_time = dt.datetime.now()
                    self.last_update_label.configure(text=f"Updated: {self.last_update_time.strftime('%I:%M %p').upper()}", text_color="gray")
                else:
                    self.temp_label.configure(text="Invalid zip code", text_color="white")
                    self.weather_label.configure(text="", text_color="white")
                    self.humidity_label.configure(text="", text_color="white")
                    self.wind_label.configure(text="", text_color="white")
                    self.name_label.configure(text="", text_color="white")
                    self.last_update_label.configure(text="", text_color="gray")
            except Exception as e:
                self.temp_label.configure(text=f"{str(e)}", text_color="white")
                self.weather_label.configure(text="", text_color="white")
                self.humidity_label.configure(text="", text_color="white")
                self.wind_label.configure(text="", text_color="white")
                self.name_label.configure(text="", text_color="white")
                self.last_update_label.configure(text="", text_color="gray")
        # Schedule next update in 10 minutes
        self.after(600000, self.update_weather)

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()