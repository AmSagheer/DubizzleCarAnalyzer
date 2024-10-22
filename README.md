# Dubizzle Car Data Scraper and Visualizer

This Streamlit application scrapes car data from Dubizzle UAE and visualizes it, allowing users to analyze car prices, mileages, and years for different makes and models.

## Features

- Select car make and model
- Set year and price ranges
- Scrape car listings from Dubizzle UAE
- Visualize data with interactive plots
- Download scraped data as CSV

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/dubizzle-car-scraper.git
   cd dubizzle-car-scraper
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Ensure you have Chrome installed, as this application uses ChromeDriver for web scraping.

## Usage

Run the Streamlit app:

```
streamlit run Home.py

```


Then, follow these steps in the web interface:


1. Select a car make from the dropdown
2. Choose a specific model
3. Adjust the year and price range sliders
4. Click "Start Data Extraction" to begin scraping and visualizing the data

## Data Visualization

The app provides two main visualizations:

1. A scatter plot of price vs. mileage, colored by year
2. Box plots showing price distribution by year and a histogram of car counts by year

## Limitations

- The scraper may be affected by changes to the Dubizzle website structure
- No explicit rate limiting is implemented, so use responsibly to avoid overloading the target website

## Contributing

Contributions, issues, and feature requests are welcome.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Disclaimer

This tool is for educational purposes only. Ensure you comply with Dubizzle's terms of service and robots.txt file when using this scraper.