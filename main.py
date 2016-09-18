import urllib2, random, threading, re

caracteresPossibles = map(chr, range(48, 58)) + map(chr, range(65, 91)) + map(chr, range(97, 123))
threads = []
outputHTML = open("sortie.html", "w")
outputHTML.write("<html><body><center>")

lock = False

class imgurRandGenerator(threading.Thread):
	nombre = 0
	def __init__ (self, nbIterations):
		threading.Thread.__init__(self)
		self.nbIterations = nbIterations
		

	def genererNom(self):
		nom = ""
		for i in range(0, random.randint(5, 7)):
			nom += caracteresPossibles[random.randint(0, 61)]
		return nom
	
	def run(self):
		global lock
		for i in range(0, self.nbIterations):
			nomFichier = self.genererNom() + ".jpg"
			url = "http://i.imgur.com/" + nomFichier
			imgurRandGenerator.nombre += 1
			try:
				image = urllib2.urlopen(url, timeout=2)
				imageContenu = image.read()
			except:
				print "Erreur : " + url + "        Nombre : " + str(imgurRandGenerator.nombre)
				continue
			if re.search("^.*removed.png$", image.geturl()) == None and imageContenu[:2] != "<!":
				print "TROUVE : " + image.geturl()
				
				lock = True
				outputHTML.write("<img style='max-width:900px; max-height:900px;' src='" + image.geturl() + "' /><br>\n")
				lock = False
				"""
				fichierImage = open(nomFichier, "wb")
				fichierImage.write(imageContenu)
				fichierImage.close()
				"""


for num in range(0, 20):
	thread = imgurRandGenerator(10)
	thread.start()
	threads.append(thread)
	print num, 

print ""
for thread in threads:
	thread.join()
	
outputHTML.write("</center></body></html>")
outputHTML.close()