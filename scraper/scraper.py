from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import sqlite3
from time import sleep


def write_question(q_id, q_tags, ans_id, ans_tags):
    with sqlite3.connect("../database/db") as conn:
        conn.execute("INSERT INTO questions (stack_id, ans_id, ans_tags, q_tags) VALUES"
                     " (?, ?, ?, ?)", (q_id, ans_id, ans_tags, q_tags))
        conn.commit()


def write_worker(stack_id, tags):
    with sqlite3.connect("../database/db") as conn:
        conn.execute("INSERT INTO worker (stack_id, tags) VALUES "
                     "(?, ?)", (stack_id, tags))
        conn.commit()


def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)


def get_questions_links():
    p_link = "https://stackoverflow.com/questions?sort=frequent&page={0}"
    parent_url = "https://stackoverflow.com"
    for i in range(1, 2):
        raw = simple_get(p_link.format(i))
        bs = BeautifulSoup(raw, 'html.parser')
        q_sum = bs.findAll("div", {"class": "question-summary"})
        for j in q_sum[:3]:
            link = j.find("a", {'class': 'question-hyperlink'})['href']
            acc = j.find('div', {'class': 'status answered-accepted'})
            if acc is not None:
                raw_2 = simple_get(parent_url + link)
                bs2 = BeautifulSoup(raw_2, 'html.parser')
                q_id = link.split('/')[2]  # returns question id
                # print(q_id)
                tags = ""  # returns question tags
                tags_set = set()
                for j in bs2.findAll("a", {'rel': "tag"}):
                    text = j.getText()
                    tags += text + ',' if text not in tags_set else ""
                    tags_set.add(text)
                # print(tags)
                answer = bs2.find('div', {'class': 'answer accepted-answer'})
                for k in answer.findAll('div', {'class': 'user-details'}):
                    for kk in k.findAll('a'):
                        if kk.has_attr('href'):
                            if 'user' in kk['href']:
                                user_link = kk['href']
                                user_stack_id = user_link.split('/')[2]  # returns user id
                                raw_3 = simple_get(parent_url + user_link + "?tab=tags&sort=votes")
                                bs3 = BeautifulSoup(raw_3, 'html.parser')
                                u_raw_tags = bs3.find('div', {'class': 'user-tab-content'})
                                user_tags = ""
                                user_tags_score_count = ""
                                for tt in u_raw_tags.findAll('td'):
                                    user_tag = tt.find('a', {'class': 'post-tag'}).getText()
                                    user_tags += user_tag + ","
                                    user_tags_score_count += user_tag + ":"
                                    score = tt.find('div', {'class': 'answer-votes'}).getText()
                                    user_tags_score_count += score + ":"
                                    if tt.has_attr('span'):
                                        count = tt.find('span', {'class': 'item-multiplier-count'}).getText()
                                    else:
                                        count = "0"
                                    user_tags_score_count += count + ","

                                # write data in database
                                write_question(int(q_id), tags, user_stack_id, user_tags)

                                write_worker(user_stack_id, user_tags_score_count)


get_questions_links()
