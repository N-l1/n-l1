import json
import requests
import urllib.parse


def main():
    """Pulls languages data from GitHub and returns percentages and bar.

    Returns:
        string: Languages percentages and bar.
    """

    # Please change to your username
    usr = 'qiz-li'

    bar = ''
    langs = {}
    yaml = 'Top languages:\n'

    # Retrieve repo names
    try:
        repos = [repo["name"] for repo in
                 requests.get(
                     url=f'https://api.github.com/users/{usr}/repos').json()
                 # Remove this to include forks
                 if not repo["fork"]]
    except TypeError:
        print("Error: Hmm, it appears that you don't have any repos?\n"
              "If you do, check your username and try again.")
        exit(1)

    # GitHub official language colors
    with open('colors.json', 'r') as file:
        colors = json.load(file)

    # Adding all languages from all user repos
    for repo in repos:
        repo_lang = requests.get(
            url=f'https://api.github.com/repos/{usr}/{repo}/languages').json()
        for lang, val in repo_lang.items():
            if lang in langs:
                langs[lang] += val
            else:
                langs[lang] = val
    total = sum(langs.values())

    # Parse data into percentages and bar
    for lang, val in dict(sorted(langs.items(),
                                 key=lambda item: item[1],
                                 reverse=True)).items():
        percent = int(val/total * 100)
        # Only if language is significant enough to show as an image
        if percent > 0:
            yaml += f'  - {lang} {percent}%\n'
            # A bit of parsing here so that the image is
            # linked to language seach for the user
            bar += (f'[![{lang}](https://via.placeholder.com/'
                    f'{int(percent*1.8)}x10/'
                    f'{colors[lang]["color"][1:]}/?text=+)]'
                    # Specificy the language to search for
                    '(https://github.com/search?l='
                    f"{urllib.parse.quote(lang)}"
                    # Search for the user
                    f"&q=user%3A{usr}"
                    # Show all files
                    '&type=code)')
    return f'``` yaml\n{yaml}```\n\n{bar}\n'


if __name__ == '__main__':
    with open('README.md', 'w') as file:
        file.write(main())
