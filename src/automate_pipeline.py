from src.util.download_util import download_wait
from src.util.download_util import num_files
from src.extraction.extract import extract
from src.util.process_data_util import process_extracted_data, split_file

username = "xiaofeng@sharethis.com"
password = "a85beacf"
RAW_DATA_PATH = "/Users/kennywu/Documents/adsupport_pipeline/raw_domains/sharethis-domains-0813.csv"
SPLIT_DATA_DIRECTORY = "/Users/kennywu/Documents/adsupport_pipeline/data"
EXTRACT_DIRECTORY = "/Users/kennywu/Documents/adsupport_pipeline/extracted_data/" #publicwww downloads go here
PROCESSED_DATA_DIRECTORY = "/Users/kennywu/Documents/adsupport_pipeline/processed_data"
REGEX_TEXT = """|(adsbygoogle)|
|(googleadservices)|
|(g.doubleclick.net)|
|(\/ads\.)|
|(amazon-adsystem.com)|
|(.criteo)|
|(taboola.com)|
|(.outbrain)|
|(.pubmatic)|
|(buysellads.)|"""

split_file(RAW_DATA_PATH, SPLIT_DATA_DIRECTORY, chunk_size=30000)
extracter = extract(username, password, EXTRACT_DIRECTORY)
extracter.remove_all_files()
extracter.upload_files(SPLIT_DATA_DIRECTORY, timeout=30)
extracter.extract_data(REGEX_TEXT, num_files=10, file_retries=1, file_min_size=600000)
process_extracted_data(EXTRACT_DIRECTORY, PROCESSED_DATA_DIRECTORY, "processed.csv")
extracter.quit()
