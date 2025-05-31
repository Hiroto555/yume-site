#!/usr/bin/env python3
import re
import os

# Classes and IDs used in branch.html
used_classes = [
    'assessment', 'bar-inner', 'bar1', 'bar2', 'bar3', 'bc-wrap', 'block', 'box-header-01', 
    'box-style-01', 'box-undertitle-01', 'branch', 'branch-sec01', 'branch-sec02', 'breadcrumb', 
    'btn-bar', 'btn-inner', 'cat', 'center', 'current-item', 'footer-bottom-01', 'footer-copy-01', 
    'footer-inner', 'footer-left-01', 'footer-right-01', 'footer-top-01', 'fs14', 'ft-sec02', 
    'ft-sec03', 'h-auto', 'h1-title-01', 'h1-wrapper-01', 'hd-ni-sec01', 'hd-ni-sec02', 'hd-ni-sec03', 
    'header-btn', 'header-inner', 'header-logo', 'header-nav', 'header-wrap', 'home', 'img-slot', 
    'img-wrap', 'inner', 'inner-detail', 'inner-face', 'inner-table-sp', 'left', 'logo', 'logo-inner', 
    'main', 'nav-btn', 'nav-inner', 'new-and-cat', 'no-js', 'number', 'oneminute', 'page', 
    'page-id-branch', 'page-template', 'page-template-branch', 'pc-visible', 'post', 'post-page', 
    'section-style-01', 'shadow', 'sp-btn', 'sp-visible', 'sub', 'tel', 'tel-and-time', 'tel-large', 
    'telnumber', 'title', 'title-inner', 'txt', 'unit-address-01', 'unit-btn-03', 'unit-flex', 
    'unit-pagetop-01', 'unit-tbl-01', 'unit-title-01', 'unit-txt-01', 'voice-inner', 'voice-wrapper-01', 
    'w-full', 'wrapper'
]

used_ids = ['contents', 'footer', 'header', 'navBtn']

# Function to extract detailed CSS selectors from a file
def analyze_css_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    # Extract all CSS rules with their selectors
    rules = []
    lines = content.split('\n')
    current_rule = ""
    brace_count = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if '{' in line and not line.startswith('@'):
            # Start of a CSS rule
            selector = line.split('{')[0].strip()
            if selector:
                rules.append(selector)
    
    return rules

def check_selector_usage(selector, used_classes, used_ids):
    """Check if a CSS selector is used in the HTML"""
    # Extract class names from selector
    class_matches = re.findall(r'\.([a-zA-Z0-9_-]+)', selector)
    id_matches = re.findall(r'#([a-zA-Z0-9_-]+)', selector)
    
    # Check if any class or ID in the selector is used
    for cls in class_matches:
        if cls in used_classes:
            return True
    
    for id_name in id_matches:
        if id_name in used_ids:
            return True
    
    # Check for pseudo-elements, media queries, etc that might be used
    if any(pseudo in selector for pseudo in [':hover', ':focus', ':active', ':before', ':after', '::before', '::after']):
        # For pseudo-selectors, check if the base class/id is used
        base_selector = re.sub(r':[a-zA-Z-]+(\([^)]*\))?', '', selector)
        return check_selector_usage(base_selector, used_classes, used_ids)
    
    return False

# Analyze each CSS file
css_files = ['common.css', 'add_an.css', 'add_ty.css', 'branch-custom.css']
base_path = '/Users/shiroto/Desktop/YumeHouse-Website/branch/nagaoka-css/'

print("=== DETAILED CSS ANALYSIS FOR BRANCH.HTML ===\n")

total_rules = 0
total_unused = 0
file_results = {}

for css_file in css_files:
    file_path = os.path.join(base_path, css_file)
    if os.path.exists(file_path):
        print(f"=== {css_file} ===")
        rules = analyze_css_file(file_path)
        
        used_rules = []
        unused_rules = []
        
        for rule in rules:
            if check_selector_usage(rule, used_classes, used_ids):
                used_rules.append(rule)
            else:
                unused_rules.append(rule)
        
        print(f"Total rules: {len(rules)}")
        print(f"Used rules: {len(used_rules)}")
        print(f"Unused rules: {len(unused_rules)}")
        print(f"Usage rate: {len(used_rules)/len(rules)*100:.1f}%")
        
        file_results[css_file] = {
            'total': len(rules),
            'used': len(used_rules),
            'unused': len(unused_rules),
            'unused_rules': unused_rules
        }
        
        total_rules += len(rules)
        total_unused += len(unused_rules)
        
        print()

print("=== SUMMARY ===")
print(f"Total CSS rules across all files: {total_rules}")
print(f"Total unused rules: {total_unused}")
print(f"Overall usage rate: {(total_rules-total_unused)/total_rules*100:.1f}%")

print("\n=== RECOMMENDATIONS ===")
for css_file, data in file_results.items():
    if data['unused'] > 0:
        print(f"\n{css_file}: Remove {data['unused']} unused rules ({data['unused']/data['total']*100:.1f}% of file)")
        if css_file == 'branch-custom.css':
            print("  This file is specifically for branch page - keep all rules")
        elif data['unused'] > 50:
            print(f"  High cleanup potential - first 10 unused rules:")
            for rule in data['unused_rules'][:10]:
                print(f"    {rule}")
        else:
            print("  Unused rules:")
            for rule in data['unused_rules']:
                print(f"    {rule}")

# Check for critical classes that might be missing definitions
print(f"\n=== MISSING DEFINITIONS ===")
missing_classes = []
for css_file in css_files:
    file_path = os.path.join(base_path, css_file)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for cls in used_classes:
            if f'.{cls}' not in content:
                missing_classes.append(cls)

# Remove duplicates
missing_classes = list(set(missing_classes))
if missing_classes:
    print("Classes used in HTML but not defined in any CSS file:")
    for cls in sorted(missing_classes):
        print(f"  .{cls}")
else:
    print("All classes used in HTML are defined in CSS files.")