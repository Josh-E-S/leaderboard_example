import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import json

# Import the Zapier integration (commented out for now)
# from zapier_integration import get_leaderboard_data_from_zapier

# Set page to wide mode
st.set_page_config(layout="wide")

# Zapier webhook URL (you would replace this with your actual webhook URL)
# ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/your_unique_webhook_url"

# Function to load data (commented out Zapier integration for now)
def load_data():
    # Uncomment the following lines to use Zapier integration
    # df = get_leaderboard_data_from_zapier(ZAPIER_WEBHOOK_URL)
    # if df is not None:
    #     return df
    
    # Placeholder data (remove this when using actual data from Zapier)
    data = {
        'Rank': [1, 2, 4, 3, 5],
        'Runner Name': ['sanderson, nick', 'johnson, chris', 'johnson, alex', 'smith, paul', 'jones, andrea'],
        'DogCallName': ['cow', 'toby', 'spot', 'linus', 'fido'],
        'LifeTimeMiles': [121.0, 24.0, 16.0, 11.0, 1.0],
        'Breed': ['border collie', 'cattle dog', 'border collie', 'irish setter', 'cattle dog']
    }
    return pd.DataFrame(data)

# Load the data
df = load_data()

# Sidebar
with st.sidebar:
    st.title("Leaderboard Dashboard")
    
    # Placeholder for Lottie animation
    try:
        with open("./assets/leaderboard.json") as f:
            lottie_data = json.load(f)
        st_lottie(lottie_data, height=200)
    except FileNotFoundError:
        st.warning("Lottie animation file not found. Please add it to ./assets/leaderboard.json")

    # Filter by breed
    breeds = ['All'] + sorted(df['Breed'].unique().tolist())
    selected_breed = st.selectbox('Filter by Breed', breeds)

    # Search functionality
    search_term = st.text_input('Search', '')

    # Sorting
    sort_column = st.selectbox('Sort by', ['Rank', 'LifeTimeMiles'])
    sort_order = st.radio('Sort order', ['Ascending', 'Descending'])

# Main content
st.title('Dog Runner Leaderboard')

# Apply filters
if selected_breed != 'All':
    filtered_df = df[df['Breed'] == selected_breed]
else:
    filtered_df = df

if search_term:
    filtered_df = filtered_df[filtered_df.apply(lambda row: search_term.lower() in ' '.join(row.astype(str)).lower(), axis=1)]

filtered_df = filtered_df.sort_values(by=sort_column, ascending=(sort_order == 'Ascending'))

# Display the table
st.dataframe(filtered_df.set_index('Rank'), hide_index=True, use_container_width=True)

# Statistics
st.subheader('Statistics')
col1, col2, col3 = st.columns(3)
col1.metric("Total Runners", len(filtered_df))
col2.metric("Total LifeTimeMiles", f"{filtered_df['LifeTimeMiles'].sum():.1f}")
col3.metric("Average LifeTimeMiles", f"{filtered_df['LifeTimeMiles'].mean():.1f}")

# Create two columns for charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Add a bar chart of top runners
    st.subheader('Top 5 Runners by LifeTimeMiles')
    top_5 = filtered_df.nlargest(5, 'LifeTimeMiles')
    fig_bar = px.bar(top_5, x='Runner Name', y='LifeTimeMiles', title='Top 5 Runners')
    fig_bar.update_layout(height=400)  # Set a fixed height
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    # Add a donut chart for breed distribution
    st.subheader('Breed Distribution')
    breed_counts = df['Breed'].value_counts()
    fig_donut = px.pie(values=breed_counts.values, names=breed_counts.index, hole=0.3, title='Breed Distribution')
    fig_donut.update_layout(height=400)  # Set a fixed height
    st.plotly_chart(fig_donut, use_container_width=True)