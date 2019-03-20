from datetime import date
import json
import requests

from secret import TRELLO_KEY
from secret import TRELLO_TOKEN
from secret import TRELLO_GOAL_LISTS
from stats import get_status_from_percentage

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


class Trello(object):
    
    @staticmethod
    def get_available_years():
        return sorted(list(TRELLO_GOAL_LISTS.keys()), reverse=True)
    
    @staticmethod
    def _get_url_for_year(year):
        list_id = TRELLO_GOAL_LISTS.get(year)
        if not list_id:
            raise Exception
        return BASE_LIST_URL.format(goals_list_id=list_id)


    @staticmethod
    def _get_attachment_urls(attachment_info):
        """Given a list of dict(card_id: "", attachment_id:""), return a dict mapping card_id -> card_url"""
        routes = [
            BASE_ATTACHMENT_ROUTE.format(
                card_id=data["card_id"],
                attachment_id=data["attachment_id"]) for data in attachment_info
        ]
        batch_params = {"urls": ",".join(routes)}
        response = requests.get(BASE_BATCH_URL, params={**base_params, **batch_params})

        # map of attachment_id -> url
        attachment_urls = {
            attachment["200"]["id"]: attachment["200"]["previews"][4]["url"]
            for attachment in response.json()
        }

        card_id_to_attachment_url = {
            attachment_dict["card_id"]: attachment_urls[attachment_dict["attachment_id"]]
            for attachment_dict in attachment_info
        }

        return card_id_to_attachment_url

    @staticmethod
    def get_yearly_stats(year):
        """Collate the stats for a particular year"""
        result = requests.get(Trello._get_url_for_year(year), params={**base_params, **list_filter_params})

        total_checked = 0
        total_items = 0

        attachment_info = []

        stats = []
        today = date.today()
        day_of_year = today.timetuple().tm_yday
        current_year = today.year
        year_completion = (100 * day_of_year) / 365 # close enough
        if current_year > year:
            year_completion = 100.0


        for goal in result.json():
            items_checked = goal["badges"]["checkItemsChecked"]
            items_in_list = goal["badges"]["checkItems"]

            total_checked += items_checked
            total_items += items_in_list

            card_id = goal["id"]
            attachment_id = goal["idAttachmentCover"]
            goal_completion = (100.0 * items_checked / items_in_list)
            tracking_percentage = (100.0 * goal_completion / year_completion)

            stats.append({
                "name": goal["name"],
                "desc": goal["desc"],
                "goal_completion": goal_completion,
                "card_id": card_id,
                "tracking_percentage": tracking_percentage,
                "goal_status": get_status_from_percentage(tracking_percentage)
            })

            attachment_info.append({"card_id": card_id, "attachment_id": attachment_id})

        stats.sort(key=lambda x: x["goal_completion"], reverse=True)
        card_id_to_attachment_url = Trello._get_attachment_urls(attachment_info)
        for goal_info in stats:
            goal_info["cover_url"] = card_id_to_attachment_url[goal_info["card_id"]]

        overall_completion = (100.0 * total_checked / total_items)
        tracking_percentage = (100.0 * overall_completion / year_completion)

        year_stats = {
            "year": year,
            "overall_completion": overall_completion,
            "goals": stats,
            "year_completion": year_completion,
            "tracking_percentage": tracking_percentage,
            "status": get_status_from_percentage(tracking_percentage)
        }

        return year_stats

