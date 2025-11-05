#!/usr/bin/env python3
"""
Test HTML files for rendering issues and validation
"""

import os
import re
import json
import sys

def test_file_exists(filepath):
    """Test if file exists"""
    if not os.path.exists(filepath):
        print(f"❌ {filepath} does not exist")
        return False
    print(f"✅ {filepath} exists")
    return True

def test_html_structure(filepath):
    """Test basic HTML structure"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for basic HTML structure
        if not re.search(r'<!DOCTYPE html>', content, re.IGNORECASE):
            print(f"❌ {filepath} missing DOCTYPE")
            return False
        
        if not re.search(r'<html.*?>', content, re.IGNORECASE):
            print(f"❌ {filepath} missing <html> tag")
            return False
        
        if not re.search(r'<head.*?>.*?</head>', content, re.IGNORECASE | re.DOTALL):
            print(f"❌ {filepath} missing <head> section")
            return False
        
        if not re.search(r'<body.*?>.*?</body>', content, re.IGNORECASE | re.DOTALL):
            print(f"❌ {filepath} missing <body> section")
            return False
        
        print(f"✅ {filepath} has valid HTML structure")
        return True
        
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return False

def test_d3_integration(filepath):
    """Test D3.js integration in graph.html"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for D3.js script
        if not re.search(r'd3js\.org|d3\.v\d+\.min\.js', content):
            print(f"❌ {filepath} missing D3.js script")
            return False
        
        # Check for data object
        if not re.search(r'const data = \{', content):
            print(f"❌ {filepath} missing data object")
            return False
        
        # Check for SVG creation
        if not re.search(r'\.append\(["\']svg["\']\)', content):
            print(f"❌ {filepath} missing SVG creation")
            return False
        
        # Check for both visualizations
        if not re.search(r'sunburst|partition', content, re.IGNORECASE):
            print(f"❌ {filepath} missing sunburst visualization")
            return False
        
        if not re.search(r'bubble|pack', content, re.IGNORECASE):
            print(f"❌ {filepath} missing bubble visualization")
            return False
        
        print(f"✅ {filepath} has valid D3.js integration")
        return True
        
    except Exception as e:
        print(f"❌ Error testing D3 integration in {filepath}: {e}")
        return False

def test_data_structure():
    """Test that generate_graph.py produces valid data"""
    try:
        # Run the graph generator
        import subprocess
        result = subprocess.run(['python3', 'generate_graph.py'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ generate_graph.py failed: {result.stderr}")
            return False
        
        print("✅ generate_graph.py runs successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error running generate_graph.py: {e}")
        return False

def test_links_in_readme():
    """Test that README.md has valid link structure"""
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all markdown links
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        
        if len(links) < 10:
            print(f"❌ README.md has too few links ({len(links)})")
            return False
        
        # Check for required sections
        required_sections = ['Learning Resources', 'Tools', 'Datasets', 'Research Papers']
        for section in required_sections:
            if section not in content:
                print(f"❌ README.md missing section: {section}")
                return False
        
        print(f"✅ README.md has {len(links)} links and required sections")
        return True
        
    except Exception as e:
        print(f"❌ Error testing README.md: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running HTML rendering tests...\n")
    
    tests = [
        ("File existence - index.html", lambda: test_file_exists('index.html')),
        ("File existence - graph.html", lambda: test_file_exists('graph.html')),
        ("File existence - README.md", lambda: test_file_exists('README.md')),
        ("HTML structure - index.html", lambda: test_html_structure('index.html')),
        ("HTML structure - graph.html", lambda: test_html_structure('graph.html')),
        ("D3.js integration - graph.html", lambda: test_d3_integration('graph.html')),
        ("Data generation", test_data_structure),
        ("README links", test_links_in_readme),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"   Test failed!")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("💥 Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
