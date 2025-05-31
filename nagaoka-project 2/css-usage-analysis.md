# CSS Usage Analysis Report for nagaoka-fresh.html

## Summary

This report analyzes the CSS files (add_an.css, add_ty.css, and common.css) to identify unused selectors in relation to the nagaoka-fresh.html file.

## 1. CSS Classes/IDs Used in the HTML

### Classes Used (Total: 113 unique classes)
- a
- bar-inner, bar1, bar2, bar3
- block, bluebar
- box-faq-01, box-flex-01, box-flow11b-01, box-header-01, box-imgtxt8d-01, box-single-article-01, box-slide-01, box-style-01
- btn-bar
- c, car, cat, center
- contents
- footer, footer-bottom-01, footer-copy-01, footer-inner, footer-left-01, footer-right-01, footer-top-01
- fs14
- ft-sec02, ft-sec03
- h-auto
- hd-ni-sec01, hd-ni-sec02, hd-ni-sec03
- header, header-btn, header-inner, header-logo, header-nav, header-wrap
- home, house
- iblock
- img, img-slot, img-wrap
- inner, inner-detail, inner-face, inner-table-sp
- invisible
- left, logo, logo-inner
- main
- mt20
- nav-btn, nav-inner
- new-and-cat
- no-js, note
- number
- page, page-id-35, page-template, page-template-index, page-template-index-php
- pc-visible, point
- q
- search
- sec-archive-column, sec-archive-news
- section-faq-01, section-flow-11b, section-imgtxt-8d, section-style-01
- shadow, slider
- sp-btn, sp-visible
- sub, svg
- tel, tel-and-time, telnumber
- title, top
- top-sec01 through top-sec08
- txt, txt-box
- unit-address-01, unit-btn-02, unit-btn-03, unit-date-01, unit-faq-01, unit-flex, unit-flow11b-01, unit-imgtxt8d-01, unit-pagetop-01, unit-point-01, unit-style-01, unit-style-02, unit-tbl-01, unit-title-01, unit-title-07, unit-txt-01, unit-worry-01
- voice-inner, voice-wrapper-01
- w-full, w1000p, w300
- wrap, wrapper
- yoast-schema-graph

### IDs Used (Total: 4 unique IDs)
- contents
- footer
- header
- navBtn

## 2. Unused CSS Selectors

### add_an.css - Unused Classes (21 total)
These classes are defined in add_an.css but not used in the HTML:
- **btn-wrap** - Button wrapper styling
- **column-wrapper-01** - Column layout wrapper
- **detail-box** - Detail content container
- **flex-wrap** - Flexbox wrapper
- **img-box** - Image container
- **list-wrap** - List wrapper
- **name** - Name styling
- **post** - Post styling
- **sec-staff-01**, **sec-staff-02** - Staff section styles
- **single-column-01**, **single-column-02** - Single column layouts
- **text** - Text styling
- **text-box** - Text container
- **text-wrap** - Text wrapper
- **time** - Time/date styling
- **title-box** - Title container
- **unit-box-02**, **unit-box-03** - Box unit styles
- **unit-title-05**, **unit-title-06** - Title unit styles

### add_ty.css - Unused Classes (1 total)
- **under** - Appears to be a modifier class for sections (e.g., sec-archive-news.under)

### common.css - Unused Classes (extensive)
The common.css file contains a large number of unused selectors, primarily:
1. **Font Awesome Icons** - The entire Font Awesome icon library is included but not used
   - fa, fa-2x, fa-3x, fa-4x, fa-5x
   - fa-500px through fa-youtube-square (hundreds of icon classes)
   - All Font Awesome utility classes (fa-spin, fa-pulse, fa-rotate-*, etc.)

2. **Other potentially unused classes** - Due to the large size of common.css (302KB), a complete analysis would require further investigation

## 3. Analysis and Recommendations

### Findings:
1. **add_an.css** contains 21 unused classes (approximately 40% of its content is unused)
2. **add_ty.css** is mostly utilized with only 1 unused class
3. **common.css** includes the entire Font Awesome library which appears completely unused

### Redundancy Analysis:
- **High redundancy in add_an.css**: Many staff-related and column-related styles are not used
- **Minimal redundancy in add_ty.css**: Well-utilized file
- **Significant redundancy in common.css**: Font Awesome library adds significant bloat

### Recommendations:
1. **Remove unused classes from add_an.css** to reduce file size by ~40%
2. **Remove Font Awesome from common.css** if icons are not needed, or use a CDN/selective import
3. **Consider consolidating CSS files** - With so many unused selectors, the three files could potentially be merged and optimized
4. **Implement CSS purging** in the build process to automatically remove unused styles

### Estimated Size Reduction:
- Removing unused classes from add_an.css: ~2-3KB reduction
- Removing Font Awesome from common.css: ~100KB+ reduction
- Total potential reduction: ~100-120KB (approximately 35-40% of total CSS size)