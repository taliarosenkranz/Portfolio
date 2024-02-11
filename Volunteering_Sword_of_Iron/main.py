import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from google_sheets import fetch_google_sheets_data, upload_registration_data
from registration import registration_form

# main function to create the Streamlit app


def main():
    st.title("Volunteer Coordination Platform")

    # navigation sidebar
    menu = ["Volunteer", "Organization"]
    choice = st.sidebar.selectbox("Select Role", menu)

    if choice == "Volunteer":
        show_volunteer_page()
    elif choice == "Organization":
        show_organization_page()


# organization registration page content
def show_organization_page():
    st.subheader("Organization Registration")

    # registration form
    registration_data = registration_form()
    print(registration_data)

    upload_registration = upload_registration_data(registration_data)

# volunteer registration page content


def show_volunteer_page():
    st.subheader("Volunteer page")
    st.write("Fetching data from Google Sheets...")

    # fetch data from Google Sheet organizations doc
    data = fetch_google_sheets_data()

    # Display data from Google Sheets
    if data:
        st.write("Data fetched successfully!")
        # Create a list of coordinates and weights (number of volunteers needed)
        coordinates = [[float(info[1]), float(info[2]), int(info[3])]
                       for info in data]

        # Creating a folium map
        map = folium.Map(location=[31.0461, 34.8516], zoom_start=8,
                         min_zoom=6, max_zoom=12, tiles="OpenStreetMap", lang='en')

        # Define the boundaries of Israel
        bounds = [(29.5, 34.2), (33.5, 35.9)]
        # Restrict the map to show only Israel
        map.fit_bounds(bounds)

        # Initialize an empty list to store coordinates
        coordinates = []

        # Add markers for each location and populate coordinates list
        for location_info in data:
            # Assuming the first column contains location names
            location_name = location_info[0]
            # Assuming the second column contains latitude
            lat = float(location_info[1])
            # Assuming the third column contains longitude
            lon = float(location_info[2])
            # Assuming the fourth column contains number of volunteers needed
            num_volunteers_needed = int(location_info[3])

            # Append coordinates to the list
            coordinates.append([lat, lon, num_volunteers_needed])

            # Create marker
            popup_text = f"{location_name}<br>Volunteers Needed: {num_volunteers_needed}"
            folium.Marker([lat, lon], popup=popup_text).add_to(map)

        # Add heatmap layer
        HeatMap(coordinates).add_to(map)

        # Display the map
        folium_static(map)
    else:
        st.write(
            "Failed to fetch data from Google Sheets. Please check your credentials")


# run the main functin to start Streamlit application
if __name__ == "__main__":
    main()
