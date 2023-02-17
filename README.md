# YOLNP - You Only Look Number Plates

Buy me a coffee :D -> https://www.buymeacoffee.com/guiflayrom

YOLNP - You Only Look Number Plates - It is a full stack project created, idealized, designed, codified by the owner of this repository. YOLNP was my first project since I decided to create my Github account. It was started in 2020, when I was 15 years old, and finally finished it now at my 18 years old, so I have a fondness for everything it has been through, and now it's time to leave it opensource ;)

YOLNP was developed with the intention of being useful for personal surveillance and data science for physical companies that are located on highways.

# Screens
![](https://i.imgur.com/YhQN8ST.png)
### Dashboard
![](https://github.com/Guiflayrom/yolnp/blob/master/resource/dashboard.png)
### All Plates Detected
![](https://github.com/Guiflayrom/yolnp/blob/master/resource/all_plates.png)
### Alerts Configuration
![](https://github.com/Guiflayrom/yolnp/blob/master/resource/alerts_page.png)
### Real Time
![](https://github.com/Guiflayrom/yolnp/blob/master/resource/real_time.png)
# Functionalities

- Process local videos and rtsp streams
- Start and stop the ALPR through requests located in a flask server
- Share a stream of image that is being processed
- Detect plates in your personal alerts list
- Check recurrenting plates
- View the plate picture when detected
- Run ALPR in Threading system
- Calculate median duration of plate in recorded videos
- Alert stealed cars by consulting (deprecated)
- Estimate median price of cars (deprecated)
- Get origin city of plate (deprecated)

# Technologies

- **CVA ->** PaddleOCR, Tensorflow, Keras, OpenCV, Flask, Numpy...
- **SERVER ->** DRF, JWT, CORS..
- **CLIENT ->** Nuxt.js, Axios, Vuex, Vuex-Localstorage...
