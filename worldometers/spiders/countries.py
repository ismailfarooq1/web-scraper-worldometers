# -*- coding: utf-8 -*-
import scrapy
import logging


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']

    def start_requests(self):
        yield scrapy.Request(url='https://www.worldometers.info/world-population/population-by-country', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0'
        })

    def parse(self, response):
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # absolute_url = f"https://www.worldometers.info{link}"
            # absolute_url = response.urljoin(link)

            yield response.follow(url=link, callback=self.parse_country, meta={'country_name': name}, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0'
            })

    def parse_country(self, response):
        name = response.request.meta['country_name']
        rows = response.xpath(
            "(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            years = row.xpath('.//td[position() = 1]/text()').get()
            population = row.xpath(
                './/td[position() = 2]/strong/text() ').get()

            yield {
                'country_name': name,
                'years': years,
                'population': population,
                'User-Agent': response.request.headers['User-Agent']
            }
