# Data Science Blog Post

# Table of Contents

* [Installation](#installation)
* [Project Motivation](#project-motivation)
* [Files Description](#file-description)
* [Results](#results)
* [Licensing, Authors, Acknowledgements](#licensing-authors-acknowledgements)



# Installations

This project should work fine with a free subscription in [Google Colaboratory](https://research.google.com/colaboratory). Once you create a free account follow the following steps:

1. Copy the content of this repository inside a folder called <my_folder>
2. Inside both notebooks run the following cells:

    - Cell #1

            from google.colab import drive
            drive.mount('/content/drive')
    
    - Cell #2

            import sys
            sys.path.append('/content/drive/<my_folder>')

3. Unzip the `datasets.zip` inside /<my_folder>/datasets. There should be 4 csv files containing the datasets from Airbnb Seattle and Airbnb Boston

These steps should be enough to run all analysis inside both `ExplorationCalendars.ipynb` and `ExplorationListings.ipynb`.

## Note

While running this notebooks you might need to install [scikit-learn](https://scikit-learn.org/). In order to do this just add the following cell to the notebook

    !pip install scikit-learn==0.20.4

# Project Motivation

As part of the first project for the Nanodegree Course in Data Science at Udacity I will analyze the Airbnb datasets for Seattle and Boston. After exploring them for a bit I came up with three questions:

1. _Can we find great accommodations at a fair price?_ 
2. _When is the best time to visit the city?_ 
3. _What are the most important listings aspects when setting a rent price?_ 

# Files Description

This repository contains two notebooks and a `.py` file that helped me answer the three questions above.

* `ExplorationCalendars.ipynb` - In this notebook you can find the transformations and explorations required to answer questions 1 and 2
* `ExplorationListings.ipynb` - In this notebook you can find the ml models trained to answer the question 3
* `helper_functions.py` - In this python script I stored the data cleaning and data transformation functions. Besides those you can find the functions that will plot all the graphs in this work

In both notebooks I walk you through the decisions made and how I arrived at each result and future steps to improve the models.

# Results

The main findings are presented at my [mediums post](https://medium.com/@jschubnell/from-tech-to-music-c00aa5c5f9e1). Other results and future steps are analyzed inside each notebook.

# Licensing, Authors, Acknowledgements

I must acknowledge Airbnb for providing the data necessary to conduct these experiments. Moreover, I want to thank the Udacity team for such an amazing course. Finally, feel free to clone and use the code provided in this repository.

For more inquires feel free to add me on [linkedin](https://www.linkedin.com/in/jo%C3%A3o-schubnell-lima/)
