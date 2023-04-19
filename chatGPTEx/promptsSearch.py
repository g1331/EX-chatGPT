import os
import re
from fuzzywuzzy import process
from xpinyin import Pinyin
import csv
import json
name_list=[]
program_path = os.path.realpath(__file__)
program_dir = os.path.dirname(program_path)
json_file_path = f'{program_dir}/prompts/prompts.json'
name_list = []
promptsJSON = {}
with open(json_file_path, 'r', encoding='utf-8') as f:
        promptsJSON = json.load(f)
        name_list.extend(prompt['act'] for prompt in promptsJSON)
promptsDict = {prompt['act']: prompt['prompt'] for prompt in promptsJSON}
pin =Pinyin()
pinlist = [[re.sub('-','',pin.get_pinyin(i)),i] for i in name_list]
def SearchPrompt(name,resultLimit=7):
        searchResults=process.extract(name, name_list, limit=resultLimit)
        searchResultsPin=process.extract(name, pinlist, limit=resultLimit)
        finalResult = [[searchResult[1], searchResult[0]]
                       for searchResult in searchResults]
        flag=0
        for searchResult in searchResultsPin:
                flag = next((1 for i in finalResult if searchResult[0][1]==i[1]), 0)
                if flag==0:
                        finalResult.append([searchResult[1],searchResult[0][1]])
        finalResult.sort(reverse=True)
        finalResultList=[]
        cnt=0
        print(finalResult)
        for res in finalResult:
                if(res[0]<50): break
                finalResultList.append(res[1])
                cnt+=1
                if cnt>=resultLimit:break
        return finalResultList
if __name__ == '__main__':
        print(SearchPrompt('zhengze'))


 