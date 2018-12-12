# 作者：larus
# 项目：给编辑们方便的扒游戏图

import requests
from bs4 import BeautifulSoup
import os
import tkinter

class GameSpider:
    def __init__(self):
        #创建主窗口
        self.root = tkinter.Tk()
        self.root.minsize=(600,400)
        self.frame = tkinter.Frame(self.root)
        self.frame.pack()
        #设置标题
        self.root.title("游戏详情页下载V1.0")
        #设置icon
        #tmp = open("tmp.ico","wb+")
        #tmp.write(base64.b64decode(img))
        #tmp.close()
        #self.root.iconbitmap("tmp.icon")
        #os.remove("tmp.ico")
        #创建一个输入框
        self.url_input = tkinter.Entry(self.frame,width=30)
        self.display_info = tkinter.Listbox(self.root,width=50)
        #创建一个查询按钮
        self.result_button = tkinter.Button(self.frame,command=self.get_full_info,text='查询')
        self.url_input.focus()
        self.display_info.insert(tkinter.END, "已经启动游戏爬虫，咔嚓咔嚓~~")
        self.display_info.insert(tkinter.END, "目前支持taptap、Steam两大平台！")
        self.display_info.insert(tkinter.END, "输入游戏链接，即可把游戏信息保存本地（文字+图片）")
        #print("已经启动游戏爬虫，咔嚓咔嚓~~")

    def gui_arrange(self):
        self.url_input.pack(side=tkinter.LEFT)
        self.display_info.pack()
        self.result_button.pack(side=tkinter.RIGHT)

# 解析游戏地址页面
    def get_game_url(self,url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9'}
        res = requests.get(url,headers=headers)
        soup = BeautifulSoup(res.text,'lxml')
        return soup
# 解析taptap游戏数据
    def get_taptap_info(self,soup):
        data = {}
        data['game_channel'] = 'taptap' #游戏渠道
        data['game_title'] = soup.select("h1")[0].text.strip() # 游戏名称
        data['game_other_title'] = soup.select('h2')[0].text # 游戏别名
        data['game_icon'] = soup.select(".header-icon-body img")[0].get('src')  #游戏icon地址
        data['game_developer'] =[developer.text.replace("\n","") for developer in soup.select("div.header-text-author")] #游戏开发者
        data['game_description'] = soup.select("#description")[0].text #游戏简介
        data['game_images'] = [img.get('src').split('?')[0] for img in soup.select('div.body-images-normal img')] #游戏图片
        print(data)
        return data
# 解析steam游戏数据
    def get_steam_info(self,soup):
        data = {}
        data['game_channel'] = 'steam' #游戏渠道
        data['game_title'] = soup.select(".apphub_AppName")[0].text.strip() # 游戏名称
        data['game_other_title'] = "" # 游戏别名
        data['game_icon'] = soup.select(".game_header_image_full")[0].get('src')  #游戏icon地址
        data['game_developer'] =[developer.text.replace("\n","") for developer in soup.select(".user_reviews div.dev_row")] #游戏开发者
        data['game_description'] = soup.select(".game_area_description")[0].text #游戏简介
        data['game_images'] = [img.get('src').replace('116x65','1920x1080') for img in soup.select('.highlight_strip_screenshot img')] #游戏图片
        print(data)
        return data
# 创建游戏文件夹
    def mkdir(self,path):

        folder = os.path.exists(path)

        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
            print
            "---  new folder...  ---"
        else:
            print
            "---  There is this folder!  ---"
# 下载icon图片
    def download_icon(self,data):
        file_path = "./{}-{}/".format(data['game_channel'],data['game_title'].replace(":","-"))
        self.mkdir(file_path)
        self.display_info.insert(tkinter.END, "正在下载icon图片")
        try:
            ir = requests.get(data['game_icon'])
            pic_type = '.jpg' if '.jpg' in data['game_icon'] else '.png'
            if ir.status_code == 200:
                image_name =data['game_title']+"-"+'icon'+ pic_type
                open(file_path+image_name,'wb').write(ir.content)
                self.display_info.insert(tkinter.END,"icon下载成功")
                #print('icon下载成功~')
        except:
            self.display_info.insert(tkinter.END, "icon图片不存在或下载失败，请重试~~")
            #print('icon图片不存在或下载失败，请重试~')

# 下载截图图片
    def download_pic(self,data):
        img_id = 1
        file_path = "./{}-{}/".format(data['game_channel'], data['game_title'].replace(":", "-"))
        self.display_info.insert(tkinter.END, "正在下载截图图片")
        self.mkdir(file_path)
        try:
            for image in data['game_images']:
                ir = requests.get(image)
                pic_type = '.jpg' if '.jpg' in image else '.png'
                if ir.status_code == 200:
                    image_name =data['game_title']+"-"+str(img_id)+ pic_type
                    open(file_path+image_name,'wb').write(ir.content)
                    self.display_info.insert(tkinter.END, "图片{}下载成功".format(img_id))
                    #print('图片下载成功~')
                    img_id += 1
                else:
                    pass
        except:
            self.display_info.insert(tkinter.END, "图片不存在或下载失败，请重试~")
            #print('图片不存在或下载失败，请重试~')

# 下载游戏简介
    def download_info(self,data):
        file_path = ".\/{}-{}\/".format(data['game_channel'], data['game_title'])
        self.mkdir(file_path)
        game_info_name = data['game_title']+'.txt'
        with open(file_path+game_info_name,'a',encoding='utf-8') as fw:
            self.display_info.insert(tkinter.END, "正在保存文字信息")
            fw.write( "-------游戏名称-------\r\n")
            fw.write(data['game_title']+"\r\n\r\n")
            fw.write("-------游戏别名-------\r\n")
            fw.write(data['game_other_title'] + "\r\n\r\n")
            fw.write("-------游戏厂商-------\r\n")
            for developer in data['game_developer']:
                fw.write(developer + "\r\n\r\n")
            fw.write("-------游戏平台地址-------\r\n")
            fw.write(data['game_channel'] + "\r\n\r\n")
            fw.write("-------游戏简介-------\r\n")
            fw.write(data['game_description'] + "\r\n\r\n")
            fw.write("-------游戏icon地址-------\r\n")
            fw.write(data['game_icon'] + "\r\n\r\n")
            fw.write("-------游戏图片地址-------\r\n")
            for image in data['game_images']:
                fw.write(image + "\r\n\r\n")
            fw.write("\n")
            self.display_info.insert(tkinter.END, "文字信息保存成功！")

## 下载游戏全部信息
    def get_full_info(self):
        url = self.url_input.get()
        self.url_input.delete(0,tkinter.END)
        self.display_info.delete(0,tkinter.END)
        game_info = self.get_game_url(url)
        if 'taptap' in url:
            game_data = self.get_taptap_info(game_info)
        elif 'steam' in url:
            game_data = self.get_steam_info(game_info)
        self.download_info(game_data)
        self.download_pic(game_data)
        self.download_icon(game_data)
        self.display_info.insert(tkinter.END, "下载完成了哦亲！")

def main():
    GS = GameSpider()
    GS.gui_arrange()
    tkinter.mainloop()
    pass

if __name__ == '__main__':
    main()









