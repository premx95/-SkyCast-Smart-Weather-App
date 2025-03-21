import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime
from PIL import Image, ImageTk
import io
import urllib.request
from ttkthemes import ThemedTk

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Forecast App")
        self.root.geometry("900x600")
        self.root.minsize(900, 600)
        
        # API Key (You should store this securely in a real application)
        self.api_key = "b548bf7c27975dd12098207b8274e5ea"
        
        # Cache for weather icons
        self.icon_cache = {}
        
        # Create frames
        self.create_frames()
        
        # Create UI elements
        self.create_header()
        self.create_search_bar()
        self.create_current_weather_display()
        self.create_forecast_display()
        self.create_footer()
        
        # Set default city
        self.default_city = "London"
        self.search_entry.insert(0, self.default_city)
        self.get_weather()
    
    def create_frames(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header frame
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search frame
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(fill=tk.X, pady=10)
        
        # Current weather frame
        self.current_weather_frame = ttk.Frame(self.main_frame)
        self.current_weather_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Forecast frame
        self.forecast_frame = ttk.Frame(self.main_frame)
        self.forecast_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Footer frame
        self.footer_frame = ttk.Frame(self.main_frame)
        self.footer_frame.pack(fill=tk.X, pady=(10, 0))
    
    def create_header(self):
        # App title
        title_label = ttk.Label(self.header_frame, text="Weather Forecast", font=("Helvetica", 24, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # Time and date
        self.datetime_label = ttk.Label(self.header_frame, text="", font=("Helvetica", 12))
        self.datetime_label.pack(side=tk.RIGHT)
        self.update_datetime()
    
    def update_datetime(self):
        now = datetime.now()
        date_string = now.strftime("%A, %B %d, %Y  %H:%M:%S")
        self.datetime_label.config(text=date_string)
        self.root.after(1000, self.update_datetime)
    
    def create_search_bar(self):
        # Search label
        search_label = ttk.Label(self.search_frame, text="Enter City:", font=("Helvetica", 12))
        search_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Search entry
        self.search_entry = ttk.Entry(self.search_frame, width=30, font=("Helvetica", 12))
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry.bind('<Return>', lambda event: self.get_weather())
        
        # Search button
        search_button = ttk.Button(self.search_frame, text="Search", command=self.get_weather)
        search_button.pack(side=tk.LEFT)
    
    def create_current_weather_display(self):
        # Create container for current weather
        self.current_container = ttk.LabelFrame(self.current_weather_frame, text="Current Weather", padding="10")
        self.current_container.pack(fill=tk.BOTH, expand=True)
        
        # City and country
        self.city_label = ttk.Label(self.current_container, text="", font=("Helvetica", 18, "bold"))
        self.city_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Weather icon
        self.weather_icon_label = ttk.Label(self.current_container)
        self.weather_icon_label.grid(row=1, column=0, rowspan=2, padx=(0, 20))
        
        # Temperature
        self.temp_label = ttk.Label(self.current_container, text="", font=("Helvetica", 36))
        self.temp_label.grid(row=1, column=1, sticky="w")
        
        # Weather description
        self.description_label = ttk.Label(self.current_container, text="", font=("Helvetica", 14))
        self.description_label.grid(row=2, column=1, sticky="w")
        
        # Weather details frame
        details_frame = ttk.Frame(self.current_container)
        details_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0), sticky="w")
        
        # Weather details
        self.feels_like_label = ttk.Label(details_frame, text="", font=("Helvetica", 12))
        self.feels_like_label.grid(row=0, column=0, sticky="w", padx=(0, 30))
        
        self.humidity_label = ttk.Label(details_frame, text="", font=("Helvetica", 12))
        self.humidity_label.grid(row=0, column=1, sticky="w", padx=(0, 30))
        
        self.wind_label = ttk.Label(details_frame, text="", font=("Helvetica", 12))
        self.wind_label.grid(row=1, column=0, sticky="w", padx=(0, 30), pady=(10, 0))
        
        self.pressure_label = ttk.Label(details_frame, text="", font=("Helvetica", 12))
        self.pressure_label.grid(row=1, column=1, sticky="w", padx=(0, 30), pady=(10, 0))
    
    def create_forecast_display(self):
        # Create container for forecast
        self.forecast_container = ttk.LabelFrame(self.forecast_frame, text="5-Day Forecast", padding="10")
        self.forecast_container.pack(fill=tk.BOTH, expand=True)
        
        # Frame to hold forecast cards
        self.forecast_cards_frame = ttk.Frame(self.forecast_container)
        self.forecast_cards_frame.pack(fill=tk.X, expand=True)
        
        # Create 5 empty forecast card frames
        self.forecast_cards = []
        for i in range(5):
            card_frame = ttk.Frame(self.forecast_cards_frame, padding="10")
            card_frame.grid(row=0, column=i, padx=5, sticky="nsew")
            
            day_label = ttk.Label(card_frame, text="", font=("Helvetica", 12, "bold"))
            day_label.pack(pady=(0, 5))
            
            icon_label = ttk.Label(card_frame)
            icon_label.pack(pady=(0, 5))
            
            temp_label = ttk.Label(card_frame, text="", font=("Helvetica", 14))
            temp_label.pack(pady=(0, 5))
            
            desc_label = ttk.Label(card_frame, text="", font=("Helvetica", 10))
            desc_label.pack(pady=(0, 5))
            
            self.forecast_cards.append({
                "frame": card_frame,
                "day": day_label,
                "icon": icon_label,
                "temp": temp_label,
                "desc": desc_label
            })
        
        # Make forecast cards evenly spaced
        for i in range(5):
            self.forecast_cards_frame.columnconfigure(i, weight=1)
    
    def create_footer(self):
        # Credits
        credits_label = ttk.Label(self.footer_frame, text="Powered by OpenWeatherMap API", font=("Helvetica", 10))
        credits_label.pack(side=tk.LEFT)
        
        # Version
        version_label = ttk.Label(self.footer_frame, text="v1.0.0", font=("Helvetica", 10))
        version_label.pack(side=tk.RIGHT)
    
    def get_weather(self):
        city = self.search_entry.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return
        
        # Show loading message
        self.city_label.config(text="Loading...")
        self.temp_label.config(text="")
        self.description_label.config(text="")
        self.root.update()
        
        try:
            # Fetch current weather
            current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            current_response = requests.get(current_url)
            current_data = json.loads(current_response.text)
            
            if current_response.status_code != 200:
                error_message = current_data.get('message', 'Unknown error')
                messagebox.showerror("Error", f"Could not fetch weather data: {error_message}")
                return
            
            # Fetch 5-day forecast
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.api_key}&units=metric"
            forecast_response = requests.get(forecast_url)
            forecast_data = json.loads(forecast_response.text)
            
            # Update UI with current weather data
            self.update_current_weather(current_data)
            
            # Update UI with forecast data
            self.update_forecast(forecast_data)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def update_current_weather(self, data):
        # Update city name and country
        city_name = data['name']
        country_code = data['sys']['country']
        self.city_label.config(text=f"{city_name}, {country_code}")
        
        # Update temperature
        temp = data['main']['temp']
        self.temp_label.config(text=f"{temp:.1f}°C")
        
        # Update weather description
        weather_desc = data['weather'][0]['description'].capitalize()
        self.description_label.config(text=weather_desc)
        
        # Update weather icon
        icon_code = data['weather'][0]['icon']
        self.update_weather_icon(self.weather_icon_label, icon_code, size=100)
        
        # Update weather details
        feels_like = data['main']['feels_like']
        self.feels_like_label.config(text=f"Feels like: {feels_like:.1f}°C")
        
        humidity = data['main']['humidity']
        self.humidity_label.config(text=f"Humidity: {humidity}%")
        
        wind_speed = data['wind']['speed']
        self.wind_label.config(text=f"Wind: {wind_speed} m/s")
        
        pressure = data['main']['pressure']
        self.pressure_label.config(text=f"Pressure: {pressure} hPa")
    
    def update_forecast(self, data):
        # Get forecast data at 12:00 for the next 5 days
        daily_forecasts = []
        date_set = set()
        
        for item in data['list']:
            dt = datetime.fromtimestamp(item['dt'])
            date_str = dt.strftime("%Y-%m-%d")
            
            # Only take one forecast per day (around noon)
            if date_str not in date_set and "12:00" in dt.strftime("%H:%M"):
                date_set.add(date_str)
                daily_forecasts.append(item)
                
                if len(daily_forecasts) >= 5:
                    break
        
        # If we couldn't get 5 days with 12:00 forecasts, just take the first forecast of each day
        if len(daily_forecasts) < 5:
            date_set.clear()
            daily_forecasts.clear()
            
            for item in data['list']:
                dt = datetime.fromtimestamp(item['dt'])
                date_str = dt.strftime("%Y-%m-%d")
                
                if date_str not in date_set:
                    date_set.add(date_str)
                    daily_forecasts.append(item)
                    
                    if len(daily_forecasts) >= 5:
                        break
        
        # Update forecast cards
        for i, forecast in enumerate(daily_forecasts):
            if i < len(self.forecast_cards):
                card = self.forecast_cards[i]
                
                # Update day
                dt = datetime.fromtimestamp(forecast['dt'])
                card['day'].config(text=dt.strftime("%A"))
                
                # Update icon
                icon_code = forecast['weather'][0]['icon']
                self.update_weather_icon(card['icon'], icon_code, size=50)
                
                # Update temperature
                temp = forecast['main']['temp']
                card['temp'].config(text=f"{temp:.1f}°C")
                
                # Update description
                weather_desc = forecast['weather'][0]['description'].capitalize()
                card['desc'].config(text=weather_desc)
    
    def update_weather_icon(self, label, icon_code, size=50):
        try:
            # Check if icon is already in cache
            if icon_code in self.icon_cache and size in self.icon_cache[icon_code]:
                label.config(image=self.icon_cache[icon_code][size])
                return
            
            # Fetch icon from OpenWeatherMap
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            with urllib.request.urlopen(icon_url) as response:
                image_data = response.read()
            
            # Create and resize image
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((size, size), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Cache the icon
            if icon_code not in self.icon_cache:
                self.icon_cache[icon_code] = {}
            self.icon_cache[icon_code][size] = photo
            
            # Update the label
            label.config(image=photo)
            
        except Exception as e:
            print(f"Error loading weather icon: {str(e)}")
            label.config(image='')

if __name__ == "__main__":
    # Create themed root window
    root = ThemedTk(theme="arc")
    
    # Create app
    app = WeatherApp(root)
    
    # Start main loop
    root.mainloop()