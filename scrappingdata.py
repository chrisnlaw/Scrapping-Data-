import urllib
from urllib2 import urlopen
from bs4 import BeautifulSoup
import os
from string import ascii_lowercase

def make_soup(url):
    thepage = urlopen(url)
    soupdata = BeautifulSoup(thepage,"html.parser")
    return soupdata
filename = "restaurant_data_kaggles.csv"
f = open(filename,"w")
soup = make_soup("https://www.tripadvisor.fr/Restaurants-g187265-Lyon_Rhone_Auvergne_Rhone_Alpes.html")
container = (soup.findAll("div", {"id": "EATERY_SEARCH_RESULTS"}))

headers = "restaurant_name ,review_number , food_type , ranking , overallRating  , wifi , livraison , average_price , lat , lng , district \n \n"
f.write(headers)

for data in container:

    titre = soup.findAll("div", {"class": "title"})
    for restaurant in titre:
        for link in restaurant.findAll('a'):
            restaurant_link_html = make_soup("https://www.tripadvisor.fr" + link.get('href'))

            restaurant_nombre_avis = restaurant_link_html.findAll("a", {"class": "more"})
            review_number = restaurant_nombre_avis[0].text
            print review_number

            restaurant_type = restaurant_link_html.findAll("span", {"class": "header_links rating_and_popularity"})
            food_type = restaurant_type[0].text
            print food_type

            restaurant_classement = restaurant_link_html.findAll("span", {"class": "header_popularity popIndexValidation"})
            ranking = restaurant_classement[0].text
            print ranking

            restaurant_note = restaurant_link_html.findAll("span", {"class": "overallRating"})
            overallRating = restaurant_note[0].text
            print overallRating

            restaurant_arrondissemnt = restaurant_link_html.findAll("span", {"class": "locality"})
            restaurant_locality = restaurant_arrondissemnt[0].text
            print restaurant_locality

            restaurant_nom = restaurant_link_html.findAll("h1", {"id": "HEADING"})
            restaurant_name = restaurant_nom[0].text
            print restaurant_name

            restaurant_location_lat = restaurant_link_html.find("div", attrs={"class":"ui_columns is-gapless is-mobile poiEntry shownOnMap"})["data-lat"]
            restaurant_location_long = restaurant_link_html.find("div", attrs={"class":"ui_columns is-gapless is-mobile poiEntry shownOnMap"})["data-lng"]
            print restaurant_location_lat , restaurant_location_long

            restaurant_container = (restaurant_link_html.findAll("div", {"id": "RESTAURANT_DETAILS"}))
            donnee = restaurant_container[0]
            contenu = donnee.findAll("div", {"class": "content"})
            if contenu[0].span and 7 < len(contenu[0].span.text) < 13:
                average_price = contenu[0].span.text
                print "prix_moyen  ", average_price
            else:
                average_price = "no informations"
            if contenu[3].text.find("Wi-Fi gratuit") is -1:
                wifi = "no"
            else:
                wifi = "yes"
            if contenu[3].text.find("emporter") is -1:
                livraison = "no"
            else:
                livraison = "yes"
            print wifi, livraison

            f.write(restaurant_name.replace(","," ").encode('utf-8') + "," + review_number.encode('utf-8') + "," + food_type.replace(","," ").encode('utf-8') + "," + ranking.encode('utf-8') + "," + overallRating.replace(",",".").encode('utf-8') + "," + wifi.encode('utf-8') + "," + livraison.encode('utf-8') + "," + average_price.replace("\n","").encode('utf-8') +","+ restaurant_location_lat.encode('utf-8') + "," +restaurant_location_long.encode('utf-8') + "," + restaurant_locality.replace(","," ").encode('utf-8') + "\n" )

link = soup.find(attrs={"class":"nav next rndBtn ui_button primary taLnk"})
while link :
    soup = make_soup("https://www.tripadvisor.fr/" + link.get('href'))
    container = (soup.findAll("div", {"id": "EATERY_SEARCH_RESULTS"}))

    for data in container:

        titre = soup.findAll("div", {"class": "title"})
        for restaurant in titre:
            for link in restaurant.findAll('a'):
                restaurant_link_html = make_soup("https://www.tripadvisor.fr" + link.get('href'))

                restaurant_nombre_avis = restaurant_link_html.findAll("a", {"class": "more"})
                if restaurant_nombre_avis:
                    review_number = restaurant_nombre_avis[0].text
                else :
                    review_number = "no information"

                restaurant_type = restaurant_link_html.findAll("span", {"class": "header_links rating_and_popularity"})
                if restaurant_type :
                    food_type = restaurant_type[0].text
                else :
                    food_type = "no information"

                restaurant_classement = restaurant_link_html.findAll("span", {"class": "header_popularity popIndexValidation"})
                if restaurant_classement:
                    ranking = restaurant_classement[0].text
                else:
                    ranking = "no_information"

                restaurant_note = restaurant_link_html.findAll("span", {"class": "overallRating"})
                if restaurant_note:
                    overallRating = restaurant_note[0].text
                else :
                    overallRating = "no information"

                restaurant_arrondissemnt = restaurant_link_html.findAll("span", {"class": "locality"})
                if restaurant_arrondissemnt:
                    restaurant_locality = restaurant_arrondissemnt[0].text
                else :
                    restaurant_locality = "no information"

                restaurant_nom = restaurant_link_html.findAll("h1", {"id": "HEADING"})
                restaurant_name = restaurant_nom[0].text

                rest_cond = restaurant_link_html.find("div", {"class": "ui_columns is-gapless is-mobile poiEntry shownOnMap"})
                if rest_cond:
                    restaurant_location_lat = restaurant_link_html.find("div", attrs={
                    "class": "ui_columns is-gapless is-mobile poiEntry shownOnMap"})["data-lat"]
                    restaurant_location_long = restaurant_link_html.find("div", attrs={
                    "class": "ui_columns is-gapless is-mobile poiEntry shownOnMap"})["data-lng"]
                else:
                    restaurant_location_lat = "no information"
                    restaurant_location_long = "no information"



                restaurant_container = (restaurant_link_html.findAll("div", {"id": "RESTAURANT_DETAILS"}))
                donnee = restaurant_container[0]
                contenu = donnee.findAll("div", {"class": "content"})
                if len(contenu)<4:
                    average_price = "no information"
                    wifi = "no"
                    livraison = "no"
                else:

                    if contenu[0].span and 7 < len(contenu[0].span.text) < 13:
                        average_price = contenu[0].span.text
                    else:
                        average_price = "no information"
                    if contenu[3].text.find("Wi-Fi gratuit") is -1:
                        wifi = "no"
                    else:
                        wifi = "yes"
                    if contenu[3].text.find("emporter") is -1:
                        livraison = "no"
                    else:
                        livraison = "yes"

                f.write(restaurant_name.replace(","," ").encode('utf-8') + "," + review_number.encode('utf-8') + "," + food_type.replace(","," ").encode('utf-8') + "," + ranking.encode('utf-8') + "," + overallRating.replace(",",".").encode('utf-8') + "," + wifi.encode('utf-8') + "," + livraison.encode('utf-8') + "," + average_price.replace("\n","").encode('utf-8') + "," + restaurant_location_lat.encode('utf-8') + "," + restaurant_location_long.encode('utf-8') + "," + restaurant_locality.replace(","," ").encode('utf-8') + "\n" )

        link = soup.find(attrs={"class": "nav next rndBtn ui_button primary taLnk"})

f.close()





