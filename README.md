# 🚁 Drone Telemetry & Analysis Dashboard

A lightweight ground-station-style dashboard built with **Python** and **Flask** for exploring drone flight logs, visualizing telemetry, and inspecting relationships between flight parameters.

![Python](https://img.shields.io/badge/Python-3.x-blue) ![Flask](https://img.shields.io/badge/Framework-Flask-green) ![Status](https://img.shields.io/badge/Status-Completed-success)

## Features

- Interactive visualization of flight parameters such as speed, altitude, and battery level
- Scatter-plot analysis for comparing two variables
- Correlation heatmap for telemetry inspection
- Basic rule-based interpretation of selected data relationships
- Dark-themed web interface
- CSV-based telemetry workflow using Pandas

![Project Interface](screenshot.png)

## Tech Stack

- Python
- Flask
- Pandas
- Seaborn
- HTML / CSS
- Jinja2

## Installation

```bash
git clone https://github.com/sefatasdemir22/drone-telemetry-dashboard.git
cd drone-telemetry-dashboard
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## Project Structure

```text
drone-telemetry-dashboard/
├── app.py
├── requirements.txt
├── drone_logs.csv
├── static/
└── templates/
    └── index.html
```

## Purpose

This project was created to practice telemetry analysis, lightweight backend development, and technical data visualization in an autonomous-systems context.

## Author

**Sefa Taşdemir**
