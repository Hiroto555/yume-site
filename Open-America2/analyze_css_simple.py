#!/usr/bin/env python3
import re
import os
from collections import defaultdict

def extract_used_classes_and_ids(html_file):
    """Extract all classes and IDs used in the HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    used_classes = set()
    used_ids = set()
    
    # Extract classes using regex
    class_pattern = r'class=["\']([^"\']+)["\']'
    for match in re.finditer(class_pattern, html_content):
        classes = match.group(1).split()
        used_classes.update(classes)
    
    # Extract IDs using regex
    id_pattern = r'id=["\']([^"\']+)["\']'
    for match in re.finditer(id_pattern, html_content):
        used_ids.add(match.group(1))
    
    # Look for JavaScript classes (js-* pattern)
    js_class_pattern = r'js-[a-zA-Z0-9_-]+'
    for match in re.finditer(js_class_pattern, html_content):
        used_classes.add(match.group(0))
    
    return used_classes, used_ids

def extract_css_selectors(css_content):
    """Extract selectors from CSS content"""
    # Remove comments
    css_content = re.sub(r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/', '', css_content)
    
    # Find all CSS rules
    rule_pattern = r'([^{]+)\s*\{([^}]+)\}'
    selectors = {}
    
    for match in re.finditer(rule_pattern, css_content):
        selector = match.group(1).strip()
        styles = match.group(2).strip()
        
        # Split multiple selectors
        for sel in selector.split(','):
            sel = sel.strip()
            if sel and not sel.startswith('@'):
                selectors[sel] = styles
    
    return selectors

def check_selector_usage(selector, used_classes, used_ids):
    """Check if a selector is used based on HTML classes and IDs"""
    # Always keep universal selectors and element selectors
    if selector == '*' or re.match(r'^[a-zA-Z]+$', selector):
        return True
    
    # Always keep :root
    if selector == ':root':
        return True
    
    # Check class selectors
    class_matches = re.findall(r'\.([a-zA-Z0-9_-]+)', selector)
    for cls in class_matches:
        if cls in used_classes:
            return True
    
    # Check ID selectors
    id_matches = re.findall(r'#([a-zA-Z0-9_-]+)', selector)
    for id_sel in id_matches:
        if id_sel in used_ids:
            return True
    
    # Check attribute selectors
    if '[' in selector and ']' in selector:
        # Keep common attribute selectors
        if 'type=' in selector or 'href' in selector:
            return True
    
    return False

def analyze_css_file(css_file, used_classes, used_ids):
    """Analyze a single CSS file"""
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    original_size = len(css_content)
    selectors = extract_css_selectors(css_content)
    
    used_selectors = {}
    unused_selectors = {}
    
    for selector, styles in selectors.items():
        if check_selector_usage(selector, used_classes, used_ids):
            used_selectors[selector] = styles
        else:
            unused_selectors[selector] = styles
    
    return {
        'file': css_file,
        'original_size': original_size,
        'total_selectors': len(selectors),
        'used_selectors': used_selectors,
        'unused_selectors': unused_selectors,
        'usage_rate': len(used_selectors) / len(selectors) * 100 if selectors else 0
    }

def create_optimized_css(css_analyses, used_classes, used_ids):
    """Create optimized CSS with only used styles"""
    optimized_css = []
    
    # Add critical inline styles from HTML
    optimized_css.append("""/* Critical inline styles from HTML */
a.cta_button{-moz-box-sizing:content-box !important;-webkit-box-sizing:content-box !important;box-sizing:content-box !important;vertical-align:middle}
.hs-breadcrumb-menu{list-style-type:none;margin:0px 0px 0px 0px;padding:0px 0px 0px 0px}
.hs-breadcrumb-menu-item{float:left;padding:10px 0px 10px 10px}
.hs-breadcrumb-menu-divider:before{content:'›';padding-left:10px}
.hs-featured-image-link{border:0}
.hs-featured-image{float:right;margin:0 0 20px 20px;max-width:50%}
@media (max-width: 568px){.hs-featured-image{float:none;margin:0;width:100%;max-width:100%}}
.hs-screen-reader-text{clip:rect(1px, 1px, 1px, 1px);height:1px;overflow:hidden;position:absolute !important;width:1px}
""")
    
    # Process each CSS file
    for analysis in css_analyses:
        if analysis['used_selectors']:
            filename = os.path.basename(analysis['file'])
            optimized_css.append(f"\n/* From {filename} */")
            
            # Group selectors with same styles
            styles_to_selectors = defaultdict(list)
            for selector, styles in analysis['used_selectors'].items():
                styles_to_selectors[styles].append(selector)
            
            # Write grouped selectors
            for styles, selectors in styles_to_selectors.items():
                combined_selector = ', '.join(selectors)
                optimized_css.append(f"{combined_selector} {{\n{styles}\n}}")
    
    return '\n'.join(optimized_css)

def main():
    base_path = '/Users/shiroto/Desktop/YumeHouse-Website/Open-America2'
    html_file = os.path.join(base_path, 'open2.html')
    
    print("Extracting used classes and IDs from HTML...")
    used_classes, used_ids = extract_used_classes_and_ids(html_file)
    
    print(f"Found {len(used_classes)} unique classes")
    print(f"Found {len(used_ids)} unique IDs")
    
    css_files = [
        os.path.join(base_path, 'styles/vendor/module_.min.css'),
        os.path.join(base_path, 'styles/vendor/template_swiper-bundle.min.css'),
        os.path.join(base_path, 'styles/vendor/template_oh2022-style.min.css'),
        os.path.join(base_path, 'styles/vendor/module_MV.min.css'),
        os.path.join(base_path, 'styles/custom.css')
    ]
    
    print("\nAnalyzing CSS files...")
    css_analyses = []
    total_original_size = 0
    
    for css_file in css_files:
        if os.path.exists(css_file):
            analysis = analyze_css_file(css_file, used_classes, used_ids)
            css_analyses.append(analysis)
            total_original_size += analysis['original_size']
            
            print(f"\n{os.path.basename(css_file)}:")
            print(f"  Total selectors: {analysis['total_selectors']}")
            print(f"  Used selectors: {len(analysis['used_selectors'])}")
            print(f"  Unused selectors: {len(analysis['unused_selectors'])}")
            print(f"  Usage rate: {analysis['usage_rate']:.1f}%")
    
    # Create optimized CSS
    print("\nCreating optimized CSS...")
    optimized_css = create_optimized_css(css_analyses, used_classes, used_ids)
    
    # Save optimized CSS
    optimized_file = os.path.join(base_path, 'styles/optimized.css')
    with open(optimized_file, 'w', encoding='utf-8') as f:
        f.write(optimized_css)
    
    optimized_size = len(optimized_css)
    reduction = (1 - optimized_size / total_original_size) * 100
    
    print(f"\nOptimization complete!")
    print(f"Original total CSS size: {total_original_size:,} bytes")
    print(f"Optimized CSS size: {optimized_size:,} bytes")
    print(f"Size reduction: {reduction:.1f}%")
    print(f"Saved to: {optimized_file}")

if __name__ == "__main__":
    main()