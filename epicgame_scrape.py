from bs4 import BeautifulSoup
import requests
import base64
from PIL import Image

def get_html(url):
    response = requests.get(url)
    if not response.ok:
        print(f'Code: {response.status_code} URL: {url}' )
    return response.text

def get_game(html):
    images = []
    link = []
    soup = BeautifulSoup(html, 'lxml')
    find_games = soup.find_all('a', class_ = 'css-1jx3eyg')
    end = int(len(find_games) / 3)
    games = find_games[0:end]
    
    for game in games:
        images.append(game.find('img').get('data-image'))
        link.append('https://www.epicgames.com'+game.get('href'))

    return link, images

def convert_image_to_base64(url):
    response = requests.get(url)
    uri = ("data:" + response.headers['Content-Type'] + ";" + "base64," + str(base64.b64encode(response.content).decode("utf-8")))
    return uri

def get_game_detail(url, image):
    informations = []

    response = requests.get(url)
    if not response.ok:
        print(f'Code: {response.status_code} URL: {url}')

    html = response.text
    source = BeautifulSoup(html, 'lxml')
    title = source.find('span', class_ = 'css-1gty6cv')
    if title:
        informations.append(source.find('span', class_ = 'css-1gty6cv').text.strip())
    else:
        informations.append(source.find('span', class_ = 'css-w5mrjp').text.strip())
    
    description = source.find('div', class_ = 'css-pfxkyb')
    if description is None:
        informations.append(source.find('span', class_ = 'css-12d0yut').text.strip())
    else:
        informations.append(description.text.strip())
   
    informations.append(convert_image_to_base64(image))
    price_html = source.find('div', class_ = 'css-169q7x3')
    # if len(price)>=2:
    #     if price[1]:
    #         base_price = (price[1].text[1:].replace(',', '.',1).replace(',',''))
    #         discount_price = (price[-1].text[1:].replace(',', '.',1).replace(',',''))
    #         if discount_price < base_price:
    #             informations.append(base_price)
    #             informations.append(discount_price)
    #         else:
    #             informations.append(base_price)
    #             informations.append(None)
    #     # else:
    #     #     informations.append (price[-1].text[1:])
    #     #     informations.append(None)
    # elif len(price) == 1:
    #     informations.append(price[-1].text[1:].replace(',', '.',1).replace(',',''))
    #     informations.append(None)
    # else:
    #     informations.append(None)
    #     informations.append(None)

    if price_html is not None:
        price = price_html.find_all('div', class_ = 'css-1x8w2lj')
        if (len(price)>1):
            base_price = (price[1].text[1:].replace(',', '.',1).replace(',',''))
            discount_price = (price[-1].text[1:].replace(',', '.',1).replace(',',''))
            informations.append(base_price)
            informations.append(discount_price)
        if (len(price)==1):
            informations.append(price[0].text[1:].replace(',', '.',1).replace(',',''))
            informations.append(None)
    else:
        informations.append(None)
        informations.append(None)



    dev_infos = source.find('div', class_ ='css-b6wrti').find_all('span',class_='css-1uf2klp')
    informations.append(dev_infos[0].text.strip())
    informations.append(dev_infos[1].text.strip())
    informations.append(dev_infos[2].text.strip())
    informations.append(dev_infos[3].text.strip())

    genres = source.find_all('a', class_ ='css-4hayrv')
    # informations['gernes'] = [genre.getText() for genre in genres]

    informations.append(source.find('div', class_ ="css-1lwib6p").text)
    rating = source.find('div', class_='css-wt3lag')
    if rating:
        informations.append(rating.find('span', class_ = "css-1uf2klp").text)
    else:
        informations.append(None)

    system_require = source.find_all('div', class_ ="css-2sc5lq")
    min_requirement = ''
    max_requirement = ''
    if system_require:
        for i in range(2,len(system_require)):
            if (i % 2 == 0):
                min_requirement += " "if system_require[i].find('span', class_ = "css-1uf2klp") is None else system_require[i].find('span', class_ = "css-1uf2klp").text+ ","
            else:
                max_requirement += " "if system_require[i].find('span', class_ = "css-1uf2klp") is None else system_require[i].find('span', class_ = "css-1uf2klp").text+ ","

    informations.append(min_requirement)
    informations.append(max_requirement)
   
    return tuple(informations)

def main():
    limit = 0
    game_detail_url = []
    game_img_url =[]
    url = f'https://www.epicgames.com/store/en-US/browse?sortBy=pcReleaseDate&sortDir=DESC&count=40&start={limit}'

    while (limit<40):
        html =get_html(url)
        game, img = get_game(html)
        if game:
            limit += 40
            url = f'https://www.epicgames.com/store/en-US/browse?sortBy=pcReleaseDate&sortDir=DESC&count=40&start={limit}'
            game_detail_url.extend(game)
            game_img_url.extend(img)

  
    game_detail_url.remove('https://www.epicgames.com/store/en-US/p/behind-the-frame-the-finest-scenery')
    game_detail_list = []
    for i in range(len(game_detail_url)):
        game_detail_list.append(get_game_detail(game_detail_url[i], game_img_url[i]))
        # print(get_game_detail(game_detail_url[i], game_img_url[i])[0])
           
    return game_detail_list
   
if __name__ == "__main__":
   main()