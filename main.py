import logging
import logging.handlers
import os
import scrapy
import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)


try:
    EMAIL_SECRET = os.environ["EMAIL_SECRET"]
except KeyError:
    EMAIL_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise

    if __name__ == "__main__":
    logger.info(f"Token value: {EMAIL_SECRET}")

class MySpider(scrapy.Spider):
    name = "Kashmir University Result"
    start_urls = ["https://egov.uok.edu.in/Results/results.aspx?rtype=3&rs=2"]
    custom_settings = {"DOWNLOAD_DELAY": 2, "CONCURRENT_REQUESTS_PER_DOMAIN": 1}

        def parse(self, response):
        try:
            if '8th Semester held in' in response.text:
                subject = "Result found for 8th Semester"
                body = "Result found for 8th Semester. Check the link: https://egov.uok.edu.in/Results/results.aspx?rtype=3&rs=2"
                message = f"Subject: {subject}\n\n{body}"
                logger.info(message)
                self.send_email(message)
                raise CloseSpider("Result found for 8th Semester")
            else:
              # time every 8 hours
                time.sleep(8*60*60)
                yield scrapy.Request(response.url, self.parse)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(8*60*60)
            yield scrapy.Request(response.url, self.parse)

    def send_email(self, message):
        try:
            import smtplib
            from_email = "hello@sahillangoo.com"
            to_email = "sahilahmed3066@gmail.com"
            password = "{password}"
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, message)
            server.quit()
            print('Email sent!')
        except Exception as e:
            print(f"Error sending email: {e}")

process = CrawlerProcess(get_project_settings())
process.crawl(MySpider)
process.start()
