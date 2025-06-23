from pathlib import Path
import requests

if __name__ == "__main__":
    search_tags = input("Search tags: ")
    include_tags = input("Include tags: ").split()
    exclude_tags = input("Exclude tags: ").split()

    download_path = Path(search_tags)
    download_path.mkdir(parents = True, exist_ok = True)

    media_types = input("File extensions: ").split()

    page = 1
    posts = requests.get(f"https://danbooru.donmai.us/posts.json?tags={search_tags}&page={page}").json()

    while posts != []:
        for post in posts:
            if post["file_ext"] not in media_types:
                continue

            if "file_url" not in post:
                continue

            exclude_tag_found = False
            for tag in exclude_tags:
                if tag in post["tag_string"]:
                    exclude_tag_found = True
                    break
            if exclude_tag_found:
                continue

            include_tag_found = True
            for tag in include_tags:
                if tag not in post["tag_string"]:
                    include_tag_found = True
                    break
            if not include_tag_found:
                continue

            print(f"Post ID: {post['id']}, Post MD5: {post['md5'] if 'md5' in post else ''}")

            post = {
                "id": post["id"],
                "file_ext": post["file_ext"],
                "tag_string_general": post["tag_string_general"].replace(" ", ", ").replace("_", " ").replace("(", "\\(").replace(")", "\\)"),
                "tag_string_character": post["tag_string_character"].replace(" ", ", ").replace("_", " ").replace("(", "\\(").replace(")", "\\)"),
                "tag_string_copyright": post["tag_string_copyright"].replace(" ", ", ").replace("_", " ").replace("(", "\\(").replace(")", "\\)"),
                "tag_string_artist": post["tag_string_artist"].replace(" ", ", ").replace("_", " ").replace("(", "\\(").replace(")", "\\)"),
                "tag_string_meta": post["tag_string_meta"].replace(" ", ", ").replace("_", " ").replace("(", "\\(").replace(")", "\\)"),
                "file_url": post["file_url"],
                "md5": post["md5"] if "md5" in post else None
            }

            if post["md5"] != None:
                media_path = download_path.joinpath(post["md5"]).with_suffix(f".{post['file_ext']}")
            else:
                media_path = download_path.joinpath(post["id"]).with_suffix(f".{post['file_ext']}")
            
            with media_path.with_suffix(".txt").open("w") as file:
                file.write(f"{post['tag_string_character']}, {post['tag_string_copyright']}, {post['tag_string_artist']}, {post['tag_string_meta']}, {post['tag_string_general']}")
            
            response = requests.get(post["file_url"], stream = True)
            with media_path.open("wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

        page += 1
        posts = requests.get(f"https://danbooru.donmai.us/posts.json?tags={search_tags}&page={page}").json()
