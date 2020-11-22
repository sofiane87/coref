import spacy
import neuralcoref
from spacy.matcher import Matcher


nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)


def match_tokens(doc, match_words):
    matcher = Matcher(nlp.vocab)
    for match_word in match_words:
        matcher.add("target_match", None, [{"TEXT": match_word}])

    for match in matcher(doc):
        yield match


def get_sentences(doc, match_words):
    for match in match_tokens(doc, match_words):
        m_token = doc[match[1]]
        if m_token._.in_coref:
            for c_cluster in m_token._.coref_clusters:
                for mention in c_cluster.mentions:
                    yield (mention.sent, mention, c_cluster)
        else:
            yield (m_token.sent, doc[match[1]:match[2]], None)
