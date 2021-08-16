"""1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json."""
import requests, json

user = 'SokolovJek'
response = requests.get(f'https://api.github.com/users/{user}/repos')
my = response.json()
repo = []
for i in my:
    repo.append(i.get('name'))
print(repo)
with open("repo_github.json", "w", encoding="utf-8") as f:
    json.dump(repo, f)