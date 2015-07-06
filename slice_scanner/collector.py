import logging
from crontab import CronTab
import time
from vendors import dominos
from selenium import webdriver

class Collector(object):
    vendors = [
        dominos.Dominos()
    ]

    def __init__(self, frequency, queue):
        self.cron = CronTab(frequency)
        self.queue = queue

    def _start_webdriver(self):
        return webdriver.Chrome('C:\\chromeDRIVER.exe')#, service_args=['--ignore-ssl-errors=true'])
        # return self.web_driver = webdriver.PhantomJS('C:\\phantomjs.exe', service_args=['--ignore-ssl-errors=true'])
        # return self.web_driver = webdriver.Firefox()

    def _collect(self):
        web_driver = self._start_webdriver()
        for session in self.vendors:
            session.set_driver(web_driver)
            self.queue.put(session.parse())
        web_driver.quit()

    def vendor_info(self):
        vendor_info = {}
        for vendor in self.vendors:
            vendor_dict = vendor.to_dict()
            vendor_info[vendor_dict["id"]] = vendor_dict
        return vendor_info

    def run(self):
        logging.info("Collector Running")
        while True:
            self._collect()
            time.sleep(self.cron.next())