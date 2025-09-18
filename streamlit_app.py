import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="Agricultural Data Analysis",
    page_icon="🌾",
    layout="wide"
)

@st.cache_data
def load_data():
    """Load and cache all datasets"""
    try:
        cropland_df = pd.read_csv('Cropland Value.csv')
        crop_prices_df = pd.read_csv('Crop Prices.csv')
        price_index_df = pd.read_csv('NASS-Data.csv')
        return cropland_df, crop_prices_df, price_index_df
    except FileNotFoundError as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

def process_cropland_data(cropland_df, selected_states, year_range):
    """Process cropland data for Plot 1"""
    if cropland_df is None:
        return None
    
    # Filter for selected states and year range
    filtered_df = cropland_df[cropland_df['State'].isin(selected_states)].copy()
    filtered_df = filtered_df[(filtered_df['Year'] >= year_range[0]) & (filtered_df['Year'] <= year_range[1])].copy()
    
    # Convert Value column to numeric (remove commas)
    filtered_df['Value_Numeric'] = filtered_df['Value'].str.replace(',', '').astype(float)
    
    return filtered_df

def process_crop_prices_data(crop_prices_df, selected_crops, year_range):
    """Process crop prices data for Plot 2"""
    if crop_prices_df is None:
        return None
    
    # Filter for selected commodities and year range
    filtered_df = crop_prices_df[crop_prices_df['Commodity'].isin(selected_crops)].copy()
    filtered_df = filtered_df[(filtered_df['Year'] >= year_range[0]) & (filtered_df['Year'] <= year_range[1])].copy()
    
    # Convert Value column to numeric
    filtered_df['Value_Numeric'] = pd.to_numeric(filtered_df['Value'], errors='coerce')
    
    return filtered_df

def process_price_index_data(price_index_df, year_range):
    """Process price index data for Plot 3"""
    if price_index_df is None:
        return None
    
    # Filter for year range
    filtered_df = price_index_df[(price_index_df['Year'] >= year_range[0]) & (price_index_df['Year'] <= year_range[1])].copy()
    
    # Convert Value column to numeric
    filtered_df['Value_Numeric'] = pd.to_numeric(filtered_df['Value'], errors='coerce')
    filtered_df = filtered_df.sort_values('Year')
    
    return filtered_df

def create_plot1(data):
    """Create interactive Plot 1: Cropland Prices by State"""
    if data is None or data.empty:
        return None
    
    fig = px.line(data, x='Year', y='Value_Numeric', color='State',
                  title='Cropland Prices by State',
                  labels={'Value_Numeric': 'Price (Dollars per Acre)', 'Year': 'Year'},
                  markers=True)
    
    fig.update_layout(
        title_font_size=16,
        xaxis_title_font_size=12,
        yaxis_title_font_size=12,
        legend_title_font_size=12
    )
    
    return fig

def create_plot2(data):
    """Create interactive Plot 2: National Crop Prices"""
    if data is None or data.empty:
        return None
    
    fig = px.line(data, x='Year', y='Value_Numeric', color='Commodity',
                  title='National Crop Prices',
                  labels={'Value_Numeric': 'Price (Dollars per Bushel)', 'Year': 'Year'},
                  markers=True)
    
    fig.update_layout(
        title_font_size=16,
        xaxis_title_font_size=12,
        yaxis_title_font_size=12,
        legend_title_font_size=12
    )
    
    return fig

def create_plot3(data):
    """Create interactive Plot 3: Price Received Index"""
    if data is None or data.empty:
        return None
    
    fig = px.line(data, x='Year', y='Value_Numeric',
                  title='National Index of Price Received',
                  labels={'Value_Numeric': 'Price Received Index (Base Year 2011 = 100)', 'Year': 'Year'},
                  markers=True)
    
    fig.update_traces(line_color='green')
    fig.update_layout(
        title_font_size=16,
        xaxis_title_font_size=12,
        yaxis_title_font_size=12
    )
    
    return fig

def main():
    """Main Streamlit app"""
    
    # Title and description
    st.title("🌾 Agricultural Data Analysis Dashboard")
    st.markdown("""
    This dashboard explores the relationship between land prices and crop prices using data from the USDA's National Agricultural Statistics Service.
    
    **Interactive Features:**
    - Adjust date ranges for each plot
    - Select which states/crops to display
    - Zoom and pan on plots
    - Hover for detailed information
    """)
    
    # Load data
    cropland_df, crop_prices_df, price_index_df = load_data()
    
    if cropland_df is None:
        st.error("Unable to load data files. Please check that all CSV files are in the correct location.")
        return
    
    # Sidebar for controls
    st.sidebar.header("Interactive Controls")
    
    # Plot 1 Controls
    st.sidebar.subheader("Plot 1: Cropland Prices")
    available_states = ['KENTUCKY', 'INDIANA', 'OHIO', 'TENNESSEE']
    selected_states = st.sidebar.multiselect(
        "Select States:", 
        available_states, 
        default=available_states
    )
    
    cropland_years = cropland_df['Year'].unique()
    plot1_year_range = st.sidebar.slider(
        "Year Range (Plot 1):",
        min_value=int(cropland_years.min()),
        max_value=int(cropland_years.max()),
        value=(1997, 2025),
        key="plot1_years"
    )
    
    # Plot 2 Controls
    st.sidebar.subheader("Plot 2: Crop Prices")
    available_crops = ['CORN', 'SOYBEANS', 'WHEAT']
    selected_crops = st.sidebar.multiselect(
        "Select Crops:", 
        available_crops, 
        default=available_crops
    )
    
    crop_years = crop_prices_df['Year'].unique()
    plot2_year_range = st.sidebar.slider(
        "Year Range (Plot 2):",
        min_value=int(crop_years.min()),
        max_value=int(crop_years.max()),
        value=(1975, 2025),
        key="plot2_years"
    )
    
    # Plot 3 Controls
    st.sidebar.subheader("Plot 3: Price Received Index")
    index_years = price_index_df['Year'].unique()
    plot3_year_range = st.sidebar.slider(
        "Year Range (Plot 3):",
        min_value=int(index_years.min()),
        max_value=int(index_years.max()),
        value=(1990, 2024),
        key="plot3_years"
    )
    
    # Create three columns for plots
    col1, col2, col3 = st.columns(3)
    
    # Plot 1: Cropland Prices by State
    with col1:
        st.subheader("Plot 1: Cropland Prices by State")
        if selected_states:
            plot1_data = process_cropland_data(cropland_df, selected_states, plot1_year_range)
            fig1 = create_plot1(plot1_data)
            if fig1:
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.warning("No data available for selected parameters.")
        else:
            st.warning("Please select at least one state.")
    
    # Plot 2: National Crop Prices
    with col2:
        st.subheader("Plot 2: National Crop Prices")
        if selected_crops:
            plot2_data = process_crop_prices_data(crop_prices_df, selected_crops, plot2_year_range)
            fig2 = create_plot2(plot2_data)
            if fig2:
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("No data available for selected parameters.")
        else:
            st.warning("Please select at least one crop.")
    
    # Plot 3: Price Received Index
    with col3:
        st.subheader("Plot 3: Price Received Index")
        plot3_data = process_price_index_data(price_index_df, plot3_year_range)
        fig3 = create_plot3(plot3_data)
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("No data available for selected parameters.")
    
    # Full-width combined plot option
    st.subheader("📊 Combined View (Bonus Feature)")
    if st.checkbox("Show all three plots in one combined chart"):
        st.info("💡 **Scaling Note**: Land prices, crop prices, and index values use different scales. Each data type is plotted on separate y-axes for better visualization.")
        
        # Create subplot with secondary y-axes
        fig_combined = make_subplots(
            rows=1, cols=1,
            specs=[[{"secondary_y": True}]],
            subplot_titles=["Combined Agricultural Data Analysis"]
        )
        
        # Add crop prices (primary y-axis) - smaller scale, more visible
        if selected_crops and plot2_data is not None and not plot2_data.empty:
            for crop in selected_crops:
                crop_data = plot2_data[plot2_data['Commodity'] == crop]
                if not crop_data.empty:
                    fig_combined.add_trace(
                        go.Scatter(x=crop_data['Year'], y=crop_data['Value_Numeric'],
                                 mode='lines+markers', name=f"{crop} Price ($/bu)",
                                 line=dict(dash='dot', width=2)),
                        secondary_y=False
                    )
        
        # Add price index (secondary y-axis)
        if plot3_data is not None and not plot3_data.empty:
            fig_combined.add_trace(
                go.Scatter(x=plot3_data['Year'], y=plot3_data['Value_Numeric'],
                         mode='lines+markers', name="Price Received Index",
                         line=dict(color='green', width=3)),
                secondary_y=True
            )
        
        # Update layout with better axis labels
        fig_combined.update_xaxes(title_text="Year")
        fig_combined.update_yaxes(title_text="Crop Prices (Dollars per Bushel)", secondary_y=False)
        fig_combined.update_yaxes(title_text="Price Received Index (Base Year 2011 = 100)", secondary_y=True)
        fig_combined.update_layout(height=600, title="Combined Crop Prices and Price Index Analysis")
        
        st.plotly_chart(fig_combined, use_container_width=True)
        
        # Separate combined plot for land prices (due to scale difference)
        st.subheader("📊 Land Prices (Separate Scale)")
        st.info("🏞️ **Land prices are shown separately due to their much larger scale ($1,000s vs $1s-$100s)**")
        
        if selected_states and plot1_data is not None and not plot1_data.empty:
            fig_land = go.Figure()
            
            for state in selected_states:
                state_data = plot1_data[plot1_data['State'] == state]
                if not state_data.empty:
                    fig_land.add_trace(
                        go.Scatter(x=state_data['Year'], y=state_data['Value_Numeric'],
                                 mode='lines+markers', name=f"{state} Land Price",
                                 line=dict(width=2))
                    )
            
            fig_land.update_layout(
                title="Cropland Prices by State",
                xaxis_title="Year",
                yaxis_title="Price (Dollars per Acre)",
                height=400
            )
            
            st.plotly_chart(fig_land, use_container_width=True)
    
    # Data summary
    st.subheader("📈 Data Summary")
    
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    with summary_col1:
        if selected_states and plot1_data is not None and not plot1_data.empty:
            latest_land_prices = plot1_data[plot1_data['Year'] == plot1_data['Year'].max()]
            st.metric("Latest Cropland Prices", 
                     f"${latest_land_prices['Value_Numeric'].mean():.0f}/acre",
                     f"Average across {len(selected_states)} states")
    
    with summary_col2:
        if selected_crops and plot2_data is not None and not plot2_data.empty:
            latest_crop_prices = plot2_data[plot2_data['Year'] == plot2_data['Year'].max()]
            st.metric("Latest Crop Prices", 
                     f"${latest_crop_prices['Value_Numeric'].mean():.2f}/bu",
                     f"Average across {len(selected_crops)} crops")
    
    with summary_col3:
        if plot3_data is not None and not plot3_data.empty:
            latest_index = plot3_data[plot3_data['Year'] == plot3_data['Year'].max()]
            if not latest_index.empty:
                st.metric("Latest Price Index", 
                         f"{latest_index['Value_Numeric'].iloc[0]:.1f}",
                         "2011 = 100")

if __name__ == "__main__":
    main()
