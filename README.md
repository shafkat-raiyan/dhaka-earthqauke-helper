# Dhaka Earthquake Helper 

A Python desktop application designed to provide immediate assistance and information during earthquake emergencies in Dhaka. 

## Key Features
*  **Nearest Hospital Locator:** Uses NumPy math to calculate the top 3 closest hospitals to your location and features a priority system based on hospital capacity for women, children, and severe injuries.
*  **Safe Grounds Search:** Allows users to find and administrators to manage safe open spaces in the city.
*  **Emergency Guidelines:** Provides instant safety instructions on what to do during an earthquake.
*  **Query History:** Automatically saves and loads your past emergency searches using local file storage.

## How to Run

**1. Create a Virtual Environment:**
`python -m venv venv`

**2. Activate the Environment:**
`venv\Scripts\activate` (Windows)

`source venv/bin/activate` (Mac/Linux)

**3. Install Dependencies:**
`pip install -r requirements.txt`

**4. Run the Application:**
`python app.py`
