import random
proxies=['8.223.31.16:80',
         '135.148.171.194:18080',
         '195.201.126.184:80',
         '20.24.43.214:80',
         '47.88.31.196:8080',
         '8.219.97.248:80',
         '200.174.198.86:8888',
         '38.188.127.123:8080',
         '34.91.114.10:8080',
         '103.191.254.2:8085']

def RandomIPServer():
    n=random.randint(0,len(proxies)-1) 
    return proxies[n]


# code for finding free working servers
# import requests
# import random
# from bs4 import BeautifulSoup as bs
# import traceback
# def get_free_proxies():
#     url="https://free-proxy-list.net/"
#     soup=bs(requests.get(url).content,'html.parser')
#     proxies=[]
#     for row in soup.find("table","table table-striped table-bordered").find_all("tr")[1:]:
#         tds=row.find_all("td")
#         try:
#             ip=tds[0].text.strip()
#             port=tds[1].text.strip()
#             proxies.append(str(ip)+":"+str(port))
#         except IndexError:
#             continue
#     return proxies

# url="https://httpbin.org/ip"
# proxies=get_free_proxies()
# working_proxies=[]
# for i in range(0,len(proxies)):
#     print("Response Number : "+str(i+1))
#     proxy=proxies[i]
#     try:
#         response=requests.get(url,proxies={"http":proxy,"https":proxy})
#         print(proxy)
#         working_proxies.append(proxy)
#     except:
#         print("Not Available")
# print(len(working_proxies))
# print(working_proxies)
