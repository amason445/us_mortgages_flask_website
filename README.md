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
 
