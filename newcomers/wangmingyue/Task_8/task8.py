from pathlib import Path
import json
folder = Path(r"D:\Projects\General-Learning\General-Learning\Task_8")
all_folder = folder / 'summary.json'
results = []
if folder.exists() and folder.is_dir():
    for path in folder.rglob('*.md'):
        if not path.is_file():
            continue
        with open(path,'r', encoding = 'utf_8') as file:
            content = file.read()
        characters = len(content)
        lines = len(content.splitlines())
        results.append({'file': str(path),'character': characters,'lines': lines })
    with open(all_folder,'w',encoding='utf-8') as file:
        json.dump(results,file,ensure_ascii=False,indent=2)
    print(results)
