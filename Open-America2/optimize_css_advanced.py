#!/usr/bin/env python3
import re
import os
import argparse
from collections import defaultdict

def extract_used_elements(html_file):
    """Extract all classes, IDs, and elements used in HTML"""
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    used_classes = set()
    used_ids = set()
    used_elements = set()
    
    # Extract classes
    class_pattern = r'class=["\']([^"\']+)["\']'
    for match in re.finditer(class_pattern, html_content):
        classes = match.group(1).split()
        used_classes.update(classes)
    
    # Extract IDs
    id_pattern = r'id=["\']([^"\']+)["\']'
    for match in re.finditer(id_pattern, html_content):
        used_ids.add(match.group(1))
    
    # Extract HTML elements
    element_pattern = r'<([a-zA-Z][a-zA-Z0-9]*)'
    for match in re.finditer(element_pattern, html_content):
        used_elements.add(match.group(1).lower())
    
    # Add commonly needed pseudo-elements
    used_elements.update(['html', 'body', '*'])
    
    return used_classes, used_ids, used_elements

def parse_css_content(css_content):
    """Parse CSS content and extract rules with better handling"""
    # Remove comments
    css_content = re.sub(r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/', '', css_content)
    
    rules = []
    
    # Handle @media queries
    media_pattern = r'(@media[^{]+)\{((?:[^{}]|\{[^}]*\})*)\}'
    media_matches = list(re.finditer(media_pattern, css_content))
    
    # Remove media queries from content for processing regular rules
    for match in reversed(media_matches):
        css_content = css_content[:match.start()] + css_content[match.end():]
    
    # Extract regular rules
    rule_pattern = r'([^{]+)\s*\{([^}]+)\}'
    for match in re.finditer(rule_pattern, css_content):
        selector = match.group(1).strip()
        styles = match.group(2).strip()
        if selector and styles:
            rules.append({'type': 'rule', 'selector': selector, 'styles': styles})
    
    # Add media queries back
    for match in media_matches:
        media_query = match.group(1).strip()
        media_content = match.group(2).strip()
        media_rules = []
        
        # Parse rules inside media query
        for rule_match in re.finditer(rule_pattern, media_content):
            selector = rule_match.group(1).strip()
            styles = rule_match.group(2).strip()
            if selector and styles:
                media_rules.append({'selector': selector, 'styles': styles})
        
        if media_rules:
            rules.append({'type': 'media', 'query': media_query, 'rules': media_rules})
    
    # Handle @keyframes
    keyframes_pattern = r'(@keyframes\s+[a-zA-Z0-9_-]+)\s*\{((?:[^{}]|\{[^}]*\})*)\}'
    for match in re.finditer(keyframes_pattern, css_content):
        rules.append({'type': 'keyframes', 'name': match.group(1), 'content': match.group(2)})
    
    return rules

def is_selector_used(selector, used_classes, used_ids, used_elements):
    """Check if a CSS selector is used with better accuracy"""
    selector = selector.strip()
    
    # Always keep certain selectors
    if selector in ['*', ':root', '::before', '::after', 'html', 'body']:
        return True
    
    # Keep @font-face
    if '@font-face' in selector:
        return True
    
    # Split compound selectors
    parts = re.split(r'[\s>+~]', selector)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Check element selectors
        element_match = re.match(r'^([a-zA-Z]+)', part)
        if element_match and element_match.group(1).lower() not in used_elements:
            return False
        
        # Check class selectors
        class_matches = re.findall(r'\.([a-zA-Z0-9_-]+)', part)
        for cls in class_matches:
            if cls in used_classes:
                return True
        
        # Check ID selectors
        id_matches = re.findall(r'#([a-zA-Z0-9_-]+)', part)
        for id_sel in id_matches:
            if id_sel in used_ids:
                return True
        
        # Check attribute selectors containing used classes/ids
        if '[' in part:
            for cls in used_classes:
                if cls in part:
                    return True
    
    # Check pseudo-class combinations
    if ':' in selector:
        base_selector = selector.split(':')[0]
        if is_selector_used(base_selector, used_classes, used_ids, used_elements):
            return True
    
    return False

def optimize_css_file(css_file, used_classes, used_ids, used_elements):
    """Optimize a single CSS file"""
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    rules = parse_css_content(css_content)
    optimized_rules = []
    
    stats = {
        'total_rules': 0,
        'kept_rules': 0,
        'removed_rules': 0
    }
    
    for rule in rules:
        if rule['type'] == 'rule':
            stats['total_rules'] += 1
            selectors = [s.strip() for s in rule['selector'].split(',')]
            used_selectors = []
            
            for selector in selectors:
                if is_selector_used(selector, used_classes, used_ids, used_elements):
                    used_selectors.append(selector)
            
            if used_selectors:
                stats['kept_rules'] += 1
                optimized_rules.append({
                    'type': 'rule',
                    'selector': ', '.join(used_selectors),
                    'styles': rule['styles']
                })
            else:
                stats['removed_rules'] += 1
                
        elif rule['type'] == 'media':
            # Process rules inside media query
            media_rules = []
            for media_rule in rule['rules']:
                selectors = [s.strip() for s in media_rule['selector'].split(',')]
                used_selectors = []
                
                for selector in selectors:
                    if is_selector_used(selector, used_classes, used_ids, used_elements):
                        used_selectors.append(selector)
                
                if used_selectors:
                    media_rules.append({
                        'selector': ', '.join(used_selectors),
                        'styles': media_rule['styles']
                    })
            
            if media_rules:
                optimized_rules.append({
                    'type': 'media',
                    'query': rule['query'],
                    'rules': media_rules
                })
                
        elif rule['type'] == 'keyframes':
            # Keep all keyframes for now (could be optimized further)
            optimized_rules.append(rule)
    
    return optimized_rules, stats

def rules_to_css(rules):
    """Convert rules back to CSS string"""
    css_parts = []
    
    for rule in rules:
        if rule['type'] == 'rule':
            css_parts.append(f"{rule['selector']} {{\n  {rule['styles']}\n}}")
        elif rule['type'] == 'media':
            media_content = []
            for media_rule in rule['rules']:
                media_content.append(f"  {media_rule['selector']} {{\n    {media_rule['styles']}\n  }}")
            css_parts.append(f"{rule['query']} {{\n" + '\n'.join(media_content) + "\n}")
        elif rule['type'] == 'keyframes':
            css_parts.append(f"{rule['name']} {{\n{rule['content']}\n}}")
    
    return '\n\n'.join(css_parts)

def main():
    parser = argparse.ArgumentParser(description="Optimize CSS files based on HTML usage.")
    parser.add_argument("html_file", help="Path to the HTML file")
    parser.add_argument("css_files", nargs='+', help="Paths to CSS files")
    args = parser.parse_args()

    html_file = args.html_file
    
    print(f"Extracting used elements from HTML file: {html_file}")
    used_classes, used_ids, used_elements = extract_used_elements(html_file)
    
    print(f"Found {len(used_classes)} unique classes")
    print(f"Found {len(used_ids)} unique IDs")
    print(f"Found {len(used_elements)} unique elements")
    
    # Start with inline styles
    optimized_css = ["""/* Critical inline styles from HTML */
a.cta_button{-moz-box-sizing:content-box !important;-webkit-box-sizing:content-box !important;box-sizing:content-box !important;vertical-align:middle}
.hs-breadcrumb-menu{list-style-type:none;margin:0px 0px 0px 0px;padding:0px 0px 0px 0px}
.hs-breadcrumb-menu-item{float:left;padding:10px 0px 10px 10px}
.hs-breadcrumb-menu-divider:before{content:'›';padding-left:10px}
.hs-featured-image-link{border:0}
.hs-featured-image{float:right;margin:0 0 20px 20px;max-width:50%}
@media (max-width: 568px){.hs-featured-image{float:none;margin:0;width:100%;max-width:100%}}
.hs-screen-reader-text{clip:rect(1px, 1px, 1px, 1px);height:1px;overflow:hidden;position:absolute !important;width:1px}"""]
    
    # Start with inline styles
    optimized_css = ["""/* Critical inline styles from HTML */
a.cta_button{-moz-box-sizing:content-box !important;-webkit-box-sizing:content-box !important;box-sizing:content-box !important;vertical-align:middle}
.hs-breadcrumb-menu{list-style-type:none;margin:0px 0px 0px 0px;padding:0px 0px 0px 0px}
.hs-breadcrumb-menu-item{float:left;padding:10px 0px 10px 10px}
.hs-breadcrumb-menu-divider:before{content:'›';padding-left:10px}
.hs-featured-image-link{border:0}
.hs-featured-image{float:right;margin:0 0 20px 20px;max-width:50%}
@media (max-width: 568px){.hs-featured-image{float:none;margin:0;width:100%;max-width:100%}}
.hs-screen-reader-text{clip:rect(1px, 1px, 1px, 1px);height:1px;overflow:hidden;position:absolute !important;width:1px}"""]
    
    # Process CSS files from arguments
    css_files_to_process = []
    for css_file_path in args.css_files:
        # Use the filename as the relative path for comments
        relative_path = os.path.basename(css_file_path)
        css_files_to_process.append((relative_path, css_file_path))

    total_original_size = 0
    total_stats = {'total_rules': 0, 'kept_rules': 0, 'removed_rules': 0}
    
    print("\nOptimizing CSS files...")
    for relative_path, css_file in css_files_to_process:
        if os.path.exists(css_file):
            print(f"\nProcessing {css_file}...")
            
            # Get original size
            with open(css_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
                total_original_size += len(original_content)
            
            # Optimize
            optimized_rules, stats = optimize_css_file(css_file, used_classes, used_ids, used_elements)
            
            # Update total stats
            for key in stats:
                total_stats[key] += stats[key]
            
            print(f"  Rules: {stats['total_rules']} total, {stats['kept_rules']} kept, {stats['removed_rules']} removed")
            
            # Add to optimized CSS
            if optimized_rules:
                optimized_css.append(f"\n/* From {relative_path} */")
                optimized_css.append(rules_to_css(optimized_rules))
    
    # Save optimized CSS
    optimized_content = '\n'.join(optimized_css)
    optimized_file = 'optimized.css'  # Save in the current working directory
    
    with open(optimized_file, 'w', encoding='utf-8') as f:
        f.write(optimized_content)
    
    optimized_size = len(optimized_content)
    reduction = (1 - optimized_size / total_original_size) * 100 if total_original_size > 0 else 0
    
    print(f"\n=== Optimization Summary ===")
    print(f"Total rules analyzed: {total_stats['total_rules']}")
    print(f"Rules kept: {total_stats['kept_rules']} ({total_stats['kept_rules']/total_stats['total_rules']*100:.1f}%)")
    print(f"Rules removed: {total_stats['removed_rules']} ({total_stats['removed_rules']/total_stats['total_rules']*100:.1f}%)")
    print(f"\nOriginal CSS size: {total_original_size:,} bytes ({total_original_size/1024:.1f} KB)")
    print(f"Optimized CSS size: {optimized_size:,} bytes ({optimized_size/1024:.1f} KB)")
    print(f"Size reduction: {reduction:.1f}% ({(total_original_size-optimized_size)/1024:.1f} KB saved)")
    print(f"\nOptimized CSS saved to: {optimized_file}")

if __name__ == "__main__":
    main()