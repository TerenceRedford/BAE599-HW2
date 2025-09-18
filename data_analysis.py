import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_and_process_data():
    """Load and process all three datasets"""
    
    # Load Cropland Value data (Plot 1)
    cropland_df = pd.read_csv('Cropland Value.csv')
    
    # Load Crop Prices data (Plot 2)  
    crop_prices_df = pd.read_csv('Crop Prices.csv')
    
    # Load NASS Price Received Index data (Plot 3)
    price_index_df = pd.read_csv('NASS-Data.csv')
    
    return cropland_df, crop_prices_df, price_index_df

def create_plot1_land_prices(cropland_df):
    """Create Plot 1: Price of land by state (KY, IN, OH, TN) from 1997-2025"""
    
    # Filter for the specific states and year range
    states = ['KENTUCKY', 'INDIANA', 'OHIO', 'TENNESSEE']
    filtered_df = cropland_df[cropland_df['State'].isin(states)].copy()
    
    # Filter for years 1997-2025
    filtered_df = filtered_df[(filtered_df['Year'] >= 1997) & (filtered_df['Year'] <= 2025)].copy()
    
    # Convert Value column to numeric (remove commas and convert to float)
    filtered_df['Value_Numeric'] = filtered_df['Value'].str.replace(',', '').astype(float)
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Plot each state
    for state in states:
        state_data = filtered_df[filtered_df['State'] == state]
        plt.plot(state_data['Year'], state_data['Value_Numeric'], 
                marker='o', linewidth=2, label=state.title())
    
    plt.title('Cropland Prices by State (1997-2025)', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Price (Dollars per Acre)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('plot1_land_prices.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return filtered_df

def create_plot2_crop_prices(crop_prices_df):
    """Create Plot 2: National price of wheat, corn and soybeans from 1975-2025"""
    
    # Filter for the specific commodities and year range
    commodities = ['CORN', 'SOYBEANS', 'WHEAT']
    filtered_df = crop_prices_df[crop_prices_df['Commodity'].isin(commodities)].copy()
    
    # Filter for years 1975-2025
    filtered_df = filtered_df[(filtered_df['Year'] >= 1975) & (filtered_df['Year'] <= 2025)].copy()
    
    # Convert Value column to numeric
    filtered_df['Value_Numeric'] = pd.to_numeric(filtered_df['Value'], errors='coerce')
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Plot each commodity
    for commodity in commodities:
        commodity_data = filtered_df[filtered_df['Commodity'] == commodity]
        plt.plot(commodity_data['Year'], commodity_data['Value_Numeric'], 
                marker='o', linewidth=2, label=commodity.title())
    
    plt.title('National Crop Prices (1975-2025)', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Price (Dollars per Bushel)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('plot2_crop_prices.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return filtered_df

def create_plot3_price_index(price_index_df):
    """Create Plot 3: National price received index from 1990-2025"""
    
    # Filter for years 1990-2025
    filtered_df = price_index_df[(price_index_df['Year'] >= 1990) & (price_index_df['Year'] <= 2025)].copy()
    
    # Convert Value column to numeric
    filtered_df['Value_Numeric'] = pd.to_numeric(filtered_df['Value'], errors='coerce')
    
    # Sort by year
    filtered_df = filtered_df.sort_values('Year')
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    plt.plot(filtered_df['Year'], filtered_df['Value_Numeric'], 
            marker='o', linewidth=2, color='green', label='Price Received Index')
    
    plt.title('National Index of Price Received (1990-2025)', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Index Value (2011 = 100)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('plot3_price_index.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return filtered_df

def main():
    """Main function to create all plots"""
    print("Loading data...")
    cropland_df, crop_prices_df, price_index_df = load_and_process_data()
    
    print("Creating Plot 1: Land Prices by State...")
    land_data = create_plot1_land_prices(cropland_df)
    
    print("Creating Plot 2: National Crop Prices...")
    crop_data = create_plot2_crop_prices(crop_prices_df)
    
    print("Creating Plot 3: Price Received Index...")
    index_data = create_plot3_price_index(price_index_df)
    
    print("All plots created successfully!")
    
    return land_data, crop_data, index_data

if __name__ == "__main__":
    main()
