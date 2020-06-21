## **Project: Capstone**
The purpose of this project is to process Covid-19 data in an attempt to analyze & visualize the data to derive statistical information & study patterns in Covid cases in the USA & worldwide.

### **Data**
The data is obtained from two distinct sources.

* Source 1: **`Covid19API`** - **https://covid19api.com**
    
    We particularly hit two endpoints - 
    
    1. **https://api.covid19api.com/countries** - This endpoint returns a list of all countries for which covid data is available
    
    2. **https://api.covid19api.com/dayone/country/country-name** - This endpoint returns covid data for the given country.
    
    **Sample Response -** 
    
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
      
    **Data Format -** **JSON**
     
    Following is the Row Count for each country - 
    
    |     | Slug                                         |   Count |
    |----:|:---------------------------------------------|--------:|
    |   0 | isle-of-man                                  |       0 |
    |   1 | jersey                                       |       0 |
    |   2 | belarus                                      |     114 |
    |   3 | saint-barthélemy                             |       0 |
    |   4 | tanzania                                     |      97 |
    |   5 | yemen                                        |      72 |
    |   6 | libya                                        |      89 |
    |   7 | chile                                        |     110 |
    |   8 | eritrea                                      |      92 |
    |   9 | antarctica                                   |       0 |
    |  10 | austria                                      |     117 |
    |  11 | china                                        |    4964 |
    |  12 | kuwait                                       |     118 |
    |  13 | kyrgyzstan                                   |      95 |
    |  14 | saint-lucia                                  |      99 |
    |  15 | zimbabwe                                     |      93 |
    |  16 | malta                                        |     106 |
    |  17 | burundi                                      |      82 |
    |  18 | cocos-keeling-islands                        |       0 |
    |  19 | germany                                      |     146 |
    |  20 | korea-south                                  |     151 |
    |  21 | micronesia                                   |       0 |
    |  22 | mongolia                                     |     103 |
    |  23 | portugal                                     |     111 |
    |  24 | switzerland                                  |     117 |
    |  25 | united-arab-emirates                         |     144 |
    |  26 | south-sudan                                  |      77 |
    |  27 | algeria                                      |     117 |
    |  28 | cambodia                                     |     146 |
    |  29 | cyprus                                       |     104 |
    |  30 | gambia                                       |      96 |
    |  31 | new-caledonia                                |       0 |
    |  32 | azerbaijan                                   |     112 |
    |  33 | bosnia-and-herzegovina                       |     108 |
    |  34 | french-polynesia                             |       0 |
    |  35 | pitcairn                                     |       0 |
    |  36 | somalia                                      |      97 |
    |  37 | argentina                                    |     110 |
    |  38 | panama                                       |     103 |
    |  39 | romania                                      |     116 |
    |  40 | saint-vincent-and-the-grenadines             |      99 |
    |  41 | togo                                         |     107 |
    |  42 | angola                                       |      93 |
    |  43 | ghana                                        |      99 |
    |  44 | lebanon                                      |     121 |
    |  45 | slovakia                                     |     107 |
    |  46 | ala-aland-islands                            |       0 |
    |  47 | faroe-islands                                |       0 |
    |  48 | new-zealand                                  |     114 |
    |  49 | papua-new-guinea                             |      93 |
    |  50 | poland                                       |     109 |
    |  51 | tunisia                                      |     109 |
    |  52 | malaysia                                     |     148 |
    |  53 | peru                                         |     107 |
    |  54 | solomon-islands                              |       0 |
    |  55 | iraq                                         |     118 |
    |  56 | cook-islands                                 |       0 |
    |  57 | cuba                                         |     101 |
    |  58 | fiji                                         |      94 |
    |  59 | liechtenstein                                |     109 |
    |  60 | pakistan                                     |     116 |
    |  61 | palestine                                    |     108 |
    |  62 | rwanda                                       |      99 |
    |  63 | british-virgin-islands                       |       0 |
    |  64 | russia                                       |     142 |
    |  65 | sudan                                        |     100 |
    |  66 | iran                                         |     123 |
    |  67 | mali                                         |      88 |
    |  68 | united-kingdom                               |    1069 |
    |  69 | estonia                                      |     115 |
    |  70 | guyana                                       |     101 |
    |  71 | jamaica                                      |     102 |
    |  72 | japan                                        |     151 |
    |  73 | el-salvador                                  |      94 |
    |  74 | antigua-and-barbuda                          |     100 |
    |  75 | bulgaria                                     |     105 |
    |  76 | christmas-island                             |       0 |
    |  77 | martinique                                   |       0 |
    |  78 | congo-brazzaville                            |      98 |
    |  79 | saint-kitts-and-nevis                        |      88 |
    |  80 | seychelles                                   |      99 |
    |  81 | gibraltar                                    |       0 |
    |  82 | honduras                                     |     102 |
    |  83 | lao-pdr                                      |      89 |
    |  84 | botswana                                     |      83 |
    |  85 | jordan                                       |     110 |
    |  86 | mexico                                       |     114 |
    |  87 | oman                                         |     118 |
    |  88 | saint-martin-french-part                     |       0 |
    |  89 | sao-tome-and-principe                        |      76 |
    |  90 | sierra-leone                                 |      82 |
    |  91 | venezuela                                    |      99 |
    |  92 | belgium                                      |     138 |
    |  93 | albania                                      |     104 |
    |  94 | andorra                                      |     111 |
    |  95 | chad                                         |      94 |
    |  96 | dominica                                     |      91 |
    |  97 | hungary                                      |     109 |
    |  98 | thailand                                     |     151 |
    |  99 | armenia                                      |     112 |
    | 100 | australia                                    |    1008 |
    | 101 | kazakhstan                                   |     100 |
    | 102 | saint-pierre-and-miquelon                    |       0 |
    | 103 | suriname                                     |      99 |
    | 104 | american-samoa                               |       0 |
    | 105 | guernsey                                     |       0 |
    | 106 | haiti                                        |      93 |
    | 107 | mayotte                                      |       0 |
    | 108 | niger                                        |      93 |
    | 109 | samoa                                        |       0 |
    | 110 | south-georgia-and-the-south-sandwich-islands |       0 |
    | 111 | bolivia                                      |     102 |
    | 112 | namibia                                      |      99 |
    | 113 | bermuda                                      |       0 |
    | 114 | maldives                                     |     105 |
    | 115 | french-southern-territories                  |       0 |
    | 116 | belize                                       |      90 |
    | 117 | canada                                       |    1508 |
    | 118 | hong-kong-sar-china                          |       0 |
    | 119 | norway                                       |     116 |
    | 120 | cameroon                                     |     107 |
    | 121 | mauritania                                   |      99 |
    | 122 | nigeria                                      |     114 |
    | 123 | malawi                                       |      80 |
    | 124 | bahrain                                      |     118 |
    | 125 | mauritius                                    |      95 |
    | 126 | anguilla                                     |       0 |
    | 127 | france                                       |    1145 |
    | 128 | gabon                                        |      99 |
    | 129 | latvia                                       |     111 |
    | 130 | tajikistan                                   |      52 |
    | 131 | barbados                                     |      96 |
    | 132 | dominican-republic                           |     112 |
    | 133 | falkland-islands-malvinas                    |       0 |
    | 134 | morocco                                      |     111 |
    | 135 | bouvet-island                                |       0 |
    | 136 | guadeloupe                                   |       0 |
    | 137 | india                                        |     143 |
    | 138 | nauru                                        |       0 |
    | 139 | united-states                                |  247898 |
    | 140 | bahamas                                      |      97 |
    | 141 | finland                                      |     144 |
    | 142 | guinea                                       |     100 |
    | 143 | paraguay                                     |     105 |
    | 144 | syria                                        |      91 |
    | 145 | qatar                                        |     113 |
    | 146 | comoros                                      |      52 |
    | 147 | senegal                                      |     111 |
    | 148 | taiwan                                       |     151 |
    | 149 | turkey                                       |     102 |
    | 150 | ethiopia                                     |     100 |
    | 151 | luxembourg                                   |     113 |
    | 152 | puerto-rico                                  |       0 |
    | 153 | djibouti                                     |      95 |
    | 154 | italy                                        |     142 |
    | 155 | afghanistan                                  |     118 |
    | 156 | kenya                                        |     100 |
    | 157 | korea-north                                  |       0 |
    | 158 | liberia                                      |      97 |
    | 159 | northern-mariana-islands                     |       0 |
    | 160 | kosovo                                       |      87 |
    | 161 | guatemala                                    |      99 |
    | 162 | kiribati                                     |       0 |
    | 163 | zambia                                       |      95 |
    | 164 | cayman-islands                               |       0 |
    | 165 | brazil                                       |     116 |
    | 166 | guinea-bissau                                |      88 |
    | 167 | macao-sar-china                              |       0 |
    | 168 | macedonia                                    |     116 |
    | 169 | marshall-islands                             |       0 |
    | 170 | montserrat                                   |       0 |
    | 171 | timor-leste                                  |      91 |
    | 172 | uruguay                                      |      99 |
    | 173 | moldova                                      |     105 |
    | 174 | réunion                                      |       0 |
    | 175 | saint-helena                                 |       0 |
    | 176 | turkmenistan                                 |       0 |
    | 177 | brunei                                       |     104 |
    | 178 | british-indian-ocean-territory               |       0 |
    | 179 | cote-divoire                                 |     102 |
    | 180 | greenland                                    |       0 |
    | 181 | sri-lanka                                    |     146 |
    | 182 | bangladesh                                   |     105 |
    | 183 | myanmar                                      |      86 |
    | 184 | turks-and-caicos-islands                     |       0 |
    | 185 | wallis-and-futuna-islands                    |       0 |
    | 186 | palau                                        |       0 |
    | 187 | grenada                                      |      91 |
    | 188 | madagascar                                   |      93 |
    | 189 | sweden                                       |     142 |
    | 190 | heard-and-mcdonald-islands                   |       0 |
    | 191 | guam                                         |       0 |
    | 192 | tokelau                                      |       0 |
    | 193 | georgia                                      |     116 |
    | 194 | san-marino                                   |     115 |
    | 195 | tonga                                        |       0 |
    | 196 | indonesia                                    |     111 |
    | 197 | denmark                                      |     321 |
    | 198 | holy-see-vatican-city-state                  |     107 |
    | 199 | saudi-arabia                                 |     111 |
    | 200 | singapore                                    |     150 |
    | 201 | us-minor-outlying-islands                    |       0 |
    | 202 | virgin-islands                               |       0 |
    | 203 | colombia                                     |     107 |
    | 204 | benin                                        |      97 |
    | 205 | burkina-faso                                 |     103 |
    | 206 | ireland                                      |     113 |
    | 207 | netherlands-antilles                         |       0 |
    | 208 | norfolk-island                               |       0 |
    | 209 | uganda                                       |      92 |
    | 210 | lesotho                                      |      39 |
    | 211 | monaco                                       |     113 |
    | 212 | serbia                                       |     107 |
    | 213 | western-sahara                               |      77 |
    | 214 | czech-republic                               |     112 |
    | 215 | aruba                                        |       0 |
    | 216 | lithuania                                    |     114 |
    | 217 | vanuatu                                      |       0 |
    | 218 | tuvalu                                       |       0 |
    | 219 | vietnam                                      |     150 |
    | 220 | israel                                       |     121 |
    | 221 | croatia                                      |     117 |
    | 222 | egypt                                        |     128 |
    | 223 | french-guiana                                |       0 |
    | 224 | greece                                       |     116 |
    | 225 | svalbard-and-jan-mayen-islands               |       0 |
    | 226 | congo-kinshasa                               |     102 |
    | 227 | equatorial-guinea                            |      98 |
    | 228 | niue                                         |       0 |
    | 229 | spain                                        |     141 |
    | 230 | iceland                                      |     114 |
    | 231 | mozambique                                   |      91 |
    | 232 | nicaragua                                    |      94 |
    | 233 | philippines                                  |     143 |
    | 234 | slovenia                                     |     108 |
    | 235 | ukraine                                      |     110 |
    | 236 | cape-verde                                   |      93 |
    | 237 | swaziland                                    |      99 |
    | 238 | montenegro                                   |      96 |
    | 239 | netherlands                                  |     487 |
    | 240 | trinidad-and-tobago                          |      99 |
    | 241 | uzbekistan                                   |      98 |
    | 242 | bhutan                                       |     107 |
    | 243 | central-african-republic                     |      98 |
    | 244 | costa-rica                                   |     107 |
    | 245 | ecuador                                      |     112 |
    | 246 | nepal                                        |     148 |
    | 247 | south-africa                                 |     108 |


* Source 2: 
    
    **`CDC`** - **https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/county-map.html**
            
    **`USAFacts`** - **https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/**
            
    The data mentioned on the CDC website is sourced from USAFacts everyday.
    
    The data was downloaded and stored in the covid_county_data folder partitioned day-wise.
    
    **Data Format -** **CSV**
    
    **Row Count -**
    
    |     | folder                                       | Number of Files | Number of Rows |
    |----:|:---------------------------------------------|-----------------|---------------:|
    |   0 | confirmed_cases                              |       150       |  150*3194      |
    |   1 | covid_deaths                                 |       150       |  150*3194      |
    |   2 | county_populcation.csv                       |         1       |      3194      |
    

### <b>ETL Architecture</b>

<img src="capstone_etl.png" width="700" height="500" >
