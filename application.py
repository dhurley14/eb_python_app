from flask import Flask
from bs4 import BeautifulSoup
import requests


# EB looks for an 'application' callable by default.
application = Flask(__name__)


@application.route('/beer/<beername>')
def display_info(beername):
    # get the beer info from beeradvocate
    print 'beername: {0}'.format(beername)
    ratingPage = find_beer_rating_page(beername)
    if('Not Found' in ratingPage):
        return 'Not Found'
    rating = get_rating_from_page(ratingPage)
    # show the username
    return 'beername: {0}, rating: {1}'.format(beername, rating)


@application.route('/')
def index():
    return 'Hello BeerBattle!'


def find_beer_rating_page(name):
    # search beer advocate for
    print 'findBeerRatingPage({0})'.format(name)
    r = requests.get('http://www.beeradvocate.com/search/?q={0}'.format(name))
    soup = BeautifulSoup(r.text, 'html.parser')
    # print soup.prettify()
    print len(soup.find_all('a'))
    for link in soup.find_all('a'):
        # print link.get('href')
        the_link = link.get('href')
        print 'outer_link: {0}'.format(the_link)
        if the_link is not None:
            if('/beer/profile' in the_link):
                print 'the_link: {0}'.format(the_link)
                return the_link
        # print 'Not Found :/'
    return 'Not Found'


def get_rating_from_page(pageLink):
    # parse rating page
    r = requests.get('http://www.beeradvocate.com{0}'.format(pageLink))
    soup = BeautifulSoup(r.text, 'html.parser')
    for span_tag in soup.find_all('span'):
        the_class = span_tag.get('class')
        if the_class is not None:
            if 'BAscore_big' in the_class[0] and 'ba-score' in the_class[1]:
                print 'found the rating: {0}'.format(span_tag.string)
                return span_tag.string
    return 'Couldn\'t find the rating, sorry :/'


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = False
    application.run()
