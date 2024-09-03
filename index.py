import argparse 
import faiss  

from sentence_transformers import SentenceTransformer
from common import parse_csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create vector index of top 1000 movies using a sequence transformer as the embedding model")

    parser.add_argument('--device', type=str, default='cuda',choices=['cuda', 'cpu'], help='Device to use, either "cuda" or "cpu". Default is "cuda".')
    parser.add_argument('--csv-path', type=str, default='imdb_top_1000.csv', help='Path to the CSV movie file. Default is "imdb_top_1000.csv".')
    parser.add_argument('--embedding_model', type=str, default='all-MiniLM-L6-v2', help='Sequence transformer model to use. Default is "all-MiniLM-L6-v2".')
    parser.add_argument('--index-name', type=str, default='movies.index', help='Name of the saved index file.')

    args = parser.parse_args()

    lines = parse_csv(args.csv_path) 

    embedding_model = SentenceTransformer(args.embedding_model, device=args.device)

    index = faiss.IndexFlatL2(embedding_model.get_sentence_embedding_dimension())

    embeddings = embedding_model.encode(lines)

    index.add(embeddings)

    faiss.write_index(index, args.index_name)
