def format_sentence(sent):
    sent_text = sent["sent_text"]
    sent_start, _ = sent["sent_span"]
    fmt_text = str(sent_text)
    for mention_text, mention_start, mention_end in sorted(sent["mentions"], key=lambda x: x[1], reverse=True):
        mention_start, mention_end = mention_start - sent_start, mention_end - sent_start
        fmt_text = fmt_text[:mention_start] + f"<b>{mention_text}</b>" + fmt_text[mention_end:]

    return f'<span class="selected_sentence">{fmt_text}</span>'


def format_text(text, sentences):
    fmt_text = str(text)
    for sent in sentences[::-1]:
        sent_start, sent_end = sent["sent_span"]
        fmt_text = fmt_text[:sent_start] + format_sentence(sent) + fmt_text[sent_end:]

    return fmt_text.replace("\n", "<br>")
