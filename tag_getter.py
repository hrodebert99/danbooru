from pathlib import Path
import requests

txt_path = Path("autocomplete.txt")
txt_path.touch()

page = 1
tags = requests.get(f"https://danbooru.donmai.us/tags.json?limit=1000&search[hide_empty]=yes&search[order]=count&page={page}").json()

while tags != []:
    print(f"Page {page}")

    for tag in tags:
        with txt_path.open("a") as file:
            file.write(f"{tag['name']},{tag['post_count']}\n")
    
    page += 1
    tags = requests.get(f"https://danbooru.donmai.us/tags.json?limit=1000&search[hide_empty]=yes&search[order]=count&page={page}").json()
