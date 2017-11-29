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

#On créer un nouveau fichier csv avec les entêtes pour chacun des attributs
def create_New_CSV(nomFichierCSV):
    entetes = [
     u'File_Name_Nifti',
     u'Surgeon_ID',
     u'Patient_ID',
     u'Localisation',
     u'Type_Of_Answer',
     u'X',
     u'Y',
     u'Z',
     u'Intensity'
    ]

    f = open(nomFichierCSV, 'w')
    ligneEntete = ",".join(entetes) + "\n"
    f.write(ligneEntete)
    
    print '\nfichier créer avec succès !\n'
    f.close()

#On ajoute un point dans le jeu de données représenté par le csv
def add_Point(nomFichierCSV,nom_Fichier_Nifti,ID_Chirurgien,ID_Patient,Localisation,Type_De_Reponse,X,Y,Z,Intensite):
    
    attributs = [nom_Fichier_Nifti,ID_Chirurgien,ID_Patient,Localisation,Type_De_Reponse,X,Y,Z,Intensite]    
    f = open(nomFichierCSV, 'a')
    item = ",".join(attributs) + "\n"
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
                    add_Point(newCSV,'NULL','NULL',ID_patient_tampon,ligne[5],ligne[6],ligne[8],ligne[9],ligne[10],comma_to_Point(ligne[3]))
            else:
                index=index+1
                                 
    finally:
        file.close()
        
##On fait la fusion de deux csv que l'on place dans un troisieme csv résultant
def merge_CSV(csv_1,csv_2,csvMerge):
    file1 = open(csv_1, "rb") 
    file2 = open(csv_2, "rb")   
    create_New_CSV(csvMerge)
    try:
        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)
        i1=0
        i2=0
        
        for ligne2 in reader2:
            exist = False
            print ligne2[0]
            if ligne2 and i2>0:  
                for ligne1 in reader1:           
                    if ligne1 and i1>0:
                        add_Point(csvMerge,ligne1[0],ligne1[1],ligne1[2],ligne1[3],ligne1[4],ligne1[5],ligne1[6],ligne1[7],ligne1[8])
                        if(exist==False and ligne1[0]==ligne2[0] and ligne1[1]==ligne2[1]):
                            exist = True
                    i1=i1+1
                if exist!=True:
                    add_Point(csvMerge,ligne2[0],ligne2[1],ligne2[2],ligne2[3],ligne2[4],ligne2[5],ligne2[6],ligne2[7],ligne2[8])
            i2=i2+1                                                       
    finally:
        file1.close()
        file2.close()  
    
merge_CSV('/home/etudiants/cluchagu1u/Bureau/testMerge1.csv','/home/etudiants/cluchagu1u/Bureau/testMerge2.csv','/home/etudiants/cluchagu1u/Bureau/testMerge3.csv')
#generate_CSV_point_data_file('/home/etudiants/cluchagu1u/Téléchargements/data_CHRU.csv','/home/etudiants/cluchagu1u/Bureau/testMerge2.csv')
#create_New_CSV('/home/etudiants/cluchagu1u/Bureau/test.csv')   
#add_Point('/home/etudiants/cluchagu1u/Bureau/test.csv','test1','test1','test1','test1','test1','test1','test1','test1','test1')
#add_Point('/home/etudiants/cluchagu1u/Bureau/test.csv','test2','test2','test2','test2','test2','test2','test2','test2','test2')
