from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote_plus
from . import models


BASE_CRAIGLIST_URL='https://chihuahua.craigslist.org/search/?query={}'
BASE_IMAGE_URL='https://images.craigslist.org/{}_300x300.jpg' #format for its images

# Create your views here.
def home(request):
    return render(request, template_name='base.html')


def new_search(request):
    search = request.POST.get('search') #es post con metodo get no get
    # print(quote_plus(search))
    models.Search.objects.create(search=search) #create obj to admin
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search)) #quote plus es formato
    # print(final_url)
    response = requests.get(final_url) #search the url
    data = response.text #print all html
    # print(data)
    soup = BeautifulSoup(data, features='html.parser') #bs para ir a obj individuales

    post_listings = soup.find_all('li', {'class': 'result-row'}) #each item

    final_postings = [] #empty list

    for post in post_listings: #for each item get title url price
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href') #post inst of postlist cuz for

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else: #if no price
            post_price = 'N/A'
#img idd 1:    89634876   ,3244876,43432
        if post.find(class_='result-image').get('data-ids'): #get image id primer, dopo :
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id) #link with individ id
            print(post_image_url)
        else:
            post_image_url ='https://craigslist.org/images/peace.jpg' #craiglist logo

        final_postings.append((post_title, post_url, post_price, post_image_url)) #list

    stuff_for_frontend = { #context
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, template_name='v_app/new_search.html', context=stuff_for_frontend)

