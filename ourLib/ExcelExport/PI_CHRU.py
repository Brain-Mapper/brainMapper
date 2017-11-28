#!/usr/bin/python
# vim: set fileencoding=utf-8 :
 
#
# Fichier: col-1-and-3.py
#
 
import csv

#On créer un nouveau fichier csv avec les entêtes pour chacun des attributs
def create_New_CSV(nomFichierCSV):
    entetes = [
     u'nom_Fichier_Nifti',
     u'ID_Chirurgien',
     u'ID_Patient',
     u'Localisation',
     u'Type_De_Reponse',
     u'X',
     u'Y',
     u'Z',
     u'Intensite'
    ]

    f = open(nomFichierCSV, 'w')
    ligneEntete = ";".join(entetes) + "\n"
    f.write(ligneEntete)
    
    print '\nfichier créer avec succès !\n'
    f.close()

#On ajoute un point dans le jeu de données représenté par le csv
def add_Point(nomFichierCSV,nom_Fichier_Nifti,ID_Chirurgien,ID_Patient,Localisation,Type_De_Reponse,X,Y,Z,Intensite):
    
    attributs = [nom_Fichier_Nifti,ID_Chirurgien,ID_Patient,Localisation,Type_De_Reponse,X,Y,Z,Intensite]    
    f = open(nomFichierCSV, 'a')
    item = ";".join(attributs) + "\n"
    f.write(item)
    f.close()
    #print 'ajout de l\'item [' + nom_Fichier_Nifti +','+ID_Chirurgien+','+ID_Patient+','+Type_De_Reponse+","+Localisation+','+X+','+Y+','+Z+','+Intensite + ']\n' 
 
#On remplit le csv à partir du csv donné par le Dr.Reich 
def generate_CSV_point_data_file(nomFichierCSV,newCSV):
    create_New_CSV(newCSV)
    file = open(nomFichierCSV, "rb")   
    try:
        reader = csv.reader(file)
        index = 0
        create_New_CSV
        ID_patient_tampon = -1
        for ligne in reader:
            if index>0:
                if ligne:
                    if ligne[0]!='':
                        ID_patient_tampon = ligne[0]
                    add_Point(newCSV,'NULL','NULL',ID_patient_tampon,ligne[5],ligne[6],ligne[8],ligne[9],ligne[10],ligne[3])
            else:
                index=index+1
                                 
    finally:
        file.close()
        
        
def merge_CSV(csv_1,csv_2):
    file1 = open(csv_1, "rb") 
    file2 = open(csv_2, "rb")   

    try:
        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)
        i1=0
        i2=0
        for ligne1 in reader1:
            if ligne1 and i1>0:  
                for ligne2 in reader2:
                    if ligne2 and i2>0:
                        if(ligne1[0]!=ligne2[0] and ligne1[1]!=ligne2[1]):
                            
                    else:
                        i2=i2+1
            else:
                i1=i1+1                                                    
    finally:
        file.close()
    
    
    
        
generate_CSV_point_data_file('/home/etudiants/cluchagu1u/Téléchargements/data_CHRU.csv','/home/etudiants/cluchagu1u/Bureau/test.csv')

#create_New_CSV('/home/etudiants/cluchagu1u/Bureau/test.csv')   
#add_Point('/home/etudiants/cluchagu1u/Bureau/test.csv','test1','test1','test1','test1','test1','test1','test1','test1','test1')
#add_Point('/home/etudiants/cluchagu1u/Bureau/test.csv','test2','test2','test2','test2','test2','test2','test2','test2','test2')