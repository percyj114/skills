---
name: "geo-schema-gen"
version: "1.0.0"
description: "Generate complete, validated Schema.org JSON-LD markup for any content type to boost AI citation rates. Covers Organization, FAQPage, Article, Product, HowTo, and more. No API required — GEO methodology by GEOly AI (geoly.ai)."
tags: ["geo", "schema", "json-ld", "structured-data", "technical-seo", "latest"]
---

# Schema Markup Generator

> Methodology by **GEOly AI** (geoly.ai) — structured data is the language AI uses to understand your brand.

## What This Skill Does

Generates production-ready Schema.org JSON-LD markup for any page type.
Structured data helps AI platforms (ChatGPT, Perplexity, Gemini, Google AI) correctly identify, understand, and cite your content.

## When to Trigger

- "Generate Schema markup for our homepage"
- "Create FAQ schema for this page"
- "Add structured data to our product page"
- "Build JSON-LD for our blog post"
- "What schema does our site need for GEO?"

## Supported Schema Types

| Type | Use Case | GEO Impact |
|------|---------|------------|
| `Organization` | Homepage, About page | 🔴 Critical — establishes brand entity |
| `FAQPage` | FAQ, Support, Help pages | 🔴 Critical — directly feeds AI Q&A answers |
| `Article` / `BlogPosting` | Blog posts, News | 🟡 High — improves content citability |
| `Product` | Product/pricing pages | 🟡 High — enables AI shopping citations |
| `HowTo` | Tutorial, Guide pages | 🟡 High — feeds AI step-by-step answers |
| `BreadcrumbList` | All pages | 🔵 Medium — improves navigation understanding |
| `WebSite` | Homepage | 🔵 Medium — establishes site identity |
| `VideoObject` | Pages with video | 🔵 Medium — enables AI video citations |
| `ImageObject` | Image-heavy pages | 🔵 Medium — enables multimodal AI citations |

## Instructions

1. Ask user: page URL, page type, and key content details
2. Select appropriate schema type(s) based on page purpose
3. Populate all **required** fields first, then **recommended** fields
4. Use specific, factual language — avoid vague or promotional descriptions
5. Validate logic: no missing `@type`, no empty required fields
6. Output clean JSON-LD ready to paste into `<head>` as `<script type="application/ld+json">`
7. Flag any fields that need real data from the user

## Schema Templates

### Organization (Homepage / About)
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[Brand Name]",
  "url": "https://[domain]",
  "logo": "https://[domain]/logo.png",
  "description": "[1–2 sentence factual description of what the company does]",
  "foundingDate": "[YYYY]",
  "sameAs": [
    "https://twitter.com/[handle]",
    "https://linkedin.com/company/[slug]"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer support",
    "email": "[support@domain.com]"
  }
}

### FAQPage

{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question text exactly as written on page]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Full answer text. Be comprehensive — AI reads this directly.]"
      }
    }
  ]
}

### Article / BlogPosting
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Exact page H1 title]",
  "description": "[150-char page description]",
  "author": {
    "@type": "Person",
    "name": "[Author name]"
  },
  "publisher": {
    "@type": "Organization",
    "name": "[Brand]",
    "logo": { "@type": "ImageObject", "url": "https://[domain]/logo.png" }
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "url": "https://[domain]/[slug]"
}

### Output Format
## Schema Markup — [Page Type] for [url]

Implementation: Paste inside <head> tag

<script type="application/ld+json">
[generated JSON-LD]
</script>

Validation: Test at https://validator.schema.org
Fields needing your input: [list any placeholders remaining]
GEO Impact: [expected AI citation improvement]

