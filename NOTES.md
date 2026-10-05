# Elia Living redesign — internal notes

Source: www.elialiving.es/en, collected 5 October 2026. Every fact on the new site comes from that site. Nothing below is shown to visitors.

## How to view

Open `index.html` in Chrome, Safari or Firefox while online. Photos, team portraits and video load live from Elia Living's own servers (imagedelivery.net and cdn-tesoro). Fonts load from Google Fonts. Smooth scrolling loads Lenis from jsDelivr; the site works without it.

## Inconsistencies found on the current site

| # | Item | What the site says | Used in redesign | Action |
|---|------|--------------------|------------------|--------|
| 1 | ELI1146 price | €1,790,000 on the homepage card; €1,890,000 on the property page and the listings page | €1,890,000 (2 of 3) | Confirm the current price |
| 2 | ELI32 price | €790,000 on its own page and most "featured" blocks; €807,000 in the featured block on the ELI1146 page | €790,000 | Confirm |
| 3 | Office postcode | 03738 in most footers; 03730 in the footer of the properties page and ELI1146 | 03738 | Confirm |
| 4 | Number of languages | Homepage: "EN, PL, ES, DE, NL" (5). Meta description: "six languages". The site itself has 8 language versions (EN, ES, PL, NL, FR, DE, RU, CA) | The 5 listed on the homepage | Confirm the advisory languages |
| 5 | Days of sunshine | "over 300", "320", "over 320" and "325" on different pages | "over 320" | Choose one figure |
| 6 | CP40 name | Page heading "Villa Altamira"; listing cards and image alt text "Property #CP40" | Villa Altamira | Fix the CRM title |
| 7 | ELI893 headline spec | Header shows "2139 Square Meters" next to beds/baths (that is the plot); built area is 319 m² | Shown as built 319 m² and plot 2,139 m² | Label sizes in the CRM feed |
| 8 | ELI893 plot | "nearly 2,150 m²" in the introduction; "2,139 m²" in the summary and specs | 2,139 m² | Align copy |
| 9 | Team page spelling | "Conceirge" (Services heading and Luna's role) | Corrected to "Concierge" | Fix on current site |
| 10 | Testimonials | Only one testimonial exists (Marek J., Warsaw) | Used once, on Home | Add more real testimonials if available |
| 11 | ELI279 and ELI283 | The "Reach out to" advisor name is empty | Shown as "The Elia Living sales team" | Assign advisors |
| 12 | Prev/next links | ELI279 and ELI283 both point to the same prev/next pair (ELI285 / ELI232) | Redesign uses its own sequence of the six residences | — |

## Claims deliberately left out or softened (need a source before publishing)

- "Costa Blanca is the nr 1 European destination" (homepage). Omitted.
- "Jávea is recognised by WHO as having one of the planet's best microclimates" (Costa Blanca page). Omitted.
- "Property prices rising 7–15% yearly, rental yields up to 8–9%" and "cost of living 30–35% lower". Omitted; cost of living softened to "noticeably lower".
- Blue Flag counts ("7 in Dénia, 71 total"). Omitted; the two named Jávea beaches are kept.
- Construction returns ("up to 30% within 18 months on renovations; 20–50% ROI on new builds"). Kept because it is a stated service offer, with the line "Figures as published by Elia Living for its developments and co-investments. Returns vary by project." **Have this reviewed for compliance.**
- Lady Elizabeth School rankings ("Top 30 El Mundo, Top 100 Forbes"). Rankings omitted; school names kept.
- "Core Values" section exists on the About page but its content did not load from the source, so it is not included rather than invented.

## Assets

- **ELI893**: only 4 of its 26 photographs were readable. The gallery shows those 4 and says so on the page. Add the remaining 22 image IDs to `data.py` and rebuild.
- **Logo**: the wordmark is typographic ("ELIA LIVING" + "Trusted Real Estate Advisors"), pending the official SVG (`EliaLiving-logo-white-SVG.svg`), which should replace it in the header, menu, curtain and footer.
- **Property photos** use Cloudflare resized variants (`w=1600,quality=82`) with automatic fallback to the original if resizing is not enabled on the account. The original site overlays a watermark; the redesign uses the clean images.
- Not used: two images whose filenames show they are Rawpixel stock (`image-from-rawpixel-…`), per the no-stock brief.
- Homepage hero uses the first ELI893 image. ELI893 is under construction, so this image is likely a visualisation; the property is labelled "New build · under construction".

## Before launch

- Forms (enquiry, consultation, newsletter) currently prepare the message and hand it to WhatsApp or email. Connect them to the Tesoro CRM / newsletter provider.
- Properties page shows the six collected residences. The live site lists 278; connect the grid and property template to the Tesoro feed (`data.py` mirrors the fields needed).
- Language versions (ES, PL, NL, FR, DE, RU, CA) are not built yet.
- Cookie consent banner is not included; required once analytics and video embeds go live.
- Guides (guides.elialiving.es) and legal pages link to the existing site.

## Rebuilding

`cd _source && python3 build.py` (after setting OUT to the parent folder) regenerates every page from `data.py`. Styles: `assets/site.css`. Motion and interaction: `assets/site.js`.
