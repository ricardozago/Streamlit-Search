from collections import Counter
import pandas as pd


def count_ocurrences(sentence):
    result = dict(Counter(sentence.split(" ")))

    df = pd.DataFrame(result.items(), columns=["palavra", "contagem"]).sort_values(
        "contagem", ascending=False
    )

    df["len"] = df["palavra"].apply(len)

    df = df.query("len>3")

    return df[:5]["palavra"].tolist()
