
# Necessary package installations
#   pip install requests
#   pip install image
#   pip install timezonefinder
#   pip install pytz



# importing the libraries
from tkinter import *
import requests
import json
import datetime
import pytz
import time
from timezonefinder import TimezoneFinder

from PIL import ImageTk, Image


# necessary details
root = Tk()
root.title("Harsh Kumar's Weather App")
root.geometry("700x600")
root['background'] = "#9ADBD6"



api = None
citytimezone = None
date = None

dt = datetime.datetime.now()

# Image
new = ImageTk.PhotoImage(Image.open('logo.png'))
panel = Label(root, image=new)
panel.place(x=350, y=370)


# Dates
def update_date():
    global dt, api, date
    obj = TimezoneFinder()
    if api != None:
        print("Test")
        x = api['coord']
        longitude = x['lon']
        latitude = x['lat']
        result = obj.timezone_at(lng=longitude, lat=latitude)
        print ("Result:" + result)
        citytimezone = pytz.timezone(result)
        dt = datetime.datetime.now(citytimezone)
        print (dt)


    date = Label(root, text=dt.strftime('%A '), bg='#9ADBD6', font=("bold", 15))
    date.place(x=5, y=130)
    month = Label(root, text=dt.strftime('%B %d'), bg='#9ADBD6', font=("bold", 15))
    month.place(x=120, y=130)


# Time
# DateTime.now().add(Duration(seconds: timezone - DateTime.now().timeZoneOffset.inSeconds))
def update_clock():
    global api
    global country
    global citytimezone
    if api != None:
        obj = TimezoneFinder()
        x = api['coord']
        longitude = x['lon']
        latitude = x['lat']
        result = obj.timezone_at(lng=longitude, lat=latitude)
        #print ("Result:" + result)
        citytimezone = pytz.timezone(result)
        #print (citytimezone)
        #print(datetime.datetime.now(citytimezone))
        
        localtimedt = datetime.datetime.now(citytimezone).strftime('%I : %M : %S %p')
        label_time.configure(text=localtimedt)
    root.after(1000,update_clock)

label_time = Label(root, text=dt.strftime("%I : %M : %S %p"), bg='#9ADBD6', font=("bold", 15))
label_time.place(x=10, y=160)

cdt = 31
cdtvar =  None
cityvar = None
def update_screen():
    global cdtvar, cdt, cityvar, date
    if cdtvar != None:
        root.after_cancel(cdtvar)
        cdt = 31

    if cityvar != None:
        root.after_cancel(cityvar)

    city_name()
    label_cdt.configure(text=cdt)
    update_cdt()
    if date != None:
        date.place_forget()
    update_date()
    update_image()



def update_cdt():
    global cdt, cdtvar
    if cdt > 0 :
        cdt = cdt - 1
    else :
        cdt = 30

    label_cdt.configure(text=cdt)
    cdtvar = root.after(30*60*1000,update_cdt)
       


label_cdt = Label(root, text='--', bg='#9ADBD6', font=("bold", 75))
label_cdt.place(x=350, y=200)

label_min = Label(root, text='Min', bg='#9ADBD6', font=("bold", 15))
label_min.place(x=465, y=265)

# Theme for the respective time the application is used
def update_image():
    global api, img, citytimezone
    obj = TimezoneFinder()
    x = api['coord']
    longitude = x['lon']
    latitude = x['lat']
    result = obj.timezone_at(lng=longitude, lat=latitude)
    citytimezone = pytz.timezone(result)
    if api != None:
        print(citytimezone)
        localhr = int(datetime.datetime.now(citytimezone).strftime('%H'))
        #localhr = int(time.strftime("%H", time.gmtime(api['dt'])))
        print (localhr)
        if (localhr) >= 18 or (localhr) <= 6:
            img = ImageTk.PhotoImage(Image.open('moon.png'))
            panel = Label(root, image=img)
            panel.place(x=350, y=0)
        else:
            img = ImageTk.PhotoImage(Image.open('sun.png'))
            panel = Label(root, image=img)
            panel.place(x=350, y=0)


# City Search
city_name = StringVar()
city_entry = Entry(root, textvariable=city_name, width=45)
city_entry.grid(row=1, column=0, ipady=10, stick=W+E+N+S)

# api key
api_key = 'ac8fffcc406ba6187175dafdd61cb0e9'


def city_name():
    global api
    # API Call
    api_request = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" +
                               city_entry.get() + "&units=metric&lang=en&appid="+api_key)

    api = json.loads(api_request.content)

    # Time
    #localtimedt = datetime.datetime.fromtimestamp(api['dt']/1000).strftime('%H:%M:%S %p')
    localtimedt = time.strftime("%I : %M : %S %p", time.gmtime(api['dt']))
    label_time.configure(text=localtimedt)

    # Temperatures
    y = api['main']
    current_temp_C = str(round(y['temp'],2)) + '\N{DEGREE SIGN}' + 'C'
    current_temp_F = str(round((y['temp'] * 1.8) + 32,2)) + '\N{DEGREE SIGN}'+'F'
    humidity = str(y['humidity']) + '%'
    temp_min = str(round(y['temp_min'],2)) + '\N{DEGREE SIGN}' + 'C / '+str(round((y['temp_min'] * 1.8) + 32,2)) + '\N{DEGREE SIGN}' + 'F'
    temp_max = str(round(y['temp_max'],2)) + '\N{DEGREE SIGN}' + 'C / '+str(round((y['temp_max'] * 1.8) + 32,2)) + '\N{DEGREE SIGN}' + 'F'
    pressure = str(y['pressure']) + ' hPa'
#   sea_level = y['sea_level']

    # Coordinates
    x = api['coord']

    longtitude = 'lon: ' +str(x['lon'])
    latitude = 'lat: ' +str(x['lat'])

    #Timezone

    tz = api['timezone']  


    # Country
    z = api['sys']
    country = z['country']
    city = api['name']

    # wind
    wind = api['wind']
    wind_speed = str(wind['speed']) + ' m/s'

    # cloud
    cloud = api['clouds']
    cloud_all = cloud['all']

    # weather
#   weathers = api['weather']
#   weather_main = weathers['main']
#   weather_desc = weathers[0][2]



    # Adding the received info into the screen
    label_temp_C.configure(text=current_temp_C)
    label_temp_F.configure(text=current_temp_F)
    label_humidity.configure(text=humidity)
    max_temp.configure(text=temp_max)
    min_temp.configure(text=temp_min)
    label_lon.configure(text=longtitude)
    label_lat.configure(text=latitude)
    label_country.configure(text=country)
    label_city.configure(text=city)
    label_pressure.configure(text=pressure)
#   label_sealevel.configure(text=sea_level)
#   label_description.configure(text=weather_desc)
#   label_clouds.configure(text=cloud_all)
    label_windspeed.configure(text=wind_speed)

    cityvar = root.after(30*60*1000,city_name)



# Search Bar and Button
city_nameButton = Button(root, text="Search City", command=update_screen)
city_nameButton.grid(row=1, column=1, padx=5, stick=W+E+N+S)


# Country Names and Coordinates
label_city = Label(root, text="...", width=0, bg='#9ADBD6', font=("bold", 15))
label_city.place(x=10, y=63)

label_country = Label(root, text="...", width=0, bg='#9ADBD6', font=("bold", 15))
label_country.place(x=135, y=63)

label_lon = Label(root, text="...", width=0, bg='#9ADBD6', font=("Helvetica", 15))
label_lon.place(x=25, y=95)
label_lat = Label(root, text="...", width=0, bg='#9ADBD6', font=("Helvetica", 15))
label_lat.place(x=150, y=95)

# Current Temperature

label_temp_C = Label(root, text="...", width=0, bg='#9ADBD6', font=("Helvetica", 50), fg='black')
label_temp_C.place(x=18, y=220)

label_temp_F = Label(root, text="...", width=0, bg='#9ADBD6', font=("Helvetica", 50), fg='black')
label_temp_F.place(x=18, y=320)


#label_description = Label(root, text="...", width=0,
#                   bg='white', font=("bold", 15))
#label_description.place(x=107, y=375)


# Other temperature details

humidity_label = Label(root, text="Humidity: ", width=0, bg='#9ADBD6', font=("bold", 15))
humidity_label.place(x=3, y=400)

label_humidity = Label(root, text="...", width=0, bg='#9ADBD6', font=("bold", 15))
label_humidity.place(x=107, y=400)


maxi = Label(root, text="Max. Temp.: ", width=0, bg='#9ADBD6', font=("bold", 15))
maxi.place(x=3, y=430)

max_temp = Label(root, text="...", width=0, bg='#9ADBD6', font=("bold", 15))
max_temp.place(x=128, y=430)


mini = Label(root, text="Min. Temp.: ", width=0, bg='#9ADBD6', font=("bold", 15))
mini.place(x=3, y=460)

min_temp = Label(root, text="...", width=0, bg='#9ADBD6', font=("bold", 15))
min_temp.place(x=128, y=460)

pressure_label = Label(root, text="Pressure.: ", width=0, bg='#9ADBD6', font=("bold", 15))
pressure_label.place(x=3, y=490)

label_pressure = Label(root, text="...", width=0, bg='#9ADBD6', font=("bold", 15))
label_pressure.place(x=128, y=490)

#sealevel_label = Label(root, text="Sea Level.: ", width=0,
#           bg='white', font=("bold", 15))
#sealevel_label.place(x=3, y=520)

#label_sealevel = Label(root, text="...", width=0,
#               bg='white', font=("bold", 15))
#label_sealevel.place(x=128, y=520)

windspeed_label = Label(root, text="Wind Speed.: ", width=0, bg='#9ADBD6', font=("bold", 15))
windspeed_label.place(x=3, y=520)

label_windspeed = Label(root, text="...", width=0, bg='#9ADBD6', font=("bold", 15))
label_windspeed.place(x=128, y=520)

#clouds_label = Label(root, text="Clouds.: ", width=0,
#           bg='white', font=("bold", 15))
#clouds_label.place(x=3, y=580)

#label_clouds = Label(root, text="...", width=0,
#               bg='white', font=("bold", 15))
#label_clouds.place(x=128, y=580)





update_clock()
root.mainloop()









