import requests
import asyncio
import lxml.html

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

    def root_scene(self):
        while self.continue_flag:
            if self.view_name == "before-search":
                self.input_key_word()
                if self.continue_flag:
                    self.searcher.search_request(self.search_word)
            elif self.view_name == "search-results":
                self.output_search_results()


    def output_search_results(self):
        #TODO:出力書いといて for 俺
        print("""============\nSearchResult\n============""")
        i = 1
        for detail in self.search_results:
            print("No.{}".format(i))
            print()




class QiitaSearcher:
    def search_request(self, word):
        """
        Qiitaに検索のリクエストを送って検索結果を保存するクラス
        Parameters
        word: String
            検索する単語
        """
        url = "https://qiita.com/search"
        raw_html = requests.get(url)
        html = lxml.html.fromstring(raw_html.text)
        #TODO: データパースしろカス
        data = None
        return data

