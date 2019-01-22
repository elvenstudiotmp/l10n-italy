.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

Italian Localization - FatturaPA - Emission - PEC Support via CRON
==================================================================

Propedeutic module to handle electronic invoices.
http://fatturapa.gov.it


Installation
============

No additional information required during installation.


Configuration
=============

Under Settings -> Automation -> Scheduled Actions enable `FATTURAPA:
Create and send via PEC` to automatically generate and send electronic invoice
via PEC channel.

During cron execution, if an invoice raises some issues it will be marked 'With error'
and the error message is stored into the history log. All invoices with error
can be selected and marked as resolved when the user check the error and solve it.
In this way, cron can reschedule corrected invoice, export and send them to AdE.

Credits
=======
* Domenico Stragapede <d.stragapede@elvenstudio.it>
* Vincenzo Terzulli <v.terzulli@elvenstudio.it>

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
