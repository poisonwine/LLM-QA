

import sys
import importlib
importlib.reload(sys)
import os
import re
from tqdm import tqdm
from langchain.docstore.document import Document
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfpage import PDFTextExtractionNotAllowed



path = './loader/test_file/'  #【设定pdf文件路径】
txt_save_path = './loader/test_file/tmp_files'  # 【设定保存TXT文件路径】


def parse(path, filename, txt_save_path):
    """
    功能：解析pdf 文本，保存到txt文件中
    path：pdf存放的文件夹路径
    filename: pdf文件名
    txt_save_path: 需要保存的txt文件夹路径

    """
    pdf_path = path + filename + '.pdf'
    fp = open(pdf_path, 'rb') # 以二进制读模式打开
    #用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument(parser=praser)
    # 连接分析器 与文档对象
    praser.set_document(doc)
    # doc.set_parser(praser)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    # doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page的内容
        for page in PDFPage.get_pages(fp=fp, pagenos=[i for i in range(50)], maxpages=50): # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    with open(txt_save_path+filename+'.txt', 'a+', encoding='utf-8') as f:
                        results = x.get_text()
                        print(results)
                        f.write(results + '\n')

from spliter.ChineseTextSplitter import ChineseTextSplitter


def extract_text_from_pdf(file_path: str):
    """Extract text content from a PDF file."""
    import PyPDF2
    contents = []
    text_spliter = ChineseTextSplitter(pdf=True, sentence_size=1024)
    from title_enhance import is_possible_title
    with open(file_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            page_text = page.extract_text().strip()
            raw_text = [text.strip() for text in page_text.splitlines() if text.strip()]
            new_text = ''

            for text in raw_text:
                # new_text += " "
                # if is_possible_title(text):
                #     pass
                text = re.sub(r'([;；!?。！？\?]["’”」』]{0,2})([^;；!?，。！？\?])', r'\1\n\2', text)
                new_text += text
                if text[-1] in ['.', '!', '?', '。', '！', '？', '…', ';', '；', ':', '：', '”', '’', '）', '】', '》', '」',
                                '』', '〕', '〉', '》', '〗', '〞', '〟', '»', '"', "'", ')', ']', '}']:
                    contents.append(new_text)
                    new_text = ''
            new_text = text_spliter.split_text1(new_text)
            if new_text:
                contents.append(new_text)
    return contents

if __name__ == '__main__':
    path = './loader/test_file/report.pdf'  # 【设定pdf文件路径】
    txt_save_path = './loader/test_file/tmp_files'  # 【设定保存TXT文件路径】
    # files = os.listdir(path)
    # for file in tqdm(files):
    #     filename = file.split('.')[0]
    # parse(path=path, filename='report', txt_save_path=txt_save_path)
    content = extract_text_from_pdf(path)
    folder_path = os.path.join(os.path.dirname(path), "tmp_files")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    fp = os.path.join(folder_path, 'load_file_pypdf.txt')
    from langchain.text_splitter import SpacyTextSplitter
    # text_splitter = SpacyTextSplitter(pipeline='zh_core_web_sm', chunk_size=1000, chunk_overlap=200)
    from modelscope.pipelines import pipeline
    # p = pipeline(
    #     task="document-segmentation",
    #     model='damo/nlp_bert_document-segmentation_chinese-base',
    #     device="cpu")

    # sent_list = [i for i in result["text"].split("\n\t") if i]
    with open(fp, 'w+', encoding='utf-8') as fout:
        # fout.write("filepath=%s,len=%s" % (filepath, len(docs)))
        print(len(content))
        for i in content:
            # texts = p(documents=str(i))
            # sent_list = [i for i in texts["text"].split("\n\t") if i]

            fout.write(str(i)+'\n')
        fout.close()
    #

    # print(content)