import requests, os

categories= ['homes-summer-residences', 'flats', 'farms-estates']
places = ['riga/all', 'jurmala', 'riga-region/all', 'aizkraukle-and-reg',
         'aluksne-and-reg', 'balvi-and-reg', 'bauska-and-reg', 'cesis-and-reg', 'daugavpils-and-reg/all',
         'dobele-and-reg', 'gulbene-and-reg', 'jekabpils-and-reg', 'jelgava-and-reg/all', 'kraslava-and-reg',
         'kuldiga-and-reg', 'liepaja-and-reg/all', 'limbadzi-and-reg', 'ludza-and-reg',
         'madona-and-reg', 'ogre-and-reg', 'preili-and-reg', 'rezekne-and-reg', 
         'saldus-and-reg', 'talsi-and-reg', 'tukums-and-reg', 'valka-and-reg',
         'valmiera-and-reg', 'ventspils-and-reg/all']


if os.path.exists('tmp') == True:
    for file in os.listdir('tmp'):
        os.remove(f'tmp/{file}')
    os.rmdir('tmp')
os.mkdir('tmp')

counter = 0
for category in categories:
    for place in places:
        try:
            for i in range(1, 100):
                url = f"https://www.ss.lv/lv/real-estate/{category}/{place}/page{i}.html"
                response = requests.get(url)
                print(response.url)
                if response.url == f"https://www.ss.lv/lv/real-estate/{category}/{place}/":
                    # print(f"skip duplicate {url}")
                    break
                else:
                    
                    file = response.text
                    with open(f"./tmp/page{counter}.html", "w", encoding='utf-8') as f:
                        f.write(file)
                    
                    if counter % 5 == 0 and counter != 0:
                        print(f"{counter} pages loaded")
                    counter += 1
        except Exception as e:
            print(f"smth failed.{type(e)}")