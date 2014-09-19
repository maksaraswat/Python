#!/usr/bin/python

from pyPdf import PdfFileWriter, PdfFileReader
import string, optparse, os, sys

# This function extracts a page from the pdf and creates an 
# output pdf file
def pageextract(document,pagenum,outfile):
	infile = PdfFileReader(open(document, "rb"))	
	pagetoextract = int(pagenum)	
	output = PdfFileWriter()
	output.addPage(infile.getPage(pagetoextract))
	outputStream = open(outfile, 'wb')
	output.write(outputStream)
	outputStream.close()

# This function removes a page and attaches another page
# at the same location provided by user. Function  
# addresses 2 cases where input file has multiple pages 
# and input file has only 1 page.If page to attach more 
# than one page then first page is attached.

def pageattach(document,document2,pagenum,outfile):
	infile1 = PdfFileReader(open(document, "rb"))
	infile2 = PdfFileReader(open(document2, "rb"))
	PagesDoc1 = infile1.getNumPages()
	output = PdfFileWriter()
	outputStream = open(outfile, 'wb')	

	if PagesDoc1 > 1:                               # If input file has multiple pages and page to attach has only 1 page
		x = 0	
		while x < PagesDoc1:
			if x < pagenum or x > pagenum:		
				output.addPage(infile1.getPage(x))
				output.write(outputStream)		
			else:
				output.addPage(infile2.getPage(0))
				output.write(outputStream)
			x = x+1
	if PagesDoc1 == 1:				# If input file has only 1 page  	
		if pagenum < PagesDoc1:
			output.addPage(infile2.getPage(0))	
			output.addPage(infile1.getPage(0))
		else:
			output.addPage(infile1.getPage(0))	
			output.addPage(infile2.getPage(0))	
		output.write(outputStream)	
	outputStream.close()

def main():
	try:
		parser = optparse.OptionParser('usage: ' + sys.argv[0] + ' -h for help')
		parser.add_option('-E', dest='document', help='specify <input file> <page to extract> <output file>')	
		parser.add_option('-R', dest='document', help='specify <input file> <page to attach> <page position> <output file>')	
		(options, args) = parser.parse_args()
		document=options.document
		if options.document !=None:
			if sys.argv[1] == '-E':			
				pageextract(document,sys.argv[3], sys.argv[4])
			if sys.argv[1] == '-R':		
				pageattach(document,sys.argv[3],int(sys.argv[4]),sys.argv[5])
		else:
			print parser.usage

	except Exception as e:
		print e


if __name__ == '__main__':
	main()
