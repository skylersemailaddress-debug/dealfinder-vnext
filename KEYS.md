# Keys & Accounts You’ll Want

**Core**
- EBAY_CLIENT_ID, EBAY_CLIENT_SECRET (Browse API OAuth)
- EBAY_APP_ID (Finding / legacy sold comps if used)
- OPENAI_API_KEY (LLM judge + normalization + optional vision)

**Retail anchors**
- GOOGLE_CSE_KEY (Google Custom Search JSON API)
- GOOGLE_CSE_CX (Custom Search Engine ID)
- (Optional) SERPAPI_KEY as backup search/anchors

**Vision**
- GOOGLE_APPLICATION_CREDENTIALS (service account JSON for Google Vision API)
- (Optional) AWS Rekognition creds as alternative

**Category-specific resale (optional; varies by compliance and availability)**
- KEEP A (Keepa key) for Amazon price history
- StockX/GOAT (often private/unofficial; prefer affiliates/partners where possible)
- Reverb API (partner) or permitted scraping via ToS-compliant method
- Discogs token (music media)
- TCGplayer API key (trading cards)

**Important:** Only integrate sources via official APIs or permitted access.
