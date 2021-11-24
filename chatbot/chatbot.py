# fmt: off
import json
import random
import re
import csv
from collections import deque
from pathlib import Path
from typing import List, Tuple, Union

import pandas as pd

from nltk.tokenize import sent_tokenize
from chatbot.features.qsearch import QSearch
from chatbot.features.sentiment_analysis import get_prediction
from chatbot.models import Question, Video, Order

from transformers import BertTokenizer, BertForSequenceClassification

# fmt: on


class Chatbot:
    """Chatbot object

    Parameters
    ----------
    rule_file: str, Path
        The name of the rule file in the rules directory.

    sa_model_path: str
        Path to the sentiment analysis model backup.
    """

    def __init__(self, rule_file: Union[str, Path], sa_model_path: str) -> None:
        
        with open("./database/database.csv") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                _, created = Question.objects.get_or_create(topic=row[0],sub_topic=row[1],video_title=row[2],question = row[3],answer = row[4],sequence_tree = row[5],topic_terms =row[6])
        
        database = pd.DataFrame.from_records(Question.objects.all().values())
        self.qsearch = QSearch(database)
        
        with open("./database/database2.csv") as f:
            reader = csv.reader(f)
            header = next(reader)
            with open("./tree.txt","w") as f:
                for row in reader:
                    f.write(",".join(self.qsearch.topic_terms(self.qsearch.sequence_tree(row[3])))+"\n")
                    _, created = Order.objects.get_or_create(topic = row[0],sub_topic = row[1],video_title = row[2],question = row[3],answer = row[4],sequence_tree = row[5],topic_terms =row[6])

        database_order = pd.DataFrame.from_records(Order.objects.all().values())
        self.osearch = QSearch(database_order)
        
        
        # init short term memory for Chatbot
        self.memory: deque = deque([], maxlen=3)
        
        # dialog scripts
        self.dialog_memories: list = []
        dialog_path = (
            Path(__file__).resolve().parent / "dialogs" / "dialogs.json"
        )
        with open(dialog_path, "r") as json_dialogs:
            self.dialogs: dict = json.load(json_dialogs)

        # sentiment analysis        
        self.sa_tokenizer = BertTokenizer.from_pretrained(sa_model_path)
        self.sa_model = BertForSequenceClassification.from_pretrained(
            sa_model_path
        )
        self.sa_model = self.sa_model.to("cpu")
        
        # intent rules
        if isinstance(rule_file, str):
            rule_file = Path(rule_file)
        rule = Path(__file__).resolve().parent / "rules" / rule_file
        with open(rule, "r") as json_rules:
            self.rules = json.load(json_rules)

    def __call__(self, query: str) -> Tuple[str, str]:
        """Answers a request using the set of rules and the API.
        Parameters
        ----------
        query: str
            User's request.
        Returns
        -------
        str:
            Chatbot's answer for a specific request.
        """
        queries = sent_tokenize(query)
        responses = []
        wipe_memory = True
        videos = []
        for query in queries:
            # Get intents
            intents = self.get_intent(query.lower())
            # Handle dialog
            if len(self.dialog_memories) > 0:
                dialog = self.dialogs.copy()
                for memory in self.dialog_memories:
                    dialog = dialog[memory]

                if "yes" in intents:
                    if dialog["yes"] != "":
                        wipe_memory = False
                        responses += [dialog["yes"]["msg"]]
                        self.dialog_memories.append("yes")
                elif "no" in intents:
                    if dialog["no"] != "":
                        wipe_memory = False
                        responses += [dialog["no"]["msg"]]
                        self.dialog_memories.append("no")

            # Search Engine
            for intent in intents:
                if intent in ["greetings", "goodbye", "thanks"]:
                    responses += [
                        random.choice(self.rules[intent]["responses"])
                    ]
                elif intent == "repeat":
                    wipe_memory = False
                    responses += [self.memory[-1]]
                
                elif intent == "question":
                    (
                        question_idxs,
                        question_scores,
                        best_question_idxs,
                    ) = self.qsearch.search(query)
                    # print("Scores: ", question_scores)
                    if best_question_idxs is not None:
                        results = self.qsearch.data.loc[
                            best_question_idxs,
                            ["id", "question", "answer", "video_title"],
                        ].values
                        best_question_id: Optional[int] = None
                        answer = ""
                        video = None
                        for result in results:
                            if len(result[2]) >= len(answer):
                                answer = result[2]
                                best_question_id = result[0]
                                video = result[3]

                        if str(best_question_id) in self.dialogs.keys():
                            wipe_memory = False
                            responses += [
                                self.dialogs[str(best_question_id)]["msg"]
                            ]
                            self.dialog_memories = [str(best_question_id)]
                        else:
                            responses += [answer]
                            if video is not None:
                                videos += [video]

                elif intent == "order":
                    (
                        question_idxs,
                        question_scores,
                        best_question_idxs,
                    ) = self.osearch.search(query)
                    # print("Scores: ", question_scores)
                    if best_question_idxs is not None:
                        results = self.osearch.data.loc[
                            best_question_idxs,
                            ["id", "question", "answer", "video_title"],
                        ].values
                        best_question_id: Optional[int] = None
                        answer = ""
                        video = None
                        for result in results:
                            if len(result[2]) >= len(answer):
                                answer = result[2]
                                best_question_id = result[0]
                                video = result[3]

                        if str(best_question_id) in self.dialogs.keys():
                            wipe_memory = False
                            responses += [
                                self.dialogs[str(best_question_id)]["msg"]
                            ]
                            self.dialog_memories = [str(best_question_id)]
                        else:
                            responses += [answer]
                            if video is not None:
                                videos += [video]


            if len(responses) == 0:
                wipe_memory = False
                # Sentiment analysis
                
                mood = get_prediction(query, self.sa_tokenizer, self.sa_model)
                if mood == "negative":
                    responses += [
                        "Oh that is sad to hear, maybe call the support at "
                        + "<a href='https://www.nissanusa.com/contact-us.html'>"
                        + "https://www.nissanusa.com/contact-us.html</a> if you "
                        + "think my answers are not satisfying."
                    ]
                elif mood == "positive":
                    responses += [
                        "Oh well, u're lucky !"
                    ]
                else:
                    responses += [
                        "Sorry, I didn't catch that. Could you reformulate, please?"
                    ]

        if wipe_memory:
            self.dialog_memories = []

        response = "@nl".join(responses)
        #videos = "@nl".join([Video.objects.get(title=video).url for video in videos])
        self.memory.append(response)
        
        return response, videos

    def get_intent(self, query: str) -> List[str]:
        """Returns the user's intent according to a query
        Parameters
        ----------
        query: str
            User's input.
        Returns
        -------
        List:
            List of the detected intents using regular expressions.
        """
        intents = []
        question_or_order_already_in_intents = False
        for key in self.rules.keys():
            if re.search(self.rules[key]["regex"], query) is not None:
                intents.append(key)
        if "question" in intents and "order" in intents:
            intents.remove("question")
        return intents