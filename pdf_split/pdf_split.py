#!/usr/bin/env python3

from pathlib import Path
from sys import argv

from PyPDF4.pdf import PdfFileReader, PdfFileWriter


class PdfSplitter:
    def __init__(self, input_file: str):
        """
        Set input PDF file
        @param input_file: filename of the input PDF file
        """
        self.input_file = Path(input_file)
        self.output_directory: Path or None = None

        self.input_pdf = self.__open_pdf()

    def __open_pdf(self) -> PdfFileReader:
        """
        Open PDF as bytes
        @return: 'PdfFileReader' object
        """
        return PdfFileReader(open(self.input_file, mode="rb"))

    def split(self, output_directory: str or None) -> None:
        """
        Split PDF into separate PDFs, one file per page
        @param output_directory: output directory to save files
        @return: none
        """
        if not output_directory:
            output_directory = "results"
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(exist_ok=True, parents=True)

        pages = self.input_pdf.getNumPages()
        for page in range(pages):
            # FIXME: Library bug? Stream closes:
            #  https://www.reddit.com/r/learnpython/comments/58kdfj/pypdf2_pdffilewriter_has_no_attribute_stream/
            #  Currently fxd with this dirty re-open method, fine for me lol
            self.input_pdf = self.__open_pdf()
            output_pdf = PdfFileWriter()
            output_pdf.addPage(self.input_pdf.getPage(pageNumber=page))
            with open(
                self.output_directory / f"{self.input_file.stem}_{page}.pdf", mode="wb"
            ) as out_file:
                output_pdf.write(out_file)


if __name__ == "__main__":
    splitter = PdfSplitter(input_file=argv[1])
    splitter.split(output_directory=argv[2] if len(argv) >= 3 else None)
