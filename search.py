import requests
import lxml.html
import shutil

class ReaderMain:
    """
    Readerのデータ管理と表示する内容
    """


    def __init__(self):
        self.view_name = "before-search"
        self.continue_flag = True
        self.have_to_change_view_flag = True
        self.search_word = ""
        self.searcher = QiitaSearcher()
        self.search_results = []
        self.article_number = 0

    def input_key_word(self):
        self.have_to_change_view_flag = False
        while True:
            key_word = input("検索する単語を入力してください\nQと入力するとアプリを終了します")
            cache = key_word.replace(" ", "")
            cache = cache.replace("　", "")
            if cache != "":
                if cache == "Q":
                    self.continue_flag = False
                else:
                    self.search_word = key_word
                    self.view_name = "search-results"
                return
    def get_divider(self, n):
        s = ""
        for i in range(0, n):
            s += "="
        return s

    def root_scene(self):
        terminal_size = shutil.get_terminal_size()
        while self.continue_flag:
            if self.view_name == "before-search":
                self.input_key_word()
            elif self.view_name == "search-results":
                self.search_results = self.searcher.search_request(self.search_word)
                self.output_search_results()
                self.select_article()
                print(self.get_divider(terminal_size[0]))
                print(self.searcher.load_article(self.search_results[self.article_number]["url"]))
                print(self.get_divider(terminal_size[0]))
                self.view_name = "before-search"

    def select_article(self):
        while True:
            n = input("記事の番号を入力してください\n>>>")
            try:
                if int(n) in range(1, len(self.search_results) + 2):
                    self.article_number =  int(n)
                    return
                else:
                    print("記事の番号にはありません")
            except ValueError:
                print("数値を入力してください")


    def output_search_results(self):
        #TODO:出力書いといて for 俺
        print("""============\nSearchResult\n============""")
        i = 1
        for detail in self.search_results:
            print("No.{}".format(i))
            print("Title:{}".format(detail["title"]))
            print("Writer:{}".format(detail["writer"]))
            i += 1




class QiitaSearcher:
    def search_request(self, word):
        """
        Qiitaに検索のリクエストを送って検索結果を保存するクラス
        Parameters
        word: String
            検索する単語
        """
        url = "https://qiita.com/search"
        params = {"q": word}
        raw_html = requests.get(url, params)
        html = lxml.html.fromstring(raw_html.text)
        results = []

        for d in range(2, 12):
            data_cache = {}

            # 記事の各要素をdata_cacheへ保存
            writer_name = html.xpath("/html/body/div[3]/div/div/div[1]/div[{}]/div[1]/a".format(d))[0].attrib["href"].strip("/")
            data_cache["writer"] = writer_name

            url = html.xpath("/html/body/div[3]/div/div/div[1]/div[{}]/div[2]/h1/a".format(d))[0].attrib["href"]
            data_cache["url"] = url

            title = html.xpath("/html/body/div[3]/div/div/div[1]/div[{}]/div[2]/h1".format(d))[0].text_content()
            data_cache["title"] = title

            # resultsへデータを保存
            results.append(data_cache)

        return results

    def load_article(self, raw_url):
        url = "https://qiita.com" + raw_url
        access = requests.get(url)
        html = lxml.html.fromstring(access.text)
        txt = html.xpath("//section[@class='it-MdContent']")[0].text_content()
        return txt

if __name__ == '__main__':
    reader = ReaderMain()
    reader.root_scene()
