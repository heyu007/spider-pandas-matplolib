# /user/bin/env python3
# -*- coding:utf-8 -*-

'''
spider class and deal some data
'''

__author__ = 'heyu <18781085152@153.com>'

import requests, re, csv, os


# 请求服务器数据
def grab(url, header):
    # 执行抓取操作
    try:
        # 发送请求
        response = requests.get(url=url, headers=header)
        # 转换字符集
        response.encoding = response.apparent_encoding
        # 返回数据
        return response.text
    except Exception as e:
        print('grab Error info:', e)
        exit()


# 处理返回数据
def deal_data(html):
    # 处理数据
    try:
        # 生成空列表
        goods_list = []
        # 匹配售价
        all_price = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
        # 商品名称
        all_title = re.findall(r'\"raw_title\"\:\".*?\"', html)
        # 商家名称
        all_nick = re.findall(r'\"nick\"\:\".*?\"', html)
        # 邮寄价格
        all_view_fee = re.findall(r'\"view_fee\"\:\".*?\"', html)
        # 店家地址
        all_item_loc = re.findall(r'\"item_loc\"\:\".*?\"', html)
        # 购买人数
        all_view_sales = re.findall(r'\"view_sales\"\:\".*?\"', html)
        # 迭代器组装数据
        for i in range(len(all_price)):
            price = eval(all_price[i].split(':')[1])
            title = eval(all_title[i].split(':')[1])
            nick = eval(all_nick[i].split(':')[1])
            view_fee = eval(all_view_fee[i].split(':')[1])
            item_loc = eval(all_item_loc[i].split(':')[1])
            view_sales = eval(all_view_sales[i].split(':')[1])
            goods_list.append([title, price, view_sales, view_fee, nick, item_loc])
        return goods_list
    except Exception as e:
        print('deal_data error info:', e)
        exit()


# 写入文件
def write_file(goods_data, file_name):
    # 创建新文件名
    file_name = str(file_name) + '.csv'
    try:
        # a 不覆盖数据，往后依次添加数据
        # newline 写入csv数据的时候不添加空白行
        with open(file_name, 'a', newline='') as csvFile:
            # csv方式写入文件数据
            f = csv.writer(csvFile)
            # 判断文件是否存在，如不存在添加抬头，否则不用添加
            if os.path.getsize(file_name) == 0:
                # 文件头部
                f.writerow(['商品名称', '价格', '购买人数', '邮递价格', '商家', '商家地址'])
            # 批量写入数据内容
            for i in range(len(goods_data)):
                goods = goods_data[i]
                f.writerow(goods)
    except Exception as e:
        print('write_file error info:', e)
        exit()


# 入口
def main(page, search_key, file_name='淘宝商品'):
    # 处理文件名，保证是合法文件名
    file_name = re.sub('[’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "", file_name)
    # 去除不可见字符
    file_name = re.sub(
        '[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+',
        '', file_name)
    # 判断是否有抓取分页的最大数量
    if not page:
        print('抓取这点儿数据，有什么用，来个99的套餐，QVQ')
        exit()
    # 单独的数字或字符串
    elif isinstance(page, (int, str, float)):
        range_list = range(int(page))
    # 列表
    elif isinstance(page, list):
        if len(page) > 1:
            page = sorted(page)
            range_list = range(int(page[0]), int(page[1]))
    else:
        range_list = range(1)

    # 判断是否有搜索关键字（没有关键字的话，只会搜索出一页数据）
    if not search_key:
        print('\n给个搜索关键字怎么了？打字的力气都没有了？还是不会？\n')
        print('\n我只教一遍啊，key1 + key2,中形式的字符串搜索关键字，表示多个条件共同作用\n')
        print('\n还有，我也不知道你抓取的什么数据，哇哦！\n')
        page = 1

    try:
        # url请求地址
        url = 'https://s.taobao.com/search?q=' + str(search_key) + '&sort=sale-desc'
        # 设置header信息
        header = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'thw=cn; t=2321734b0a42dda4f103c5c3d9583c19; cna=7J+9FWL2Ox4CAX1HkuxYcZxr; tracknick=%5Cu4F55%5Cu79B91992; _cc_=WqG3DMC9EA%3D%3D; tg=0; enc=sYqdp0Sm%2B1gl%2FojDSZmsRxGka%2FjwGXlPLvjCHTj07dBKADtEgYwruP0auw%2B8IduW%2BwI3capQNa5sc76XUkjV%2FQ%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; _m_h5_tk=e7adc7830facca2641e023288983b249_1568876160772; _m_h5_tk_enc=033b8c488613e62e9fd498646f09464d; v=0; cookie2=1f912dcf167479c4dcc09d4657b492e9; _tb_token_=5bee9387f8733; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=E0CB054CF98CC937B3EB202FA7F8A6D5; l=cBEfq1bgqUC12RXXBOfNquI8ag79UpdXhsPzw4_ixIB19WBZYpiICHwBLTwWT3QQE95b3exy3ycOQR3B-j438xgKqelyRs5mp; isg=BNTUlFwIdQTy7eGMkwpqGhfYpRKGhfj7lfxrIm66tNplWXqjlDyKpu-fWRHkoTBv',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        }
        # 抓取分页数据
        for i in range_list:
            # 组装分页+url地址
            if page == 0:
                member = str('')
            else:
                member = '&s=' + str(44 * i)
            # 抓取
            html = grab(url + member, header)
            # 处理
            deal_res = deal_data(html)
            # 写入
            write_file(deal_res, file_name)
            print('已下载' + str(i + 1) + '页数据')
        print('bingo 搞定了！')
    except Exception as e:
        print('error info:', e)
        exit()


if __name__ == '__main__':
    main([0, 1], '女鞋', '女鞋')
