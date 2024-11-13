import tkinter as tk
from tkinter import messagebox
import requests
import time
from PIL import Image, ImageTk

def getWeather(event=None):
    city = textField.get().strip()
    if not city:
        messagebox.showwarning("Warning", "Please enter a city name.")
        return

    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=06c921750b9a82d8f5d1294e1586276f"
    
    try:
        loading_label.config(text="Loading...")
        json_data = requests.get(api).json()
        
        if json_data.get("cod") != 200:
            messagebox.showerror("Error", f"City '{city}' not found.")
            loading_label.config(text="")
            return
        
        condition = json_data['weather'][0]['main']
        icon = json_data['weather'][0]['icon']
        temp = int(json_data['main']['temp'] - 273.15)
        min_temp = int(json_data['main']['temp_min'] - 273.15)
        max_temp = int(json_data['main']['temp_max'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']
        sunset = time.strftime('%I:%M %p', time.gmtime(json_data['sys']['sunset'] - 21600))
        sunrise = time.strftime('%I:%M %p', time.gmtime(json_data['sys']['sunrise'] - 21600))

        final_info = f"{condition}\n{temp}°C"
        final_data = (
            f"Min Temp: {min_temp}°C\n"
            f"Max Temp: {max_temp}°C\n"
            f"Pressure: {pressure} hPa\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind} m/s\n"
            f"Sunrise: {sunset}\n"
            f"Sunset: {sunrise}"
        )

        label1.config(text=final_info)
        label2.config(text=final_data)
        
        icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
        icon_image = Image.open(requests.get(icon_url, stream=True).raw)
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo
        loading_label.config(text="")

    except Exception as e:
        loading_label.config(text="")
        messagebox.showerror("Error", "Failed to retrieve data. Check your internet connection.")

root = tk.Tk()
root.geometry("700x600")
root.title("Weather App")
root.configure(bg="#3a7ca5")

f_large = ("Helvetica", 16, "bold")
f_small = ("Helvetica", 14)

header = tk.Label(root, text="Weather App", font=("Helvetica", 28, "bold"), fg="white", bg="#3a7ca5")
header.pack(pady=10)

frame = tk.Frame(root, bg="#3a7ca5")
frame.pack(pady=10)

textField = tk.Entry(frame, justify='center', width=20, font=("Helvetica", 20), bd=2, relief="groove")
textField.grid(row=0, column=0, padx=10)
textField.focus()

search_btn = tk.Button(frame, text="Search", font=f_small, width=10, bg="#1cc88a", fg="white", command=getWeather)
search_btn.grid(row=0, column=1, padx=10)

textField.bind('<Return>', getWeather)

icon_label = tk.Label(root, bg="#3a7ca5")
icon_label.pack(pady=15)

label1 = tk.Label(root, font=("Helvetica", 32), fg="white", bg="#3a7ca5")
label1.pack()

label2 = tk.Label(root, font=f_large, fg="white", bg="#3a7ca5", justify="left")
label2.pack(pady=20)

loading_label = tk.Label(root, text="", font=f_small, fg="yellow", bg="#3a7ca5")
loading_label.pack(pady=5)

root.mainloop()
