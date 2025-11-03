# gis-population-app

![sample_merged_map](/readme_figures/app/sample_merged_map.png)

## Why This Project Matters

This project is a hands-on showcase of my skills in **Python, MySQL, Docker, Kubernetes, Terraform and data visualization** — and reflects my interest in **GIS** (Geographic Information Systems). It demonstrates how I can design, build, and containerize a&nbsp;complete application that integrates multiple technologies — bringing together **development**, **data engineering**, and **DevOps practices** with **geospatial analysis**.

### Skills Demonstrated
- **Python**: building CLI tools, working with APIs, processing CSV and GeoJSON data.
- **APIs & Data Integration**: fetching real-world data from the World Bank API and GeoJSON sources.   
- **Databases (MySQL)**: schema creation, data insertion, and querying via Python integration.
- **Docker & Kubernetes**: orchestrating multi-container environments (app + database).
- **Terraform**: implementing Infrastructure as Code (IaC) to automate environment provisioning and configuration.   
- **Data Visualization & GIS**: creating trend graphs with `matplotlib`, interactive maps with `folium` and geocoding with `geopy`.
- **Development & Automation**: creating a local development cluster using `kind` (Kubernetes-in-Docker), `devbox` (isolated dev environment) and `task` (task automation).

---

## Introduction

This repository contains a simple GIS CLI Python application that works with continents, countries, and their population data. It integrates with a MySQL database to store the data, and can be easily run using Docker containers — whether through `docker-compose`, Kubernetes, or Terraform.

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
#### 2. Install an additional [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) distribution (e.g., Ubuntu) to provide a Linux environment for Kubernetes and development operations. Enable its integration within Docker Desktop. Log into the specific distro using the command: 
`wsl -d <distro>`
#### 3. Install Devbox within your Linux distro using:
`curl -fsSL https://get.jetify.com/devbox | bash` <br>
<br>
or follow the [Jetify Documentation](https://www.jetify.com/docs/devbox/installing-devbox).

#### 4. Clone this repository to your local machine.
#### 5. Set your own `MYSQL_ROOT_PASSWORD` and `MYSQL_PASSWORD` in the `.env` file.

---

## Devbox

Devbox allows you to create an isolated development environment (“box”) within your Linux distro and initialize a dedicated shell to work with specific tools, without affecting the rest of your Ubuntu system. It works similarly to Python’s .venv.

In the main directory, the `devbox.json` file defines all dependencies to be installed — for example, `kubectl` (to manage Kubernetes), `kind` (to create a local Kubernetes cluster), `go-task` (to automate command-based tasks), or `terraform` (to define infrastructure as code).

Additionally, initialization hooks enable `kubectl` command completion and create useful aliases such as `k` for `kubectl` and `tl` for `task --list-all`.

#### To start the Devbox shell to work with the defined dependencies, run:

`devbox shell`

---

## Docker Approach

Once Docker Desktop and Devbox are installed, you can run all required containers using a simple Docker Compose–based approach.
For that, you’ll use the Task app. Simply type `tl` in your terminal to list all available tasks within the project.
To view the specific commands behind each task, check the `Taskfile.yaml` files in the main directory or in subdirectories such as docker or kubernetes.

![figure1](/readme_figures/task/figure1.png)

#### 1. Start the application and database containers in detached mode

`task docker:01-compose`

**Note:** the `population-app` container will wait until `mysql-db` is up and in a healthy state.

#### 2. Log into the application container to run the app

`task 1-docker:02-log-into-population-app-container`

#### 3. Log into the database container when needed

To access the MySQL db container:

`task 1-docker:03-log-into-mysql-db-container`

Then log into the database (enter the password manually when prompted):

`mysql -u app -p`

#### 4. Delete the created containers

`task 1-docker:04-delete-composed-containers`

---

## Kubernetes Approach

You can also run the application using Kubernetes.
For that purpose, a Kind (Kubernetes in Docker) cluster will be created, and the application resources will be deployed to it using .yaml manifests.

### Kind Cluster
---

#### 1. Generate `kind-config.yaml` file with the path to your current working directory

`task 2-kind:01-generate-config`

#### 2. Create a local Kind cluster to work with Kubernetes

`task 2-kind:02-create-cluster`

#### 3. When you finish working with the app and Kubernetes, delete the cluster

`task 2-kind:03-delete-cluster`

### Kubernetes Operations
---

#### 1. Create a Kubernetes namespace within your Kind cluster and set it as default

`task 3-k8s:01-create-namespace`

#### 2. Build Docker images (if they haven't been built yet)

`task 3-k8s:02-build-images`

#### 3. Load the images into the Kind cluster

`task 3-k8s:03-load-images-into-kind-cluster`

#### 4. Create a Kubernetes secret for database credentials

`task 3-k8s:04-create-db-k8s-secret`

#### 5. Deploy the `mysql-db` to the Kind cluster

`task 3-k8s:05-deploy-mysql-db`

#### 6. Deploy the `population-app` to the Kind cluster

`task 3-k8s:06-deploy-population-app`

#### 7. Log into the `population-app` pod

`task 3-k8s:07-log-into-population-app-pod`

#### 8. Log into the `mysql-db` pod

`task 3-k8s:08-log-into-mysql-db-pod`

#### 9. Delete the `gis-population-app` namespace and all its resources

`task 3-k8s:09-delete-namespace`

#### 10. Remove the Docker images from the Kind cluster

`task 3-k8s:10-remove-images-from-kind-cluster`

---

## Terraform Approach

You can also run the application using Terraform together with Kubernetes.  
For this purpose, a local Kind cluster will be created using the Terraform Kind provisioner, and the application resources will be deployed to it using `.tf` templates.

#### 1. Initialize Terraform

`task 4-terraform:01-initialize`

#### 2. Create a local Kind cluster to work with Kubernetes

`task 4-terraform:02-kind-cluster-setup`

#### 3. Create a Kubernetes namespace within your Kind cluster and set it as default

`task 4-terraform:03-creating-kubernetes-namespace`

#### 4. Build Docker images (if they haven't been built yet)

`task 3-k8s:02-build-images`

#### 5. Load the images into the Kind cluster

`task 3-k8s:03-load-images-into-kind-cluster`

#### 6. Create a Kubernetes secret for database credentials

`task 3-k8s:04-create-db-k8s-secret`

#### 7. Create other Kubernetes resources

`task 4-terraform:04-creating-kubernetes-resources`

#### 8. Log into the `population-app` pod

`task 3-k8s:07-log-into-population-app-pod`

#### 9. Log into the `mysql-db` pod

`task 3-k8s:08-log-into-mysql-db-pod`

#### 10. Destroy all resources created by Terraform

`task 4-terraform:05-destroy`

---

## Running the Application

#### 1. After logging into the `population-app` container, start the application:

`python app.py`

#### 2. Follow the step-by-step menu to use the app’s functionalities.

![figure1](/readme_figures/app/figure1.png)

---

## Application Workflow

### Step 1. 
Insert data into the `continents` table. For example, add "Europe".

![figure2](/readme_figures/app/figure2.png)

### Step 2. 
View the contents of the `continents` table and select which continent to work with.

![figure3](/readme_figures/app/figure3.png)

### Step 3. 
Display countries belonging to the selected continent.

![figure4](/readme_figures/app/figure4.png)

### Step 4. 
Fetch population data from the World Bank API [[1]](#references) for chosen year.

**Note:** If you want to fetch data for other years, simply repeat Step 4 (fetching) and Step 5 (inserting). Some data for specific countries/years may not be available in the API.

![figure5](/readme_figures/app/figure5.png)

### Step 5. 
Create the `countries_population` table in MySQL and insert the fetched data.

![figure6](/readme_figures/app/figure6.png) 

### Step 6.
Work with graph and marker map.

6.1. Choose countries and years, then export SQL data to a `population_data.csv` file.

![figure7](/readme_figures/app/figure7.png)

6.2. Generate a `graph.png` and `markers_map.html`.

![figure8](/readme_figures/app/figure8.png)

Example outputs:

![sample_graph](/readme_figures/app/sample_graph.png)

![sample_markers_map](/readme_figures/app/sample_markers_map.png)

### Step 7. 
Create a choropleth map.

Step 7.1. Select countries for the map.

![figure9](/readme_figures/app/figure9.png)

Step 7.2. Fetch GeoJSON data from world.geo.json [[2]](#references), save it as `filtered_countries.geojson`, and generate `choropleth_map.html`.

![figure10](/readme_figures/app/figure10.png)

Example:

![sample_choropleth_map](/readme_figures/app/sample_choropleth_map.png)

### Step 8.
Create an interactive merged map (markers + choropleth).

Step 8.1. Select countries and years.

![figure11](/readme_figures/app/figure11.png)

Step 8.2. Generate the interactive `merged_map.html`.

![figure12](/readme_figures/app/figure12.png)

Example:

![sample_merged_map](/readme_figures/app/sample_merged_map.png)

---

## References

[1] The World Bank Group API: https://api.worldbank.org

[2] world.geo.json - johan's GitHub repository: https://github.com/johan/world.geo.json

[3] GeoPy Documentation: https://geopy.readthedocs.io/en/stable/

[4] Nominatim: https://nominatim.org/

[5] OpenStreetMap Foundation: https://osmfoundation.org/wiki/Main_Page

[6] Folium Documentation: https://python-visualization.github.io/folium/latest/

[7] ISO 3166-1 alpha-2 codes - Wikipedia: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

[8] Docker: Beigneer to Pro: https://courses.devopsdirective.com/docker-beginner-to-pro/lessons/00-introduction/01-main

[9] Kubernetes: Beginner to Pro: https://courses.devopsdirective.com/kubernetes-beginner-to-pro/lessons/00-introduction/01-main

[10] Terraform: Beginner to Pro: https://courses.devopsdirective.com/terraform-beginner-to-pro/lessons/00-introduction/01-main