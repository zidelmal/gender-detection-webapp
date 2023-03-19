# gender-predictor-webapp

# Welcome to Gender Predictor WebApp

A Flask based project to predict the gender of a user, according to his FirstName.
The objectif from it is to correct the data related to gender, that encounter every data-driver company in the process of data analysis (profilling, churn prediction, defining persona, etc) or their marketing process.

# Overview of the webApp

![image](https://user-images.githubusercontent.com/88236219/226205360-0f012b32-cd4d-43da-806b-49c30053e601.png)

# Competitive Intelligence

# Welcome to Yassir Express CI

A Scrapy based project to scrape restaurants from different websites.
The objectif from it is to scrap multiple website in minimum time due to the daily need for this data.

## Installation

Use the following command to clone the project on your local machine
```bash
https://github.com/zidelmal/yassir-express-ci.git
```
Browse to the main folder using
```bash
cd yassir-express-ci
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

```bash
pip install -r requirements.txt
```
or
```bash
python -m pip install -r requirements.txt
```

## Single Usage

```bash
scrapy crawl [SpiderName]
```
[SpiderName] must be one of the following :

For Algeria : 
*  JumiaFoodDZ for www.food.jumia.dz
*  FoodBeeper for www.foodbeeper.com
*  Fast Delivery for www.fastdelivery.dz

For Morocco : 
*  JumiaFoodMA for www.food.jumia.ma
*  Glovo for www.glovoapp.com/ma/fr/
*  Kaalix for www.kaalix.com

For Tunisia : 
*  JumiaFoodTN for www.food.jumia.com.tn/
*  Glovo for www.glovoapp.com/tn/fr/

## Usage by bloc

```bash
python main.py
```
or 
```bash
python3 main.py
```
With this command the scraping of all sites based in the same country and it will match their data then save the result in a Google sheet to update a Looker Dashboard
