import json
import requests
from bs4 import BeautifulSoup

url = "https://www.amazon.in/s?k=digisol&s=review-rank&lo=list&qid=1560316256&ref=sr_pg_1"

response = requests.get(url)

html_1 = BeautifulSoup(response.text ,'html.parser')

'''print(html_1)'''

products = html_1.find_all(attrs={"class" : "a-link-normal a-text-normal","target":"_blank"})
#print(len(products))

with open("amazon.csv","w",encoding = "UTF-8") as file:
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
            response = requests.get(product_review_url)
            html = BeautifulSoup(response.text, 'html.parser')
            reviews = html.find_all(attrs={"data-hook": "review-body"})
            if(len(reviews)==0):
                break
            for review in reviews:
                file.write(str(j)+": ")
                file.write(review.text)
                file.write("\n")
                j = j+1
                print(i)
            #print(review.text+"\n")
