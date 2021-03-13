import json
import requests


def main():
    """Pulls languages data from GitHub and returns percentages and bar.

    Returns:
        string: Languages percentages and bar.
    """

    # Please change to your username
    usr = 'ilzq'

    bar = ''
    langs = {}
    yaml = 'Top languages:\n'

    # GitHub official language colors
    with open('colors.json', 'r') as file:
        colors = json.load(file)

    repos = [repo["name"] for repo in
             requests.get(
                 url=f'https://api.github.com/users/{usr}/repos').json()
             # Remove this to include forks
             if not repo["fork"]]

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
        yaml += f'  - {lang} {percent}%\n'
        bar += (f'[![{lang}](https://via.placeholder.com/'
                f'{int(percent*1.8)}x10/{colors[lang]["color"][1:]}/?text=+)]'
                f"(https://github.com/search?l={lang.replace(' ', '+')}&q=user"
                f"%3A{usr}+language%3A{lang.replace(' ', '+')})")
    return f'``` yaml\n{yaml}```\n\n{bar}\n'


if __name__ == '__main__':
    with open('README.md', 'w') as file:
        file.write(main())
