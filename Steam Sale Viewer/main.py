import requests
from bs4 import BeautifulSoup
import tkinter as tk
import gui


def get_game_titles():
    # TODO: Implement code to get the game titles you want to search for
    game_title = input("Enter the game title you want to search for: ")
    return game_title

def scrape_steam_sale(game_titles):
    # TODO: Implement code to scrape the Steam sale page and check for game titles
    url = "https://store.steampowered.com/search/?os=win&supportedlang=english&specials=1&ndl=1"
    if game_titles:
        url += f"&term={game_titles.replace(' ', '%20')}"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    games = soup.find_all("a", class_="search_result_row")
    
    game_data = []
    for game in games:
        title = game.find("span", class_="title").text.strip()
        if game_titles and game_titles.lower() not in title.lower():
            continue
        discount_block = game.find("div", class_="discount_block search_discount_block")
        if discount_block:
            original_price = discount_block.text.strip()
            #print(title)
            #print(original_price)
        else:
            continue
        
        release_date = game.find("div", class_="col search_released responsive_secondrow").text.strip()
        if release_date:
            #print(release_date)
            pass
        else:
            release_date = "Release date not available"

        review_summary = game.find("span", class_="search_review_summary")
        if review_summary:
            review_summary = review_summary["data-tooltip-html"]
            pass
        else:
            review_summary = "No reviews available"

        image_link = game.find("div", class_="col search_capsule").find("img")["src"]

        game_data.append({
            "title": title,
            "original_price": original_price,
            "release_date": release_date,
            "review_summary": review_summary,
            "image_link": image_link
        })
    return game_data

def cui_main():
    search_option = input("Do you want to search for a specific game title? (yes/no): ")
    if search_option.lower() == "yes":
        game_titles = get_game_titles()
    else:
        game_titles = []

    scrape_steam_sale(game_titles)
        


def main():
    #cui_main()
    gui.gui_main()

if __name__ == "__main__":
    main()