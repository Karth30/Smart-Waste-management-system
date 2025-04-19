# Smart-Waste-management-system

INTRODUCTION:

This project aims to develop an IoT-based smart waste bin monitoring system that uses an ultrasonic sensor to detect garbage levels and an MQ2 sensor to identify harmful gas emissions. The sensor data is logged to Google Sheets via Google Apps Script, and email alerts are sent when thresholds are exceeded. A Streamlit dashboard is used to provide real-time visualizations, making the system efficient, responsive, and user-friendly for better waste management and safety

HARDWARE REQUIRED:

1. NodeMCU (ESP8266)
2. Ultrasonic Sensor (HC-SR04)
3. MQ2 Gas Sensor
4. Breadboard and jumper wires
5. USB cable (for ESP8266)
6. Power supply (5V)

SOFTWARE REQUIRED:

1. Arduino IDE
2. Google Sheets
3. Google Apps Script
4. Streamlit (Python framework)

WORKING PRINCIPLE:

1. ESP8266 reads values from the ultrasonic and MQ2 sensors.
2. It sends the data to a Google Sheet using a webhook or API.
3. Apps Script monitors the sheet, and when:
• Garbage level > threshold → sends “Bin is Full” alert.
• Gas level > threshold → sends “Gas Detected” alert.
4. Streamlit app fetches the latest data from Google Sheets and shows real-time status.
   
ALGORITHM:

1. Initialize sensors and Wi-Fi.
2. Measure distance using ultrasonic sensor.
3. Measure gas concentration using MQ2.
4. Calculate garbage fill percentage.
5. Send data to Google Sheet.
6. Check thresholds via Apps Script.
7. If limits crossed, send email alert.

BLOCK DIAGRAM:

![image](https://github.com/user-attachments/assets/60a44717-5737-48d4-8187-86c9ad31dc31)

FLOW CHART:

![image](https://github.com/user-attachments/assets/11847408-032e-45f8-8a24-00734663a503)

IMPLEMENTATION:

The implementation of this project revolves around the integration of multiple hardware and software components to form a seamless, responsive, and intelligent system capable of monitoring waste levels and detecting fire hazards in real-time. At the heart of the system lies the ESP8266 NodeMCU microcontroller, chosen for its cost-effectiveness and built-in Wi-Fi capability, making it ideal for IoT-based remote monitoring applications. The project deploys two primary sensors—an ultrasonic sensor (HC-SR04) and a gas sensor (MQ2)—to gather environmental data from a smart bin setup. The ultrasonic sensor is responsible for measuring the distance between the top of the bin and the waste inside. When waste accumulates and reaches a certain threshold—typically below 5 centimeters from the sensor—the system classifies the bin as full and triggers a "BIN OVERFLOW ALERT" condition. Concurrently, the MQ2 gas sensor constantly monitors the air quality for the presence of combustible gases and smoke. A significant rise in gas concentration, calibrated against a clean baseline, is interpreted as a potential fire hazard. This activates a "FIRE ALERT" mechanism within the system. The NodeMCU reads both sensor outputs periodically and processes this information to determine whether an alert condition exists. Data collected from the sensors, including the timestamp, distance, gas concentration value, and the alert status, is formatted into a JSON object and sent over the internet using HTTPS POST requests to a Google Apps Script endpoint. The Google Apps Script, hosted in conjunction with a Google Sheet, acts as a backend server that receives the data and stores it systematically in the spreadsheet. This setup enables persistent data logging for historical analysis and auditing. Furthermore, the script contains logic to automatically generate and send email alerts using the GmailApp service based on the type of alert received. For instance, if a "FIRE ALERT" is detected, an emergency email is sent to a predefined recipient with the relevant sensor readings and a timestamp, urging immediate attention. Similarly, "BIN OVERFLOW ALERT" emails notify personnel to empty the bin promptly. To avoid spamming, both alerts are throttled using timestamp-based cooldowns, allowing only one alert per condition every two minutes. To provide a user-friendly visualization, an optional Streamlit-based dashboard can be developed, fetching data from the Google Sheet and rendering interactive graphs and status indicators. This dashboard serves as a monitoring tool that can be accessed remotely, providing a live view of the system’s performance and health. The entire system operates autonomously once powered and connected to a Wi-Fi network, requiring minimal human intervention. It embodies a practical and scalable solution to urban waste management challenges and early fire detection, potentially deployable in smart city infrastructures, office complexes, and public areas. By leveraging the Internet of Things (IoT), the project exemplifies how real-time data acquisition, cloud integration, and automated alerting mechanisms can converge to create intelligent, responsive systems that enhance public safety and environmental cleanliness.

RESULTS:

The following are the images collected from the implementation of the project:

![image](https://github.com/user-attachments/assets/39314f47-b9b5-4bf8-9e3e-1725bf51d2ae)

Sensor values displayed in the Serial Monitor

![image](https://github.com/user-attachments/assets/18194185-e4a3-471f-91a2-f66cf4fb1a56)

Values uploaded in Google Sheets

![image](https://github.com/user-attachments/assets/9d26f425-8364-4d17-a5fe-86797b0d26ad)

Admin Login Page

![image](https://github.com/user-attachments/assets/f30d77a9-f7ab-4b3a-8c0d-a99a5ea54d05)

Sensor values displayed in the User Interface

![image](https://github.com/user-attachments/assets/14de4817-c5eb-43a4-b74f-d9d6501889b9)

 Alert Table
 
 ![image](https://github.com/user-attachments/assets/17ca285d-f462-4316-97f8-03464115d808)

 Distance Trends over time

 ![image](https://github.com/user-attachments/assets/24a8468d-30bb-4988-8543-77623e3fa3e3)

 Gas Sensor trend over time

 ![image](https://github.com/user-attachments/assets/132125ac-2128-4778-b0ef-92656d196818)

  Email based Alert system

  CONCLUSION:

  In conclusion, this IoT-based smart waste and fire monitoring system offers a practical and efficient solution for enhancing urban sanitation and safety. By combining sensor data with cloud-based logging and automated alerts, it provides continuous, real-time feedback that can prompt timely human intervention. The integration of Wi-Fi communication and Google Apps Script enables seamless data sharing and alert delivery, making it both scalable and user-friendly. This project not only addresses common civic issues like overflowing bins and potential fire hazards but also lays a foundation for further smart city innovations.








