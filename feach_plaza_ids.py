import requests
import re


def get_all_plaza_ids():
    cookies = {
        '_ga': 'GA1.1.1688052202.1681837500',
        'ASP.NET_SessionId': 'e24as3pzqvybobrzsz14poky',
        '_ga_T9160NXX5D': 'GS1.1.1681837500.1.1.1681837690.0.0.0',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,mr;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        # 'Cookie': '_ga=GA1.1.1688052202.1681837500; ASP.NET_SessionId=e24as3pzqvybobrzsz14poky; _ga_T9160NXX5D=GS1.1.1681837500.1.1.1681837690.0.0.0',
        'Origin': 'https://tis.nhai.gov.in',
        'Referer': 'https://tis.nhai.gov.in/tollplazasataglance.aspx?language=en',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = "{'TollName':''}"

    response = requests.post(
        'https://tis.nhai.gov.in/TollPlazaService.asmx/GetTollPlazaInfoGrid',
        cookies=cookies,
        headers=headers,
        data=data,
    )

    l = re.findall('TollPlazaPopup\(\d+\)', response.text)
    ids = [int(re.findall('\d+', str_)[0]) for str_ in l]
    return sorted(ids)

if __name__ == '__main__':
    print(get_all_plaza_ids())
