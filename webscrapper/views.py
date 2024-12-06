from django.shortcuts import render
from webscrapper.forms import BookSearchForm
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests

def scrape_reviews(book_name):
    # Get URL of the Book
    book_name = book_name.replace(" ", "_")
    search_url = f"https://www.goodreads.com/search?q={book_name}"
    
    try:
        url_client = urlopen(search_url)
        page_variable_goodreads = url_client.read()
        goodreads_html = bs(page_variable_goodreads, 'html.parser')
        
        # Search for specific Div of books
        book_box = goodreads_html.find_all("tr", {"itemscope": True, "itemtype": "http://schema.org/Book"})
        if not book_box:
            return {"error": "No books found."}
        
        # To get the link of the first book after search
        link1 = "https://www.goodreads.com" + book_box[0].td.a['href']
        
        # Get the HTML page of the first book
        req_link = requests.get(link1)
        book_html = bs(req_link.text, 'html.parser')
        
        # Extract reviewer names and reviews
        review_box_profile = book_html.find_all("div", {"class": "ReviewerProfile__name"})
        extracted_names = [i.text.strip() for i in review_box_profile]
        
        comment_box = book_html.find_all("div", {"class": "TruncatedContent"})
        extracted_reviews = [comment.text.strip() for comment in comment_box[3:]]
        
        # Combine names and reviews
        names_and_reviews = dict(zip(extracted_names, extracted_reviews))
        return {"reviews": names_and_reviews}
    except Exception as e:
        return {"error": str(e)}

def home(request):
    reviews = None
    error = None
    
    if request.method == 'POST':
        form = BookSearchForm(request.POST)
        if form.is_valid():
            book_name = form.cleaned_data['book_name']
            result = scrape_reviews(book_name)
            if "error" in result:
                error = result["error"]
            else:
                reviews = result["reviews"]
    else:
        form = BookSearchForm()
    
    return render(request, 'home.html', {'form': form, 'reviews': reviews, 'error': error})
