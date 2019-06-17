import requests
import json

request = requests.get("https://maps.googleapis.com/maps/api/place/details/json?placeid=ChIJm4VQ9Va3vzsR6FEvW5boks0&key=AIzaSyBgLCJ3pj3lTZ6dcvGdx8CmUrvQYQsmC9U")

json = request.json()

reviews = json['result']['reviews']

review_text = []


with open("gmaps.csv","w",encoding="UTF-8") as file:
    for review in reviews:
        file.write("Rating: " + str(review['rating'])+ " Review: "+review['text'])
        file.write("\n")

print(review_text)



