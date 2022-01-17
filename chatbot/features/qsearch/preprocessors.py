import nltk
nltk.download('omw-1.4')
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re
import string

from typing import Callable, List, Tuple


class Format(object):
    def __call__(self, input_) -> str:
        """ Applies transformations to a provided string.
        """
        output = input_.lower()
        # keep uppercase for personal pronoun "I"
        output = re.sub(r"^i | i ", " I ", output)
        output = re.sub(r"'[a-z]", "", output)
        # remove punctuation
        output = output.translate(str.maketrans("", "", string.punctuation))
        # remove leading and trailing whitespaces
        output = " ".join([word for word in output.split(" ") if word != ""])

        return output


class Lemmatize(object):
    def __init__(self) -> None:
        self.wnl = WordNetLemmatizer()

    def nltk_tag_to_wordnet_tag(self, nltk_tag):
        """ Converts nltk tag to wordnet tag
        """
        if nltk_tag.startswith("J"):
            return wordnet.ADJ
        elif nltk_tag.startswith("V"):
            return wordnet.VERB
        elif nltk_tag.startswith("N"):
            return wordnet.NOUN
        elif nltk_tag.startswith("R"):
            return wordnet.ADV
        else:
            return None

    def __call__(self, content: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        return [
            (self.wnl.lemmatize(token, self.nltk_tag_to_wordnet_tag(tag)), tag)
            if self.nltk_tag_to_wordnet_tag(tag) is not None
            else (token, tag)
            for token, tag in content
        ]


class Preprocess(object):
    def __init__(self, transforms: List[Callable[[str], str]]) -> None:
        self.transforms = transforms

    def __call__(self, input_: str) -> str:
        for transform in self.transforms:
            input_ = transform(input_)

        return input_


class StopwordDestroyer(object):
    def __init__(self, stopwords):
        self.stopwords = stopwords

    def __call__(self, content):
        return " ".join(
            [t for t in word_tokenize(content) if t not in self.stopwords]
        )
