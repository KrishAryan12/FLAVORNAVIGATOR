import streamlit as st
import logging
from MainFileV2 import run
import subprocess

class WebApp:

    with open('textfile1.txt', 'w') as txt:
        pass

    # Set page configuration
    st.set_page_config(
        page_title="Flavor Navigator 🍽️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Set up logging
    logging.basicConfig(filename="restaurant_search.log", level=logging.INFO, format="%(asctime)s - %(message)s")

    # Custom CSS for styling
    custom_css = """
    <style>
    /* Styling for the entire application container */
    .app-container {
        font-family: 'Arial', sans-serif;
        text-align: center;
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
        background-color: #f8f8f8;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
      }
    
      /* Styling for the header section */
      header {
        background-color: #ffc107;
        color: #333;
        padding: 20px;
        border-radius: 10px 10px 0 0;
        font-size: 24px;
        font-weight: bold;
      }
    
      /* Styling for input container */
      .input-container {
        background-color: #fff;
        padding: 20px;
        border-radius: 0 0 10px 10px;
      }
    
      /* Styling for input fields */
      input {
        width: 100%;
        padding: 12px;
        margin: 10px 0;
        border: 2px solid #ccc;
        border-radius: 5px;
        font-size: 16px;
      }
    
      /* Styling for the "Add Details" button */
      button {
        background-color: #0a192f;
        color: #fff;
        border: none;
        padding: 12px 24px;
        cursor: pointer;
        border-radius: 5px;
        font-size: 16px;
        transition: background-color 0.3s ease;
      }
    
      button:hover {
        background-color: #333;
      }
    
      /* Styling for details container */
      .details-container {
        margin-top: 20px;
        text-align: left;
      }
    
      /* Styling for detail cards */
      .detail-card {
        background-color: #fff;
        border: 1px solid #ccc;
        padding: 16px;
        margin: 10px 0;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }
    
      .detail-card p {
        font-size: 18px;
      }
    
      /* Styling for instructions container */
      .instructions-container {
        margin-top: 20px;
        text-align: left;
        font-size: 16px;
      }
    
      /* Styling for the unordered list in instructions */
      ul {
        list-style-type: disc;
        margin-left: 20px;
      }
    
      /* Styling for the list items in instructions */
      li {
        margin-bottom: 10px;
      }
    
      /* Styling for the buttons in the sidebar input boxes 
      .sidebar .sidebar-content .stNumberInput input[type="number"],
      .sidebar .sidebar-content .stNumberInput input[type="number"]{
        -webkit-appearance: none;
        appearance: none;
        margin: 0;
        -moz-appearance: textfield;
      }
      */  
        
      .sidebar .sidebar-content .stNumberInput input[type="number"] {
        -moz-appearance: textfield;
      }
      .sidebar .sidebar-content .stNumberInput input[type="number"] {
        -moz-appearance: textfield;
      }
      .sidebar .sidebar-content .stNumberInput input[type="number"] {
        -moz-appearance: textfield;
      }
    
      .sidebar .sidebar-content .stNumberInput button {
        background-color: #0a192f;
        color: #fff;
        border: none;
        padding: 10px;
        cursor: pointer;
        border-radius: 5px;
        font-size: 16px;
        transition: background-color 0.3s ease;
        -moz-appearance: textfield;
      }
    
      .sidebar .sidebar-content .stNumberInput button:hover {
        background-color: #fff;
        -moz-appearance: textfield;
      }
      
      .sidebar .sidebar-content .stNumberInput button:before {content: "+";}
      .sidebar .sidebar-content .stNumberInput button.decrement:before {content: "-";}
    </style>
    """

    # Render custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    # App container
    st.markdown('<div class="app-container">', unsafe_allow_html=True)

    # Header HTML
    header_html = """
        <header>
            <h1>🍽 Flavor Navigator</h1>
            <p>Find restaurants based on your preferences</p>
        </header>
    """

    # Footer HTML
    footer_html = """
        <div style="background-color: #0a192f; color: #fff; padding: 10px; text-align: center; border-radius: 0 0 10px 10px;">
            <p>Developed by Data.py</p>
        </div>
    """

    # Render Header
    st.markdown(header_html, unsafe_allow_html=True)

    # Sidebar for user input
    st.sidebar.header("Enter Your Preferences")

    budget = st.sidebar.number_input("Enter your budget", min_value=0, step=200)
    distance = st.sidebar.number_input("Enter the distance radius ", min_value=0, step=1)
    location = st.sidebar.text_input("Enter your location")

    if st.sidebar.button("Search"):
        # Display selected preferences
        st.subheader("Your Preferences:")
        st.write(f"*Budget:* Rs. {budget}")
        st.write(f"*Distance:* {distance} kms")
        st.write(f"*Location:* {location}")

    # Input container
    st.markdown('<div class="input-container">', unsafe_allow_html=True)

    # Add some instructions
    st.markdown(
        """
        <div class="instructions-container">
            <h2>How to use:</h2>
            <ol>
                <li>Adjust your budget, preferred distance, and location in the sidebar.</li>
                <li>Click the 'Search' button to find restaurants.</li>
                <li>Explore the results based on your choices.</li>
                <li>Enjoy your meal!</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Close input container
    st.markdown('</div>', unsafe_allow_html=True)

    # Details container
    st.markdown('<div class="details-container">', unsafe_allow_html=True)

    # Add Details button
    if st.button("Add Details"):
        # Display the entered details
        st.markdown(
            f"""
            <div class="detail-card">
                <p><strong>Entered Details:</strong></p>
                <p><strong>Budget:</strong> Rs. {budget}</p>
                <p><strong>Distance:</strong> {distance} kms</p>
                <p><strong>Location:</strong> {location}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        (run(budget, location, float(distance) * 1000))

        # Display the content of the text file with text style
        text_file_path = "textfile1.txt"  # Replace with your text file path
        with open(text_file_path, "r") as text_file:
            text_content = text_file.read()
        st.markdown(
            """
            <div class="detail-card">
                <p><strong>Restaurants Near You at Your Budget:</strong></p>
                <p>{}</p>
            </div>
            """.format(text_content),
            unsafe_allow_html=True
        )

    # Close details container
    st.markdown('</div>', unsafe_allow_html=True)

    # Render Footer
    st.markdown(footer_html, unsafe_allow_html=True)

    # Close app container
    st.markdown('</div>', unsafe_allow_html=True)
