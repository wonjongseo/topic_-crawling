import json
import requests
from bs4 import BeautifulSoup


level = 12

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
}
errors = []
with open("ERROR_TOKIC" + str(level) +  "data.json", "r", encoding="utf-8") as f:
    # 2. json.load() 로 파이썬 객체로 변환
    errors = json.load(f)


for error in errors:
    print('error' + error) 





# my_list = []
error_list = []

def parseDetailPage(url, headers): 
    temp = {}
    response2 = requests.get(url, headers=headers)
    response2.raise_for_status()
    soup2 = BeautifulSoup(response2.text, "html.parser")
    all_tables_html = soup2.find(id="mainContent").find_all("table")

    all_tables_len  = len(all_tables_html)

    mean_index = -1
    yomikata_index = -1
    yuizigo_index = -1
    example_index = -1
    descption_index = -1
    for index in range(all_tables_len):
        if index == 0 or index == 1: 
            continue
        if all_tables_html[index].text.__contains__("   意味  ："):
            mean_index = index
        if all_tables_html[index].text.__contains__("   読み方  ："):
            yomikata_index = index
        if all_tables_html[index].text.__contains__("   類義語  ："):
            yuizigo_index = index
        if all_tables_html[index].text.__contains__("・"):
            example_index = index
        if mean_index != -1 and  yomikata_index  != -1 and  yuizigo_index != -1 and  example_index != -1:
            break

    if mean_index != -1 :
        temp["japan"] = all_tables_html[mean_index].text
    if yomikata_index != -1 :
        temp["yomikata"] = all_tables_html[yomikata_index].text
    if yuizigo_index  != -1 :
        temp["yuizigo"] = all_tables_html[yuizigo_index].text

    if yuizigo_index != -1 :
        descption_index = yuizigo_index + 1 
    else :
        if yomikata_index != -1 :
            descption_index = yomikata_index + 1
        
    if descption_index != -1:
        temp["desc"] = all_tables_html[descption_index].text


    # 예문 테이블 인덱스 탐색

    try: 
        if example_index == -1 :
            if descption_index != -1:
                # 예문 테이블이 대부분 설명 밑에 있어서 설명 인덱스 + 1
                example_index = descption_index + 1 
            else :
                # 그것도 아니라면 대충 끼워맞추기
                example_index = all_tables_len - 3 
        
        # 끼워맞추다가 실패하는 거 방지
        if  all_tables_len < 3: 
            print("Count of all Table is short 3")
            return temp


        examples_html = all_tables_html[example_index].select('tr')

        examples_html_len = len(examples_html)
        examples = []
        for index in range(0, examples_html_len, 2):
            example = {}
            example_word =  examples_html[index].text
            example_mean =  examples_html[index+1].text

            example['word'] = example_word
            example['mean'] = example_mean
            examples.append(example)
        
        temp['examples'] = examples
    except:
        print("❌ Do not parse example html", url)
        error_list.append(url)
    temp['category'] = str(level)
    return temp


for url in errors:
    print("Cralwing to ", url)
    try:
        parseDetailPage(url=url, headers= headers)
    except Exception as e:
        print(f"Error at page {url}: {e}")
    # finally:
    #     with open( "TOKIC" + str(level) + "data.json", "w", encoding="utf-8") as f:
    #         json.dump(my_list, f, ensure_ascii=False, indent=2)
    #     # with open( "TOKIC" + str(level) + "last_read_page.json", "w", encoding="utf-8") as f:
    #     #     json.dump({str(level) +  "last_page" : i}, f, ensure_ascii=False, indent=2)
    #     with open( "ERROR_TOKIC" + str(level) + "data.json", "w", encoding="utf-8") as f:
            # json.dump(error_list, f, ensure_ascii=False, indent=2)

print("data.json 파일로 저장 완료")