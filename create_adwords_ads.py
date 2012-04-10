# -*- coding:utf-8 -*-
#filename:create_adwords_ads.py
#time:20120410
"""此脚本用于创建Google adwords广告。原始数据是
[账户,关键词,目录,子目录]的txt文件，生成一份编辑好csv文件，
导入AdWords编辑器中。"""

import csv
import os
import time

def get_data():
    file_path=raw_input(u'请输入待处理文件路径：')
    f=open(file_path,'rb')
    data=f.read().split('\r\n')
    f.close()
    data=[item.split('\t') for item in data]
    return data


def create_ads(data):
    #表头
    header=['Campaign',
            'Ad Group',
            'Max CPC',
            'Display Network Max CPC',
            'Placement Max CPC',
            'Keyword',
            'Keyword Type',
            'Headline',
            'Description Line 1',
            'Description Line 2',
            'Display URL',
            'Destination URL',
            ]
    max_cpc=1.21
    display_network_max_cpc=0.08
    placement_max_cpc=0

    f=open(os.path.join(os.getcwd(),'\\ads_'+time.strftime('%M%S')+'.csv'),'wb')
    writer=csv.writer(f)
    writer.writerow(header)    

    for item in data:
        #创建系列名
        if item[3]!='No category':
            campaign='QP-%s(%s)'%(item[2],item[3])
        else:
            campaign='QP-%s'%(item[2])

        #创建广告组名
        ad_group=item[1].title()

        #创建关键词，即item[1]
        keyword=item[1]

        #创建匹配方式
        if item[1].find(' ')==-1:
            keyword_type='exact'
        else:
            keyword_type='broad'

        #创建显示url
        display_url='Made-in-China.com'

        #创建目标url
        url_prefix="http://www.made-in-china.com/products-search/hot-china-products/"
        new_item=item[1].replace(' ','_')
        destination_url=url_prefix+new_item+".html"

        #三条广告创意模板
        creation=[
            ["{KeyWord:for_keyword}",
             "China {KeyWord:for_keyword} Suppliers",
             "High Quality, Competitive Price.",
             ],
            ["China {KeyWord:for_keyword}",
             "Good Price On {KeyWord:for_keyword}",
             "Trusted, Audited China Suppliers.",
             ],
            ["China {Keyword:for_keyword}",
             "Find Audited China Manufacturers",
             "Of {Keyword:for_keyword}. Order Now!",
             ],
            ]

        #如果关键字（item[1]）字符数小于20，就嵌入广告模板中
        if len(item[1])<20:
            creation=map(lambda i:map(lambda j:j.replace('for_keyword',item[1]).title(),i),creation)

        #写入出价
        writer.writerow([campaign,ad_group,max_cpc,display_network_max_cpc,placement_max_cpc])

        #写入广告创意    
        for i in creation:
            try:
                writer.writerow([campaign,ad_group,'','','','','',
                                 i[0], #广告语标题
                                 i[1], #广告描述语1
                                 i[2], #广告描述语2
                                 display_url,
                                 destination_url
                                 ])
            except Exception, e:
                pass

        #写入关键词
        writer.writerow([campaign,ad_group,'','','',keyword,keyword_type])

    f.close()


if __name__=='__main__':
    data=get_data()
    create_ads(data)
    print 'ok!'
    
