import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
#lets makes some Class's

#python 2.x
class Email(object):
	#initialise the instance
	def __init__(self,txEmail,rxEmail,password,subject):
		self.txEmail = txEmail
		self.rxEmail = rxEmail
		self.port = 465 # FOR SSL
		self.password = password
		self.subject = subject
		self.emailServer = "smtp.gmail.com"
		self.message = MIMEMultipart("alternative")

	def testMethod(self):
		print("TX EMAIL: " + self.txEmail)

	def defineBasicMessage(self, message):
		self.message = message

	#send a simple text based email
	def sendBasicEmail(self):
		context = ssl.create_default_context()
		
		with smtplib.SMTP_SSL(self.emailServer, self.port, context = context) as server:
			server.login(self.txEmail, self.password)
			server.sendmail(self.txEmail, self.rxEmail, self.message)

	#define the plain text used as a backup in the advanced HTML email
	def defineAdvancedEmailPlain(self, plainText):
		self.plainText = plainText
		plainPart = MIMEText(self.plainText, "plain")
		self.message.attach(plainPart)

	#pass the html file to the object to be sent in the email
	def HTMLfile(self,htmlFile):
		fp = open(htmlFile,'r')
		self.html = fp.read()
		fp.close()
		
		HTMLPart = MIMEText(self.html, "html")
		self.message.attach(HTMLPart)
		print("attached HTML")

	def HTMLfileWithVariables(self,htmlFile,values):
		fp = open(htmlFile)
		strHTML = fp.read()
		fp.close()
		completeHTML = strHTML.format(*values)
		HTMLPart = MIMEText(completeHTML, "html")
		self.message.attach(HTMLPart)
		print("attached HTML with values")

	def htmlAddImage(self,imageLocation,imageName):
		fp = open(imageLocation, 'rb')
		imageData = fp.read()
		fp.close()

		image = MIMEImage(imageData)
		image.add_header('Content-ID','<{}>'.format(imageName))
		self.message.attach(image)

	def sendHTMLEmail(self):
		#message = MIMEMultipart("alternative")
		self.message["Subject"] = self.subject
		self.message["From"] = self.txEmail
		self.message["To"] = self.rxEmail	
	
		#Turn plain/html into MIMETEXT objects
		#print(self.html)
		#part1 = MIMEText(self.plainText, "plain")
		#part2 = MIMEText(self.html, "html")

		#ADD HTML/Plain-tect parts to the MIMEMultipart message
		#message.attach(part1)
		#message.attach(part2)

		context = ssl.create_default_context()
		with smtplib.SMTP_SSL(self.emailServer,self.port,context=context) as server:
			server.login(self.txEmail, self.password)
			server.sendmail(self.txEmail,self.rxEmail,self.message.as_string())

	def addAttachment(self, fileName, fileLocation):
		with open(fileLocation, "rb") as attachment:
			#add file as application/octet-stream
			attachPart = MIMEBase("application","octet-stream")
			attachPart.set_payload(attachment.read())

		encoders.encode_base64(attachPart)
		attachPart.add_header("Content-Disposition","attachment; filename= {}".format(fileName)) 
		self.message.attach(attachPart)


#Testing Code

#basicEmail = Email("freezertemperaturemonitor@gmail.com","arlw87@googlemail.com","t3mpeR@tur3","Basic Email")
#basicEmail.defineBasicMessage("This is a basic email test")
#print(basicEmail.message)
#basicEmail.sendBasicEmail()


#send a more advanced email
#print("Send a more addvanced email.....")
#advancedEmail = Email("freezertemperaturemonitor@gmail.com","arlw87@googlemail.com","t3mpeR@tur3","Advanced Email")
#advancedEmail.defineAdvancedEmailPlain("Plain Text for if the HTML email doesnt work")
#advancedEmail.HTMLfile("test.html")
#advancedEmail.addAttachment("test.pdf")
#advancedEmail.sendHTMLEmail()



