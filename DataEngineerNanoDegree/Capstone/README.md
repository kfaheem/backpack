## **Project: Capstone**
The purpose of this project is to process Covid-19 data in an attempt to analyze & visualize the data to derive statistical information & study patterns in Covid cases in the USA & worldwide.

### **Data**
The data is obtained from two distinct sources.

* Source 1: `Covid19API`["https://covid19api.com"]
    We particularly hit two endpoints - 
    1. "https://api.covid19api.com/countries" - This endpoint returns a list of all countries for which covid data is available
    2. "https://api.covid19api.com/dayone/country/<contry-name>" - This endpoint returns covid data for the given country.
    
    Sample Response - 
        [
          {
            "Country": "Switzerland",
            "CountryCode": "CH",
            "Lat": "46.82",
            "Lon": "8.23",
            "Cases": 1,
            "Status": "confirmed",
            "Date": "2020-02-25T00:00:00Z"
          },
          {
            "Country": "Switzerland",
            "CountryCode": "CH",
            "Lat": "46.82",
            "Lon": "8.23",
            "Cases": 1,
            "Status": "confirmed",
            "Date": "2020-02-26T00:00:00Z"
          }
      ]
### <b>ETL Architecture</b>

<img src="capstone_etl.png" width="550" height="150" ></b>

Row Count

confirmed cases - 150 files * 3194 rows
covid deaths - 150 files * 3194 rows
county_population - 3194 rows