import openai
import pandas as pd
import numpy as np
from tqdm import tqdm
import time


excel_path = ''        # excel 路径，最好放在 original 下面，例如：original/app-orgnization（翻译字段）.xlsm
result_name = ''       # 记得加上 .xlsx 后缀，例如： DDESB.xlsx

df = pd.read_excel(excel_path,engine='openpyxl')

separator = '--}}--{{--'

test = separator.join(df[df.columns[1]].values[:20])


ROLE_SETUP_PROMPT = '''
You are a professional translator:
1. You are fluent in both English and Chinese.
2. You are familar with technical terms in web technology, web application and product development. For instance, you know that '功能' should be translated to 'feature' instead of 'function;
3. You are good at translating documents, manuals, files and paper.
4. You will ask me for advice if you are not sure what a word is meant in one language.
'''

REQUIREMENT_SETUP_PROMPT = '''
You are now going to translate official documents of a website.
Here are some requirements:
1. Your translation style should be technical.Here is an example enclosed in curly brackets, which contains source material, good style of translation and bad style.
{ 
source material: "可将想要收纳的模块拖拽添加到这里"
good style: "Modules intended for storage can be added via drag-and-drop here." 
bad style: "You can drag and drop the modules you want to store here."
}
2. You will be given a string separable by a special separator "--}}--{{--" . Seperate the string with this separator first.
3. Each substring is a source material that needs translation.
4. Hold your translation of individual words consistent across multiple source material.
5. Your translation should also be a string separated the separator  "--}}--{{--" 
6. Make sure each piece of translation uses the good style.
7. If there are less than 3 words in your translation, capitalize every word.
8. If there are more than 3 words in your translation, capitalize only the first word as if it is a sentence.
9. When you return the result, concatenate each of your translation string with the same separator "--}}--{{--"
'''

chunk_size = 50
chunck_counts = len(df[df.columns[1]].values)//chunk_size+1




# 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

openai.api_key = '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'

setups = [
{"role": "system", "content": ROLE_SETUP_PROMPT},
{"role": "system", "content": REQUIREMENT_SETUP_PROMPT},
]

results = []

for i in tqdm(np.arange(chunck_counts)):
    
    if i%10==0:

        setups = [
                {"role": "system", "content": ROLE_SETUP_PROMPT},
                {"role": "system", "content": REQUIREMENT_SETUP_PROMPT},
                ]

    completion = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=setups + [
        {"role": "user", "content": separator.join(df[df.columns[1]].values[i*chunk_size:(i+1)*chunk_size])},
    ]
    )
    translation = completion.choices[0]['message']['content']
    results += translation.split(separator)
    setups += [{"role":"assistant","content":translation}]
    time.sleep(1.5)

pd.DataFrame({'translation':results}).to_excel('translated/{result_name}'.format(result_name = result_name),index=False)