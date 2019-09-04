import pdfkit



class CreatePDF(object):
	def __init__(self,html,values,pdf):
		self.html = html
		self.values = tuple(values)
		self.pdf = pdf


	def basicPDF(self):
		#read in the html file as a string
		file = open(self.html,'r')
		strHTML = file.read()
		file.close()
		print(strHTML)
		print(self.values)
		print(self.values[0])
		completeHTML = strHTML.format(*self.values)
		print(completeHTML)
		pdfkit.from_string(completeHTML,self.pdf)

	def scaleA4PDF(self):
		settings = {'page-size':'A4','dpi':400,'zoom':2}
		file = open(self.html,'r')
		strHTML = file.read()
		file.close()
		completeHTML = strHTML.format(*self.values)
		pdfkit.from_string(completeHTML,self.pdf,options=settings)

#list = ("X","y","z")
#pdf = basicPDF("test2.html",list,"out2.pdf")		
#pdf.createPDF()
