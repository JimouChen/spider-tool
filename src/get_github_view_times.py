import requests
from bs4 import BeautifulSoup

url = 'https://camo.githubusercontent.com/17a6fac0d2f9ea9b5bfa6a6e0f06f4ccd2b3871ae3e11e8527012ad35892a44b/68747470733a2f2f70726f66696c652d636f756e7465722e676c697463682e6d652f4a696d6f754368656e2f636f756e742e737667'

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}


def get_my_github_view_number():
    session = requests.Session()
    response = session.get(url=url, headers=header).text
    nums = BeautifulSoup(response, 'xml')
    view_num = ''
    for tspan in nums.find_all('tspan'):
        view_num += tspan.text
    # print(view_num)

    print('my github view times:', int(view_num))


if __name__ == '__main__':
    get_my_github_view_number()
