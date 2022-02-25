# Syngen

Syngen is a small program that generates synonyms for use in Forest bots and elsewhere. It uses the modern wordnet library [wn](https://github.com/goodmami/wn) under the hood.

There are two scripts in this repo. `syngen.py` will print a list of synonyms to stdout or to a file. `syngraph.py` will generate a graph visualization in HTML format and open it in a browser.

Both scripts take an argument for part of speech. This can be either a single type, like `v` or `n`, or a list, like `v,n,a`. 

Depth levels above 2 are not recommended, due to combinatorial explosion 😅 

## syngen.py

```
usage: syngen.py [-h] [-d DEPTH] [-o OUTPATH] [-p POS] words [words ...]

list synonyms for a term

positional arguments:
  words                 the words to graph synonyms for

optional arguments:
  -h, --help            show this help message and exit
  -d DEPTH, --depth DEPTH
                        depth to extend graph
  -o OUTPATH, --outpath OUTPATH
                        file to write results
  -p POS, --pos POS     part of speech of word(s)
```

## syngraph.py

```
usage: syngraph.py [-h] [-d DEPTH] [-o OUTPATH] [-p POS] words [words ...]

graph synonyms for a term

positional arguments:
  words                 the words to graph synonyms for

optional arguments:
  -h, --help            show this help message and exit
  -d DEPTH, --depth DEPTH
                        depth to extend graph
  -o OUTPATH, --outpath OUTPATH
                        file to write figure
  -p POS, --pos POS     part of speech of word(s)
  ```