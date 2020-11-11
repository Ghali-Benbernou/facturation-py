from datetime import date
import json
import os
import xml.etree.ElementTree
from lxml import etree
from xml.dom import minidom


# importation de la date local
auj = date.today()
# declaration des variables

num_fac = ""
tax = ""
selection = ""
prod_name = []
stock_qty = []
prod_prix = []

# les classes


class Client(object):
    def __init__(self, nom, ville):
        self.nom = nom
        self.ville = ville


class Prod(object):
    def __init__(self, nom, prix, quant):
        self.nom = nom
        self.prix = prix
        self.quant = quant


# fonction de listing
def list_display(liste):
    listing = ""
    for i, e in enumerate(liste):
        listing += "N " + str(i + 1) + ": " + str(e)
        if i < len(liste) - 1:
            listing += "\n"
    return listing


select = ""

# Menu principale du programme
while select != 0:
    print "\n\t\t\tMENU:\n"
    print "1-Creation Facture "
    print "2-Clients"
    print "3-Produits"
    print "4-Factures"
    print "0-Quite\n"

    select = raw_input()
    # 1-creation de la fact
    if select == '1':

        # Num de fact
        facture_num = raw_input("Num Facture : ")

        # choix du client
        client = []
        with open("client.json", 'r') as f:
            client = json.load(f)
        print 'Choix du client :'
        print '1 : client existent'
        print '2 : Ajouter Nouveau'

        choix = raw_input("Votre choix : ")

        nom_cl = ""
        # client existant
        if choix == "1":
            print "\t\t\tListe des Clients :"
            print list_display(client)

            num_cl = raw_input("N du client : ")
            nom_cl = client[int(num_cl) - 1]
        # nouveau client
        else:
            nom_cl = raw_input("Nom client : ")
            ville_cl = raw_input("ville client : ")

            cl = Client(nom_cl, ville_cl)
            client.append(cl.__dict__)

            with open('client.json', 'w') as f:
                json.dump(client, f, indent=2)

            print cl.__dict__
            print "client ajoute !"
        # coix de produits
        prod_add = []
        prod_exsi = []

        with open("prod.json", 'r') as f:
            prod_exsi = json.load(f)

            print "\t\t\tSaisie des produits"
            print "1: Choisir un produit existant"
            print "2: Nouveau produit "

            choix = raw_input("Votre choix : ")
        p = True
        while p:
            # produits existant
            if choix == "1":

                print "\t\t\t Produits disponible"
                print list_display(prod_exsi)

                num_prod = raw_input("N du produit: ")
                index_prod = int(num_prod) - 1
                qty_stock = prod_exsi[index_prod]['quant']

                new_qty = int(raw_input("Qte: "))

                product_name = prod_exsi[index_prod]['nom']
                product_price = prod_exsi[index_prod]['prix']

                prod_add.append({
                    'nom': product_name,
                    'quant': new_qty,
                    'prix': product_price})


                prod_add[len(prod_add) - 1]['quant'] = new_qty
                prod_exsi[index_prod]['quant'] = qty_stock - new_qty

                

            # nouveaux prod
            else:
                with open("prod.json", 'r') as f:
                    prod_exsi = json.load(f)

                prod_name = raw_input("Nom Produit: ")
                stock_qty = int(raw_input("quantite stock: "))
                inv_qty = int(raw_input("quantite client: "))
                prod_prix = int(raw_input("Prix de Vente: "))

                prod_add.append({
                    'nom': prod_name,
                    'quant': inv_qty,
                    'prix': prod_prix})
                stock_qty -= inv_qty

                pr = Prod(prod_name, prod_prix, stock_qty)
                prod_exsi.append(pr.__dict__)

                with open('prod.json', 'w') as f:
                    json.dump(prod_exsi, f, indent=2)

                print "Nouveau produit ajoute..."

            pp = raw_input("fermmer la facture ? Oui ou Non : ")
            if pp in ["oui", "OUI", "Oui", "o", "O"]:
                p = False
            else:
                print "1: Choisir un produit existant"
                print "2: Nouveau produit "

                choix = raw_input("Votre choix : ")
        # la tax
        tax = raw_input("*taxe : ")
        total_ht = 0
        x = 0
        while (x < len(prod_add)):
            total_ht += int(prod_add[x]['prix']
                            ) * int(prod_add[x]['quant'])
            x += 1

        total_ttc = total_ht * int(tax) / 100 + total_ht

        ################  TXT ###############

        fichier_n = open("Facture" + facture_num + ".txt", "w")
        fichier_n.write("\n\t\t\t\tFacture n" + facture_num)
        fichier_n.write("\nNom : " + str(nom_cl))
        fichier_n.write("\nDate: " + str(auj))

        fichier_n.write("\n\n\n")

        x = 0
        total_prix = []
        fichier_n.write(
            "\nProduit: \t\t\tQuantite: \t\tPrix unitaire: \t\tSous total: ")
        while (x < len(prod_add)):
            if x > 0:
                print""

            total_prix.append(
                int(prod_add[x]["prix"]) * int(prod_add[x]["quant"]))
            fichier_n.write("\n\n" + prod_add[x]["nom"] + "\t\t\t\t\t\t\t" + str(prod_add[x]["quant"]) + "\t\t" + str(
                prod_add[x]["prix"]) + "\t\t" + str(total_prix[x]) + " DZD")

            x = x + 1

        fichier_n.write("\n\n\nTotal HT: " + str(total_ht) + " DZD")

        fichier_n.write("\nTaxe: " + str(tax) + " %")

        fichier_n.write("\nTotal TTC: " + str(total_ttc) + " DZD")

        fichier_n.write("\n\t\t\t\t\t\tTOTAL a PAYER: " +
                        str(total_ttc) + " DZD")

        fichier_n.close()
        print "\t\tFacture Cree ! ....."

        ###########    XML     ############

        root = etree.Element("facture")
        root.set("id", facture_num)
        root.set("date", str(auj))
        client = etree.SubElement(root, "client")
        client.text = str(nom_cl)
        Produits = etree.SubElement(root, "Produits")
        for i, p in enumerate(prod_add):
            Prod = etree.SubElement(Produits, "prod")
            nom = etree.SubElement(Prod, "nom_prod")
            nom.text = p['nom']
            qte = etree.SubElement(Prod, "quantitee")
            qte.text = str(p['quant'])
            pr = etree.SubElement(Prod, "prix")
            pr.text = str(p['prix'])
            sous_total = etree.SubElement(Prod, "Sous_total")
            sous_total.text = str(total_prix[i])
        ht = etree.SubElement(root, "ht")
        ht.text = str(total_ht)
        tva = etree.SubElement(root, "tva")
        tva.text = str(tax)
        ttc = etree.SubElement(root, "ttc")
        ttc.text = str(total_ttc)

        file = open("xml_fact" + facture_num + ".xml", "w")
        file.write(etree.tostring(
            root, pretty_print=True, xml_declaration=True))
        file.close()

        xml_string = ""
        with open("xml_fact" + facture_num + ".xml", 'r') as file:
            xml_string = file.read()
            file.close()
        #Menu Client 
    elif select == '2':

        c = True
        while c:
            print "\t\t\tClient:\n"
            print "1-ajouter un client"
            print "2-modifier un client"
            print "3-supprimer un client"
            print "4-liste des clients"
            print "0-retour\n"
            select = raw_input("selectionez une action :")
            #ajout d'un client
            if select == "1":
                with open("client.json", 'r') as f:
                    client = json.load(f)

                nom_cl = raw_input("Nom client : ")
                ville_cl = raw_input("ville client : ")

                cl = Client(nom_cl, ville_cl)
                client.append(cl.__dict__)

                with open('client.json', 'w') as f:
                    json.dump(client, f, indent=2)

                print cl.__dict__
                print "Nouveau client ajoute"
                #suppresion d'un client
            if select == "3":
                with open("client.json", 'r') as f:
                    client = json.load(f)

                print "\t\tListe des Clients :"
                print list_display(client)

                num_cl = raw_input("N du client : ")
                nom_cl = client[int(num_cl) - 1]

                client.remove(nom_cl)

                with open('client.json', 'w') as f:
                    json.dump(client, f, indent=2)
                print "Client Supprimer..."
            #affichage des clients
            if select == "4":
                with open("client.json", 'r') as f:
                    client = json.load(f)

                print "\t\tListe des Clients :"
                print list_display(client)

            if select == "0":
                c = False
    #Menu Produit
    elif select == '3':
        p = True
        while p:
            print "\t\t\tPRODUITS:\n"
            print "1-ajouter un produit"
            print "2-modifier un produit"
            print "3-supprimer un produit"
            print "4-liste des produits"
            print "0-retour\n"
            select = raw_input("selectionez une action :")
            #ajout d'un produit
            if select == "1":
                with open("prod.json", 'r') as f:
                    prod_exsi = json.load(f)

                prod_name = raw_input("Nom Produit: ")
                stock_qty = int(raw_input("quantite stock: "))
                prod_prix = int(raw_input("Prix de Vente: "))

                pr = Prod(prod_name, prod_prix, stock_qty)
                prod_exsi.append(pr.__dict__)

                with open('prod.json', 'w') as f:
                    json.dump(prod_exsi, f, indent=2)

                print "Nouveau produit ajoute..."
            #Modification d'un produit
            if select == "2":
                with open("prod.json", 'r') as f:
                    prod_exsi = json.load(f)

                print "\t\t\t Produits disponible"
                print list_display(prod_exsi)

                num_prod = raw_input("N du produit a modifier : ")
                index_prod = int(num_prod) - 1

                prod_name = raw_input("Nom Produit: ")
                stock_qty = int(raw_input("quantite stock: "))
                prod_prix = int(raw_input("Prix de Vente: "))

                print "produit modifier..."
            #suppresion d'un produit 
            if select == "3":
                with open("prod.json", 'r') as f:
                    prod_exsi = json.load(f)

                print "\t\t\t Produits disponible"
                print list_display(prod_exsi)

                num_prod = raw_input("N du produit: ")
                index_prod = prod_exsi[int(num_prod) - 1]

                prod_exsi.remove(index_prod)

                with open('prod.json', 'w') as f:
                    json.dump(prod_exsi, f, indent=2)

                print "Produit Supprimer..."    
            if select == "4":
                
                prod_exsi = []

                with open("prod.json", 'r') as f:
                    prod_exsi = json.load(f)

                print "\t\t\t Produits disponible"
                print list_display(prod_exsi)

            if select == "0":
                p = False

    #Menu des Factures    
    elif select =="4":
        f=True
        while f:
            print "\t\t\t FACTURES :\n"
            print "1-facture existante"
            print "0-retour\n"
            c=raw_input("Selectionnez une action :")
            if c =="1":

                nf=raw_input("entrez le numero de facture :")
                 
                xmldoc = minidom.parse('xml_fact'+nf+'.xml')
                print xmldoc
                print xmldoc.toxml()
            elif c=="0":
                f=False



    elif select == '0':
        break
