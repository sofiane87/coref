import spacy
import neuralcoref
from spacy.matcher import Matcher


nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)


def split_sentence(sent):
    return [token.text for token in nlp.tokenizer(sent)]


def match_tokens(doc, match_sentences):
    matcher = Matcher(nlp.vocab)
    for match_sentence, case_sensitive in match_sentences:
        match_words = split_sentence(match_sentence)
        if case_sensitive:
            key = "TEXT"
        else:
            key = "LOWER"
        matcher.add("target_match", None, [{key: match_word} for match_word in match_words])

    for match in matcher(doc):
        yield match


def get_sentences(doc, match_sentences):
    for match in match_tokens(doc, match_sentences):
        m_token = doc[match[1]]
        if m_token._.in_coref:
            for c_cluster in m_token._.coref_clusters:
                for mention in c_cluster.mentions:
                    yield {"sentence": mention.sent,
                           "sentence_text": mention.sent.text.strip(),
                           "mention": mention,
                           "coref_cluster": c_cluster,
                           "mention_start": mention.start,
                           "mention_end": mention.end,
                           "sentence_start": mention.sent.start_char,
                           "sentence_end": mention.sent.end_char}
        else:
            yield {"sentence": m_token.sent,
                   "sentence_text": m_token.sent.text.strip(),
                   "mention": doc[match[1]:match[2]],
                   "coref_cluster": None,
                   "mention_start": m_token.idx,
                   "mention_end": m_token.idx + len(m_token.text),
                   "sentence_start": m_token.sent.start_char,
                   "sentence_end": m_token.sent.end_char}


if __name__ == "__main__":
    from pprint import PrettyPrinter
    doc = nlp(u"""Hey ! have you seen what John has done yesterday?
    Absolutely appaling that a managing director would behave like that ...
    Anyway, I have tried your recipee and it worked out great ! I think I will cook that often from now on !
    To get back to him, hopefully someone will ensure he's punished for his behaviour.""")

    pp = PrettyPrinter(indent=1)
    for match_sent in get_sentences(doc, [("John", True), ("managing director", False)]):
        pp.pprint(match_sent)
