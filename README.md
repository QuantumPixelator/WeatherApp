# Weather App

A simple GUI weather application that displays current weather information for a given zip code.

![Screenshot](screenshot.png)

## Features
- Enter a zip code to get current weather
- Displays temperature in Fahrenheit (color-coded: blue ≤32°F, green 33-84°F, red ≥85°F), weather condition (orange), humidity (cyan), wind speed (magenta), and location (yellow)
- Updates automatically every 10 minutes
- Dark theme with custom icon
- Colorful, easy-to-read interface

## Requirements
- Python 3.14
- requests
- customtkinter

## Setup
1. Ensure Python is installed.
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `.venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install requests customtkinter`
5. Obtain an API key from [weatherapi.com](https://www.weatherapi.com/)
6. Copy `config.example.json` to `config.json` and replace `"your_api_key_here"` with your actual API key
7. Run the app: `python weather.py`

## API
Uses weatherapi.com current weather API. API key must be stored in `config.json`.

## License
This project is provided under the IDGAF license - see the [LICENSE](LICENSE) file for details.