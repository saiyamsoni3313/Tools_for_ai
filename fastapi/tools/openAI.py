from retry import retry
from constants import MAX_CONTEXT_WINDOW, SUMMARIZE_MODEL, JSON_MODEL
import os
from openai import OpenAI
import re
from html import unescape
import json
from fastapi import HTTPException

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def summarizeOpenAI(query, text, entities):

    content = f"You are a helpful assistant. Write a concise summary of the following text in English: {text}."
    if query:
        content = f"You are a helpful assistant that summarizes the following text in English. The summary should be concise and accurate. Do not include any information that is not relevant to the query. If the text is not relevant to the query, return an empty string. The query is: {query}. The text is: {text}."

    if entities and entities != "":
        content = f"You are a helpful assistant. Write a concise summary of the following text in English: {text}. Data points to focus on while summarizing are {entities}. Ensure that the summary is accurate and provides a clear overview of the information presented in the original text."
        if query:
            content = f"You are a helpful assistant that summarizes the following text in English. The summary should be concise and accurate. Do not include any information that is not relevant to the query. If the text is not relevant to the query, return an empty string. Data points to focus on while summarizing are {entities}. Ensure that the summary is accurate and provides a clear overview of the information presented in the original text. The query is: {query}. The text is: {text}."
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": content}],
        model=SUMMARIZE_MODEL,
        temperature=0.7,
        max_tokens=500,
    )
    return response.choices[0].message.content


def split_text_into_chunks(text):
    # Split the text into manageable chunks without breaking sentences
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk + [word])) <= MAX_CONTEXT_WINDOW:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def clean_text(text, remove_images=True):
    try:
        # Strip HTML tags
        try:
            text = re.sub(r"<[^>]+>", "", text)
        except Exception as e:
            print(f"Error stripping HTML tags: {e}")

        # Convert HTML entities to their corresponding characters
        try:
            text = unescape(text)
        except Exception as e:
            print(f"Error unescaping HTML entities: {e}")

        # Remove image URLs
        if remove_images:
            try:
                text = re.sub(
                    r"https?://[\w\.-]+/\S+\.(jpg|jpeg|png|gif|bmp)(\?\S*)?", "", text
                )
            except Exception as e:
                print(f"Error removing image URLs: {e}")

        # Replace multiple spaces with a single space and trim leading/trailing spaces
        try:
            text = re.sub(r"\s+", " ", text).strip()
        except Exception as e:
            print(f"Error replacing multiple spaces: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return text


def process_search_results(query, parsed_content, entities=None):
    text_chunks = split_text_into_chunks(clean_text(parsed_content, True))
    summarized_content = ""
    for chunk in text_chunks:
        summary = summarizeOpenAI(query, chunk, entities)
        summarized_content += summary + " "
    if entities and entities != "":
        try:
            return jsonOpenAI(summarized_content, entities)
        except Exception as e:
            print(f"Error creating JSON: {e}")
            return HTTPException(status_code=500, detail="Error creating JSON")
    return summarized_content.strip()


@retry(tries=3, delay=2, backoff=2)
def jsonOpenAI(response, entities):
    print(f"Json OpenAI {response}")
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"Your task is to take the unstructured text provided and convert it into a well-organized table format using JSON. Keys in the JSON object should be {entities}. Extract the relevant information from the text and populate the corresponding values in the JSON object. Ensure that the data is accurately represented and properly formatted within the JSON structure. The resulting JSON table should provide a clear, structured overview of the information presented in the original text. Do not add any new keys.",
            },
            {
                "role": "user",
                "content": f"Do not respond in Markdown. The text is: {response}",
            },
        ],
        model=JSON_MODEL,
        temperature=0.7,
        max_tokens=500,
    )
    print("Json Response")
    print(response.choices[0].message.content)
    return str(json.loads(response.choices[0].message.content))
