# Product Validation Wizard voor Odoo 18

Deze module voegt een wizard toe aan Odoo 18 om producten te valideren voor publicatie (bijv. op de webshop). De wizard controleert:

- Er moet een foto (image) aanwezig zijn.
- Er moet een prijs ingesteld zijn (verkoopprijs > 0).
- De voorraad bij de goedkoopste leverancier moet minstens X stuks zijn (configureerbaar, default 10; gebruikt `supplier_stock` uit `supplier_pricelist_sync`).
- Het product moet voldoen aan verkoopcriteria (bijv. een boolean-veld `is_sellable` op het product).

## Installatie
1. Plaats de module in je Odoo addons-map.
2. Herstart Odoo en update de Apps-lijst.
3. Installeer via Apps > Product Validation Wizard.
4. Afhankelijkheden: `product`, `purchase`, `stock`, `website` (voor publicatie), en optioneel `supplier_pricelist_sync`.

## Gebruik
- Ga naar **Inventaris > Producten > Producten**.
- Open een product en klik op de knop **Valideer voor Publicatie**.
- De wizard toont de checks. Als alles OK, publiceert het het product (zet `website_published = True`).

## Aanpassingen
- Minimum stock: Pas `min_stock_required` aan in de wizard.
- Verkoopcriteria: Voeg een custom veld `is_sellable` toe aan producten.

Auteur: Jouw naam / sybdeb  
Licentie: LGPL-3 (standaard voor Odoo).  
Odoo versie: 18.0
