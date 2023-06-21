import json
import requests


def main():
    """Pulls languages data from GitHub and returns percentages and bar.

    Returns:
        tuple: Tuple of languages percentages and bar.
    """

    # Please change to your username
    usr = 'qiz-li'

    langs = {}

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

    # Initial formatting
    yaml = '``` yaml\nTop languages:\n'
    bar = ('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 6" height="6">
  <defs>
    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">\n''')

    start = 0
    # Parse data into percentages and bar
    for lang, val in dict(sorted(langs.items(),
                                 key=lambda item: item[1],
                                 reverse=True)).items():
        percent = val / total * 100
        yaml += f'  - {lang} {round(percent, 1) if int(percent) == 0 else int(percent)}%\n'
        # Use percentage to construct a svg bar with language color
        bar += (
            f'''        <stop offset="{start}%" stop-color="{colors[lang]["color"]}" />
        <stop offset="{start + percent}%" stop-color="{colors[lang]["color"]}" />\n''')
        start += percent

    # File end formatting
    yaml += ('```\n\n[![Languages bar](bar.svg)]'
             f'(https://github.com/search?q=user%3A{usr}&type=code)\n')
    bar += '''    </linearGradient>
  </defs>
  <rect x="0" y="0" width="100%" height="6px" fill="url(#gradient)" rx="1.5" />
</svg>'''

    return yaml, bar


if __name__ == '__main__':
    yaml, bar = main()
    with open('README.md', 'w') as file:
        file.write(yaml)
    with open('bar.svg', 'w') as file:
        file.write(bar)
