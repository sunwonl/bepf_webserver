from xhtml2pdf import pisa


def convertHtmlToPdf(sourceHtml, outputFilename):
    # open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
            sourceHtml,                # the HTML to convert
            dest=resultFile)           # file handle to recieve result

    # close output file
    resultFile.close()                 # close output file

    # return True on success and False on errors
    return pisaStatus.err


if __name__ == '__main__':
    source_html = ''
    with open('tmp.html', 'r', encoding='utf-8') as r:
        for l in r.readlines():
            source_html += l
    ofname = 'tmp.pdf'

