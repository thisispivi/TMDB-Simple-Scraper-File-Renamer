import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.themoviedb.org/tv/105556/season/2" + "?language=it-IT"
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "files")


def get_titles():
    titles = []
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("div", {'class': ['title']})
    for r in results:
        row = r.find_all("a", {"class": ['no_click', 'open']})
        if (row != []):
            anime = str(row).split("title=\"")[1].split(": Season ")[0]
            season = str(row).split("title=\"")[1].split(": Season ")[1][:1]
            episode = str(row).split("title=\"")[1].split(
                ": Episode ")[1].split(" - ")[0]
            if (len(episode) == 1):
                episode = "0"+episode
            title = str(row).split("title=\"")[1].split(
                ": Episode ")[1].split(" - ")[1].split("\">")[0].replace(".", "")
            titles.append({"anime": anime, "season": season,
                           "episode": episode, "title": title})
    return titles


def get_files_list():
    files = []
    for file in os.listdir(path):
        if (".ini" not in file):
            files.append(file)
    return files


def replace_error_char(string):
    return string.replace("?", "").replace(":", "").replace("/", "").replace("\"", "")


def get_new_title(title, extension):
    return replace_error_char(title["anime"]) + " - S" + title["season"] \
        + "E" + title["episode"] + " - " + \
        replace_error_char(title["title"]) + "." + extension


def rename_files(titles, files):
    for i in range(0, len(titles)):
        os.rename(os.path.join(path, files[i]), os.path.join(
            path, get_new_title(titles[i], files[i].split(".")[1])))


def print_list(list):
    for l in list:
        print(l)


if __name__ == '__main__':
    print("Getting Titles from: " + URL + "\n")
    titles = get_titles()
    print("Done!\n")
    print_list(titles)
    print("\n")
    print("Getting the files in the folder\n")
    files = get_files_list()
    print("Done!\n")
    print_list(files)
    print("Num files: " + str(len(files)))
    print("Num titles: " + str(len(titles)))
    print("\nIs the number of files equal the number of episodes? " +
          str(len(files) == len(titles)))
    rename_files(titles, files)
    print("Done!\n")
    print("Getting the new files in the folder\n")
    files = get_files_list()
    print("Done!\n")
    print_list(files)
