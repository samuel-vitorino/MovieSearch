import argparse
import os
import torch
import transformers
import faiss

from sentence_transformers import SentenceTransformer
from common import parse_csv, print_logo

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create vector index of top 1000 movies using a sequence transformer as the embedding model")

    parser.add_argument('--device', type=str, default='cuda',choices=['cuda', 'cpu'], help='Device to use, either "cuda" or "cpu". Default is "cuda".')
    parser.add_argument('--csv-path', type=str, default='data/imdb_top_1000.csv', help='Path to the CSV movie file. Default is "imdb_top_1000.csv".')
    parser.add_argument('--assistant-model', type=str, default='meta-llama/Meta-Llama-3.1-8B-Instruct', help='Sequence transformer model to use. Default is "all-MiniLM-L6-v2".')
    parser.add_argument('--embedding-model', type=str, default='all-MiniLM-L6-v2', help='Sequence transformer model to use. Default is "all-MiniLM-L6-v2".')
    parser.add_argument('--index-name', type=str, default='data/movies.index', help='Name of the saved index file. Default is movies.index')
    parser.add_argument('--k', type=int, default=5, help='Nearest neighbours to use. Default is 5')
    parser.add_argument('--max-output-tokens', type=int, default=4096, help='Max output tokens by the assistant model. Default is 4096')

    args = parser.parse_args()

    print("Loading assistant model...")

    pipeline = transformers.pipeline(
        "text-generation",
        model=args.assistant_model,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map=args.device,
    )
    
    print("Loading embedding model...")

    embedding_model = SentenceTransformer(args.embedding_model, device=args.device)
    
    print("Loading index...")

    index = faiss.read_index(args.index_name)
    lines = parse_csv(args.csv_path) 

    print_logo()

    prompt = input("Type your search query: ")

    distances, indices = index.search(embedding_model.encode([prompt]), k=args.k)

    system_prompt = "You are a movie/shows recommendation assistant. Respond to the user query using only the following movie information, " \
                    "if you don't find anything related to the user query in the information, say so, but don't add new information. Movie Data: \n."

    for i in indices[0]:
        system_prompt += f"{lines[i]}\n"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    outputs = pipeline(
        messages,
        max_new_tokens=args.max_output_tokens,
        pad_token_id=pipeline.tokenizer.eos_token_id
    )

    print(f'\n{outputs[0]["generated_text"][-1]["content"]}\n')

