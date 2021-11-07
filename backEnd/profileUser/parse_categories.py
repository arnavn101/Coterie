import json
data = None
import os

ROOT_DIR = 'profileUser'
with open(os.path.join(ROOT_DIR, 'raw_interest_list.json'), 'r') as f:
    data = json.load(f)

output_dict = {}
interests_list = {}

for interest in data:
    category = interest['category']
    sub_category = interest['subCategory']
    title = interest['title']
    interests_list[title] = 0

    if category not in output_dict:
        output_dict[category] = {}
    
    if sub_category not in output_dict[category]:
        output_dict[category][sub_category] = []

    output_dict[category][sub_category].append(title)

with open(os.path.join(ROOT_DIR ,'categories.py'), 'w') as f:
    f.write('categories = ' + json.dumps(output_dict))

with open(os.path.join(ROOT_DIR ,'interests_list.py'), 'w') as f:
    f.write('interests_dict = ' + json.dumps(interests_list))


        