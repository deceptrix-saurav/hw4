# Problem 9 — Usability improvements

## Front end

1. **Responsive layout:** the product grid collapses to one column on small screens and navigation spacing adapts, so shoppers can browse comfortably on a phone.
2. **Clickable, contextual product results:** catalogue cards and chat search cards link to the same product-detail route, so shoppers never lose the path from discovery to full product information.

## Agent / backend

1. **Database-first lookup tools:** price and stock responses come from SQLite joins rather than model guesses. This protects the business from inaccurate availability claims.
2. **Structured response caps:** catalogue searches return at most 12 `ProductCard` records and chat requests are capped at 1,000 characters. This keeps responses readable and limits unnecessary model/tool work.
