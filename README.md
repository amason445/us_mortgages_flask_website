# US Mortgage Data with Flask and CouchDB

## Project Summary
This repository contains artifacts from my second capstone project that I built during my graduate program at Regis University. For this project, I built a NoSQL database and a Flask website to analyze US Mortgage data. The mortgage data was sourced from the Consumer Protection Finance Bureau (CPFB) and contains nationwide residential mortgage loan data. It includes financial and demographic data for individual loans issued in the United States. The mortgages are diverse and include everything from standard, fixed rate loans, VA loans, and adjustable rate mortgages. CouchDB views were written on top of this data and ingested into a Flask website which contains a variety of visualizations. The visualizations trend financial metrics over time and they are also mapped to state counties. This repository also includes the test cases and context for my CouchDB architecture.

The full scrape from the CPFB was 35 gigabytes and included full pipline data of around 90 million mortgage loans from 2018 to 2022. For this scope of this project, I took a subset of this data for Arizona, Colorado, New Mexico and Utah which was about 1.8 gigabytes and contained around 4,630,000 mortgages from 2018 to 2022. Additionally, I had some issues rendering and writing the website views. This portion required a lot of research and I eventually used OpenAI's ChatGPT to help me with some of the rendering, HTML and CSS. Finally, I originally intended to use HoloViews for this project but I switched to Folium. Folium seems to work really well with Flask because it renders cleanly and easily.


 
