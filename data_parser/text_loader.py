from langchain.document_loaders import UnstructuredFileLoader, TextLoader, CSVLoader
from data_parser.loader.pdf_loader import UnstructuredPaddlePDFLoader
from langchain.document_loaders.pdf import PDFMinerLoader
from data_parser.spliter.ChineseTextSplitter import ChineseTextSplitter
import os

def load_file(name, filepath):
    if filepath.lower().endswith('.pdf'):
        if name == 'paddle':
            loader = UnstructuredPaddlePDFLoader(filepath, mode="elements")
        elif name == 'pdfminer':
            loader = PDFMinerLoader(file_path=filepath)

        textsplitter = ChineseTextSplitter(pdf=True, sentence_size=1000)

        docs = loader.load_and_split(textsplitter)


    write_check_file(name, filepath, docs)
    # print(docs)
    return docs


def write_check_file(name, filepath, docs):
    folder_path = os.path.join(os.path.dirname(filepath), "tmp_files")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    fp = os.path.join(folder_path, 'load_file_'+ name+'.txt')
    with open(fp, 'w', encoding='utf-8') as fout:
        # fout.write("filepath=%s,len=%s" % (filepath, len(docs)))
        # fout.write('\n')
        for i in docs:
            fout.write(str(i))
            fout.write('\n')
        fout.close()


if __name__ == '__main__':
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loader/test_file", "report.pdf")
    print(filepath)
    docs = load_file(filepath=filepath, name='paddle')

    # print(docs)