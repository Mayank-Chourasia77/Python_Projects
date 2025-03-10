import sys
import requests
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QApplication
from PyQt5.QtCore import Qt

class weather(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name : ",self)
        self.city_input = QLineEdit(self)
        self.get_weather = QPushButton("Get Weather",self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather.setObjectName("get_weather")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet(""" 
              QLabel , QPushButton{
                 font-family:calibri;
                 }
                 QLabel#city_label{
                    font-size:40px;
                    font-style:italic;
                 }
                 QLineEdit#city_input{
                    font-size:40px;
                 }
                 QPushButton#get_weather{
                   font-size:30px;
                   font-weight:bold;
                 }
                 QLabel#temperature_label{
                     font-size:75px;
                 }
                 QLabel#emoji_label{
                 font-size:100px;
                 font-family:Segoe UI emoji;
                 }
                 QLabel#description_label{
                   font-size:50px;
                 }
        
        """)
        self.get_weather.clicked.connect(self.get_weather_detail)

    def get_weather_detail(self):
        api_key = "06a209014e3aacd8a3e087054f9cb64c"
        city_name = (self.city_input.text()).capitalize()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)


        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("bad request\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized\nInvalid API Key")
                case 403:
                    self.display_error("Forbidden\nAccess is denied")
                case 404:
                    self.display_error("Not found\nCity not found")
                case 500:
                    self.display_error("Internal server error\nPlease try again later")
                case 502:
                    self.display_error("bad Gateway\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured\n{http_error}")


        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nCheck your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error\nThe request time out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects\nCheck the URL ")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Requests Error:\n{req_error}")



    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size:30px")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size:75px")
        tem_k = data["main"]["temp"]
        tem_f = (tem_k*9/5)-459.67

        weather_description = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]

        self.temperature_label.setText(f"{tem_f:.0f}°F")
        self.description_label.setText(weather_description)
        self.emoji_label.setText(self.get_weather_emoji(weather_id))

    def get_weather_emoji(self, weather_id):
        if 200 <= weather_id <= 232:
            return "🌧️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = weather()
    weather_app.show()
    sys.exit(app.exec_())

