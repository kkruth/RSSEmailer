import feedparser
import time
import smtplib
import re


def send_email(otsikko, viesti):
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login("rssemailer1@gmail.com", "BSoarXB3")
        sposti = f"Subject: {otsikko}\n\n{viesti}"
        smtp.sendmail("rssemailer1@gmail.com", "gehveli@gmail.com", sposti.encode("utf-8"))


def check_if_new_ep(rss, latest_pub, name):
    if latest_pub != rss.entries[0].published_parsed:
        latest_pub = rss.entries[0].published_parsed
        episode_name = rss.entries[0].title
        episode_description = rss.entries[0].description
        episode_description = re.sub("\<.*?\>", "", episode_description)
        send_email(f"Uusi {name} jakso: {episode_name}", f"Jakson kuvaus:\n\n{episode_description}")
        return latest_pub
    else:
        return latest_pub


def main():
    casefile_rss = feedparser.parse("https://audioboom.com/channels/4940872.rss")
    casefile_latest_ep = casefile_rss.entries[0].published_parsed

    tvbb_rss = feedparser.parse("https://anchor.fm/s/8e3ae9c/podcast/rss")
    tvbb_latest_ep = tvbb_rss.entries[0].published_parsed

    herras_rss = feedparser.parse("https://hakkerit.libsyn.com/rss")
    herras_latest_ep = herras_rss.entries[0].published_parsed

    while True:
        casefile_rss = feedparser.parse("https://audioboom.com/channels/4940872.rss")
        casefile_latest_ep = check_if_new_ep(casefile_rss, casefile_latest_ep, "Casefile")

        tvbb_rss = feedparser.parse("https://anchor.fm/s/8e3ae9c/podcast/rss")
        tvbb_latest_ep = check_if_new_ep(tvbb_rss, tvbb_latest_ep, "Ten Very Big Books")

        herras_rss = feedparser.parse("https://hakkerit.libsyn.com/rss")
        herras_latest_ep = check_if_new_ep(herras_rss, herras_latest_ep, "Herrasmieshakkerit")

        time.sleep(60)


if __name__ == "__main__":
    main()
