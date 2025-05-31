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

# Function to extract CSS selectors from a file
def extract_css_selectors(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract class selectors (simplified)
    class_selectors = re.findall(r'\.([a-zA-Z0-9_-]+)', content)
    
    # Extract ID selectors  
    id_selectors = re.findall(r'#([a-zA-Z0-9_-]+)', content)
    
    return set(class_selectors), set(id_selectors)

# Analyze each CSS file
css_files = ['common.css', 'add_an.css', 'add_ty.css', 'branch-custom.css']
base_path = '/Users/shiroto/Desktop/YumeHouse-Website/branch/nagaoka-css/'

all_css_classes = set()
all_css_ids = set()
file_analysis = {}

for css_file in css_files:
    file_path = os.path.join(base_path, css_file)
    if os.path.exists(file_path):
        classes, ids = extract_css_selectors(file_path)
        all_css_classes.update(classes)
        all_css_ids.update(ids)
        file_analysis[css_file] = {'classes': classes, 'ids': ids}
        print(f"\n=== {css_file} ===")
        print(f"Classes defined: {len(classes)}")
        print(f"IDs defined: {len(ids)}")

# Find unused classes and IDs
unused_classes = all_css_classes - set(used_classes)
unused_ids = all_css_ids - set(used_ids)

print(f"\n=== SUMMARY ===")
print(f"Total CSS classes defined: {len(all_css_classes)}")
print(f"Total CSS IDs defined: {len(all_css_ids)}")
print(f"Classes used in HTML: {len(used_classes)}")
print(f"IDs used in HTML: {len(used_ids)}")
print(f"Unused classes: {len(unused_classes)}")
print(f"Unused IDs: {len(unused_ids)}")

print(f"\n=== UNUSED CLASSES ===")
for cls in sorted(unused_classes):
    print(f".{cls}")

print(f"\n=== UNUSED IDS ===")
for id_name in sorted(unused_ids):
    print(f"#{id_name}")

# Check which files contain which unused rules
print(f"\n=== UNUSED RULES BY FILE ===")
for css_file, data in file_analysis.items():
    unused_in_file = data['classes'] & unused_classes
    if unused_in_file:
        print(f"\n{css_file}:")
        for cls in sorted(unused_in_file):
            print(f"  .{cls}")