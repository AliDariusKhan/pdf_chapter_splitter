from collections import OrderedDict
from PyPDF2 import PdfFileReader, PdfFileWriter

file_pdf = PdfFileReader('file.pdf')
file_destinations = file_pdf.getOutlines()

def get_chapters(file_pdf, 
                 file_destinations, 
                 depth=float('inf'),
                 prev_chap_start=0, 
                 prev_chap_title='Front',  
                 indentation=0):
    chapters = OrderedDict()
    total_page_no = file_pdf.getNumPages()
    for destination in file_destinations:
        if type(destination) == PyPDF2.generic.Destination:
            chap_start = file_pdf.getDestinationPageNumber(destination)
            chapters[prev_chap_title] = range(prev_chap_start, chap_start)            
            prev_chap_start = chap_start
            prev_chap_title = ''.join([char for char in destination.title
                                       if ord(char) < 128 and char != '/'])
        elif indentation < depth:
            new_chapters, prev_chap_start, prev_chap_title = get_chapters(file_pdf, 
                                                                          destination, 
                                                                          depth,
                                                                          prev_chap_start, 
                                                                          prev_chap_title,
                                                                          indentation + 1)
            
            chapters.update(new_chapters)
    chapters[prev_chap_title] = range(prev_chap_start, total_page_no)
    return chapters, prev_chap_start, prev_chap_title

chapters, _, _ = get_chapters(file_pdf, file_destinations)

def write_chapters(file_pdf, files_output, chapters):
    writer = PdfFileWriter()
    for chap_title, page_range in chapters.items():
        for page_no in page_range:
            writer.addPage(file_pdf.getPage(page_no))
        with open(chap_title + '.pdf', 'wb') as output_chap:
            writer.write(output_chap)
        writer = PdfFileWriter()

write_chapters(file_pdf, files_output, chapters)
