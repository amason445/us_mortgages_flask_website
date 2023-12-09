# US Mortgage Data with Flask and CouchDB

## Project Summary
This repository contains artifacts from my second capstone project that I built during my graduate program at Regis University. For this project, I built a NoSQL database and a Flask website to analyze US Mortgage data. The mortgage data was sourced from the Consumer Protection Finance Bureau (CPFB). CouchDB views were written on top of this data and ingested into a Flask website which contains a variety of visualizations. The visualizations trend financial metrics over time and they are also mapped to state counties. This repository also includes the test cases and context for my CouchDB architecture.

The full scrape from the CPFB was 35 gigabytes and included full pipline data of around 90 million mortgage loans from 2018 to 2022. For this scope of this project, I took a subset of this data for Arizona, Colorado, New Mexico and Utah which was about 1.8 gigabytes and contained around 4,630,000 mortgages from 2018 to 2022. Additionally, I had some issues rendering and writing the website views. This portion required a lot of research and I eventually used OpenAI's ChatGPT to help me with some of the rendering, HTML and CSS. Finally, I originally intended to use HoloViews for this project but I switched to Folium. Folium seems to work really well with Flask because it renders cleanly and easily.

## Technology Used
- Flask
- CouchDB
- Python
- Pandas, GeoPandas, GeoJSON
- Matplotlib, Seaborn, Folium
- HTML/CSS

For all packages and dependenices used, please see requirements.txt. A vitural environment was used for this project and this file can be used to conigure it with pip.<br> Use:
`pip -r requirements.txt`

## Data Source

This data was source from the Consumer Protection Finance Bureau's Home Mortgage Disclosure Act API. The data collects lending records submitted by nationwide mortgage lenders focusing on residential mortgages. It covers a diverse range of products including fixed rate mortgages, adjustable rate mortgages, VA Loans, first and second liens and includes rich financial data ranging from the loan amount, loan term, interest rates to fees and products costs. Additionally, it includes rich demographic data including ethnicity, gender, income, geographical information and credit information (including Debt to Income). The API documentation and data dictionary are linked below:

- [API Documentation](https://ffiec.cfpb.gov/documentation/api/data-browser/)
- [Data Dictionary](https://ffiec.cfpb.gov/documentation/publications/loan-level-datasets/lar-data-fields)

## Project Layout
- CouchDB: Samples and Design Document: Contains sample JSON documents from the CouchDB Database and the most recent design document.
- ShapeETL: Contains a prototype script to process state and county geopgraphies so they can be joined with the mortgage data and rendered.
- app: Contains the full Flask app including modules and HTML/CSS templates needed to render the website.
- load_db: Contains the load process from the API to CouchDB. The initial logs are included.
- tests: Contains unit tests and the most recent outputs

## Flask Architecture
This website uses an "Model-View-View-Model" architecture detailed below. First, models are queried from CouchDB design document and combined, hen they are wrangled and visualized before finally being rendered into an HMTL/CSS front end view. The models are built using something similar to an interface in Java which makes them easy to reuse and test. These models are brought into a variety of view models leveraging Seaborn, Matplotlib and Folium.

- [MVVM Architecture](https://learn.microsoft.com/en-us/dotnet/architecture/maui/mvvm)

## Sample Data and Results
Below, I've included some sample visualizations from the project from Colorado.
![alt_text](https://github.com/amason445/us_mortgages_map_reduce/blob/main/tests/graphs/loan_volume_graphs/CO_volumes.png)
![alt text](https://github.com/amason445/us_mortgages_map_reduce/blob/main/tests/graphs/interest_rate_graphs/CO_interest_rate.png)

## Future Ideas
- Migrate the website to the Cloud to increase processing power and scale
- Build a distributed system with CouchDB to increase scale
- Scrape more US States and set up the process to scrape annually
- Build out the website to include more financial metrics, borrower credit and income data and demographic data
- Set up robust security and error handling for public deployment
- Incorporate other Flask packages like an email server or migrate to a more robust framework like Django

## References
- Awati, R., & Wigmore, I. (2022). What is monolithic architecture in software? WhatIs.com. https://www.techtarget.com/whatis/definition/monolithic-architecture
- Color Hunt. (n.d.). Color palette: #F3EEEA #ebe3d5 #B0A695 #776B5D. https://colorhunt.co/palette/f3eeeaebe3d5b0a695776b5d
- Consumer Financial Protection Bureau. (n.d.). Home Mortgage Disclosure Act - Data browser API. HMDA Documentation. https://ffiec.cfpb.gov/documentation/api/data-browser/
- Consumer Financial Protection Bureau. (n.d.). Home Mortgage Disclosure Act - Public HMDA - LAR Data Fields. HMDA Documentation. https://ffiec.cfpb.gov/documentation/publications/loan-level-datasets/lar-data-fields
- Design Documents - Apache CouchDB Documentation. (n.d.). https://docs.couchdb.org/en/stable/ddocs/index.html
- Frank, S. (n.d.). Home price to income ratio. Longtermtrends. https://www.longtermtrends.net/home-price-median-annual-income-ratio/ 
- GeeksforGeeks. (2023, July 10). HTML cheat sheet - a basic guide to HTML. https://www.geeksforgeeks.org/html-cheat-sheet-a-basic-guide-to-html/
- GeoPandas. (n.d.). Interactive mapping. https://geopandas.org/en/stable/docs/user_guide/interactive_mapping.html
- Grinberg, M. (2018). Flask web development: Developing web applications with Python. O’Reilly.
- HTML Cheat Sheet. (n.d.). JavaScript (JS) cheat sheet online. https://htmlcheatsheet.com/js/
- HTML Color Codes. (2015, September 4). Color picker. https://htmlcolorcodes.com/color-picker/
- What is CouchDB? IBM. (n.d.). https://www.ibm.com/topics/couchdb
- Mitrani, A. (2022, June 16). Creating choropleth maps with Python’s folium library. Medium. https://towardsdatascience.com/creating-choropleth-maps-with-pythons-folium-library-cfacfb40f56
- OpenAI. (2023). ChatGPT (Mar 14 version) [Large language model]. https://chat.openai.com/chat
- Python Visualization. (n.d.). Folium - Folium 0.1.dev1+g6040f42 documentation. https://python-visualization.github.io/folium/latest/
- Stonis, M. (n.d.). Model-View-ViewModel - .NET. Model-View-ViewModel - .NET | Microsoft Learn. https://learn.microsoft.com/en-us/dotnet/architecture/maui/mvvm
- US Census Bureau. (2022, December 5). Tiger/line shapefiles. Census.gov. https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
- W3Schools. (n.d.). CSS tutorial. https://www.w3schools.com/css/
- W3Schools. (n.d.). Java Interface. https://www.w3schools.com/java/java_interface.asp
![image](https://github.com/amason445/us_mortgages_map_reduce/assets/77219320/7349bd65-46a4-4f81-8772-1a847e52bde5)

