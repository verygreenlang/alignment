import pandas as pd
import pickle
import json
from dateutil import parser, tz
from datetime import datetime
import os
import plotly.express as px
import plotly.graph_objects as go
from tqdm import tqdm

import string


def load_news(news_path):
    d = []
    for news in os.listdir(news_path):
        for date in os.listdir(news_path + news):
            data_path = news_path + news + "/" + date
            try:
                with open(data_path, "rb") as f:
                    content = pickle.load(f)
                if "entries" in content.keys():
                    for entry in content["entries"]:
                        new_d = {}
                        new_d["text"] = (
                            str(entry.get("title")) + " " + str(entry.get("summary"))
                        )
                        new_d["date"] = entry.get("published")
                        d.append(new_d)

            except EOFError:
                pass
            except Exception as e:
                print("error loading news ")
                print(e)
                pass
    return pd.DataFrame(d)


def topic_in_text(topics, text):
    if text :
        clean_text = text.lower()
        for topic in topics:
            if topic.lower() in clean_text:
                return True
    return False


class NewsGraphs:
    def __init__(self, data_path, industry, esg, company_name=None):
        self.topic_industry = industry
        self.esg_industry = esg
        self.company_name = company_name

        self.data_path = (
            data_path
            + os.sep
            + "/news"
            + os.sep
            + "graphs/"
            + company_name.replace(" ", "_")
            + "/"
        )
        self.github_news_path = data_path + "/news/rssfeeds/github/"
        self.wikidata_news_path = data_path + "/news/rssfeeds/wikidata/"
        os.system("mkdir -p " + self.data_path + "relevent")

    def generate(self):
        number_of_cluster = 10
        cache_path = "/home/famat/Desktop/test_df2.csv"
        if os.path.isfile(cache_path):
            news_df = pd.read_csv(cache_path)
        else:
            news_df2 = load_news(self.wikidata_news_path)
            news_df1 = load_news(self.github_news_path)
            news_df = pd.concat([news_df1, news_df2])
            news_df = news_df.drop_duplicates()
            cache_path = "/home/famat/Desktop/test_df.csv"
            if os.path.isfile(cache_path):
                news_df.to_csv(cache_path)
        for topic in tqdm(self.topic_industry, desc=" mining industry topics "):
            # for topic in self.topic_industry :
            news_df["industry"] = news_df["text"].apply(
                lambda x: topic_in_text([topic], x)
            )
            news_df = news_df[news_df["industry"]]

            for esgtopic in tqdm(self.esg_industry, desc=" mining esg topics "):
                # for esgtopic in self.esg_industry:
                try:
                    news_df["esg"] = news_df["text"].apply(
                        lambda x: topic_in_text([esgtopic], x)
                    )
                    industry_df = news_df[news_df["industry"]]
                    industry_df = industry_df.drop_duplicates()
                    industry_df = industry_df.dropna()
                    industry_df["date_dt"] = industry_df["date"].apply(
                        lambda x: parser.parse(x, tzinfos={"CDT": 0 * 3600})
                    )
                    industry_df["date_dt_timestamp"] = industry_df["date"].apply(
                        lambda x: parser.parse(x, tzinfos={"CDT": 0 * 3600}).timestamp()
                    )
                    industry_df["dateGroups"] = pd.qcut(
                        industry_df["date_dt_timestamp"], number_of_cluster
                    ).astype("str")
                    industry_df["esg"] = industry_df["esg"].apply(
                        lambda x: 1 if x else 0
                    )
                    industry_df["industry"] = industry_df["industry"].apply(
                        lambda x: 1 if x else 0
                    )
                    industry_df["dateGroups"] = industry_df["dateGroups"].apply(
                        lambda x: datetime.fromtimestamp(
                            int(
                                x.split(",")[1]
                                .replace("]", "")
                                .replace(" ", "")
                                .split(".")[0]
                            )
                        )
                    )
                    industry_df = industry_df.sort_values(by=["dateGroups"])
                    counted = industry_df.groupby("dateGroups").sum()
                    counted.head()

                    if counted.sum()["esg"] / counted.sum()["industry"] > 0:

                        # print(counted["es.sum())value_counts().get("1"))
                        # print(counted["industry"].value_counts().get("1"))
                        industry_col_name = "Topic: " + topic
                        esg_col_name = "Topics: " + topic + " AND " + esgtopic

                        counted = counted.rename(
                            columns={"industry": industry_col_name, "esg": esg_col_name}
                        )
                        # print(counted)
                        fig1 = px.line(
                            counted,
                            x=counted.index,
                            y=[esg_col_name, industry_col_name],
                            color_discrete_map={
                                industry_col_name: "#456987",
                                esg_col_name: "#124D03",
                            },
                            markers=True,
                        )
                        # fig2 = px.line(counted, x=counted.index, y='industry',markers=True)#,line_color="green")
                        # fig1.update_traces(line_color='#124D03')

                        fig = go.Figure(data=fig1.data)  # + fig2.data)

                        alphabet = string.ascii_lowercase
                        interesting_ratio = 0.1 * counted.sum()[esg_col_name]
                        annotation_iteration = 0
                        for index in counted.index[
                            counted[esg_col_name] > interesting_ratio
                        ].tolist():

                            fig.add_annotation(
                                showarrow=True,
                                arrowhead=1,
                                align="right",
                                x=index,  # counted.max(axis = 1).idxmax(),
                                y=counted[esg_col_name].loc[index],
                                text=alphabet[annotation_iteration].upper(),  # "--",
                                opacity=0.7,
                                bordercolor="black",
                                borderwidth=1,
                            )
                            annotation_iteration += 1
                        if annotation_iteration > 0:
                            topic1 = topic
                            topic2 = esgtopic
                            fig.update_layout(
                                title="Interest of topics: " + topic1 + " X " + topic2,
                                xaxis_title="Date",
                                yaxis_title="News Count",
                            )

                            legend_title = (
                                """ This Graph represent the interest of the esg topic <br> <b>"""
                                + esgtopic
                                + "</b> <br> "
                                + """ for all the news articles that contains the topic <br> <b>"""
                                + topic
                                + """</b> </br>"""
                            )
                            fig.update_layout(legend_title_text=legend_title)

                            # fig.show()

                            image_path = (
                                self.data_path
                                + "relevent/"
                                + topic.replace(" ", "_")
                                + "_"
                                + esgtopic.replace(" ", "_")
                                + ".png"
                            )
                            # print("image path", image_path)
                            fig.write_image(image_path)
                except Exception as e:
                    print(e)

        # fig.to_image()
