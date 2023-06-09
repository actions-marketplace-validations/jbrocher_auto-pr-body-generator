import nltk

nltk.download("punkt")
from nltk.tokenize import word_tokenize


class PromptsAreNotEmpty(Exception):
    pass


class PromptGenerator:
    MAX_TOKENS = 500
    DEFAULT_PROMPT = """ 
        Generate a body in markdown for a Python github pull request. The PR must contain
        a quick sumarry of the changes, as well as element the reviewer should pay attention to. The body must be based off the following git diff:  
    """

    def __init__(self, diff_file: str):
        self.diff_file = diff_file
        self._prompts = []

    def clear(self):
        self._prompts = []

    @property
    def prompts(self):
        return self._prompts

    def generate_prompts(self, max_tokens=None, force=False):
        if len(self._prompts) > 0 and not force:
            raise PromptsAreNotEmpty(
                "Prompts have already be generated, call clear() first or sue force=True"
            )
        self.clear()

        # The default prompt is included in the max token limit
        prompt_tokens = len(word_tokenize(self.DEFAULT_PROMPT))
        max_tokens = (
            self.MAX_TOKENS - prompt_tokens
            if max_tokens is None
            else max_tokens - prompt_tokens
        )

        with open(self.diff_file, "r") as f:
            text = f.read()
            words = word_tokenize(text)
            for i in range(0, len(words), max_tokens):
                partial_diff = " ".join(words[i : i + max_tokens])
                prompt = f"{self.DEFAULT_PROMPT}{partial_diff}"
                self._prompts.append(prompt)
        return self._prompts
