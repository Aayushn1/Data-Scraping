import requests
from bs4 import BeautifulSoup
import json

url = "https://www.flipkart.com/computers/pr?sid=6bo&q=digisol&otracker=categorytree&p%5B%5D=facets.serviceability%5B%5D%3Dtrue&p%5B%5D=facets.brand%255B%255D%3DDigisol"

response = requests.get(url)
html = BeautifulSoup(response.text,'html.parser')

products = html.find_all(attrs={"class":"_2cLu-l"})
print(len(products))

with open('flipkart.csv',"w",encoding="UTF-8") as file:
    for product in products:
        address = "https://www.flipkart.com" + product["href"]
        response1 = requests.get(address)
        html1 = BeautifulSoup(response1.text,'html.parser')
        #print(html1)
        all_reviews = html1.find(attrs={"class":"swINJg _3nrCtb"})

        if(all_reviews == None):
            continue

        print(product["title"]+"\n")
        file.write(product["title"]+" :\n")
        j = 0;
        for i in range(1,100):

            rev_address ="https://www.flipkart.com" + all_reviews.parent["href"] + "&page=%d" %(i)

            review_response = requests.get(rev_address)

            review_html = BeautifulSoup(review_response.text,'html.parser')

            review_text = review_html.find_all(attrs={"class":"qwjRop"})

            for review in review_text:
                rev_text = review.div.div
                file.write(str(j) + " " + rev_text.text+"\n")
                j = j+1

        file.write("\n--------------------------------------------------\n")
        #print(rev_address)