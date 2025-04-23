from flask import Flask, jsonify
from bs4 import BeautifulSoup
import os
import requests

app = Flask(__name__)

def get_soup(url):
    html = requests.get(url).text
    return BeautifulSoup(html, "html.parser")

def find_schedule_tables(soup):
    academic_calendar = {}
    tables = soup.find("ul", class_="list-tab-accordian").find_all("li")
    for table in tables:
        term_title = table.find("h3").get_text(strip=True)
        schedule = table.find("dl", class_="dl-horizontal")
        if not schedule:
            continue
        dates = schedule.find_all("dt")
        dates_info = schedule.find_all("dd")
        academic_calendar[term_title] = [
            f"{dt.get_text(strip=True)} - {dd.get_text(' ', strip=True)}"
            for dt, dd in zip(dates, dates_info)
        ]
    return academic_calendar

@app.route("/calendar", methods=["GET"])
def get_calendar():
    soup = get_soup("https://www.deanza.edu/calendar/")
    calendar = find_schedule_tables(soup)
    return jsonify(calendar)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

