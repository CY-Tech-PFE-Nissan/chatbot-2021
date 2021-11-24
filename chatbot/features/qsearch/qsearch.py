import nltk
from nltk import RegexpParser, ne_chunk, pos_tag, word_tokenize
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Tuple, Union

from .preprocessors import Lemmatize, Preprocess, Format


def search(tree: nltk.tree.Tree, tags: List[str]) -> List[str]:
    """ Searches for given tags in provided nltk.tree.Tree.

    Parameters
    ----------
    nltk.tree.Tree
        Sequence tree computed using nltk.
    tags
        List of the tags to look for.
    Returns
    -------
    list
        List of the words that have a tag in the input tag list.
    """
    if not isinstance(tree, nltk.tree.Tree):
        _, tag = tree.split("/")
        return [tree] if tag in tags else []
    else:
        output = []
        if tree.label() in tags:
            output = [" ".join(tree.leaves())]
        for child in tree:
            output += search(child, tags)

        return output


def reduce_np(tree: nltk.tree.Tree) -> str:
    subjects = search(tree, ["NN", "NNS", "NNP", "NNPS", "PRP"])
    if len(subjects) > 0:
        return " ".join(subjects)
    adjts = search(tree, ["JJ", "JJR", "JJS"])
    if len(adjts) > 0:
        return " ".join(adjts)
    dets = search(tree, ["CD", "DT", "PRP\\$"])
    return " ".join(dets)


def reduce_vp(tree: nltk.tree.Tree) -> str:
    verbs = search(tree, ["VB", "VBN", "VBD", "VBP", "VBZ", "VBG"])
    return str(verbs[-1])


#########################################


class Query(object):
    """ Base class to handle user query

    Parameters
    ----------
    data: str
        nltk `Tree` string representation of the query.
    """

    def __init__(self, data: str) -> None:
        self.data = nltk.tree.Tree.fromstring(data)

    def get_clean_tree(self) -> nltk.tree.Tree:
        """ Generates nltk Tree free from "useless" tokens
        """
        output: str = "(S"
        for child in self.data:
            if isinstance(child, nltk.tree.Tree):
                subtree: str
                if child.label() == "QSP":
                    subtree = str(child[1])
                else:
                    subtree = str(child)
                output += f" {subtree}"

        output += ")"
        # print(output)
        return nltk.tree.Tree.fromstring(output)

    def get_topic_terms(self, ling_units: List[str]) -> List[str]:
        """ TODO
        """
        return [
            " ".join([term.split("/")[0] for term in terms.split(" ")])
            for terms in search(self.get_clean_tree(), ling_units)
        ]

    def get_tokens(self, tags: List[str]) -> List[str]:
        """ Gets token associated to given tags in sequence tree.
        """
        if isinstance(tags, list):
            if len(tags) > 0:
                return search(self.data, tags)

        raise TypeError(
            f"tags argument should be of type list not {type(tags)}. ",
            "moreover len(tags) has to be > 0.",
        )

    def get_reduced_tree(self) -> nltk.tree.Tree:
        """ FIXME: should be more flexible.
        """
        output: str = "(S"
        for child in self.data:
            if isinstance(child, nltk.tree.Tree):
                subtree: str
                if child.label() == "QSP":
                    subtree = reduce_np(child[-1])
                    subtree += f" {reduce_vp(child[-1])}"
                elif child.label() == "NP":
                    subtree = reduce_np(child)
                elif child.label() == "VP":
                    subtree = reduce_vp(child)
                elif child.label() == "SP":
                    subtree = reduce_np(child)
                    subtree += f" {reduce_vp(child)}"
                elif child.label() == "GNP":
                    subtree = reduce_np(child[0])
                    subtree += f" {str(child[1])}"
                    subtree += f" {reduce_np(child[2])}"
                elif child.label() == "WH":
                    subtree = str(child[0])
                else:
                    subtree = str(child)
                output += f" {subtree}"

        output += ")"
        return nltk.tree.Tree.fromstring(output)

    def get_reduced(self) -> List[str]:
        """ TODO
        """
        return [leaf.split("/")[0] for leaf in self.get_reduced_tree().leaves()]

    def cos_similarity(self, other: "Query") -> float:
        content_self = self.get_reduced()
        content_other = other.get_reduced()

        return len(list(set(content_self) & set(content_other))) / len(
            set(content_other + content_self)
        )

    def align_similarity(self, other: "Query") -> int:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return self.data.__repr__()


class Question(Query):
    """ Class to handle user's query as a question.
    """

    def __init__(self, data: str) -> None:
        super().__init__(data)

    @property
    def qtype(self) -> str:
        """ FIXME: should handle multiple questions
        """
        wh_words = self.get_tokens(["WH"])
        if len(wh_words) > 0:
            return wh_words[0]
        else:
            return "yn"


class QSearch(object):
    """ Question Search class for identifying question topic and question focus
    using question dataset, and returns closest questions to a given one.

    Parameters
    ----------
    root: str, Path
        Path to the question database used as knowledge for identifying
        close questions to an user's question.

    transforms: qsearch.Preprocess
        Preprocessing functions for question data.
    """

    available_metrics = ["cosine"]

    def __init__(
        self,
        data: pd.DataFrame,
        linguistic_units: List[str] = ["NP", "VP"],
        transforms: Preprocess = Preprocess([Format()]),
    ) -> None:
        self.data = data
        self.transforms = transforms
        self.ling_units = linguistic_units
        grammar = r"""
            NP: {<[CDJN].*|PRP\$>+}         # Noun Phrase
            VP: {<VB.*>+}                   # Verb Phrase
            SP: {<NP|PRP>{1}<MD>?<VP>{1}}   # Subject Phrase
            WH: {<W.*>}                     # WH-word
            QSP: {<MD|VP><SP>}              # Subject Question Form
            GNP: {<NP><IN|TO><NP>}          # Noun Phrase Group
        """
        self.parser = RegexpParser(grammar)
        self.lemmatizer = Lemmatize()

        # self.compute_sequence_tree()
        # self.compute_topic_terms()

        self.categories = (
            self.data.groupby(["topic"])
            .size()
            .reset_index()
            .rename(columns={0: "count"})
        )

    def sequence_tree(self, query: str) -> str:
        return str(
            self.parser.parse(
                ne_chunk(
                    self.lemmatizer(
                        pos_tag(word_tokenize(self.transforms(query)))
                    ),
                    binary=True,
                )
            )
        ).replace("\n", "")

    def topic_terms(self, tree: str) -> List[str]:
        """ Extracts topic terms from question data.

        FIXME: `nltk.pos_tag` is not perfect and wrongly tags some words. A fix
        could be to use a different tagger or implement a new one, though
        none is perfect.
        """
        return Question(tree).get_topic_terms(self.ling_units)

    def compute_sequence_tree(self) -> None:
        """ Computes sequence tree for the whole dataset.
        """
        self.data["sequence_tree"] = self.data.apply(
            lambda row: self.sequence_tree(row["question"]), axis=1,
        )

    def compute_topic_terms(self) -> None:
        """ Extracts topic terms from all questions in the database.
        """
        self.data["topic_terms"] = self.data.apply(
            lambda row: ",".join(self.topic_terms(row["sequence_tree"])),
            axis=1,
        )

    def compute_qtype(self) -> None:
        """ Identifies question type for all question in the database.
        """
        self.data["qtype"] = self.data.apply(
            lambda row: Question(row["sequence_tree"]).qtype, axis=1,
        )

    def match(self, topic_term: str, qtopic_terms: List[str]) -> bool:
        for qtopic_term in qtopic_terms:
            if topic_term in qtopic_term:
                return True

        return False

    def topic_profile(self, topic_terms: List[str]) -> np.ndarray:
        """ Computes the topic profile for each topic term.

        Parameters
        ----------
        topic_terms: str-list

        Returns
        -------
        numpy.ndarray
            A matrix where each column is associated to a topic term, and each
            row to a category.

                |t1         |t2         |...|tn         |
            |c1 |p(c1|t1)   |p(c1|t2)   |...|p(c1|tn)   |
            |c2 |p(c2|t1)   |p(c2|t2)   |...|p(c2|tn)   |
            |...|...        |...        |...|...        |
            |cm |p(cm|t1)   |p(cm|t2)   |...|p(cm|tn)   |

        Definition
        ----------
        The topic profile `θ(t)` of a topic term `t` in a categorized question
        collection is a probability distribution of categories `{p(c|t)/c∈C}`
        where `C` is a set of categories.
        """
        output = np.zeros((len(self.categories), len(topic_terms),))
        tmp_data = self.data.copy()
        tmp_data["topic_terms"] = tmp_data.apply(
            lambda row: row["topic_terms"].split(","), axis=1,
        )
        for index, topic_term in enumerate(topic_terms):
            tmp_data[f"topic_term_{index}"] = tmp_data.topic_terms.apply(
                lambda qtopic_terms: 1
                if self.match(topic_term, qtopic_terms)
                else 0
            )

            topic_term_count = (
                tmp_data[["topic", f"topic_term_{index}"]]
                .groupby(["topic"])
                .mean()
                .reset_index()[f"topic_term_{index}"]
                .values
            )

            output[:, index] = (
                topic_term_count / np.sum(topic_term_count)
                if np.sum(topic_term_count) != 0
                else 1 / len(self.categories)
            )

        return output

    def predict_category(self, topic_profile: np.ndarray) -> np.ndarray:
        """ Predicts a category according to a topic profile.
        """
        return topic_profile.mean(axis=1)

    def specificity(
        self, topic_profile: np.ndarray, eps: float = 0.001
    ) -> np.ndarray:
        """ Computes the specificity according to topic profiles.

        Parameters
        ----------
        topic_profile: numpy.ndarray

        eps: float (default=0.001)
            Smoothing parameter used to cope with the topic terms whose
            entropy is 0.

        Definition
        ----------
        The specificity `s(t)` of a topic term `t` is the inverse of the
        entropy of the topic profile `θ(t)`.

        """
        return 1 / (
            -np.sum(
                np.array(
                    [
                        np.nan_to_num(
                            topic_profile[:, topic_term]
                            * np.log2(topic_profile[:, topic_term])
                        )
                        for topic_term in range(topic_profile.shape[1])
                    ]
                ),
                axis=1,
            )
            + eps
        )

    def topic_chain(
        self, topic_terms: List[str], specificities: np.ndarray
    ) -> List[str]:
        """ Returns the topic chain of a question according to its topic terms
        and their specificities.

        Parameters
        ----------
        topic_terms: str-list

        specificities: numpy.ndarray

        Definition
        ----------
        A topic chain `qc` of a question `q` is a sequence of ordered topic
        terms `t1` -> `t2` -> `...` -> `tm` such that

        * `ti` is included in `q`, `1`<=`i`<=`m`;

        * `s(tk)`>`s(tl)`, `1`<=`k`<`l`<=`m`.
        """
        chain = [
            term
            for _, term in sorted(
                zip(list(specificities), topic_terms), reverse=True
            )
        ]

        return chain

    def search(
        self, query: str, metric: str = "cosine", threshold: float = 0.3
    ):
        """ Searches from closest question given a question

        Returns
        -------
        np.ndarray
            Indexes of the questions with similarity higher than `threshold`.
        np.ndarray
            Similarity vector corresponding to the questions.
        np.ndarray
            Indexes of the questions with the highest similarity score.
        """
        assert (
            metric in self.available_metrics
        ), f"metric {metric} not available"

        # inits Question object
        tree = self.sequence_tree(query)
        question = Question(tree)
        # inits candidates
        candidates = self.data.copy()
        # predicts question category
        topic_terms = question.get_topic_terms(self.ling_units)

        # If no topic found return nothing
        if not len(topic_terms) > 0:
            return None, None, None

        topic_profile = self.topic_profile(topic_terms)
        preds = self.predict_category(topic_profile)
        # checks whether a topic is dominating
        if preds.std() > 0.05:
            category = self.categories["topic"].values[np.argmax(preds)]
            # gets all questions in database in the predicted category
            candidates = candidates[candidates["topic"] == category]

        # compute similarity
        if metric == "cosine":
            candidates["similarity"] = candidates.apply(
                lambda row: question.cos_similarity(
                    Question(row["sequence_tree"])
                ),
                axis=1,
            )
        # get question with similarity higher than the threshold
        candidates = candidates[candidates.similarity >= threshold]

        if len(candidates) > 0:
            scores = candidates.similarity.values
            idxs = candidates.index.values
            best_idxs = idxs[scores == np.max(scores)]

            # sort results according to similarity scores
            scores_inds = scores.argsort()
            sorted_idxs = idxs[scores_inds[::-1]]
            sorted_scores = scores[scores_inds[::-1]]

            return sorted_idxs, sorted_scores, best_idxs
        else:
            return None, None, None

    def test_predict(self) -> Tuple[float, np.ndarray]:
        """ Tests QSearch category prediction

        Returns
        -------
        float:
            Overall accuracy.
        numpy.ndarray:
            Accuracy for each category.
        """
        perf = np.zeros(len(self.categories))
        predictions = self.data.apply(
            lambda row: self.categories.topic.values[
                np.argmax(
                    self.predict_category(
                        self.topic_profile(row["topic_terms"].split(","))
                    )
                )
            ],
            axis=1,
        )

        for i in range(len(self.categories)):
            category = self.data.topic.values == self.categories.topic.values[i]
            perf[i] = (
                predictions[category] == self.data.topic.values[category]
            ).mean()

        return (
            (predictions.values == self.data.topic.values).mean(),
            perf,
        )

    def test_search(self) -> float:
        """ Tests QSearch search method
        Original question should be in the first 3 results.

        Returns
        -------
        float:
            Overall accuracy.
        """
        search_results = self.data.apply(
            lambda row: row.name in self.search(row["question"])[2], axis=1,
        )

        return search_results.values.mean()

    def update_data(self) -> None:
        """ Updates sequence_tree and topic terms columns.
        """
        self.compute_sequence_tree()
        self.compute_topic_terms()

    def save_data(self, path: Union[str, Path]) -> None:
        """ Saves data into a CSV file.
        """
        self.update_data()
        self.data.to_csv(path, index=False)

    def __repr__(self) -> str:
        return str(self.categories)
