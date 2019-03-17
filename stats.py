import json
import pprint
import requests

from secret import TRELLO_KEY
from secret import TRELLO_TOKEN


goals_lists = {
    2019: "5c26fc0ae7850e0a2d6957aa",
    2018: "5a2c84deeb730b2c9c39b7ce",
    2017: "586189b1841687618588f644",
    2016: "568572f8023086e7ced9ea5e",
}

BASE_LIST_URL = "https://api.trello.com/1/lists/{goals_list_id}/cards"

BASE_ATTACHMENT_ROUTE = "/cards/{card_id}/attachments/{attachment_id}"
BASE_BATCH_URL = "https://api.trello.com/1/batch/"

base_params = {
    "key": TRELLO_KEY,
    "token": TRELLO_TOKEN
}

list_filter_params = {
    "fields": ",".join(["name", "desc", "badges","idAttachmentCover"])
}


def get_url_for_year(year):
    list_id = goals_lists.get(year)
    if not list_id:
        raise Exception
    return BASE_LIST_URL.format(goals_list_id=list_id)


def get_attachment_urls(attachment_info):
    routes = [
        BASE_ATTACHMENT_ROUTE.format(card_id=data["card_id"], attachment_id=data["attachment_id"]) for data in attachment_info
    ]
    print(routes)
    response = requests.get(BASE_BATCH_URL, params={**base_params})
    #print(response.json()["url"])

    
def get_yearly_stats(year):
    result = requests.get(get_url_for_year(year), params={**base_params, **list_filter_params})

    total_checked = 0
    total_items = 0

    attachment_info = []

    stats = []
    

    for goal in result.json():
        items_checked = goal["badges"]["checkItemsChecked"]
        items_in_list = goal["badges"]["checkItems"]

        total_checked += items_checked
        total_items += items_in_list

        card_id = goal["id"]
        attachment_id = goal["idAttachmentCover"]

        stats.append({
            "name": goal["name"],
            "completion": (100.0 * items_checked / items_in_list),
            "card_id": card_id
        })

        attachment_info.append({"card_id": card_id, "attachment_id": attachment_id})
        
    get_attachment_urls(attachment_info)

    stats.sort(key=lambda x: x["completion"], reverse=True)

    year_stats = {
        "year": year,
        "overall_completion": (100.0 * total_checked / total_items),
        "goal_completion": stats,
    }

    pprint.pprint(year_stats)



get_yearly_stats(2019)


"""
Year
status
breakdown


"""

