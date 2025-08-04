#!/usr/bin/env python3
"""
Link Checker for Markdown Files
Validates external URLs, local file references, and internal anchors in markdown files.
"""

import os
import re
import requests
import urllib.parse
from pathlib import Path
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from datetime import datetime
import time

@dataclass
class LinkResult:
    """Represents the result of checking a single link"""
    url: str
    status: str  # 'success', 'broken', 'warning'
    error_message: str = ""
    status_code: int = None
    redirect_url: str = None

@dataclass
class FileResult:
    """Represents all link results for a single file"""
    file_path: str
    links: List[Tuple[int, str, LinkResult]]  # (line_number, link_text, result)

class MarkdownLinkChecker:
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.timeout = 10
        self.max_retries = 2
        
    def extract_links_from_markdown(self, file_path: Path) -> List[Tuple[int, str, str]]:
        """Extract all links from a markdown file with line numbers"""
        links = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line_num, line in enumerate(lines, 1):
                # Markdown link pattern: [text](url)
                markdown_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', line)
                for text, url in markdown_links:
                    links.append((line_num, f"[{text}]({url})", url.strip()))
                
                # Direct URL pattern: http(s)://...
                direct_urls = re.findall(r'<?(https?://[^\s>]+)>?', line)
                for url in direct_urls:
                    if not any(url in existing_url for _, _, existing_url in links if line_num == _):
                        links.append((line_num, url, url.strip()))
                
                # Image references: ![alt](path)
                image_links = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', line)
                for alt, url in image_links:
                    links.append((line_num, f"![{alt}]({url})", url.strip()))
        
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            
        return links
    
    def check_external_url(self, url: str) -> LinkResult:
        """Check if an external URL is accessible"""
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.head(url, timeout=self.timeout, allow_redirects=True)
                
                if response.status_code < 400:
                    redirect_info = response.url if response.url != url else None
                    return LinkResult(
                        url=url,
                        status='success',
                        status_code=response.status_code,
                        redirect_url=redirect_info
                    )
                else:
                    # Try GET request if HEAD fails
                    response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
                    if response.status_code < 400:
                        redirect_info = response.url if response.url != url else None
                        return LinkResult(
                            url=url,
                            status='success',
                            status_code=response.status_code,
                            redirect_url=redirect_info
                        )
                    else:
                        return LinkResult(
                            url=url,
                            status='broken',
                            error_message=f"HTTP {response.status_code}",
                            status_code=response.status_code
                        )
                        
            except requests.exceptions.Timeout:
                if attempt < self.max_retries:
                    time.sleep(1)
                    continue
                return LinkResult(
                    url=url,
                    status='broken',
                    error_message="Request timeout"
                )
            except requests.exceptions.ConnectionError:
                if attempt < self.max_retries:
                    time.sleep(1)
                    continue
                return LinkResult(
                    url=url,
                    status='broken',
                    error_message="Connection error"
                )
            except Exception as e:
                return LinkResult(
                    url=url,
                    status='broken',
                    error_message=f"Error: {str(e)}"
                )
        
        return LinkResult(url=url, status='broken', error_message="Max retries exceeded")
    
    def check_local_file(self, file_path: str, current_file: Path) -> LinkResult:
        """Check if a local file exists"""
        try:
            # Handle relative paths
            if file_path.startswith('../'):
                # Resolve relative to current file's directory
                target_path = (current_file.parent / file_path).resolve()
            elif file_path.startswith('./'):
                target_path = (current_file.parent / file_path[2:]).resolve()
            else:
                # Assume relative to current file's directory
                target_path = (current_file.parent / file_path).resolve()
            
            if target_path.exists():
                return LinkResult(
                    url=file_path,
                    status='success'
                )
            else:
                return LinkResult(
                    url=file_path,
                    status='broken',
                    error_message=f"File not found: {target_path}"
                )
                
        except Exception as e:
            return LinkResult(
                url=file_path,
                status='broken',
                error_message=f"Path resolution error: {str(e)}"
            )
    
    def check_internal_anchor(self, anchor: str, file_path: Path) -> LinkResult:
        """Check if an internal anchor exists in the file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Convert anchor to expected header format
            anchor_clean = anchor.lstrip('#').lower().replace(' ', '-').replace('_', '-')
            
            # Find all headers in the markdown
            headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
            header_anchors = [h.lower().replace(' ', '-').replace('_', '-') for h in headers]
            
            if anchor_clean in header_anchors:
                return LinkResult(
                    url=anchor,
                    status='success'
                )
            else:
                return LinkResult(
                    url=anchor,
                    status='broken',
                    error_message=f"Anchor not found in document"
                )
                
        except Exception as e:
            return LinkResult(
                url=anchor,
                status='broken',
                error_message=f"Error checking anchor: {str(e)}"
            )
    
    def categorize_and_check_link(self, url: str, current_file: Path) -> LinkResult:
        """Categorize link type and check it accordingly"""
        url = url.strip()
        
        # External URLs
        if url.startswith(('http://', 'https://')):
            return self.check_external_url(url)
        
        # Internal anchors
        elif url.startswith('#'):
            return self.check_internal_anchor(url, current_file)
        
        # Local files (relative paths)
        elif url.startswith(('../', './', '/')):
            return self.check_local_file(url, current_file)
        
        # Assume local file if no protocol
        else:
            return self.check_local_file(url, current_file)
    
    def check_file(self, file_path: Path) -> FileResult:
        """Check all links in a single markdown file"""
        print(f"Checking {file_path}...")
        
        links = self.extract_links_from_markdown(file_path)
        results = []
        
        for line_num, link_text, url in links:
            result = self.categorize_and_check_link(url, file_path)
            results.append((line_num, link_text, result))
            
            # Brief pause to be respectful to external servers
            if result.url.startswith(('http://', 'https://')):
                time.sleep(0.1)
        
        return FileResult(file_path=str(file_path), links=results)
    
    def check_directory(self, directory: str = "labs") -> List[FileResult]:
        """Check all markdown files in a directory"""
        results = []
        md_files = list(Path(directory).glob("*.md"))
        
        if not md_files:
            print(f"No markdown files found in {directory}")
            return results
        
        print(f"Found {len(md_files)} markdown files to check...")
        
        for md_file in sorted(md_files):
            results.append(self.check_file(md_file))
        
        return results
    
    def generate_report(self, results: List[FileResult]) -> str:
        """Generate a markdown report from the results"""
        report = []
        report.append("# Link Checker Report")
        report.append(f"\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary statistics
        total_links = sum(len(file_result.links) for file_result in results)
        broken_links = sum(1 for file_result in results for _, _, link_result in file_result.links if link_result.status == 'broken')
        success_links = total_links - broken_links
        
        report.append("## Summary")
        report.append(f"- **Total files checked:** {len(results)}")
        report.append(f"- **Total links found:** {total_links}")
        report.append(f"- **Successful links:** {success_links}")
        report.append(f"- **Broken links:** {broken_links}")
        report.append(f"- **Success rate:** {(success_links/total_links*100):.1f}%" if total_links > 0 else "- **Success rate:** N/A")
        report.append("")
        
        # Categorize links by type
        external_links = []
        local_file_links = []
        anchor_links = []
        
        for file_result in results:
            for line_num, link_text, link_result in file_result.links:
                if link_result.url.startswith(('http://', 'https://')):
                    external_links.append((file_result.file_path, line_num, link_text, link_result))
                elif link_result.url.startswith('#'):
                    anchor_links.append((file_result.file_path, line_num, link_text, link_result))
                else:
                    local_file_links.append((file_result.file_path, line_num, link_text, link_result))
        
        # Link type summary
        report.append("## Link Types Summary")
        report.append(f"- **External URLs:** {len(external_links)}")
        report.append(f"- **Local files:** {len(local_file_links)}")
        report.append(f"- **Internal anchors:** {len(anchor_links)}")
        report.append("")
        
        # Detailed results by file
        report.append("## Detailed Results by File")
        report.append("")
        
        for file_result in results:
            report.append(f"### {file_result.file_path}")
            
            if not file_result.links:
                report.append("*No links found in this file.*")
                report.append("")
                continue
            
            file_broken = [link for _, _, link in file_result.links if link.status == 'broken']
            file_success = len(file_result.links) - len(file_broken)
            
            report.append(f"- **Total links:** {len(file_result.links)}")
            report.append(f"- **Successful:** {file_success}")
            report.append(f"- **Broken:** {len(file_broken)}")
            report.append("")
            
            if file_broken:
                report.append("#### Broken Links:")
                for line_num, link_text, link_result in file_result.links:
                    if link_result.status == 'broken':
                        report.append(f"- **Line {line_num}:** `{link_text}`")
                        report.append(f"  - **Error:** {link_result.error_message}")
                        if link_result.status_code:
                            report.append(f"  - **Status Code:** {link_result.status_code}")
                        report.append("")
        
        # Broken links summary
        if broken_links > 0:
            report.append("## All Broken Links Summary")
            report.append("")
            
            for file_result in results:
                file_broken_links = [(line_num, link_text, link_result) for line_num, link_text, link_result in file_result.links if link_result.status == 'broken']
                
                if file_broken_links:
                    report.append(f"### {file_result.file_path}")
                    for line_num, link_text, link_result in file_broken_links:
                        report.append(f"- **Line {line_num}:** `{link_result.url}`")
                        report.append(f"  - **Error:** {link_result.error_message}")
                        report.append("")
        
        # External URL details
        if external_links:
            report.append("## External URLs Details")
            report.append("")
            
            external_broken = [link for link in external_links if link[3].status == 'broken']
            external_success = len(external_links) - len(external_broken)
            
            report.append(f"- **Total external URLs:** {len(external_links)}")
            report.append(f"- **Successful:** {external_success}")
            report.append(f"- **Broken:** {len(external_broken)}")
            report.append("")
            
            if external_broken:
                report.append("### Broken External URLs:")
                for file_path, line_num, link_text, link_result in external_broken:
                    report.append(f"- **{file_path}:{line_num}** - `{link_result.url}`")
                    report.append(f"  - **Error:** {link_result.error_message}")
                    report.append("")
        
        # Local file details
        if local_file_links:
            report.append("## Local File Links Details")
            report.append("")
            
            local_broken = [link for link in local_file_links if link[3].status == 'broken']
            local_success = len(local_file_links) - len(local_broken)
            
            report.append(f"- **Total local file links:** {len(local_file_links)}")
            report.append(f"- **Successful:** {local_success}")
            report.append(f"- **Broken:** {len(local_broken)}")
            report.append("")
            
            if local_broken:
                report.append("### Broken Local File Links:")
                for file_path, line_num, link_text, link_result in local_broken:
                    report.append(f"- **{file_path}:{line_num}** - `{link_result.url}`")
                    report.append(f"  - **Error:** {link_result.error_message}")
                    report.append("")
        
        return "\n".join(report)

def main():
    """Main function to run the link checker"""
    print("Starting link checker for markdown files...")
    
    checker = MarkdownLinkChecker()
    results = checker.check_directory("labs")
    
    if not results:
        print("No results to report.")
        return
    
    # Generate and save report
    report = checker.generate_report(results)
    
    report_file = "link-checker-report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nLink checker completed!")
    print(f"Report saved to: {report_file}")
    
    # Print summary to console
    total_links = sum(len(file_result.links) for file_result in results)
    broken_links = sum(1 for file_result in results for _, _, link_result in file_result.links if link_result.status == 'broken')
    
    print(f"\nSummary:")
    print(f"- Total links checked: {total_links}")
    print(f"- Broken links: {broken_links}")
    print(f"- Success rate: {((total_links-broken_links)/total_links*100):.1f}%" if total_links > 0 else "N/A")

if __name__ == "__main__":
    main()
