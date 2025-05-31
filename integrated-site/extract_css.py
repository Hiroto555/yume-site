#!/usr/bin/env python3
import re
import sys

def extract_used_css(css_content, html_classes, html_ids, html_elements):
    """Extract only CSS rules that are used in the HTML"""
    
    # Split CSS into rules
    # This regex matches CSS rules including media queries
    rule_pattern = re.compile(
        r'(?:^|\n)([^{}]+)\{([^{}]+(?:\{[^{}]*\}[^{}]*)*)\}',
        re.MULTILINE | re.DOTALL
    )
    
    # Media query pattern
    media_pattern = re.compile(r'^@media[^{]+$', re.MULTILINE)
    
    # Font-face pattern
    fontface_pattern = re.compile(r'^@font-face', re.MULTILINE)
    
    # Keyframes pattern
    keyframes_pattern = re.compile(r'^@(?:-webkit-)?keyframes', re.MULTILINE)
    
    used_rules = []
    current_media = None
    
    # Add base reset styles
    reset_rules = []
    
    # Process CSS content line by line for better control
    lines = css_content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('/*'):
            if line.startswith('/*'):
                # Keep charset and important comments
                if '@charset' in line or 'Font Awesome' in line:
                    used_rules.append(lines[i])
            i += 1
            continue
            
        # Check for @font-face
        if line.startswith('@font-face'):
            # Keep all font-face rules (for FontAwesome)
            rule_content = [line]
            i += 1
            brace_count = 1
            while i < len(lines) and brace_count > 0:
                if '{' in lines[i]:
                    brace_count += lines[i].count('{')
                if '}' in lines[i]:
                    brace_count -= lines[i].count('}')
                rule_content.append(lines[i])
                i += 1
            used_rules.extend(rule_content)
            continue
            
        # Check for @media
        if line.startswith('@media'):
            media_rule = [line]
            i += 1
            # Collect the entire media query block
            brace_count = 1
            media_content = []
            while i < len(lines) and brace_count > 0:
                if '{' in lines[i]:
                    brace_count += lines[i].count('{')
                if '}' in lines[i]:
                    brace_count -= lines[i].count('}')
                if brace_count > 1:  # Inside media query
                    media_content.append(lines[i])
                elif brace_count == 1 and '}' in lines[i]:
                    # Check if any rules in media query are used
                    media_str = '\n'.join(media_content)
                    if should_keep_css_block(media_str, html_classes, html_ids, html_elements):
                        used_rules.extend(media_rule)
                        used_rules.extend(media_content)
                        used_rules.append(lines[i])
                i += 1
            continue
            
        # Check for regular CSS rules
        if line and not line.startswith('@'):
            # Get the selector
            selector_match = re.match(r'^([^{]+)\s*\{', line)
            if selector_match:
                selector = selector_match.group(1).strip()
                if should_keep_selector(selector, html_classes, html_ids, html_elements):
                    # Collect the entire rule
                    rule_content = [line]
                    i += 1
                    brace_count = 1
                    while i < len(lines) and brace_count > 0:
                        if '{' in lines[i]:
                            brace_count += lines[i].count('{')
                        if '}' in lines[i]:
                            brace_count -= lines[i].count('}')
                        rule_content.append(lines[i])
                        if brace_count == 0:
                            break
                        i += 1
                    used_rules.extend(rule_content)
                    continue
                    
        i += 1
    
    return '\n'.join(used_rules)

def should_keep_css_block(css_block, html_classes, html_ids, html_elements):
    """Check if a CSS block contains any used selectors"""
    # Look for any class, id, or element that's used
    for cls in html_classes:
        if f'.{cls}' in css_block:
            return True
    for id_name in html_ids:
        if f'#{id_name}' in css_block:
            return True
    for elem in html_elements:
        if re.search(f'\\b{elem}\\b', css_block):
            return True
    return False

def should_keep_selector(selector, html_classes, html_ids, html_elements):
    """Check if a CSS selector should be kept"""
    
    # Always keep these
    if selector in ['*', 'html', 'body', '::before', '::after', ':root']:
        return True
        
    # Keep combined html, body rules
    if 'html' in selector and 'body' in selector:
        return True
        
    # Keep reset styles (long selector lists)
    if selector.count(',') > 5:
        return True
        
    # Check for used classes
    for cls in html_classes:
        if f'.{cls}' in selector:
            return True
            
    # Check for used IDs
    for id_name in html_ids:
        if f'#{id_name}' in selector:
            return True
            
    # Check for used elements
    for elem in html_elements:
        # Match element at start, after space, after comma, or with pseudo
        if re.search(f'(^|\\s|,|>|\\+|~){elem}(\\s|:|\\.|#|\\[|,|$)', selector):
            return True
            
    # Keep attribute selectors for common attributes
    if re.search(r'\[(type|class|id|href|src|alt|title|data-)[^\]]*\]', selector):
        return True
        
    return False

# Lists from branch.html analysis
html_classes = [
    "assessment", "bar-inner", "bar1", "bar2", "bar3", "bc-wrap", "box-header-01", 
    "box-style-01", "box-undertitle-01", "branch", "branch-sec01", "branch-sec02", 
    "breadcrumb", "btn-bar", "cat", "center", "current-item", "footer-bottom-01", 
    "footer-copy-01", "footer-inner", "footer-left-01", "footer-right-01", 
    "footer-top-01", "fs14", "ft-sec02", "ft-sec03", "h-auto", "h1-title-01", 
    "h1-wrapper-01", "hd-ni-sec01", "hd-ni-sec02", "hd-ni-sec03", "header-btn", 
    "header-inner", "header-logo", "header-nav", "header-wrap", "home", "img-slot", 
    "img-wrap", "inner", "inner-detail", "inner-face", "inner-table-sp", "left", 
    "logo", "logo-inner", "main", "nav-btn", "nav-inner", "new-and-cat", "no-js", 
    "number", "page", "page-id-branch", "page-template", "page-template-branch", 
    "pc-visible", "post", "post-page", "section-style-01", "shadow", "sp-btn", 
    "sp-visible", "sub", "tel", "tel-and-time", "tel-large", "telnumber", 
    "text-center", "title", "title-inner", "txt", "unit-address-01", "unit-btn-03", 
    "unit-flex", "unit-pagetop-01", "unit-tbl-01", "unit-title-01", "unit-txt-01", 
    "voice-inner", "voice-wrapper-01", "w-full", "wrapper", "block"
]

html_ids = ["contents", "footer", "header", "navBtn"]

html_elements = [
    "html", "head", "meta", "script", "link", "title", "body", "header", "div", 
    "h1", "a", "span", "nav", "ul", "li", "p", "main", "section", "h2", "br", 
    "h3", "figure", "img", "figcaption", "table", "tbody", "tr", "th", "td", 
    "footer", "address", "strong", "small"
]

# Read CSS file
with open('nagaoka-css/common.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

# Extract used CSS
used_css = extract_used_css(css_content, html_classes, html_ids, html_elements)

# Write optimized CSS
with open('nagaoka-css/common-optimized.css', 'w', encoding='utf-8') as f:
    f.write(used_css)

print(f"Optimized CSS created: common-optimized.css")
print(f"Original size: {len(css_content)} bytes")
print(f"Optimized size: {len(used_css)} bytes")
print(f"Reduction: {100 - (len(used_css) / len(css_content) * 100):.1f}%")