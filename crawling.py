import json
import requests
from bs4 import BeautifulSoup


level = 12

BASE_URL = "https://www.kpedia.jp"
START_URL = ""

START_PAGE_INDEX = 1
LAST_PAGE_INDEX = 1

if level == 12:  # TOPIC 1,2급
    START_URL = "https://www.kpedia.jp/p/302-2?nCP="
    # LAST_PAGE_INDEX = 14
    LAST_PAGE_INDEX = 5
elif level == 34:# TOPIC 3,4급
    START_URL = "https://www.kpedia.jp/p/303-2?nCP="
    # LAST_PAGE_INDEX = 62
    LAST_PAGE_INDEX = 5
else :           # TOPIC 5,6급
    START_URL = "https://www.kpedia.jp/p/304-2?nCP="
    LAST_PAGE_INDEX = 5
    # LAST_PAGE_INDEX = 113

# 2. リクエストヘッダ（任意：User-Agentを指定すると弾かれにくくなります）
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
}



my_list = []
error_list = []

def parse(url, headers): 
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # エラーがあれば例外を投げる

    # 4. BeautifulSoupでパース
    soup = BeautifulSoup(response.text, "html.parser")

    # 5. タイトルを取得

    html_table = soup.select("#mainContent > table.school-course")

    if (len(html_table) == 0):
        return
    html_words = html_table[0].select("tr")

    for html_word in html_words:
        html_tds = html_word.select("td")
        if (len(html_tds) == 0):
            continue
        temp = {}
        temp['category'] = str(level)
        for index in range(3):
            html_td = html_tds[index]
            td = html_td.text
            if (index == 0):
                temp["korea"] = td
            elif (index == 1):
                temp["yomikata"] = td
            elif (index == 2):
                temp["japan"] = td
                html_as = html_td.select("a")

                if(len(html_as) != 0):
                    html_a = html_as[0]
                    html_suffic = html_a.get("href")
                    
                    temp['id'] = html_suffic
                    detail_url = BASE_URL + html_suffic
                    
                    # response2 = requests.get("https://www.kpedia.jp/w/44668", headers=headers)
                    response2 = requests.get(detail_url, headers=headers)
                    response2.raise_for_status()
                    soup2 = BeautifulSoup(response2.text, "html.parser")
                    all_tables_html = soup2.find(id="mainContent").find_all("table")

                    all_tables_len  = len(all_tables_html)

                    mean_index = -1
                    yomikata_index = -1
                    yuizigo_index = -1
                    descption_index = -1
                    example_index = -1
                    
                    # 예제의 인덱스 찾을 리스트, 
                    # ・의 개수로 찾는다.
                    # 인덱스 0은 모든 문자열이 포함되어있기 때문에 continue.
                    # 아래에서 max_count_of_dot_index 를 사용하는데 continue한 0 index 때문에 max_count_of_dot_index + 1 해줘야함
                    count_of_dot_list = []
                    for index in range(all_tables_len):
                        if index == 0: 
                            continue
                        count_of_dot_list.append(all_tables_html[index].text.count(' ・ '))
                        if all_tables_html[index].text.__contains__("   意味  ："):
                            mean_index = index
                        if all_tables_html[index].text.__contains__("   読み方  ："):
                            yomikata_index = index
                        if all_tables_html[index].text.__contains__("   類義語  ："):
                            yuizigo_index = index


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

                    max_count_of_dot = max(count_of_dot_list)
                    max_count_of_dot_index = count_of_dot_list.index(max_count_of_dot)
                    example_index = max_count_of_dot_index + 1
                    
                    if set(count_of_dot_list) != {0}:     
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
                                continue


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
                            print("❌ Do not parse example html", detail_url)
                            error_list.append(detail_url)
                    
                    my_list.append(temp)
                    print(len(my_list))
                    print('-----------------------')

           

                else:
                    print("Error")



for i in range(START_PAGE_INDEX, LAST_PAGE_INDEX , 1) :
    url = START_URL + str(i)
    

    print("Cralwing to ", url)
    try:
        parse(url=url, headers= headers)
    except Exception as e:
        print(f"Error at page {i}: {e}")
    finally:
        with open( "TOKIC" + str(level) + "data.json", "w", encoding="utf-8") as f:
            json.dump(my_list, f, ensure_ascii=False, indent=2)
        # with open( "TOKIC" + str(level) + "last_read_page.json", "w", encoding="utf-8") as f:
        #     json.dump({str(level) +  "last_page" : i}, f, ensure_ascii=False, indent=2)
        with open( "ERROR_TOKIC" + str(level) + "data.json", "w", encoding="utf-8") as f:
            json.dump(error_list, f, ensure_ascii=False, indent=2)

print("data.json 파일로 저장 완료")