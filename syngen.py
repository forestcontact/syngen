from urllib.parse import _ResultMixinStr
import wn
from textwrap import fill
from typing import Union

en = wn.Wordnet("oewn:2021")


def get_all_synonyms(terms: Union[list, str], pos: str = "v", depth: int = 0):
    results = {}  # type: dict

    def get_synonyms(results: dict, term: str, current_depth: int):
        for syn in en.synsets(term):
            if syn.pos in pos:
                desc = fill(f"❧ {syn.pos}, \n{syn.definition()}", width=80)
                results[desc] = set()
                hyponyms = syn.hyponyms()
                hyponyms.append(syn)
                for child in hyponyms:
                    for word in child.words():
                        results[desc].add(word.lemma())
                        if current_depth < depth:
                            get_synonyms(results, word.lemma(), current_depth + 1)

    if type(terms) is str:
        terms = [terms]

    for term in terms:
        get_synonyms(results, term, 0)

    return results


if __name__ == "__main__":
    import argparse

    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="list synonyms for a term",
    )

    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=0,
        help="depth to extend graph",
    )
    parser.add_argument(
        "-o",
        "--outpath",
        type=str,
        default=None,
        help="file to write results",
    )
    parser.add_argument(
        "-p",
        "--pos",
        type=str,
        default="v",
        help="part of speech of word(s)",
    )
    parser.add_argument(
        "words",
        nargs="+",
        help="the words to graph synonyms for",
    )

    # parse the arguments
    args = parser.parse_args()

    try:
        results = get_all_synonyms(args.words, args.pos, args.depth)
        str_results = {k: "\n".join(v) for k, v in results.items()}

        fmtd_results = "\n".join(["\n".join([k, v]) for k, v in str_results.items()])
        if args.outpath:
            with open(args.outpath, "w") as f:
                print(fmtd_results, file=f)
        else:
            print(fmtd_results)

    except Exception as e:
        parser.error(str(e))
