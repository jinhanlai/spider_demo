# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy_study.fang.fang.items import NewHouseItem, ESFHouseItem


class HouseSpiderSpider(scrapy.Spider):
    name = 'house_spider'
    
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")
        provice = None
        for tr in trs:
            tds = tr.xpath(".//td")[1:]
            prov_text = tds[0].xpath(".//text()").get().strip()
            if prov_text:
                provice = prov_text
            if provice == "其它":
                continue
            city_ct = tds[1].xpath(".//a")
            for cc in city_ct:
                city = cc.xpath(".//text()").get()
                city_link = cc.xpath(".//@href").get()
                url = city_link.split(".fang")
                sche = url[0]
                try:
                    domain = url[1]
                except:
                    # 跳过台湾这个城市
                    break
                new_house_link = sche + ".newhouse.fang" + domain + "house/s/"
                old_house_link = sche + ".esf.fang" + domain
                if city == "北京":
                    new_house_link = "https://newhouse.fang.com/house/s/"
                    old_house_link = "https://esf.fang.com/"
                yield scrapy.Request(url=new_house_link, callback=self.parse_newhouse, meta={
                    "info": (provice, city)
                })
                yield scrapy.Request(url=old_house_link, callback=self.parse_oldhouse, meta={
                    "info": (provice, city)
                })

    def parse_newhouse(self, response):
        provice, city = response.meta.get("info")
        lis = response.xpath("//div[contains(@class,'nl_con')]/ul/li")
        for li in lis:
            try:
                name = li.xpath(".//div[@class='nlcd_name']/a/text()").get().strip()
            except:
                continue
            house_type = li.xpath(".//div[contains(@class,'house_type')]/a/text()").getall()
            house_type = list(map(lambda x: re.sub(r"\s", "", x), house_type))
            house_type = "/".join(list(filter(lambda x: x.endswith("居"), house_type)))  # 过滤掉所有不以ju结尾的数据
            price = "".join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
            price = re.sub(r"\s|广告", "", price)
            area = "".join(li.xpath(".//div[contains(@class,'house_type')]/text()").getall())
            area = re.sub(r'\s|－|/', "", area)
            address = li.xpath(".//div[@class='address']/a/@title").get()

            district = "".join(li.xpath(".//div[@class='address']/a//text()").getall())
            district = re.search(r".*\[(.+)\].*", district).group(1)

            sale = li.xpath(".//div[contains(@class,'fangyuan')]/span/text()").get()
            origin_url = response.urljoin(li.xpath(".//div[@class='nlcd_name']/a/@href").get())
            item = NewHouseItem(provice=provice, city=city, name=name, price=price, house_type=house_type, area=area
                                , address=address, district=district, sale=sale, origin_url=origin_url)
            yield item
        next_url = response.xpath("//div[@class='page']//a[@class='next']/@href").get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_newhouse,
                                 meta={"info": (provice, city)})

    def parse_oldhouse(self, response):
        provice, city = response.meta.get("info")
        shop_list = response.xpath("//div[contains(@class,'shop_list')]/dl[@class='clearfix']")
        for shop in shop_list:
            item = ESFHouseItem(provice=provice, city=city)
            try:
                name = shop.xpath(".//dd/h4[@class='clearfix']/a/span//text()").get().strip()  # 房子名字
            except:
                pass
            item["name"] = name
            try:
                price_type = "".join(shop.xpath(".//dd[@class='price_right']/span//text()").getall()).split("万")  # 房子总价
                price = price_type[0] + "万"
                unit = price_type[1]
            except:
                pass
            item["price"] = price
            item["unit"] = unit
            house = "".join(shop.xpath(".//dd/p[@class='tel_shop']//text()").getall()).split("|")  # 房屋类型(几室几厅)
            house = list(map(lambda x: x.strip(), house))
            for hs in house:
                if "厅" in hs:
                    item["house_type"] = hs
                elif "层" in hs:
                    item["floor"] = hs
                elif "向" in hs:
                    item["toward"] = hs
                elif "年" in hs:
                    item["year"] = hs
                elif "㎡" in hs:
                    item["area"] = hs
            address = shop.xpath(".//dd/p[@class='add_shop']/span/text()").get()  # 房子所在地址
            district = shop.xpath(".//dd/p[@class='add_shop']/a/@title").get()
            origin_url = response.urljoin(shop.xpath(".//dd/h4[@class='clearfix']/a/@href").get())  # 房子连接
            item["address"] = address
            item["district"] = district
            item["origin_url"] = origin_url
            yield item
        infor = response.xpath("//div[@class='page_al']/p/a")
        text = infor.xpath(".//text()").getall()
        url = infor.xpath(".//@href").getall()
        for index, nextinfo in enumerate(text):
            if nextinfo == "下一页":
                # print("="*50)
                # print(nextinfo,response.urljoin(url[index]))
                yield scrapy.Request(url=response.urljoin(response.urljoin(url[index])), callback=self.parse_oldhouse,
                                     meta={"info": (provice, city)})
