



urls = list()

N = 0
default_url = url
for url in urls:
    response = requests.get(f"{url}/page{N}.html")

    if response.url == default_url:
        if parse('pageN.html') == parse('first_page.html'):
            skip_url() 

        else:
            load_to_db(parse('first_page.html'))

    else:
        load_to_db(parse('first_page.html'))
        duplicate('first_page.html', 'pageN.html')

    N += 1
