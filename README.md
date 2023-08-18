# ad_automation-
Automate ad dectection via publicwww
Uses selenium (firefox driver), and pandas for pre and post processing of data
Run Automate Pipeline Class 
Pipeline process - 
1) Upload inital domain data to raw_domains folder as csv (RAW_DATA_PATH) variable
2) Code splits domains into 30k chunks and automatically uploads and extracts ad regex from lists
3) Extracted data is sent to extracted data folder
4) Data is cleaned and aggregated and sent to processed_data folder as "processed.csv" 

