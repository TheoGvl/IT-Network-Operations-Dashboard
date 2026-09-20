# IT & Network Operations Dashboard

A real-time, web-based system monitoring dashboard built with Python and **NiceGUI**. This tool provides live insights into local machine metrics, simulating core IT operations and basic cybersecurity monitoring environments. 

This project demonstrates practical application of system administration concepts by directly interfacing with system hardware and network traffic data, packaged in a reactive, browser-based UI.

## Features

* **Live Resource Tracking:** Real-time monitoring of CPU usage and RAM allocation using dynamic circular progress indicators.
* **Network Traffic Analysis:** Tracks inbound and outbound network data (Bytes Sent/Received) to help visualize bandwidth usage and spot potential traffic anomalies.
* **Performance History:** Interactive ECharts integration displaying a live, scrolling history of CPU performance over time.
* **Professional UI:** Built with a clean, dark-mode aesthetic utilizing NiceGUI's backend-driven Vue.js web-server capabilities.

## Installation & Usage

1. **Clone the repository:**
   ```
   git clone https://github.com/theogvl/it-ops-dashboard.git
   ```

2. **Install dependencies:**
   Make sure you have Python installed, then install the required libraries:
   ```
   pip install nicegui psutil
   ```

3. **Run the dashboard:**
   Navigate to the project folder and start the local server:
   ```
   python web_dash.py
   ```
   *The dashboard will operate locally and run in the background without needing an external internet connection.*

## Technologies Used
* Python 3
* NiceGUI (Web Framework)
* psutil (System & Network Utilities)
