#!/usr/bin/env python3


"""
Scrape data from a webpage. Use urllib's urlopen function to return the webpage's source code.
From there, use regex to crop the relevant section.
Use regex further to identify the exact items we want to extract.
Use Beautiful Soup to remove html tags. Save as a dictionary.
"""


from string import capwords
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import json


def get_data(source):

    data = urlopen(source)  # Returns HTTPResponse object
    html = data.read().decode("utf-8")  # Returns html page format
    team = re.search(r'<section id="the-team">.*?</section>', html, re.DOTALL)  # Returns relevant section of page
    team = team.group()  # Converts match object to string

    # Find individual members
    members = re.findall(r'<div class="member-name text-center">.*?</div>.*?<div class="member-points">.*?</div>', team, re.DOTALL)
    team_members = []

    for member in members:
        member_dict = {}
        name = re.search(r'<p class="font-gilroy-bold">.*?</p>', member, re.DOTALL).group()  # Return member name
        job = re.search(r'<span>.*?</span>', member, re.DOTALL).group()  # Return member job title
        bio = re.search(r'<div class="member-points">.*?</div>', member, re.DOTALL).group()  # Return member bio
        bio_items = re.findall('<p>.*?</p>', bio, re.DOTALL)  # Returns each line of bio
        
        # Convert to BeautifulSoup object
        name_soup = BeautifulSoup(name, "html.parser")
        job_soup = BeautifulSoup(job, "html.parser")

        # Remove all html tags and capitalize 1st letter of each word
        clean_name = name_soup.get_text()
        clean_name = capwords(clean_name)
        clean_job = job_soup.get_text()
        clean_job = capwords(clean_job)

        # Remove all html tags and capitalize 1st letter of each sentence
        bio_list = []
        for item in bio_items:
            bio_soup = BeautifulSoup(item, "html.parser")
            clean_bio = bio_soup.get_text()

            j = clean_bio.strip().capitalize()
            j = j.replace("\r", "")
            j = j.replace("\n", "")
            j = re.sub(r"\s{2,}", " ", j)
            bio_list.append(j)           
        final_bio = " ".join(bio_list)

        # Store member name, job, and bio as a dictionary and add to list
        member_dict["Name"] = clean_name
        member_dict["Job Title"] = clean_job
        member_dict["Bio"] = final_bio
        team_members.append(member_dict)
       
        # Convert to json format
        team_json = json.dumps(team_members, indent = 4)
        team_json = re.sub(r"\\u2019", "'", team_json)
        team_json = re.sub(r"\\u2014", "-", team_json)
        team_json = re.sub(r"\\u201[c-d]", "'", team_json)
        
    return team_json


source = "https://returnqueen.com/about-us"
print(get_data(source))


""" 
Expected Results:

[
    {
        "Name": "Melissa S.",
        "Job Title": "Vice President Of Growth",
        "Bio": "A jersey girl at heart, melissa practically grew up in the retail industry. Ball of energy. don't even bother trying to keep up. Always 10 steps ahead. Talk to her about charcuterie boards. Deliriously proud dance mom."
    },
    {
        "Name": "Mary G.",
        "Job Title": "Vice President Of Strategy",
        "Bio": "A dynamic and strategic retail veteran. Long-standing record of successes across the retail/wholesale landscape. Loves her nj beach living. Wouldn't give up her family and friends for anything. Looking for mary? you'll find her hiking. #nature"
    },
    {
        "Name": "Mallory K.",
        "Job Title": "Vice President Of Marketing",
        "Bio": "Friend to all things small and cute. you can find her making friends with stray cats. Yes, those are her real eyelashes. Can recite every line of 'the office.' every.single.one. Used to own a children's clothing brand! Lived in jolly old london for a year."
    },
    {
        "Name": "Marc G.",
        "Job Title": "Customer Service Manager",
        "Bio": "New jersey native. Marc prides himself on his problem-solving skills and passion for helping people. Little league coach and team president. Practices patience 24/7. There is nobody as calm as marc."
    },
    {
        "Name": "Lauren W.",
        "Job Title": "Office Manager",
        "Bio": "Radiates light, instant smiles and positive energy when you are greeted by lauren. Organized? her standards are pretty high, step up. Loves working out, hiking and all things outdoors, but the weather better be warm! #hatesthecold Boop! she is a massive schitts creek fan- who isn't? Proud momma and wife."
    },
    {
        "Name": "Eizik G.",
        "Job Title": "Developer & Product Manager",
        "Bio": "Born in london Now lives in ny and thrives on the hustle Family man with two adorable kids Spare time? it's gonna be guitar The most easygoing guy you'll find, he never gets rattled by pressure."
    },
    {
        "Name": "Manu A.",
        "Job Title": "Lead Engineer",
        "Bio": "Originally from alappuzha, a small town in the southern state of india. Always held a passion for problem-solving. For the last three years, he's been a self-proclaimed nomad, living in many exotic places. Now finds himself in tallinn, estonia. World traveler"
    },
    {
        "Name": "Antonio F.",
        "Job Title": "Warehouse Manager",
        "Bio": "A bronx native now living in lincoln park, nj. Educated at big box management. Big-time motorcycle aficionado. For fun, he builds choppers and collects spray paint. Loves all types of music, particularly 50's and 60's rock and roll."
    },
    {
        "Name": "David W.",
        "Job Title": "Qa Tester",
        "Bio": "Loves hockey. Went to school for video game design. He's a very chilled out guy. did we mention super patient? Loves the caffeine. Always learning..kind of like an evolving robot that takes over the world."
    },
    {
        "Name": "James R.",
        "Job Title": "Qa Tester",
        "Bio": "Is one with nature and all earthly creatures. Enjoys sport climbing. Loves a movie-good, bad or really bad. Fave genre is horror or sci-fi. Loves all kinds of tech stuff!"
    },
    {
        "Name": "Kevin W.",
        "Job Title": "Software Engineer",
        "Bio": "Known to be a tik-toker. we don't judge, kevin. Is the official office snack monster. Enjoys an occasional basketball game. Lover of puzzles. He's big on exploring new places."
    },
    {
        "Name": "Ari U.",
        "Job Title": "Senior Front-end Developer",
        "Bio": "We've got outselves a painter here folks. Exercise maven-loves to lift things up and put them down. Loves a good dessert. Major movie buff-we'll bring the popcorn. Total tech and design nerd."
    }
]
"""