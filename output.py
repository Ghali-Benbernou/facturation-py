###########    XML     ############

def fact_xml():

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


        ################  TXT ###############
def fact_txt():

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

