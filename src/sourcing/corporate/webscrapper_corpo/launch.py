import scrapy
from scrapy.crawler import CrawlerProcess
from get_all.get_all.spiders.getall import GetAllSpider
from optparse import OptionParser


if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option(
        "-c", "--company_url", dest="company_url", help="write report to FILE"
    )
    parser.add_option(
        "-o", "--output_path", dest="output_path", help="write report to FILE"
    )

    (options, args) = parser.parse_args()

    process = CrawlerProcess(
        {"USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"}
    )
    company_url = options.company_url
    output_path = options.output_path
    domain = company_url.replace("http://", "").replace("http://", "").split("/")[0]

    process.crawl(
        GetAllSpider,
        start_urls=[company_url],
        # allowed_domains=["*."+domain],
        output_path=output_path,
    )
    process.start()  # the script will block here until the crawling is finished
