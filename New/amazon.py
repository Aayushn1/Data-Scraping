import json
import requests
from bs4 import BeautifulSoup
import random

url = "https://www.amazon.in/s?k=digisol&s=review-rank&qid=1560834076&ref=sr_st_review-rank"

response = requests.get(url)

html_1 = BeautifulSoup(response.text ,'html.parser')

'''print(html_1)'''

print(html_1)

products = html_1.find_all(attrs={"class" : "a-link-normal a-text-normal","target":"_blank"})
print(len(products))

proxies_list = ["128.199.109.241:8080", "113.53.230.195:3128", "125.141.200.53:80", "125.141.200.14:80",
                "128.199.200.112:138", "149.56.123.99:3128", "128.199.200.112:80", "125.141.200.39:80",
                "134.213.29.202:4444"]

proxies = {'https': random.choice(proxies_list)}


with open("amazon1.csv","w",encoding = "UTF-8") as file:
    for product in products:
        splitted_url = product["href"].split('/')
        #print(splitted_url)
        #print(splitted_url)
        # product_review_url = "www.amazon.in"+splitted_url[1]+"product-reviews"+splitted_url[3]+"ref=cm_cr_arp_d_paging_btm_next_%d?ie=UTF8&reviewerType=all_reviews&pageNumber=%d" %(i,i)
        j=1;
        file.write(splitted_url[1] + ":")
        file.write("\n")

        for i in range(1,100):
            # print(i)
            #url = "https://www.amazon.in/Digisol-DG-HR3400-300Mbps-Wireless-Broadband/product-reviews/B00IL8DR6W/ref=cm_cr_getr_d_paging_btm_next_%d?ie=UTF8&reviewerType=all_reviews&pageNumber=%d" % (i,i)
            product_review_url = "https://www.amazon.in/" + splitted_url[1] + "/product-reviews/" + splitted_url[3] + "/ref=cm_cr_getr_d_paging_btm_next_%d?ie=UTF8&reviewerType=all_reviews&pageNumber=%d" % (i, i)
            response = requests.get(url = product_review_url)
            html = BeautifulSoup(response.text, 'html.parser')
            reviews = html.find_all(attrs={"data-hook": "review-body"})
            reviews_dates = html.find_all(attrs={"data-hook":"review-date"})
            review_profile_name = html.find_all(attrs={"class":"a-profile-name"})
            pro = splitted_url[1];
            if(len(reviews)==0):
                break
            for i in range(0,len(reviews)-1):
                review = str(review_profile_name[i].text) + "," + str(reviews_dates[i].text).replace(",","") + "," + "Amazon"+","+ str(reviews[i].text).replace(","," ").replace("\n","") + "," + str(pro)+ ","+ "No" + "," + "No\n"
                file.write(review)
            print(splitted_url[1])
        file.write("\n--------------------------------------------------\n")

            #print(review.text+"\n")
