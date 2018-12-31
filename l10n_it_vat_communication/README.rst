.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Italian Localization - Spesometro2017
=====================================

Gestisce la Comunicazione periodica IVA con l'elenco delle fatture emesse e
ricevute e genera il file da inviare all'Agenzia delle Entrate.
Questo obbligo è conosciuto anche come Spesometro 2017 e sostistuisce il
precedente obbbligo chiamato Spesometro.

Funzione | Status | Note
--- | --- | ---
Fatture clienti e fornitori detraibili | :white_check_mark: | Fatture ordinarie
Fatture fornitori indetraibili | :white_check_mark: | Tutte le percentuali di indetraibilità
Fatture a privati senza Partita IVA| :white_check_mark: | Necessario codice fiscale
Fatture semplificata | :white_check_mark: | Per clienti senza PI ne CF
Fatture senza IVA | :white_check_mark: | Fatture esenti, NI, escluse, eccetera
Escludi importi Fuori Campo IVA | :white_check_mark: | Totale fattura in Comunicazione può essere diverso da registrazione
Escludi CAP e provincia no Italia in comunicazione | :white_check_mark: | Da nazione, oppure da partita IVA oppure Italia
Escludi CF no Italia in comunicazione | :white_check_mark: | Da nazione, oppure da partita IVA oppure Italia
Controlli dati anagrafici |
Conversione ISO-Latin1 | :white_check_mark: | Evita rifiuto partner stranieri
IVA differita | :white_check_mark: | Da codice imposte
IVA da split-payment | :white_check_mark: | Da codice imposte
Ignora autofatture | :white_check_mark: | Esclusione tramite sezionale
Ignora corrispettivi | :white_check_mark: | Esclusione tramite sezionale
Ignora avvisi di parcella | :white_check_mark: | Esclusione tramite sezionale
Identificazione Reverse Charge | :white_check_mark: | Da codice imposte
Fatture vendita UE | :white_check_mark: | Inserite in spesometro
Fatture vendita extra-UE | :white_check_mark: | Inserite in spesometro
Fatture acq. intra-UE beni | :x: | In fase di rilascio
Fatture acq. intra-UE servizi | :white_check_mark: | Tutte le fatture EU (provvisoriamente)
Rettifica dichiarazione | :x: | In fase di rilascio
Nomenclatura del file | :white_check_mark: |
Dimensioni del file | :x: | Nessuna verifica anche futura


Specification:

URL | Descrizione
--- | ---
http://www.agenziaentrate.gov.it/wps/content/Nsilib/Nsi/Strumenti/Specifiche+tecniche/Specifiche+tecniche+comunicazioni/Fatture+e+corrispettivi+ST/ | Validazione contro schema xml
http://www.agenziaentrate.gov.it/wps/content/Nsilib/Nsi/Strumenti/Specifiche+tecniche/Specifiche+tecniche+comunicazioni/Fatture+e+corrispettivi+ST/ | File accettati da portale fatturaPA Agenzia delle Entrate

Configuration
-------------

:it:

* Contabilità > Configurazione > Sezionali > Sezionali :point_right: Impostare sezionali autofatture
* Contabilità > Configurazione > Imposte > Imposte :point_right: Impostare natura codici IVA
* Contabilità > Clienti > Clienti :point_right: Impostare nazione, partita IVA, codice fiscale e Cognome/nome
* Contabilità > Fornitori > Fornitori :point_right: Impostare nazione, partita IVA, codice fiscale e Cognome/nome
* Contabilità > Elaborazione periodica > Fine periodo > Comunicazione :point_right: Gestione Comunicazione e scarico file xml


Known issues / Roadmap
----------------------

:ticket: enable xml download with PyXB==1.2.5

Credits
=======

Contributors
------------
* Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
* Andrei Levin <andrei.levin@didotech.com>
* Domenico Stragapede <d.stragapede@elvenstudio.it>
* Vincenzo Terzulli <v.terzulli@elvenstudio.it>

Funders
-------
This module has been financially supported by

* SHS-AV s.r.l. <https://www.zeroincombenze.it/>
* Didotech srl <http://www.didotech.com>


Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
