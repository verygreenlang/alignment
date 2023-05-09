import os
from bs4 import BeautifulSoup
import glob
from git import Repo
from src.tools.caching import JsonCachingHandler #PickleCachingHandler
class GithubRssFeeds:
    def __init__(self,data_path):
        self.data_path = data_path
        self.github_rss_path = data_path + os.sep + "github"+ os.sep + "rssfeeds" + os.sep
        self.github_path = data_path + os.sep + "github" + os.sep + "repo"
        os.system("mkdir -p " + self.github_path)
        os.system("mkdir -p " + self.github_rss_path)
        self.repo_github_url = "https://github.com/plenaryapp/awesome-rss-feeds"
        self.repo_github_data  = self.github_path + os.sep + "awesome-rss-feeds"
        os.system("mkdir -p " + self.repo_github_data)
        self.github_rss_filename = self.github_rss_path + "all.json"

    def get(self):
        data = JsonCachingHandler(self.github_rss_filename).get()
        if data is not None : return data
        content = []
        self.download_git_repo()
        for file in self.list_filename():
            content.append(self.get_data_from_opml_file(file))
        JsonCachingHandler(self.github_rss_filename).store(content)
        return content


    def download_git_repo(self):
        if os.path.isdir(self.repo_github_data ): return
        Repo.clone_from(self.repo_github_url, self.repo_github_data)

    def list_filename(self):
        files = []
        for f in glob.glob(self.repo_github_data + '/**/*.opml', recursive=True):
            files.append(f)
        return files

    def  get_data_from_opml_file(self, filename):
        with open(filename,"r") as f:
            content = f.readlines()
        soup = BeautifulSoup(" \n".join( content))
        soup.prettify()
        file_data = dict()
        data_links = []
        for el in soup.find_all("outline") :#, {"class":"black"})
            if "rss" == el.get('type'):
                source_data = dict()
                source_data["description"] = el.get("description")
                source_data["title"] = el.get("title")
                source_data["xmlurl"] = el.get("xmlurl")
                data_links.append(source_data)
            elif el.get("text") is not None :
                # print(el.get("text"))
                file_data["annotation"] = el.get("text")
        file_data["data_links"] = data_links
        return file_data
