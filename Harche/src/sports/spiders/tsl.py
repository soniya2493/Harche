from scrapy.spiders import Spider
from scrapy.selector import Selector
import datetime
import hashlib
from scrapy.http.request import Request
from scrapy.contrib.linkextractors import LinkExtractor
from sports.items import Website

class TslSpider(Spider):
	name = "tsl"
	start_urls = ['http://www.tennisleaguestats.com/',]
	
	allowed_domains = ['tennisleaguestats.com']
	
	def parse(self, response):
		item = Website()
		baseurl = response.xpath('//base/@href').extract()[0]
		for sel in response.selector.xpath("//a[contains(text(),'2015')]/@href").extract():
			linkurl = (baseurl + sel)
			print linkurl
			yield Request(linkurl,callback=self.parse_level1_contents)
		
	def parse_level1_contents(self, response):
		baseurl = response.xpath('//base/@href').extract()[0]
		le = LinkExtractor()
		for link in le.extract_links(response):
			if self.allowed_domains[0] in link.url:
				yield Request(link.url, callback=self.parse_level2_contents)

	def parse_level2_contents(self, response):
		baseurl = response.xpath('//base/@href').extract()[0]
		le = LinkExtractor()
		for link in le.extract_links(response):
			if self.allowed_domains[0] in link.url:
				yield Request(link.url, callback=self.parse_level3_contents)

	def parse_level3_contents(self, response):
		baseurl = response.xpath('//base/@href').extract()[0]
		le = LinkExtractor()
		for link in le.extract_links(response):
			if self.allowed_domains[0] in link.url:
				yield Request(link.url, callback=self.final_contents)
			
	def final_contents(self, response):
		sites = Selector(response).xpath('//div[@id="yearsRow2Column2"]')
		items=[]
		
		def find_between( s, first, last ):
				try:
					start = s.index( first ) + len( first )
					end = s.index( last, start )
					return s[start:end]
				except ValueError:
					return ""
	
					
		for site in sites:
			item = Website()
			item['player'] = site.xpath('//td[1][@class="tdatlevelleft" or "tdatlevelgleft"]/a/text()').extract()
			url =str(response.url)
			item['age_div'] = site.xpath('//td[1][contains(@class,"tdatlevel")]/following-sibling::td[1][contains(@class,"tdatlevel")]/text()').extract()
			item['tls_rating'] = site.xpath('//td[2][contains(@class,"tdatlevel")]/following-sibling::td[2][contains(@class,"tdatlevel")]/text()').extract()
			item['tls_ntrp_level'] = site.xpath('//td[4][@class="tdatlevel" or "tdatlevelg"]/text()').extract() 
			item['ntrp_eff_level'] = site.xpath('//td[5][@class="tdatlevel" or "tdatlevelg"]/text()').extract() 
			item['ntrp_eff_type'] = site.xpath('//td[6][@class="tdatlevel" or "tdatlevelg"]/text()').extract() 
			item['ntrp_eff_year'] = site.xpath('//td[7][@class="tdatlevel" or "tdatlevelg"]/text()').extract() 
			item['ntrp_end_level'] = site.xpath('//td[8][@class="tdatlevel" or "tdatlevelg"]/text()').extract() 
			item['ntrp_end_type'] = site.xpath('//td[9][@class="tdatlevel" or "tdatlevelg"]/text()').extract() 
			item['city_state'] = site.xpath('//td[10][@class="tdatlevelleft" or "tdatlevelleftg"]/text()').extract() 
			item['run_date']=datetime.datetime.now()			
			sect = str(site.xpath('//tr[5]/th[@class="thsmall"]/text()').extract())			
			facil = str(site.xpath('//tr[7]/th[@class="thsmall"]/text()').extract())
			sect_temp=sect.replace("- ","")
			sect_temp=sect_temp.replace("&nbsp","")
			sect_temp=sect_temp.replace("']","")
			s=sect_temp+"+"
			secti=find_between( s, "Section ", " District " )
			area=find_between(s, "Area ","+")		
			item['section']=secti
			item['area']=area			
			facil_temp=facil.replace("- ","")
			facil_temp=facil_temp.replace("&nbsp","")
			facil_temp=facil_temp.replace("[u'","")
			f="+"+facil_temp			
			if "Men" in url:
				sex="M"
				facility=find_between( f,"+", "Men")			
			else:
				sex="W"
				facility=find_between( f,"+", "Women")
			item['facility']=facility
			item['sex']=sex
		
			item['url']=url
	 
			#item['player_hash']=player_hash
			items.append(item)
		
		return items
