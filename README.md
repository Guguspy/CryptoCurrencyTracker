CryptoCurrencyTracker 💵
===

## Table of contents
* [Informations](#Informations)
* [Utilisations](#Utilisations)
* [Wallet.dat](#Wallet.dat)



## Informations
* Version: 1.0
* Sans interface graphique
* Veillez à remplir correctement le Wallet.dat
* Veillez à compléter le champ MAIL et PASS dans les fonctions ```sendmailError()``` et ```sendmail()```

	
## Utilisations
Ce programme vous permet de suivre votre Wallet, ou un actif, en recevant une notification par mail lors d'une variation (positive ou négative), ce taux de variation peut-être défini (par défaut 10%).

En prévision : Ajout d'une interface graphique avec → modification du Wallet.dat dans l'interface.


## Wallet.dat
```
##########
[WalletName:PourcentageVariation]
##########
ID_crypto*:nb_unit
ID_crypto*:nb_unit
ID_crypto*:nb_unit
```

Voici un lien pour trouver l'id : https://api.coingecko.com/api/v3/coins/list
