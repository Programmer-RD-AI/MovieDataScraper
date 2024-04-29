import base64

from moviedata import *


def encode(message: str) -> bytes:
    """
    Encode string for privacy and encryption.
    """
    msg_bytes = message.encode("latin-1")
    string_bytes = base64.b64encode(msg_bytes)
    string = string_bytes.decode("latin-1")
    return string


def get_page(url: str, cookies: dict):
    try:
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
        }
        # req = requests.get(url, headers=headers, cookies=cookies, timeout=10, verify=False)
        req = http.get(url, headers=headers, cookies=cookies, timeout=10, verify=False)
        return [True, BeautifulSoup(req.content, "html.parser")]
    except:
        return [False, None]


class Save:
    def __init__(self, data: Dict, name: str) -> None:
        self.indexs = range(len(data[list(data.keys())[0]]))
        self.data = pd.DataFrame(data, index=self.indexs)
        self.name = name
        self.file_path = f"{PATH}/data/{self.name}/{self.name}"
        if name not in os.listdir(f"{PATH}/data/"):
            os.mkdir(f"{PATH}/data/{name}")

    def save_csv(self) -> bool:
        self.data.to_csv(self.file_path + ".csv", index=False)
        return True

    def save_json(self) -> bool:
        self.data.to_json(self.file_path + ".json")
        return True


def get_reviews_details(reviews: List[BeautifulSoup]) -> List:
    review_details = []
    for review in reviews:
        review_url = review.find("a").attrs["href"]
        review_three_elems = review.find("span", class_="three-Elements")
        review_three_elems = (
            review_three_elems.find_all("span") if review_three_elems else [None] * 2
        )
        review_count, review_type = (
            review_three_elems[0].text if review_three_elems[0] else None,
            review_three_elems[1].text if review_three_elems[1] else None,
        )
        review_details.append([review_url, review_count, review_type])
    return review_details


def add_to_dict(dictionary: Dict, data_values: List) -> Dict:
    for idx, key in enumerate(dictionary):
        dictionary[key].append(data_values[idx])
    return dictionary


def wait_for_threads(threads: List[threading.Thread]) -> bool:
    for thread in threads:
        thread.join()
    return True


def save(data: Dict, name: str):
    s = Save(data, name)
    s.save_csv()
    s.save_json()


# requests.exceptions.ConnectionError: HTTPSConnectionPool: Max retries exceeded with url (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object"))
