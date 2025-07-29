import ollama
import pandas as pd
import json
import time
import re
from typing import Optional
from importlib import resources

__all__ = ['filter_literature', 'summarize_literature']


def _init_ai_model(model: str = 'gemma3:12b', prompt: Optional[str] = None, **kwargs):
    """Initialize the LLM model and return its response."""
    temperature = kwargs.get('temperature', 0)
    client = ollama.Client()

    try:
        response = client.generate(model=model,
                                   prompt=prompt,
                                   options={"temperature": temperature, "format": "json"})
        return response.response

    except Exception as e:
        print(f"LLM exception noted: {e}")
        return None


def _load_prompt(template_path: str):
    """Utility function to load a prompt from a .txt file."""
    with open(template_path, 'r') as f:
        return f.read()


def _build_prompt(df: pd.DataFrame, topic: str, mode: str, filter_by: str = 'titles', num_summary_points: int = 3,
                 custom_prompt_path: Optional[str] = None):
    """Builds the prompt for either filtering or summarizing articles."""
    entries = []
    for i, row in df.iterrows():
        content = row.title if filter_by == 'titles' else row.abstract
        entries.append(f"ARTICLE #{i}: {content}\n")

    joined_entries = "\n".join(entries)

    if custom_prompt_path:
        prompt = _load_prompt(custom_prompt_path)

    else:

        if mode == 'filter':
            with resources.files("pnt.AI_review_tools").joinpath("base_filter_prompt.txt").open('r', encoding='utf-8') as f:
                prompt = f.read()

        else:
            with resources.files("pnt.AI_review_tools").joinpath("base_summarize_prompt.txt").open('r', encoding='utf-8') as f:
                prompt = f.read()


    return prompt.format(topic=topic,
                         filter_by=filter_by,
                         num_summary_points=num_summary_points,
                         joined_entries=joined_entries)


def _process_articles_in_chunks(df: pd.DataFrame, process_request: str, model: str = 'gemma3:12b', chunk_size: int = 3,
                               topic: Optional[str] = None, filter_by: str = 'titles', num_summary_points: int = 3,
                               custom_prompt_path: Optional[str] = None):
    """Processes the DataFrame in chunks and sends them to the LLM."""
    assert process_request in ['filter', 'summarize'], "process_request must be 'filter' or 'summarize'"

    processed_result = []
    total_articles = len(df)
    chunks = [df[i:i + chunk_size] for i in range(0, total_articles, chunk_size)]
    print(f"\nTotal articles fetched: {total_articles}")
    print(f"Total chunks to process: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        start_idx, end_idx = i * chunk_size, min((i + 1) * chunk_size, total_articles)
        print(f"\nProcessing chunk {i + 1} of {len(chunks)} (Articles {start_idx + 1} to {end_idx})...")

        prompt = _build_prompt(chunk,
                               topic=topic,
                               mode=process_request,
                               filter_by=filter_by,
                               num_summary_points=num_summary_points,
                               custom_prompt_path=custom_prompt_path)

        result = _init_ai_model(prompt=prompt, model=model)

        if result:
            try:
                clean_result = re.sub(r"^```json|```$", "", result.strip())
                parsed = json.loads(clean_result)
                if isinstance(parsed, list):
                    processed_result.extend(parsed)

            except Exception as e:
                print(f"Failed to parse JSON from chunk {i + 1}: {e}\nRaw output:\n{result}")

        time.sleep(1)

    return processed_result


def summarize_literature(df: pd.DataFrame, summary_topic: str, **kwargs):
    """
    Function to summarize a chunked set of article abstracts using a local LLM via Ollama.
    Optionally, it can generate an overall summary across all chunk-level results.

    Arguments:
    - df (pd.DataFrame): A DataFrame containing article data. Must include a column named 'abstract'.

    - summary_topic (str): The main topic or question the summary should address.

    **kwargs:
    - chunk_size (int): Number of articles per LLM chunk (default: 5).

    - model (str): Ollama model name to use (default: 'gemma3:12b').

    - filter_by (str): Field to summarize ('abstracts' or 'titles', default: 'abstracts').

    - num_summary_points (int): Number of summary points per chunk (default: 3).

    - custom_prompt_path (str): Path to a custom prompt template file (optional).

    - provide_overall_summary (bool): If True, creates a final combined summary across all chunks.
    """

    processed_results = _process_articles_in_chunks(df=df,
                                                    process_request='summarize',
                                                    topic=summary_topic,
                                                    chunk_size=kwargs.get('chunk_size', 5),
                                                    model=kwargs.get('model', 'gemma3:12b'),
                                                    filter_by=kwargs.get('filter_by', 'abstracts'),
                                                    num_summary_points=kwargs.get('num_summary_points', 3),
                                                    custom_prompt_path=kwargs.get('custom_prompt_path'))

    if kwargs.get('provide_overall_summary', False):
        summary_points, supporting_articles = [], []
        for chunk in processed_results:
            summary_points.append(chunk.get('summary point'))
            supporting_articles.append(chunk.get('supporting articles'))

        entries = []
        for points, articles in zip(summary_points, supporting_articles):
            entries.append(f"Summary point: {points} (supporting articles: {articles})")

        joined_entries = '\n'.join(entries)

        with resources.files("pnt.AI_review_tools").joinpath("overall_summary_prompt.txt").open('r', encoding='utf-8') as f:
                prompt = f.read()
                
        prompt = prompt.format(joined_entries=joined_entries, topic=summary_topic)

        overall_summary_results = _init_ai_model(prompt=prompt, model=kwargs.get('model', 'gemma3:12b'))

        return overall_summary_results.replace("\\n", "\n")

    else:
        return processed_results


def filter_literature(df: pd.DataFrame, filter_topic: str, **kwargs):
    """
    Function to filters out articles deemed irrelevant to a defined literature topic using local LLMs.

    Arguments:
    - df (pd.DataFrame): A DataFrame of articles with a 'title' or 'abstract' column.

    - filter_topic (str): The topic or criteria to use for filtering relevance.

    **kwargs:
    - chunk_size (int): Number of articles to send in each LLM request (default: 5).
    - model (str): Name of the Ollama-compatible LLM to use (default: 'gemma3:12b').
    - filter_by (str): Column to evaluate ('titles' or 'abstracts', default: 'titles').
    - custom_prompt_path (str): Path to custom prompt file for filtering (optional).
    - write_outliers_to_csv (bool): If True, writes removed article indices and justifications to a .csv file.
    """

    processed_results = _process_articles_in_chunks(df=df,
                                                    process_request='filter',
                                                    topic=filter_topic,
                                                    chunk_size=kwargs.get('chunk_size', 5),
                                                    model=kwargs.get('model', 'gemma3:12b'),
                                                    filter_by=kwargs.get('filter_by', 'titles'),
                                                    custom_prompt_path=kwargs.get('custom_prompt_path'))

    removed_articles, justifications = [], []
    for chunk in processed_results:
        removed_articles.append(chunk.get('article_number'))
        justifications.append(chunk.get('justification'))

    if kwargs.get('write_outliers_to_csv', False):
        pd.DataFrame(zip(removed_articles, justifications),
                     columns=['removed_articles', 'justifications']).to_csv('articles_filtered_out.csv', index=False)

    return df[~df.index.isin(removed_articles)]
