# spider_demo
网络爬虫学习项目

1.创建scrpy项目：在终端或者命令行输入
	scrapy startproject module  创建名为module的项目
	scrapy genspider  [爬虫名字] [域名]  #创建普通的spider
	scrapy genspider -t crawl [爬虫名字] [域名]  #使用CrawlSpider爬虫
2.修改setting文件：
	ROBOTSTXT_OBEY = true改为false
	DEFAULT_REQUEST_HEADERS里面添加User-Agent
3.启动scrapy
    创建一个start.py文件 ，在里面写入 cmdline.execute("scrapy crawl jianshu_spider".split()) #jianshu_spider为爬虫名字
    或者在命令行中输入scrapy crawl jianshu_spider
scrapy shell 网页  里面可以使用xpath语法这些，判断验证数据是否正确
	

redis分布式爬虫:
在项目所在目录下进入cmd，输入pip freeze > requirements.txt 导出项目所用到的所有的包

把项目改成分布式爬虫步骤：
    1.把spiders下的爬虫那个类继承为（from scrapy_redis.spiders import RedisSpider）
    2.删除start_urls 增加一个redis_key="XXX"（意思是去redis里面寻找key） eg redis_key="fang:start_urls"
    3.在配置文件中修改：
        SCHEDULER="scrapy_redis.scheduler.Scheduler"
        DUPEFILTER_CLASS="scrapy_redis.duperfilter.REPDuperFilter"
        ITEM_PIPELINES={
                    'scrapy_redis.pipelines.RedisPipeline':300
                }
        SCHEDULER_PERSIST=True
        REDIS_HOST='127.0.0.1'
        REDIS_PORT=6379
    4.然后打包发到ubuntu中(要删除掉requirements.txt文件)
            unzip fang.zip 解压文件
    5.运行爬虫
        在爬虫服务器上进入到文件所在路径，输入命令scrapy runspider 【爬虫名字】
        在redis服务器上，推入一个开始的url链接
                redis-cli > lpush [redis_key] start_urls
