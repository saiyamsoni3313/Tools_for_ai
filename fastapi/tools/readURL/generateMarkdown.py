from tools.readURL.models import ContentURL, ReadURL
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import MarkdownifyTransformer
from tools.openAI import process_search_results, clean_text
from tools.readURL.utils import download_pdf_if_appropriate


def generateMarkdownForPage(data: ReadURL) -> ContentURL:
    try:
        info = {}
        scrape_from = []
        content = []
        summarized_content = []

        for url in data.urls:
            docs = download_pdf_if_appropriate(url)
            if docs is not None:
                info[url] = docs
            else:
                scrape_from.append(url)

        loader = AsyncHtmlLoader(scrape_from)
        docs = loader.load()

        md = MarkdownifyTransformer()
        converted_docs = md.transform_documents(docs)

        for i, docs in enumerate(converted_docs):
            info[scrape_from[i]] = docs.page_content

        for url in data.urls:
            content.append(info[url])

        if not data.summarize:
            return ContentURL(urls=data.urls, content=clean_text(content, False))

        for stuff in content:
            information = process_search_results(None, stuff, data.entities)
            summarized_content.append(information)

        return ContentURL(urls=data.urls, content=summarized_content)
    except Exception as e:
        return ContentURL(urls=[], content=["Error reading Webpage: {e}"])
