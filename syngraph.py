import wn
import networkx as nx
from pyvis.network import Network
from textwrap import fill
from typing import Union

en = wn.Wordnet("oewn:2021")


def graph_synsets(terms: Union[list, str], pos: str = "v", depth: int = 0):

    G = nx.Graph(
        depth=depth,
    )

    def add_term_links(G: nx.Graph, term: str, current_depth: int):
        for syn in en.synsets(term):
            if syn.pos in pos:
                desc = fill(f"{syn.pos}, \n{syn.definition()}", width=25)
                G.add_node(desc, color="cornflowerblue")
                G.add_edge(term, desc)
                hyponyms = syn.hyponyms()
                hyponyms.append(syn)
                for child in hyponyms:
                    for word in child.words():
                        G.add_node(word.lemma(), color="darkseagreen")
                        G.add_edge(desc, word.lemma())

                        if current_depth < depth:
                            add_term_links(G, word.lemma(), current_depth + 1)

    for term in terms:
        add_term_links(G, term, 0)

    return G


def plot_graph(G: nx.Graph):
    net = Network(height="100%", width="100%")
    net.from_nx(G)
    net.show("ex.html")


if __name__ == "__main__":
    import argparse

    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="graph synonyms for a term",
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
        help="file to write figure",
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

    # run the graph computation
    try:
        G = graph_synsets(args.words, args.pos, args.depth)
        net = Network(height="100%", width="100%")
        net.from_nx(G)

        if args.outpath:
            net.show(args.outpath)
        else:
            net.show(f"output.html")

        print(nx.info(G))
    except Exception as e:
        parser.error(str(e))
