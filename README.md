# MovieSearch

A minimal example how we can use RAG with LLMs to make a recommendation assistant based on specific parts of custom data instead of inserting all the data into context. The goal is to use the minimal dependecies, so we only use [SBERT](https://www.sbert.net/) as the embedding model, an huggingface transformers model (e.g. [Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct)), and Meta's [Faiss](https://github.com/facebookresearch/faiss) as the vector indexing library.

In this example, we use a small [CSV file](https://www.kaggle.com/datasets/inductiveanks/top-1000-imdb-movies-dataset) as our data for the top 1000 movies on IMDb. But feel free to modify the code/system prompt to use other data. Depending on the chosen embedding model the results can vary, and keep in mind the movie list is limited. Bigger LLMs have a quite broad knowledge of movies, so smaller ones would benefit more from a system like this. It is also much useful when applied to documents/data that is not in the training set of the LLM, for example, private documents.

I have only tested this using the Llama-3.1-8B-Instruct model, but you could try it on other LLMs supported by the transformers library. In theory you could run this only on the CPU, depending on the size of the LLM, but a GPU is definitely recommended.

## Usage examples

![Examples of using MovieSearch](examples.png)

## Instructions

Assuming you already have pytorch installed, install faiss, transformers and sentence-transformers:

```properties
python index.py --embedding_model [SBERT embedding model]
```

### Creating the vector index file

I already include a movie vector index in the data folder, but if you want to create a new one with other embedding model use:

```properties
python index.py --embedding_model [SBERT embedding model]
```

### Search

If you used all the default arguments, to search the movie(s) with a query just run:

```properties
python search.py
```

To change the LLM use the --assistant-model argument. Other arguments such as the number of neighbours to consider in k-NN are available, see --help.