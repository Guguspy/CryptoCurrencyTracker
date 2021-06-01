
#---------- IMPORT ----------#

#--------------------#

    #Module -> Requêtes API

import requests
import json

#--------------------#

    #Module -> Temps

import datetime
from time import strftime
from time import gmtime, strftime
import time

#--------------------#

    #Module -> Obtenir ligne texte

import linecache

#--------------------#

    #Module -> Envoie email

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import mimetypes
import email.mime.application

#--------------------#

    #Module -> OS

import os

#--------------------#



#--------------------#

    #pour eviter les erreurs en .exe
##import pkg_resources.py2_warn

#---------- IMPORT ----------#


# https://api.coingecko.com/api/v3/coins/list
# curl -X GET "https://api.coingecko.com/api/v3/simple/price?ids=stellar&vs_currencies=usd" -H "accept: application/json"



"""
╔                                                                                               ╗
#Function
Envoie un mail en cas d'erreur du programme, avec l'erreur.
(En temps normal, le programme se relance, un mail sera juste envoyé pour informer de l'erreur)
╚                                                                                               ╝
"""


def sendmailError(error):
    error=str(error)
    smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
    smtp_ssl_port = 465
    s = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    s.login('MAIL','PASS')

    msg = MIMEMultipart()
    msg['Subject'] = 'Error Script'
    msg['From'] = 'CryptoCurrencyTracker:1.0'
    msg['To'] = 'reverdyguillaume73@gmail.com'

    txt = MIMEText('Bonjour,\nVoici l\'erreur\n'+error+'\n\n\nHave a nice day ! ☺ \n\n[CryptoCurrencyTracker:1.0] By Gugus')
    msg.attach(txt)

    s.send_message(msg)
    s.quit()


    """
    ╔                                                                                                                                                           ╗
    #Function
    Envoie un mail pour informer la variation subit sur un actif ou un wallet.
    paramètres envoyés : Nom (Actif ou Wallet), Pourcentage de Variation (- ou +), le prix de départ (avant la variation), le prix final (après la variation) 
    ╚                                                                                                                                                           ╝
    """

def sendmail(walletChange,PercentVar, PreviousPrice, ActualPrice):
    try:
        smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
        smtp_ssl_port = 465
        s = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        s.login('MAIL','PASS')

        msg = MIMEMultipart()
        msg['Subject'] = 'Variation sur votre wallet ['+walletChange+']'
        msg['From'] = 'CryptoCurrencyTracker:1.0'
        msg['To'] = 'reverdyguillaume73@gmail.com'

        txt = MIMEText('Bonjour,\nvotre wallet ['+walletChange+'] a varié de '+PercentVar+' % .\nPassant alors de '+PreviousPrice+'€ à '+ActualPrice+' € .\nHave a nice day ! ☺ \n\n[CryptoCurrencyTracker:1.0] By Gugus')
        msg.attach(txt)

        s.send_message(msg)
        s.quit()
    except:
        print('Error [sendmail] : ',datetime.datetime.now())
        exit()


    """
    ╔                                                               ╗
    #Function
    Retourne les lignes comprenant la chaîne de caractères saisi
    ╚                                                               ╝
    """

def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results


    """
    ╔                                                           ╗
    #Function
    Retourne des retours à la ligne suivant le paramètre (int).
    ╚                                                           ╝
    """

def wipe(n):
    for i in range(0, n):
        print("\n")


    """
    ╔                                                   ╗
    #Function
    Requête permettant d'obtenir l'actif crypto en euro
    ╚                                                   ╝
    """

def getcurrency(Unit):
    LinkCurrency="https://api.coingecko.com/api/v3/simple/price?ids="+Unit+"&vs_currencies=eur"
    Currency = requests.get(LinkCurrency, headers={"accept": "application/json"})
    return Currency.json()[Unit]['eur']


    """
    ╔                                                                                                   ╗
    #Function
    • Récupère la variation (si existant, sinon fixé à 10%) de ce wallet ;
    • Calcul le total du wallet (ou actif) ; 
    
    • Nom + prix → dans une liste (Si non présent dans la liste) ;
    
    • Si nom + prix déjà dans la liste :
        • Calcul la variation entre nouveau prix et ancien ;
        • Si + ou - que la variation fixé :
            • Envoie mail
            • Remplace l'ancien prix par le nouveau
        • Sinon    
            • Refait un tour
    • Attente de 10mn (Pour éviter que la requête via l'API nous bloque)   
    
    • Multiple try:catch permettant d'envoyer un mail en cas d'erreur et de le relancer par la suite
    
    • Multiple ajustement des différents nombres (pour éviter 100 chiffres après la virgule) 
    ╚                                                                                                   ╝
    """

def CryptoCurrency():
    try:
        for Wallet in listeWallet:
            TotalWalletPrice = 0
            matched_lines = search_string_in_file('Wallet.dat', Wallet)
            for elem in matched_lines:
                lineprofileselect = elem[0]
                WalletName = linecache.getline('Wallet.dat', lineprofileselect)
                WalletName = WalletName[:-1]

                if ":" in WalletName:
                    LWalletName = int(WalletName.index(':'))
                    Pourcentage_Variation = WalletName[(1 + LWalletName):]
                    Pourcentage_Variation = Pourcentage_Variation[:-1]
                    Pourcentage_Variation=int(Pourcentage_Variation)
                else:
                    Pourcentage_Variation=10

            valid = True
            while valid:
                lineprofileselect = lineprofileselect + 1
                Crypto = linecache.getline('Wallet.dat', lineprofileselect)
                Crypto = Crypto[:-1]
                if detectWallet1 in Crypto or detectWallet2 in Crypto or detectWallet3 in Crypto:
                    pass
                elif ":" in Crypto:
                    LCrypto = int(Crypto.index(':'))
                    CryptoName = Crypto[:LCrypto]
                    CryptoNbUnit = float(Crypto[(1 + LCrypto):])
                    # print(CryptoNbUnit)
                    # print("Portefeuille pour ",CryptoName," =",getcurrency(CryptoName)*CryptoNbUnit," €")
                    TotalWalletPrice = getcurrency(CryptoName) * CryptoNbUnit + TotalWalletPrice
                elif detectWallet4 in Crypto:
                    valid = False

                    point = "."

                    TotalWalletPrice = str(TotalWalletPrice)
                    TotalWalletPrice2 = TotalWalletPrice

                    TotalWalletPrice = TotalWalletPrice.split(point, 1)[0]
                    TotalWalletPrice2 = TotalWalletPrice2.split(point, 1)[1]

                    TotalWalletPrice = str(TotalWalletPrice)
                    TotalWalletPrice2 = str(TotalWalletPrice2)
                    TotalWalletPrice2 = TotalWalletPrice2[:3]

                    TotalWalletPrice = TotalWalletPrice + '.' + TotalWalletPrice2

                    print("Votre Wallet sur", Wallet, "vaut", TotalWalletPrice,"€    [",datetime.datetime.now(),"]")
                    if WalletName in ListVariationWallet:
                        VerifPrixIndex = ListVariationWallet.index(WalletName) + 1
                        VerifPrix = ListVariationWallet[VerifPrixIndex]
                        VerifPrix=float(VerifPrix)
                        TotalWalletPrice=float(TotalWalletPrice)
                        if VerifPrix == TotalWalletPrice:
                            pass
                        elif VerifPrix > TotalWalletPrice or VerifPrix < TotalWalletPrice:
                            PercentageVarWallet = 100 * TotalWalletPrice / VerifPrix - 100
                            if PercentageVarWallet < -Pourcentage_Variation or PercentageVarWallet > Pourcentage_Variation:
                                STR_WalletName = str(Wallet)
                                STR_PercentageVarWallet = str(PercentageVarWallet)

                                point = "."

                                STR_PercentageVarWallet = STR_PercentageVarWallet
                                STR_PercentageVarWallet2 = STR_PercentageVarWallet

                                STR_PercentageVarWallet = STR_PercentageVarWallet.split(point, 1)[0]
                                STR_PercentageVarWallet2 = STR_PercentageVarWallet2.split(point, 1)[1]

                                STR_PercentageVarWallet = str(STR_PercentageVarWallet)
                                STR_PercentageVarWallet2 = str(STR_PercentageVarWallet2)
                                STR_PercentageVarWallet2 = STR_PercentageVarWallet2[:3]

                                STR_PercentageVarWallet = STR_PercentageVarWallet + '.' + STR_PercentageVarWallet2

                                STR_VerifPrix = str(VerifPrix)
                                STR_TotalWalletPrice = str(TotalWalletPrice)
                                sendmail(STR_WalletName, STR_PercentageVarWallet, STR_VerifPrix, STR_TotalWalletPrice)
                                ListVariationWallet[VerifPrixIndex]=TotalWalletPrice
                    else:
                        ListVariationWallet.append(WalletName)
                        ListVariationWallet.append(TotalWalletPrice)
        print("\n")
        time.sleep(600)
        CryptoCurrency()
    except Exception as error:
        try:
            sendmailError(error)
            CryptoCurrency()
        except Exception as error:
            sendmailError(error)
            print("Erreur [CryptoCurrency] :",datetime.datetime.now())
            time.sleep(600)
            CryptoCurrency()


"""
╔                                                                           ╗
• Liste les nom de wallet (ou actif) avec divers méthodes de détection ; 
╚                                                                           ╝
"""

nodatdata = False
nothing = ""
listevide = []
listeWallet = []
detectWallet1 = '['
detectWallet2 = ']'
detectWallet3 = '#'
detectWallet4 = ''

Walletfile = open("Wallet.dat", "r")
for Wallet in Walletfile:
    if detectWallet1 in Wallet and detectWallet2 in Wallet and not detectWallet3 in Wallet:

        Wallet = Wallet
        Wallet = Wallet[:-2]
        Wallet = Wallet[1:]

        if ":" in Wallet:
            LWallet = int(Wallet.index(':'))
            Wallet = Wallet[:LWallet]
            Var_Percentage_Wallet = Wallet[(1 + LWallet):]
            listeWallet.append(Wallet)
        else:
            listeWallet.append(Wallet)


Walletfile.close()
choixprofilverif = False

ListVariationWallet = []
CryptoCurrency()




