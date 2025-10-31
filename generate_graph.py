#!/usr/bin/env python3
"""
Generate visual graph from README.md links
"""

import re
import json

def parse_readme():
    """Parse README.md and extract links organized by topics"""
    
    with open('README.md', 'r') as f:
        content = f.read()
    
    # Extract sections and links
    sections = {}
    current_section = None
    current_subsection = None
    
    lines = content.split('\n')
    
    for line in lines:
        # Main sections (## )
        if line.startswith('## '):
            current_section = line[3:].strip()
            sections[current_section] = {}
            current_subsection = None
            
        # Subsections (### )
        elif line.startswith('### '):
            if current_section:
                current_subsection = line[4:].strip()
                sections[current_section][current_subsection] = []
                
        # Links (- [title](url))
        elif line.startswith('- [') and current_section and current_subsection:
            match = re.match(r'- \[([^\]]+)\]\(([^)]+)\)', line)
            if match:
                title, url = match.groups()
                # Clean title (remove description after " - ")
                clean_title = title.split(' - ')[0]
                sections[current_section][current_subsection].append({
                    'name': clean_title,
                    'url': url
                })
    
    return sections

def create_d3_data(sections):
    """Convert sections to D3 hierarchical data"""
    
    children = []
    
    for section_name, subsections in sections.items():
        if not subsections:  # Skip empty sections
            continue
            
        section_children = []
        
        for subsection_name, links in subsections.items():
            if links:  # Only add subsections with links
                subsection_data = {
                    'name': subsection_name,
                    'children': links
                }
                section_children.append(subsection_data)
        
        if section_children:  # Only add sections with content
            section_data = {
                'name': section_name,
                'children': section_children
            }
            children.append(section_data)
    
    return {
        'name': 'ML Resources',
        'children': children
    }

def update_graph_html(data):
    """Update graph.html with new data"""
    
    # Read current HTML
    with open('graph.html', 'r') as f:
        html_content = f.read()
    
    # Create new data section with proper indentation for sunburst
    data_js = f"        const data = {json.dumps(data, indent=12)};"
    
    # Find the data section more reliably
    start_marker = "        const data = {"
    start_idx = html_content.find(start_marker)
    
    if start_idx == -1:
        print("❌ Could not find data section in graph.html")
        return
    
    # Find the end of the data object by counting braces
    brace_count = 0
    end_idx = start_idx
    found_first_brace = False
    
    for i in range(start_idx, len(html_content)):
        char = html_content[i]
        if char == '{':
            brace_count += 1
            found_first_brace = True
        elif char == '}':
            brace_count -= 1
            if found_first_brace and brace_count == 0:
                # Find the semicolon after the closing brace
                semicolon_idx = html_content.find(';', i)
                if semicolon_idx != -1:
                    end_idx = semicolon_idx + 1
                else:
                    end_idx = i + 1
                break
    
    # Replace the data section
    updated_html = html_content[:start_idx] + data_js + html_content[end_idx:]
    
    # Write updated HTML
    with open('graph.html', 'w') as f:
        f.write(updated_html)
    
    print("✅ Sunburst graph updated! Open graph.html in your browser to view.")

if __name__ == "__main__":
    print("📊 Generating graph from README.md...")
    
    sections = parse_readme()
    data = create_d3_data(sections)
    update_graph_html(data)
    
    print(f"📈 Found {len(data['children'])} main sections")
    for section in data['children']:
        subsection_count = len(section['children'])
        link_count = sum(len(sub['children']) for sub in section['children'])
        print(f"  - {section['name']}: {subsection_count} subsections, {link_count} links")
