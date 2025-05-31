# CSS Analysis Results for branch.html

## Summary

After analyzing the branch.html file and all CSS files in the nagaoka-css directory, here are the findings:

### Files Analyzed
- **HTML**: `/Users/shiroto/Desktop/YumeHouse-Website/branch/branch.html`
- **CSS Files**:
  - `common.css` (18,921 lines)
  - `add_an.css` (533 lines) 
  - `add_ty.css` (86 lines)
  - `branch-custom.css` (90 lines)

## Classes and IDs Used in branch.html

### CSS Classes (86 total)
```
assessment, bar-inner, bar1, bar2, bar3, bc-wrap, block, box-header-01, 
box-style-01, box-undertitle-01, branch, branch-sec01, branch-sec02, breadcrumb, 
btn-bar, btn-inner, cat, center, current-item, footer-bottom-01, footer-copy-01, 
footer-inner, footer-left-01, footer-right-01, footer-top-01, fs14, ft-sec02, 
ft-sec03, h-auto, h1-title-01, h1-wrapper-01, hd-ni-sec01, hd-ni-sec02, hd-ni-sec03, 
header-btn, header-inner, header-logo, header-nav, header-wrap, home, img-slot, 
img-wrap, inner, inner-detail, inner-face, inner-table-sp, left, logo, logo-inner, 
main, nav-btn, nav-inner, new-and-cat, no-js, number, oneminute, page, 
page-id-branch, page-template, page-template-branch, pc-visible, post, post-page, 
section-style-01, shadow, sp-btn, sp-visible, sub, tel, tel-and-time, tel-large, 
telnumber, title, title-inner, txt, unit-address-01, unit-btn-03, unit-flex, 
unit-pagetop-01, unit-tbl-01, unit-title-01, unit-txt-01, voice-inner, voice-wrapper-01, 
w-full, wrapper
```

### IDs (4 total)
```
contents, footer, header, navBtn
```

## CSS Usage Analysis

### branch-custom.css (Branch-specific styles)
- **Usage Rate**: 93.8% (15/16 rules used)
- **Recommendation**: KEEP ALL - This file is specifically designed for the branch page
- **Key Rules Used**:
  - `.branch-sec01` - Branch introduction section styling
  - `.branch-sec02` - Branch information cards section
  - `.voice-wrapper-01` - Container for branch information cards
  - `.voice-inner` - Individual branch card styling
  - `.tel-large` - Large telephone number styling
  - `.img-wrap` - Image gallery styling

### common.css (Main framework CSS)
- **Usage Rate**: ~10.3% (412/4001 rules used)
- **File Size**: 302KB (very large)
- **Contains**: Font Awesome icons, base framework, numerous unused components
- **Recommendation**: This file contains a massive CSS framework with many unused rules

### add_an.css (Additional styles)
- **Usage Rate**: ~27.7% (26/94 rules used)
- **Key Used Rules**:
  - `.voice-wrapper-01 .img-wrap` - Image gallery grid layout
  - Footer-related styles used by the site

### add_ty.css (Typography/Archive styles)
- **Usage Rate**: 0% (0/15 rules used)
- **Recommendation**: CAN BE REMOVED entirely for branch page
- **Contains**: Archive news styles, date formatting - not used on branch page

## Detailed Recommendations

### 1. Safe to Remove Completely
**File**: `add_ty.css`
- Contains 15 unused rules (100% unused on branch page)
- Rules are for archive pages (.sec-archive-news, .sec-archive-column, etc.)
- **Saving**: Reduce CSS by 86 lines

### 2. High Cleanup Potential
**File**: `common.css`
- **Current Size**: 302KB with 18,921 lines
- **Usage**: Only ~10% used on branch page
- **Contains large amounts of**:
  - FontAwesome icons (not used on branch page)
  - Bootstrap-like grid systems (minimal usage)
  - Form components (not used on branch page)
  - Complex UI components (not used)

**Major unused categories**:
- FontAwesome icons (.fa-* classes) - 685 rules
- Grid/layout utilities (.col-*, .row-*, etc.)
- Form styling (.input-*, .select-*, etc.)  
- Button variants (.btn-* besides basic ones)
- Complex UI components

### 3. Moderate Cleanup
**File**: `add_an.css`
- ~73% of rules unused on branch page
- Keep the `.voice-wrapper-01` related rules (used for branch cards)
- Many staff/employee-related styles unused on branch page

## Specific Unused CSS Rules by Category

### FontAwesome (Completely Unused)
All 685+ FontAwesome icon classes (.fa-home, .fa-phone, .fa-email, etc.) are unused on the branch page.

### Layout/Grid Components (Mostly Unused)
- Complex grid systems
- Flexbox utilities (beyond basic ones used)
- Advanced positioning classes

### Form Components (Completely Unused)
- Input styling
- Select dropdowns
- Form validation classes
- Submit button variations

### UI Components (Mostly Unused)
- Modal/popup components
- Slider/carousel components
- Advanced button styles
- Complex typography variants

## Recommendations for Cleanup

### Immediate Actions (Safe & High Impact)

1. **Remove add_ty.css** - 100% unused, saves 86 lines
2. **Create minimal branch.css** - Extract only used rules from common.css
3. **Keep branch-custom.css unchanged** - Specifically designed for this page

### Advanced Cleanup (Requires Testing)

1. **Create optimized common.css** containing only:
   - Reset/normalize styles
   - Basic typography
   - Layout utilities actually used
   - Component styles for: header, footer, breadcrumb, tables, basic buttons

2. **Estimated Size Reduction**: 
   - From ~302KB to ~30-50KB (80-85% reduction)
   - Remove ~3,500+ unused CSS rules

### Critical Classes That Must Be Retained

**Layout & Structure**:
- `.wrapper`, `.inner`, `.section-style-01`
- `.box-header-01`, `.header-*`, `.footer-*`
- `.pc-visible`, `.sp-visible`, `.sp-btn`

**Branch-Specific**:
- All rules in `branch-custom.css`
- `.voice-wrapper-01`, `.voice-inner` 
- `.unit-title-01`, `.unit-tbl-01`, `.unit-btn-03`

**Utility Classes**:
- `.fs14`, `.shadow`, `.center`, `.left`
- `.w-full`, `.h-auto`

## File Size Impact

**Current Total**: ~320KB CSS
**After Cleanup**: ~50-60KB CSS
**Reduction**: ~80% smaller CSS bundle
**Load Time Improvement**: Significant, especially on mobile

## Implementation Priority

1. **High Priority**: Remove `add_ty.css` (immediate 0% risk)
2. **Medium Priority**: Clean unused FontAwesome icons from `common.css`
3. **Low Priority**: Advanced cleanup of `common.css` (requires thorough testing)

This analysis shows that there's significant opportunity for CSS optimization, with the potential to reduce the CSS bundle size by 80% while maintaining all functionality needed for the branch page.