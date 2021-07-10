import pdfrw
from pyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import fileinput
import img2pdf


# To get total no. of pages of a pdf

pages = len(pdfrw.PdfReader("pdf_document").pages)


# to split a pdf document into chunks

with open("pdf_file_name", 'rb') as file:

    reader = PdfFileReader(file, strict=False)
    file_counter = 1
    i = 0
    current_file_size = 0
    writer = PdfFileWriter()
    current_page_count = len(pdfrw.PdfReader("pdf_file_name").pages)
    while i < current_page_count:
        if current_file_size == 1000:
            file_name = f"some_file_name_{file_counter}"
            with open(file_name, 'wb') as pdf_output:
                writer.write(pdf_output)
            current_file_size = 0
            file_counter += 1
            writer = PdfFileWriter()

        writer.addPage(reader.getPage(i))
        i += 1
        current_file_size += 1

    file_name = f"some_file_name_{file_counter}"
    with open(file_name, 'wb') as pdf_output:
        writer.write(pdf_output)


# to write multiple chunks to single file
file_names = ["file_name_1", "file_name_3", "file_name_2"]
sorted_chunks = sorted(file_names, key=lambda x: x.split("_")[-1])

with open("big_file", 'wb') as bfile, fileinput.input(sorted_chunks) as cfile:

    for line in cfile:
        bfile.write(line)


# convert img to pdf

with open("file.pdf", 'wb') as pdf_file, open("img.jpg", 'r') as img:

    pdf_file.write(img2pdf(img))
