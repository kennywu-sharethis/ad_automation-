import os
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.util.download_util import download_wait, verify_file_size, get_publicwww_filename, remove_file
from src.util.download_util import num_files as nf
import time

class extract():
    WEBSITE_NAME = "https://publicwww.com"

    def __init__(self, username: str, password: str, extract_dir: str, num_clusters = 0):
        """

        :param username: username of publicww
        :param password: username of publicww
        :param extract_dir: requires absolute path
        :param num_clusters: initial number of clusters in publicwww
        """
        options = webdriver.FirefoxOptions()
        options.add_argument("--detach")
        options.set_preference("browser.download.folderList", 2)
        # Set the custom download directory path
        options.set_preference("browser.download.dir", extract_dir)
        self.driver = webdriver.Firefox(options=options)
        self.retrieve_website()
        self.login(username, password)
        self.extract_dir = extract_dir
        self.num_clusters = num_clusters

    def retrieve_website(self):
        self.driver.get(extract.WEBSITE_NAME)

    def login(self, username: str, password: str):
        # click login
        login = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/nav/ul[2]/li[2]/a")
        login.click()
        # enter details
        self.driver.find_element(By.XPATH, "//*[@id=\"input01\"]").send_keys(username)
        self.driver.find_element(By.XPATH, "//*[@id=\"input02\"]").send_keys(password)
        login = self.driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/form/div[3]/div/button")
        login.click()

    def upload_files(self, directory: str, timeout: int = 25):
        """
        Automate uploading of files, CANNOT UPLOAD MORE THAN 100
        CALL REMOVE_ALL_FILES BEFORE ENDING PROGRAM AFTER UPLOAD
        :param directory: directory folder of all csv files to be uploaded
        :param timeout: how long upload should take before timing out
        :return:
        """
        wait = WebDriverWait(self.driver, timeout)
        files = os.listdir(directory)
        self.to_cluster_page()
        for i, file in enumerate(files, start=1):
            (self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div/div[2]/form/input[1]")
             .send_keys(os.path.join(directory, file)))
            self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div/div[2]/form/input[2]").click()
            wait.until(EC.visibility_of_element_located((By.XPATH, f"//*[@id=\"cluster_name_{i}\"]")))
            self.num_clusters = i

    def remove_all_files(self):
        """
        Removes all files on cluster page
        Call before ending program to prevent error
        :return:
        """
        self.to_cluster_page()
        for i in range (1, 100):
            if len(self.driver.find_elements(By.XPATH, f"/html/body/div[2]/div/div/div/form/table/tbody/tr[{i}]/td[1]/input")):
                self.driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div/form/table/tbody/tr[{i}]/td[1]/input").click()
            else:
                break

        if len(self.driver.find_elements(By.XPATH, "/html/body/div[2]/div/div/div/form/input[8]")):
            self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/form/input[8]").click()
            alert = self.driver.switch_to.alert
            alert.accept()
        time.sleep(2)

    def to_cluster_page(self):
        cluster = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/nav/ul[1]/li[3]/a")
        cluster.click()

    def extract_data(self, regex: str = "", num_files: int = 0, file_retries: int = 0, file_min_size:int = 0):
        """
        Extracts all data into the extract directory specified by the class instance

        :param regex: regex extract - make sure each regex extraction is on own line - upto 10 regex
        :param num_files: number of files to be extracted
        :param file_retries: number of allowed file retry if download is cut short
        :param file_min_size: size file downloaded needs to exceed or else retry - in bytes
        :return:
        """
        if num_files > self.num_clusters:
            raise Exception("exceeded cluster size")

        if num_files == 0:
            num_files = self.num_clusters

        for i in range(self.num_clusters, self.num_clusters-num_files, -1):

            under_threshold = True
            retry = 0
            # click on cluster
            self.driver.find_element(By.XPATH, "/html/body/div[1]/div/nav/ul[1]/li[3]/a").click()
            # Click on cluster and extract
            self.driver.find_element(By.XPATH,
                                     f"/html/body/div[2]/div/div/div/form/table/tbody/tr[{i}]/td[1]/input").click()
            # click on extract
            self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/form/input[7]").click()
            # enter regex
            self.driver.find_element(By.XPATH, "//*[@id=\"regex\"]").send_keys(regex)

            while file_retries >= retry and under_threshold:
                under_threshold = False
                files = nf(self.extract_dir)

                self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/form/div[3]/button").click()
                download_wait(self.extract_dir, nfiles=files + 1)
                filename = get_publicwww_filename(self.extract_dir)

                if (file_retries != 0 and file_retries >= retry + 1
                        and not verify_file_size(os.path.join(self.extract_dir, filename), threshold=file_min_size)):
                    under_threshold = True
                    retry = retry + 1
                    remove_file(os.path.join(self.extract_dir, filename))

        self.num_clusters = self.num_clusters - 1

    def quit(self):
        self.driver.quit()


