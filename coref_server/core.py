import spacy
import neuralcoref
from spacy.matcher import Matcher


nlp = spacy.load('en_core_web_lg')
neuralcoref.add_to_pipe(nlp, blacklist=False)


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


def get_sentences(text, match_sentences):
    doc = nlp(text)
    sentences = {}
    for match in match_tokens(doc, match_sentences):
        m_token = doc[match[1]]
        if m_token._.in_coref:
            for c_cluster in m_token._.coref_clusters:
                for mention in c_cluster.mentions:
                    sent_span = mention.sent.start_char, mention.sent.end_char
                    if sent_span not in sentences:
                        sentences[sent_span] = {
                            "sent": mention.sent,
                            "sent_text": mention.sent.text,
                            "coref_cluster": c_cluster,
                            "sent_span": sent_span,
                            "mentions": [(mention, mention.start_char, mention.end_char)]

                        }
                    else:
                        sentences[sent_span]["coref_cluster"] = c_cluster
                        sentences[sent_span]["mentions"].append((mention, mention.start_char, mention.end_char))

        else:
            sent_span = m_token.sent.start_char, m_token.sent.end_char
            if sent_span not in sentences:
                sentences[sent_span] = {
                    "sent": m_token.sent,
                    "sent_text": m_token.sent.text,
                    "coref_cluster": None,
                    "sent_span": sent_span,
                    "mentions": [(m_token, m_token.idx, m_token.idx + len(m_token))]

                }
            else:
                sentences[sent_span]["mentions"].append((m_token, m_token.idx, m_token.idx + len(m_token)))

    return [sentences[span] for span in sorted(sentences.keys())]


if __name__ == "__main__":
    from pprint import PrettyPrinter
    doc = u"""Hey ! have you seen what John has done yesterday?
    Absolutely appaling that a managing director would behave like that ...
    Anyway, I have tried your recipee and it worked out great ! I think I will cook that often from now on !
    To get back to him, hopefully someone will ensure he's punished for his behaviour."""

    pp = PrettyPrinter(indent=1)
    for match_sent in get_sentences(doc, [("John", True), ("managing director", False)]):
        pp.pprint(match_sent)
