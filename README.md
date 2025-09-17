# gis-population-app

## Why This Project Matters

This project is designed as a hands-on showcase of my skills in **Python, MySQL, Docker, data visualization, and GIS (Geographic Information Systems)**.  
It demonstrates how I can design, build, and containerize a complete application that integrates multiple technologies often used in DevOps, data-driven environments, and spatial data analysis.

### Skills Demonstrated
- **Python**: building CLI tools, working with APIs, processing CSV and GeoJSON data.  
- **Databases (MySQL)**: schema creation, data insertion, and querying via Python integration.  
- **Data Visualization & GIS**: creating trend graphs with `matplotlib` and interactive spatial maps with `folium`.  
- **APIs & Data Integration**: fetching real-world data from the World Bank API and GeoJSON sources.  
- **Docker & Docker Compose**: orchestrating multi-container environments (app + database).  
- **Geospatial Analysis**: geocoding with `geopy`, working with country boundaries, choropleth mapping, and interactive map generation. 

This application highlights my ability to combine **development**, **data engineering**, **DevOps practices**, and **GIS skills** into a single project — making it a strong example of my problem-solving and technical skills.

---

## Introduction

This repository contains a simple GIS CLI Python application that works with continents, countries, and their population data.  
It integrates with a MySQL database to store the data, and can be easily run using Docker containers (via `docker-compose`).

### Main Features
- Fetching population data for selected countries and years via the World Bank API [[1]](#references),
- Managing continents, countries and population data in MySQL (creation, reading, and storage),
- Creating population trend graphs (PNG) with `matplotlib` for selected countries and years based on CSV files,
- Fetching GeoJSON files with country boundaries via world.geo.json [[2]](#references), 
- Geocoding country locations using `geopy` `Nominatim` [[3,4,5]](#references),
- Creating interactive OpenStreetMap [[5]](#references) maps (markers and choropleths) using `folium` [[6]](#references).

---

## Prerequisites

#### 1. Install [Docker Desktop](https://docs.docker.com/desktop/) to run containers locally.
#### 2. Clone this repository to your local machine.
#### 3. Set your own `MYSQL_ROOT_PASSWORD` and `MYSQL_PASSWORD` in the `.env` file.

---

## Docker Setup

<p> Once Docker Desktop is installed, you can run all required containers.<br>
I recommend using Git Bash inside Visual Studio Code, but Windows CMD, PowerShell, or macOS/Linux Terminal will also work.</p> 

#### 1. Start the application and database containers in detached mode:

`docker compose -f containers/docker-compose.yml up -d`

**Note:** the `population-app` container will wait until `mysql-db` is up and in a healthy state.

#### 2. Log into the application container to run the app:

`docker exec -it population-app bash`

#### Additional Commands

To access the MySQL container:

`docker exec -it mysql-db bash`

Then log into the database (enter the password manually when prompted):

`mysql -u app -p`

---

## Running the Application

#### 1. After logging into the `population-app` container, start the application:

`python app.py`

#### 2. Follow the step-by-step menu to use the app’s functionalities.

![figure1](/readme_figures/figure1.png)

---

## Application Workflow

### Step 1. 
Insert data into the `continents` table. For example, add "Europe".

![figure2](/readme_figures/figure2.png)

### Step 2. 
View the contents of the `continents` table and select which continent to work with.

![figure3](/readme_figures/figure3.png)

### Step 3. 
Display countries belonging to the selected continent.

![figure4](/readme_figures/figure4.png)

### Step 4. 
Fetch population data from the World Bank API [[1]](#references) for chosen year.

**Note:** If you want to fetch data for other years, simply repeat Step 4 (fetching) and Step 5 (inserting). Some data for specific countries/years may not be available in the API.

![figure5](/readme_figures/figure5.png)

### Step 5. 
Create the `countries_population` table in MySQL and insert the fetched data.

![figure6](/readme_figures/figure6.png) 

### Step 6.
Work with graph and marker map.

6.1. Choose countries and years, then export SQL data to a `population_data.csv` file.

![figure7](/readme_figures/figure7.png)

6.2. Generate a `graph.png` and `markers_map.html`.

![figure8](/readme_figures/figure8.png)

Example outputs:

![sample_graph](/readme_figures/sample_graph.png)

![sample_markers_map](/readme_figures/sample_markers_map.png)

### Step 7. 
Create a choropleth map.

Step 7.1. Select countries for the map.

![figure9](/readme_figures/figure9.png)

Step 7.2. Fetch GeoJSON data from world.geo.json [[2]](#references), save it as `filtered_countries.geojson`, and generate `choropleth_map.html`.

![figure10](/readme_figures/figure10.png)

Example:

![sample_choropleth_map](/readme_figures/sample_choropleth_map.png)

### Step 8.
Create an interactive merged map (markers + choropleth).

Step 8.1. Select countries and years.

![figure11](/readme_figures/figure11.png)

Step 8.2. Generate the interactive `merged_map.html`.

![figure12](/readme_figures/figure12.png)

Example:

![sample_merged_map](/readme_figures/sample_merged_map.png)

---

## References

[1] The World Bank Group API: https://api.worldbank.org

[2] world.geo.json - johan's GitHub repository: https://github.com/johan/world.geo.json

[3] GeoPy Documentation: https://geopy.readthedocs.io/en/stable/

[4] Nominatim: https://nominatim.org/

[5] OpenStreetMap Foundation: https://osmfoundation.org/wiki/Main_Page

[6] Folium Documentation: https://python-visualization.github.io/folium/latest/

[7] ISO 3166-1 alpha-2 codes - Wikipedia: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2