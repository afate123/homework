import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re
import xlwt

findISBN = re.compile(r'ISBN:(.*?)<a')#记录书籍的ISBN
findName = re.compile(r'<h3 class="my-0 mb-2">(.*?)</h3>',re.S)#记录书籍的名字
findAuthor = re.compile(r'<a href=".*">(.*?)</a>')#记录书籍的作者名字
findImgLink= re.compile(r'<img.*src="(.*?)".*>')#记录书籍封面的链接

def saveData(datalist,savepath):#保存函数
     print("save....")
     book = xlwt.Workbook(encoding="utf-8",style_compression=0)
     sheet = book.add_sheet('BX-Books',cell_overwrite_ok=True)
     col = ('ISBN','Book-Title','Book-Author','Image-URL')#给出列的标签名
     for i in range(0,4):
         sheet.write(0,i,col[i])#先输出标签
     for i in range(0,10):#输出数据，此处的数字为需要爬取的书籍数目
         print("第%d条"%(i+1))
         data =datalist[i]
         for j in range(0,4):
             sheet.write(i+1,j,data[j])#写入数据
     book.save(savepath)
     
     
     
def getData(baseurl):
    datalist=[]
    for i in range(100000,100010):#书籍的url是从100000开始的
        url = baseurl + str(i)
        html = askURL(url)
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="col-sm-12 col-lg-9"):
            data=[]
            item=str(item)
            ISBN =re.findall(findISBN,item)[0]#获取ISBN
            data.append(ISBN)#写入ISBN
            Author=re.findall(findAuthor,item)[0]#获取作者名
            data.append(Author)#写入作者名
            Name = re.findall(findName,item)[0].replace('\r','')#获取书籍名
            data.append(Name.replace('\n',''))#写入书籍名
            ImgLink =re.findall(findImgLink, item)[0]#获取书籍封面链接
            data.append(ImgLink)#写入书籍封面链接
            datalist.append(data)
            print(datalist)
            
    return datalist



def askURL(url):
    head={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        }#伪装浏览器
    request =urllib.request.Request(url,headers=head)
    html =""
    try:
        response=urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:#异常处理
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html
baseurl = "https://www.bookcrossing.com/journal/"
datalist = getData(baseurl)
savepath = "BX-Books.xls"
saveData(datalist,savepath)
    