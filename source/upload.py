from langchain.document_loaders import (
    NotebookLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
import os

DATA_DIR = os.path.dirname(os.getcwd())
SOURCE_DIR = os.path.join(DATA_DIR, 'source')
CHROMA_PERSIST_DIR = os.path.join(DATA_DIR, "source/chroma-persist")
CHROMA_COLLECTION_NAME = "katalk-bot"

LOADER_DICT = {
    "py": TextLoader,
    "md": UnstructuredMarkdownLoader,
    "ipynb": NotebookLoader,
    'txt': TextLoader
}


def upload_embedding_from_file(file_path):
    loader = LOADER_DICT.get(file_path.split(".")[-1])
    if loader is None:
        raise ValueError("Not supported file type")
    documents = loader(file_path).load()

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    print(docs, end='\n\n\n')

    Chroma.from_documents(
        docs,
        OpenAIEmbeddings(),
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=CHROMA_PERSIST_DIR,
    )
    print(f'{file_path} db success')


def upload_embeddings_from_dir(dir_path):
    def _supported_extension(filename):
        return filename.split('.')[-1] in ['txt']

    failed_upload_files = []

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if _supported_extension(file):
                file_path = os.path.join(root, file)

                try:
                    upload_embedding_from_file(file_path)
                    print("SUCCESS: ", file_path)
                except Exception as e:
                    print("FAILED: ", file_path + f" by({e})")
                    failed_upload_files.append(file_path)


def upload_katalk_files(dir):
    # 실행시 OPENAI_API_KEY 환경변수에 키를 추가해 둘 것
    upload_embeddings_from_dir(dir)

def check_chroma():
    from pprint import pprint

    db = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=OpenAIEmbeddings(),
        collection_name=CHROMA_COLLECTION_NAME,
    )

    docs = db.similarity_search("소셜 API 기능소개")  # get_relevant_documents 와는 넘겨주는 형식만 좀 다름. ... 뭐가 다른진 잘 모르겠다??

    pprint(docs)

def main():
    # 한번만 돌리기
    #    upload_katalk_files(SOURCE_DIR)
    check_chroma()
    pass


if __name__ == '__main__':
    main()
