#!/usr/bin/python
# vim: set fileencoding=utf-8 :
 
#
# Fichier: col-1-and-3.py
#
 
import csv

#On retire les virgule des décimals par des points pour ne pas posé de problèmes avec le séparateur
def comma_to_Point(string):
    string2 = string.replace(',','.')
    return string2

def file_exists(fichier):
   try:
      file(fichier)
      return True
   except:
      return False
      
#Créer un nouveau fichier csv avec les entêtes pour chacun des attributs
def create_New_CSV(nomFichierCSV):
    entetes = [
     u'File_Name_Nifti',
     u'Surgeon_ID',
     u'Patient_ID',
     u'Localisation',
     u'Point_Name',
     u'Type_Of_Answer',
     u'X',
     u'Y',
     u'Z',
     u'Intensity'
    ]

    f = open(nomFichierCSV, 'w')
    ligneEntete = ",".join(entetes) + "\n"
    f.write(ligneEntete)
    
    print '\"'+nomFichierCSV+'\" has been created'
    f.close()

#Ajoute un point dans un csv uniquement si celui ci n'existe pas déja
def add_Point(nomFichierCSV,attributs):
    file = open(nomFichierCSV, 'a+')
    exist = False
    try:
        reader = csv.reader(file)
        for ligne in reader:
            if ligne:
                #On discrimine sur l'ID_Chirurgien, l'ID_patient et le nom du point
                if ligne[1]==attributs[1] and ligne[2]==attributs[2] and ligne[4]==attributs[4]:
                    exist = True
        if exist==False:
            item = ",".join(attributs) + "\n"
            file.write(item)
    finally:
        file.close()
 
#Remplit le csv à partir du csv donné par le Dr.Reich 
def generate_CSV_point_data_file(nomFichierCSV,newCSV):
    create_New_CSV(newCSV)
    file = open(nomFichierCSV, "rb")   
    try:
        reader = csv.reader(file)
        index = 0
        ID_patient_tampon = -1
        for ligne in reader:
            if index>0:
                if ligne:
                    if ligne[0]!='':
                        ID_patient_tampon = ligne[0]
                    attributs = ['NULL','NULL',ID_patient_tampon,ligne[5],ligne[2],ligne[6],ligne[8],ligne[9],ligne[10],comma_to_Point(ligne[3])]
                    add_Point(newCSV,attributs)
            else:
                index=index+1
                                 
    finally:
        file.close()
        
#Fait la fusion de deux csv que l'on place dans un troisieme csv résultant
def merge_CSV(csv_1,csv_2):
    file = open(csv_2, "rb") 
    try:
        reader = csv.reader(file)
        for ligne in reader:
            add_Point(csv_1,ligne)
    finally:
        file.close()
    print('\"'+csv_2+'\" has been merged with the file \"'+csv_1+'\"')
    
#Fusion d'une liste de fichier CSV    
def merge_multiple_CSV(output_CSV,list_CSV):
    if file_exists(output_CSV)==False:
        create_New_CSV(output_CSV)
    for file in list_CSV:
        merge_CSV(output_CSV,file)
    

generate_CSV_point_data_file('data_CHRU.csv','template_data.csv')
merge_multiple_CSV('csv_merged.csv',['file1.csv','file2.csv','file3.csv'])
