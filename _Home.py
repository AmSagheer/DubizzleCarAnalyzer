# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from concurrent.futures import ThreadPoolExecutor

# Dictionary of car models
car_models = {
    'Mercedes-Benz': ['S-Class', 'C-Class', 'E-Class', 'G-Class', 'GLE-Class', 'CLA', 'GLC', 'A-Class', 'GLE Coupe', 'GLS-Class', 'CLS-Class', 'E-Class Coupe', 'V-Class', 'C-Class Coupe', 'SL-Class', 'GLA', 'GL-Class', 'S-Class Coupe', 'GT', 'M-Class', 'GLC Coupe', 'GLB', 'AMG', 'A200', 'GLK-Class', 'SLK-Class', 'CLE-Class', 'C43', 'EQS', 'CLS 450', 'Vito', 'Sprinter', 'CL-Class', 'G-Class Brabus', 'Viano', 'SLS', 'EQE', 'CLK-Class', 'SEL-Class', 'EQC', 'GLC 63', 'SLR', 'R-Class', '500/560', 'EQB', 'SLC', 'X Class', '240/260/280', '300/350/380', '450 SEL', 'EQA', 'S580e', 'B-Class', 'SEC-Class', 'Other'],
    'Toyota': ['Land Cruiser', 'Prado', 'Corolla', 'Rav 4', 'Camry', 'Yaris', 'Hilux', 'Fortuner', 'Hiace', 'Highlander', 'FJ Cruiser', 'Rush', 'Tundra', 'Land Cruiser 79 series', 'Sienna', 'Corolla Cross', 'Supra', '4Runner', 'C-HR', 'Avalon', 'Sequoia', 'Granvia', 'Innova', 'Previa', 'Prius', 'Land Cruiser 76 series', 'Land Cruiser 70', 'Avanza', '86', 'Raize', 'Tacoma', 'Crown', 'Urban Cruiser', 'Alphard', 'Levin', 'Pickup', 'Coaster', 'Veloz', 'Aurion', 'Zelas', 'GR86', 'XA', 'bZ3', 'BZ4X', 'Corona', 'Cressida', 'Rumion', 'Scion', 'Venza', 'Other'],
    'Nissan': ['Patrol', 'Altima', 'Sunny', 'Kicks', 'Pathfinder', 'Sentra', 'X-Trail', 'Maxima', 'Rogue', 'Armada', 'Tiida', 'Xterra', 'Urvan', 'Juke', 'Micra', 'Murano', 'Navara', 'Versa', '370z', 'Qashqai', 'Pickup', 'GT-R', 'Quest', 'Van', '350Z', 'Patrol Pickup', 'Silvia', '300ZX', '400Z', 'Leaf', 'Skyline', 'Sylphy', 'Titan', 'Z', 'Other'],
    'BMW': ['X5', '5-Series', '7-Series', '3-Series', 'X6', '4-Series', 'X7', 'X1', '6-Series', '2-Series', 'X3', 'X4', 'X2', 'M4', '1-Series', 'iX', 'Z4', '8-Series', 'M2', 'M3', 'M8', 'M5', 'M850i', 'i8', 'i3', 'i7', 'XM', 'M6', 'i5', 'i4', 'iX3', 'M1', 'Z8', 'Other'],
    'Land Rover': ['Range Rover', 'Range Rover Sport', 'Defender', 'Range Rover Evoque', 'Range Rover Velar', 'Discovery Sport', 'Discovery', 'LR4', 'LR2', 'LR3'],
    'Ford': ['Mustang', 'Edge', 'Explorer', 'F-Series Pickup', 'Ecosport', 'Focus', 'Escape', 'Figo', 'Fusion', 'Bronco', 'Expedition', 'Ranger', 'Taurus', 'Transit', 'Fiesta', 'Pickup', 'Territory', 'Flex', 'F-Series', 'GT', 'Escort', 'Shelby Cobra', 'Crown Victoria', 'Mustang Mach-E', 'Thunderbird', 'Tourneo', 'Van', 'Everest', 'Five Hundred', 'Mondeo', 'Super Duty'],
    'Hyundai': ['Sonata', 'Tucson', 'Elantra', 'Santa Fe', 'Accent', 'Veloster', 'Creta', 'H1', 'Kona', 'Palisade', 'Genesis', 'Avanti', 'Staria', 'Grand Santa Fe', 'Azera', 'Venue', 'Grand i10', 'i10', 'i30', 'Grandeur', 'Porter', 'Santa Cruz', 'Ioniq', 'Coupe', 'i20', 'Trajet', 'Veracruz', 'Other'],
    'Porsche': ['Cayenne', 'Carrera / 911', 'Macan', 'Panamera', 'Cayman', 'Boxster', 'Taycan', '918 Spyder', '718 Spyder', '968', 'Other'],
    'Lexus': ['RX-Series', 'ES-Series', 'LS-Series', 'LX570', 'IS-Series', 'GS-Series', 'LX600', 'GX 460', 'IS300', 'IS350', 'LX-Series', 'NX 300', 'GX-Series', 'NX 350', 'NX 200t', 'UX 200', 'RC', 'IS-F', 'TX', 'LC 500', 'LM 350h', 'RC F', 'NX 350H', 'CT-Series', 'IS-C', 'LM 300', 'NX-Series', 'UX-Series', 'LFA', 'NX 450H', 'SC-Series', 'Other'],
    'Audi': ['Q7', 'Q5', 'A8', 'A5', 'A3', 'A6', 'A4', 'Q8', 'S3/RS3', 'Q3', 'A7', 'S7/RS7', 'TT', 'S6/RS6', 'e-tron', 'S8', 'S5/RS5', 'RS Q8', 'R8', 'RSQ3', 'A1', 'S3', 'RS e-tron', 'S4/RS4', 'SQ8', 'Q2', 'Other'],
    'Kia': ['Sportage', 'Optima', 'Sorento', 'K5', 'Picanto', 'Carnival', 'Cerato', 'Rio', 'Soul', 'Seltos', 'Telluride', 'K3', 'Pegas', 'Stinger', 'Cadenza', 'Forte', 'Sedona', 'Sonet', 'Bongo', 'Carens', 'Mohave', 'Morning', 'EV5', 'K8', 'K9', 'Niro', 'EV6', 'K900', 'Koup', 'Oprius', 'Quoris'],
    'Jeep': ['Grand Cherokee', 'Wrangler', 'Wrangler Unlimited', 'Cherokee', 'Gladiator', 'Compass', 'Renegade', 'Wrangler 4xe', 'Grand Wagoneer', 'Grand Cherokee L', 'Liberty', 'Patriot', 'Other'],
    'Volkswagen': ['Tiguan', 'Touareg', 'Golf R', 'GTI', 'Golf', 'Passat', 'Teramont', 'ID.4', 'Beetle', 'Jetta', 'T-Roc', 'Scirocco', 'ID.6', 'CC', 'Transporter', 'Eos', 'Polo', 'Arteon', 'Caddy', 'Crafter', 'ID.7', 'Multivan', 'Atlas', 'Bora', 'Amarok', 'E-Lavida', 'Eurovan', 'ID.3', 'Viloran'],
    'Chevrolet': ['Camaro', 'Tahoe', 'Captiva', 'Silverado', 'Corvette', 'Malibu', 'Impala', 'Cruze', 'Traverse', 'Spark', 'Trax', 'Suburban', 'Groove', 'Trailblazer', 'Aveo', 'Blazer', 'Equinox', 'Caprice', 'Sonic', 'Express', 'Avalanche', 'Chevelle', 'Colorado', 'Lumina', 'Astro', 'Bel Air', 'Epica', 'Nova', 'Pickup'],
    'Mitsubishi': ['Pajero', 'Attrage', 'Lancer', 'ASX', 'Outlander', 'L200', 'Montero Sport', 'Canter', 'EclipseCross', 'Xpander', 'Mirage', 'Lancer EX', 'Montero', 'Pajero Sport', 'Eclipse', 'Evolution', 'Galant', 'Nativa', 'Van', '3000GT', 'Triton', 'Other'],
    'Dodge': ['Charger', 'Challenger', 'Ram', 'Durango', 'Journey', 'Neon', 'Nitro', 'Caravan', 'Avenger', 'Caliber', 'Dakota', 'Dart', 'Pickup', 'Van', 'Viper'],
    'Honda': ['Accord', 'Civic', 'CR-V', 'Pilot', 'Odyssey', 'City', 'HR-V', 'Jazz', 'MR-V', 'ENS1', 'ZR-V', 'Crosstour', 'Odyssey J', 'Passport', 'ENP1', 'M-NV', 'Other'],
    'Rolls-Royce': ['Cullinan', 'Ghost', 'Wraith', 'Phantom', 'Dawn', 'Spectre', 'Silver Seraph', 'Other'],
    'Infiniti': ['QX80', 'QX50', 'Q50', 'QX60', 'QX70', 'Q30', 'FX45/FX35', 'Q60', 'QX55', 'Q70', 'G37', 'JX-Series', 'QX30', 'QX56', 'G25', 'FX50', 'EX35', 'M-Series', 'FX37', 'G35', 'Q40'],
    'Bentley': ['Bentayga', 'Continental GT', 'Continental Flying Spur', 'Continental', 'Continental GTC', 'Mulsanne', 'Flying Spur', 'Azure', 'Arnage'],
    'MINI': ['Cooper', 'Countryman', 'Clubman', 'Coupe', 'Paceman', 'Roadster', 'Cooper Clubman', 'Other'],
    'Mazda': ['6', 'CX-9', '3', 'CX-5', 'CX-3', '2', 'CX-30', 'MX-5', 'Mazda CX-5', 'Pickup', 'CX-7', 'Mazda 3', 'Mazda CX-9', 'Mazda CX-90'],
    'Ferrari': ['812 GTS', 'SF90 Stradale', 'Roma', '296 GTB', '812 Superfast', 'SF90 Spider', '488 Spider', '488 GTB', 'Portofino', 'F8 Spider', 'Purosangue', '488 Pista', 'F8 Tributo', 'F430', 'California', '488', 'GTC4 Lusso', '488 Pista Spider', '296 GTS', '458', 'California T', 'F430 Spider', '360', 'Portofino M', '348', '458 Italia', '458 Spider', 'FF', 'GTC4 Lusso T', 'LaFerrari', '612 Scaglietti', 'F12 Berlinetta', 'Testarossa', '458 Speciale', '512', '599 GTB', 'F12', '246 Dino', '355', '412', '599', '599 GTO', 'F40', 'Other'],
    'GMC': ['Yukon', 'Sierra', 'Acadia', 'Terrain', 'Hummer', 'Canyon', 'Envoy', 'Pickup', 'Savana'],
    'Renault': ['Duster', 'Koleos', 'Megane', 'Symbol', 'Captur', 'Talisman', 'Fluence', 'Dokker', 'Safrane', 'Zoe', 'Logan', 'Trafic', 'Twizy', 'Other'],
    'Lamborghini': ['Urus', 'Huracan', 'Aventador', 'Revuelto', 'Gallardo', 'Murcielago', 'Countach', 'Diablo', 'Other'],
    'Cadillac': ['Escalade', 'ATS', 'XT5', 'CTS/Catera', 'CT6', 'CT5', 'SRX', 'XT6', 'CT4', 'XT4', 'DTS/De Ville', 'XTR/Eldorado', 'Fleetwood', 'Lyriq', 'STS/Seville', 'XTS', 'Other'],
    'Suzuki': ['Jimny', 'Swift', 'Grand Vitara', 'Baleno', 'Ertiga', 'Vitara', 'Ciaz', 'Dzire', 'Fronx', 'Celerio', 'APV Van', 'S-PRESSO', 'SX4', 'Carry', 'Liana', 'Other'],
    'Tesla': ['Model 3', 'Model Y', 'Model X', 'Model S', 'Cybertruck'],
    'Jaguar': ['F-Pace', 'XF', 'F-Type', 'E-Pace', 'XE', 'XJ-Series', 'XK', 'XJ6', 'XJS', 'XJ8', 'I-Pace', 'X-Type', 'XK8'],
    'Maserati': ['Ghibli', 'Levante', 'Quattroporte', 'GranTurismo', 'MC20', 'Grecale', 'GranCabrio', 'Other'],
    'Peugeot': ['3008', '208', '2008', 'Boxer', 'Partner', '5008', '508', '308', '5008 GT LINE', '3008 GT LINE', 'Expert', '301', 'RCZ', '207', '408', '307', '308cc', '2008 GT LINE', '208 GT LINE', 'Landtrek', 'Traveller', '308 GT LINE', 'e-208'],
    'MG': ['ZS', 'RX5', 'RX8', 'MG5', 'HS', 'GT', 'One', 'MG6', '360', 'GS', 'MG 7', 'T60', 'Whale'],
    'Jetour': ['Dashing', 'T2', 'X70 Plus', 'X70', 'X90', 'X90 Plus', 'X70 FL', 'X70 S'],
    'Lincoln': ['Navigator', 'MKX', 'MKC', 'Aviator', 'MKZ', 'Nautilus', 'Continental', 'Corsair', 'MKT', 'Town Car', 'MKS', 'Other']}

# Base URL for scraping
base_url = "https://uae.dubizzle.com/motors/used-cars"

# Set up Streamlit page configuration
st.set_page_config(page_title="Dubizzle-Scanner", page_icon="🚗")

# Main title of the app
st.title('Car Data Scraper and Visualizer')

# UI components for user input
st.markdown('<p class="selector-style">Select Car Maker</p>', unsafe_allow_html=True)
selected_maker = st.selectbox('Select Maker', options=car_models, label_visibility="collapsed")

# Get available models for the selected maker
if selected_maker in car_models:
    available_models = car_models[selected_maker]
else:
    available_models = []

st.markdown('<p class="selector-style">Select Car Model</p>', unsafe_allow_html=True)
selected_model = st.selectbox('Select Model', options=available_models, label_visibility="collapsed")

# Get current year for the year range slider
current_year = datetime.now().year
st.markdown('<p class="selector-style">Select Year Range</p>', unsafe_allow_html=True)
min_year, max_year = st.slider('Year Range', min_value=2000, max_value=current_year, value=(2017, current_year), label_visibility="collapsed")

st.markdown('<p class="selector-style">Select Price Range (AED)</p>', unsafe_allow_html=True)
min_price, max_price = st.slider('Price Range', min_value=0, max_value=1000000, value=(50000, 100000), label_visibility="collapsed")

# Validation checks
if min_year >= max_year:
    st.error("Minimum year must be less than maximum year.")
    st.stop()

if min_price >= max_price:
    st.error("Minimum price must be less than maximum price.")
    st.stop()

# Button to start data extraction
start_button = st.button('Start Data Extraction', disabled=(min_year >= max_year or min_price >= max_price))

# Initialize session state for storing data and options
if 'data' not in st.session_state:
    st.session_state.data = None
if 'selected_specs' not in st.session_state:
    st.session_state.selected_specs = "All Specs"
if 'specs_options' not in st.session_state:
    st.session_state.specs_options = ["All Specs"]

def update_selected_specs():
    st.session_state.selected_specs = st.session_state.specs_selector

@st.cache_data(show_spinner=False)
def extract_data(maker, model, year_low, year_high, price_low, price_high):
    # Set up Chrome options for headless browsing
    options = Options()
    options.add_argument('--headless')
    options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    data = []
    page = 1

    try:
        # Construct the base URL with filters
        base_url_with_filters = f"{base_url}/{maker.lower().replace(' ', '-').replace('/', '')}/{model.lower().replace(' ', '-').replace('/', '')}/"

        while True:
            # Construct the full URL with all filters and pagination
            url = f"{base_url_with_filters}?price__gte={price_low}&price__lte={price_high}&year__gte={year_low}&year__lte={year_high}&page={page}"
            driver.get(url)
            time.sleep(random.uniform(2, 4))  # Sleep for a random time to avoid detection

            try:
                # Wait for the page to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            except Exception as e:
                st.error(f"Timeout waiting for page to load: {e}")
                continue

            html_content = driver.page_source
            if not html_content:
                st.error("Failed to retrieve HTML content.")
                continue

            # Parse the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')
            listing_card_wrapper = soup.find('div', {'id': 'listing-card-wrapper'})
            child_divs = listing_card_wrapper.find_all('div', recursive=False)
            if not child_divs:
                break # No more listings found, exit the loop

            def process_child(child):
                try:
                    # Extract relevant information from each listing
                    elements = {
                        'price': child.find('div', {'data-testid': 'listing-price'}),
                        'title': child.find('h2', {'data-testid': 'subheading-text'}),
                        'year': child.find('div', {'data-testid': 'listing-year'}),
                        'specs': child.find('div', {'data-testid': 'listing-regional specs'}),
                        'mileage': child.find('div', {'data-testid': 'listing-kms'}),
                        'location': child.find('h4', {'data-testid': 'location-pin'}),
                        'link': child.find('a', href=True)
                    }

                    if all(elements.values()):
                        return {
                            'title': elements['title'].text.strip(),
                            'price': str(elements['price'].text.strip()),
                            'year': int(elements['year'].text.strip()) if elements['year'].text.strip().isdigit() else None,
                            'specs': elements['specs'].text.strip(),
                            'mileage': str(elements['mileage'].text.strip()),
                            'location': elements['location'].text.strip(),
                            'link': f"{base_url}{elements['link']['href']}" if not elements['link']['href'].startswith('http') else elements['link']['href']
                        }
                except Exception as e:
                    st.error(f"Error extracting data from a child div: {e}")
                    return None

            # Use ThreadPoolExecutor for parallel processing of listings
            with ThreadPoolExecutor(max_workers=20) as executor:
                results = list(executor.map(process_child, child_divs))

            data.extend([r for r in results if r])
            page += 1

    except Exception as e:
        st.error(f"Error extracting data: {e}")
        return pd.DataFrame()

    finally:
        driver.quit()

    return pd.DataFrame(data)

@st.cache_data(show_spinner=False)
def process_data(data):
    def clean_and_convert(x):
        if isinstance(x, str):
            return pd.to_numeric(x.replace(' km', '').replace(' AED', '').replace(',', ''), errors='coerce')
        else:
            return pd.to_numeric(x, errors='coerce')

    # Clean and convert mileage and price columns
    data['mileage'] = data['mileage'].apply(clean_and_convert)
    data['price'] = data['price'].apply(clean_and_convert)
    data['year'] = data['year'].astype(int)
    return data

@st.cache_data(show_spinner=False)
def get_summary_stats(data, selected_specs):
    # Filter data based on selected specs
    filtered_data = data if selected_specs == "All Specs" else data[data['specs'] == selected_specs]
    # Calculate summary statistics
    summary = filtered_data.groupby('year')['price'].agg(['mean', 'median', 'std', 'count']).round(2)
    summary = summary.rename(columns={'mean': 'Average', 'median': 'Median', 'std': 'Std Dev', 'count': 'Count'})
    # Format the summary for display
    summary['Average'] = summary['Average'].apply(lambda x: f"{x:,.0f}")
    summary['Median'] = summary['Median'].apply(lambda x: f"{x:,.0f}")
    summary['Std Dev'] = summary['Std Dev'].apply(lambda x: f"{x:,.0f}")
    return summary

def plot_data(data, selected_specs):
    # Filter data based on selected specs
    filtered_data = data if selected_specs == "All Specs" else data[data['specs'] == selected_specs]

    if filtered_data.empty:
        st.write(f"No data available for {selected_specs}.")
        return

    # Get and display summary statistics
    summary = get_summary_stats(data, selected_specs)
    st.write(f"Statistical Summary of Prices by Year ({selected_specs})")
    st.table(summary)

    # Create scatter plot
    fig = px.scatter(filtered_data, x='mileage', y='price', color='year',
                     title=f'{selected_maker} {selected_model} - Price vs. Mileage ({selected_specs})',
                     labels={'mileage': 'Mileage (km)', 'price': 'Price (AED)', 'year': 'Year'},
                     hover_data=['specs'])

    fig.update_traces(marker=dict(size=8, opacity=0.7))
    fig.update_layout(
        height=600, width=800,
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
        legend_title_font_size=14,
        coloraxis_colorbar_title_font_size=14,
        font_color="black"
    )
    fig.update_xaxes(tickformat=',d')
    fig.update_yaxes(tickformat=',d')

    # Adjust color axis to show only integer years
    min_year = filtered_data['year'].min()
    max_year = filtered_data['year'].max()
    fig.update_layout(
        coloraxis_colorbar=dict(
            tickvals=list(range(min_year, max_year + 1)),
            ticktext=list(range(min_year, max_year + 1))
        )
    )

    # Add trendline
    fig.add_traces(px.scatter(filtered_data, x='mileage', y='price', trendline='ols').data[1])
    fig.data[-1].line.color = 'rgba(255, 0, 0, 0.5)'
    fig.data[-1].line.width = 3

    st.plotly_chart(fig)

    # Create box plot and histogram
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=(f"Price Distribution by Year ({selected_specs})", 
                                        f"Count of Cars by Year ({selected_specs})"),
                        vertical_spacing=0.1)

    fig.add_trace(go.Box(x=filtered_data['year'], y=filtered_data['price'], name='Price Distribution',
                         marker_color='rgba(0, 128, 255, 0.7)', line_color='rgba(0, 0, 0, 0.5)'), row=1, col=1)
    fig.add_trace(go.Histogram(x=filtered_data['year'], name='Car Count',
                               marker_color='rgba(0, 200, 100, 0.7)', marker_line_color='rgba(0, 0, 0, 0.5)'), row=2, col=1)

    fig.update_layout(
        height=800, width=800, 
        title_text=f"{selected_maker} {selected_model} - Price and Count Analysis ({selected_specs})",
        title_font_size=20,
        showlegend=False,
        font_color="black"
    )
    fig.update_xaxes(title_text="Year", title_font_size=16, tickformat='d', dtick=1)  # Set dtick to 1 for integer years
    fig.update_yaxes(title_text="Price (AED)", row=1, col=1, title_font_size=16, tickformat=',d')
    fig.update_yaxes(title_text="Count", row=2, col=1, title_font_size=16)

    st.plotly_chart(fig)

@st.cache_data(show_spinner=False)
def normalize_data(data):
    scaler = MinMaxScaler()
    numerical_cols = ['price', 'year', 'mileage']
    data[numerical_cols] = scaler.fit_transform(data[numerical_cols])
    return data

def calculate_score(data, criteria):
    if criteria == 'value':
        return (data['year'] / data['price']) * (1 / data['mileage'])
    elif criteria == 'lowest_mileage':
        return -data['mileage']
    elif criteria == 'newest':
        return data['year']
    elif criteria == 'lowest_price':
        return -data['price']
        
def get_top_5_cars(data, criteria):
    score = calculate_score(data, criteria)
    data_copy = data.copy()
    data_copy.loc[:, 'score'] = score
    return data_copy.sort_values('score', ascending=False).head(5)
       
# Main execution flow    
if start_button:
    with st.spinner("Extracting data..."):
        data = extract_data(selected_maker, selected_model, min_year, max_year, min_price, max_price)
        
    if not data.empty:
        processed_data = process_data(data)
        st.session_state.data = processed_data
        st.write(processed_data.head(100).style.format({'year': '{:d}'}))
        if len(processed_data) > 100:
            st.write("Showing first 100 records. Use the plots below for full data analysis.")
            csv = processed_data.to_csv(index=False)
            st.download_button(
                label="Download full dataset as CSV",
                data=csv,
                file_name=f"{selected_maker}_{selected_model}_data.csv",
                mime="text/csv",
            )
        st.session_state.specs_options = ["All Specs"] + list(processed_data['specs'].unique())
        st.success(f"Extracted {len(processed_data)} records. Plot generated successfully.")
    else:
        st.error("No data found for the selected criteria.")

if st.session_state.data is not None:
    st.subheader("Data Analysis")
    selected_specs = st.selectbox('Select Specs', options=st.session_state.specs_options, key='specs_selector', index=0)
    plot_data(st.session_state.data, selected_specs)

    st.subheader("Find Top 5 Cars")
    criteria_options = ['Value', 'Lowest_mileage', 'Newest', 'Lowest_price']
    priority_criteria = st.selectbox("Select your top priority:", criteria_options, key='priority')

    if st.button("Show Top 5 Cars"):
        normalized_data = normalize_data(st.session_state.data)
        top_5 = get_top_5_cars(normalized_data, priority_criteria)
        st.write("Top 5 Cars based on your priority:")
        st.write(top_5[['title', 'price', 'year', 'mileage', 'specs', 'link']])

# CSS styling
st.markdown("""
    <style>
    div[data-baseweb="select"] > div {
        border-color: #1E90FF;
        border-radius: 4px;
    }
    div[data-baseweb="select"] span {
        color: #1E90FF;
        font-weight: bold;
    }
    div[data-baseweb="select"] svg {
        color: #1E90FF;
    }
    div[data-baseweb="select"]:hover > div {
        border-color: #0000FF;
    }
    ul[data-baseweb="menu"] {
        background-color: #f0f8ff;
    }
    ul[data-baseweb="menu"] li {
        color: #1E90FF;
    }
    ul[data-baseweb="menu"] li[aria-selected="true"] {
        background-color: #1E90FF;
        color: white;
    }
    .selector-style {
        font-size: 16px;
        font-weight: bold;
        color: #1E90FF;
        margin-bottom: 0px;
    }
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 250px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 250px;
        margin-left: -250px;
    }
    </style>
""", unsafe_allow_html=True)

# Make these accessible to other pages
st.session_state.car_models = car_models
st.session_state.extract_data = extract_data
st.session_state.process_data = process_data
st.session_state.plot_data = plot_data