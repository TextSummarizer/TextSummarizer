import summarizer

s = summarizer.Summarizer(
    model_path="C:/Users/Gianni Mastroscianni/Desktop/Magistrale/Accesso Intelligente all'Informazione ed Elaborazione del Linguaggio Naturale/Progetto/word2vec_models/enwiki_20161220_skip_300.bin",
    regex=True)

s.set_redundancy_threshold(0.95)
s.set_tfidf_threshold(0.2)
summary = s.summarize(
    "Pearl Jam is an American rock band formed in Seattle, Washington, in 1990. Since its inception, the band's line-up has comprised Eddie Vedder (lead vocals), Mike McCready (lead guitar), Stone Gossard (rhythm guitar) and Jeff Ament (bass). The band's fifth member is drummer Matt Cameron (also of Soundgarden), who has been with the band since 1998. Boom Gaspar (piano) has also been a session/touring member with the band since 2002. Drummers Dave Krusen, Matt Chamberlain, Dave Abbruzzese and Jack Irons are former members of the band. Formed after the demise of Gossard and Ament's previous band, Mother Love Bone, Pearl Jam broke into the mainstream with its debut album, Ten, in 1991. One of the key bands in the grunge movement of the early 1990s, over the course of the band's career, its members became noted for their refusal to adhere to traditional music industry practices, including refusing to make proper music videos or give interviews, and engaging in a much-publicized boycott of Ticketmaster. In 2006, Rolling Stone described the band as having \"spent much of the past decade deliberately tearing apart their own fame.\" To date, the band has sold nearly 32 million records in the United States and an estimated 60 million worldwide. Pearl Jam has outlasted and outsold many of its contemporaries from the alternative rock breakthrough of the early 1990s, and is considered one of the most influential bands of that decade. Stephen Thomas Erlewine of AllMusic referred to Pearl Jam as \"the most popular American rock & roll band of the '90s\". Pearl Jam were inducted into the Rock and Roll Hall of Fame on April 7, 2017, in their first year of eligibility.",
    150)

print summary