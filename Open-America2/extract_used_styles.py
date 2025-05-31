#!/usr/bin/env python3
import re
from bs4 import BeautifulSoup
import os
import cssutils
import logging
from collections import defaultdict

# Suppress cssutils warnings
cssutils.log.setLevel(logging.ERROR)

def extract_used_classes_and_ids(html_file):
    """Extract all classes and IDs used in the HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    used_classes = set()
    used_ids = set()
    
    # Extract classes
    for element in soup.find_all(class_=True):
        classes = element.get('class', [])
        for cls in classes:
            used_classes.add(cls)
    
    # Extract IDs
    for element in soup.find_all(id=True):
        used_ids.add(element['id'])
    
    # Also extract classes from JavaScript (e.g., js-* classes)
    script_content = str(soup)
    js_class_pattern = r'["\']([a-zA-Z0-9_-]+(?:--[a-zA-Z0-9_-]+)*)["\']'
    potential_classes = re.findall(js_class_pattern, script_content)
    
    # Filter to keep only those that look like CSS classes
    for cls in potential_classes:
        if re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*(?:--[a-zA-Z0-9_-]+)*$', cls):
            if cls in script_content and ('addClass' in script_content or 'classList' in script_content or 'className' in script_content):
                used_classes.add(cls)
    
    return used_classes, used_ids

def parse_css_file(css_file):
    """Parse CSS file and extract all selectors"""
    selectors = defaultdict(list)
    
    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Parse CSS
        sheet = cssutils.parseString(css_content)
        
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                selector_text = rule.selectorText
                selectors[selector_text].append({
                    'file': css_file,
                    'styles': rule.style.cssText
                })
    except Exception as e:
        print(f"Error parsing {css_file}: {e}")
    
    return selectors

def analyze_css_usage(html_file, css_files):
    """Analyze which CSS rules are actually used"""
    used_classes, used_ids = extract_used_classes_and_ids(html_file)
    
    print(f"Found {len(used_classes)} unique classes used in HTML")
    print(f"Found {len(used_ids)} unique IDs used in HTML")
    
    # Analyze each CSS file
    all_selectors = {}
    for css_file in css_files:
        selectors = parse_css_file(css_file)
        all_selectors.update(selectors)
    
    # Check which selectors are used
    used_selectors = set()
    unused_selectors = set()
    
    for selector in all_selectors:
        is_used = False
        
        # Check for class selectors
        class_matches = re.findall(r'\.([a-zA-Z0-9_-]+(?:--[a-zA-Z0-9_-]+)*)', selector)
        for cls in class_matches:
            if cls in used_classes:
                is_used = True
                break
        
        # Check for ID selectors
        id_matches = re.findall(r'#([a-zA-Z0-9_-]+)', selector)
        for id_sel in id_matches:
            if id_sel in used_ids:
                is_used = True
                break
        
        # Check for element selectors (always keep)
        if re.match(r'^[a-zA-Z]+', selector.strip()):
            is_used = True
        
        # Keep pseudo-classes and pseudo-elements related to used classes
        if ':' in selector:
            base_selector = selector.split(':')[0]
            for cls in used_classes:
                if f'.{cls}' in base_selector:
                    is_used = True
                    break
        
        # Keep @rules (media queries, keyframes, etc.)
        if selector.startswith('@'):
            is_used = True
        
        if is_used:
            used_selectors.add(selector)
        else:
            unused_selectors.add(selector)
    
    return used_classes, used_ids, used_selectors, unused_selectors, all_selectors

def main():
    base_path = '/Users/shiroto/Desktop/YumeHouse-Website/Open-America2'
    html_file = os.path.join(base_path, 'open2.html')
    
    css_files = [
        os.path.join(base_path, 'styles/vendor/module_.min.css'),
        os.path.join(base_path, 'styles/vendor/template_swiper-bundle.min.css'),
        os.path.join(base_path, 'styles/vendor/template_oh2022-style.min.css'),
        os.path.join(base_path, 'styles/vendor/module_MV.min.css'),
        os.path.join(base_path, 'styles/custom.css')
    ]
    
    print("Analyzing CSS usage...")
    used_classes, used_ids, used_selectors, unused_selectors, all_selectors = analyze_css_usage(html_file, css_files)
    
    print(f"\nTotal selectors: {len(all_selectors)}")
    print(f"Used selectors: {len(used_selectors)}")
    print(f"Unused selectors: {len(unused_selectors)}")
    print(f"Usage rate: {len(used_selectors) / len(all_selectors) * 100:.1f}%")
    
    # Save results
    with open(os.path.join(base_path, 'css_analysis.txt'), 'w', encoding='utf-8') as f:
        f.write("=== USED CLASSES ===\n")
        for cls in sorted(used_classes):
            f.write(f"{cls}\n")
        
        f.write("\n=== USED IDS ===\n")
        for id_val in sorted(used_ids):
            f.write(f"{id_val}\n")
        
        f.write("\n=== UNUSED SELECTORS ===\n")
        for selector in sorted(unused_selectors):
            f.write(f"{selector}\n")

if __name__ == "__main__":
    main()