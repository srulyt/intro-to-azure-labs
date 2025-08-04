# Link Checker for Azure Labs Documentation

This repository contains a comprehensive link validation tool for the Azure labs markdown documentation.

## Quick Start

Run the link checker:

```bash
python link_checker.py
```

This will generate a detailed report in `link-checker-report.md`.

## Summary of Current Status

**Last Check:** 2025-08-01 00:53:15

- **Total Files:** 8 markdown files
- **Total Links:** 146 links found
- **Success Rate:** 58.2% (85 working, 61 broken)

### Link Types Found:
- **External URLs:** 40 links (27 working, 13 broken)
- **Local Files:** 106 links (58 working, 48 broken)
- **Internal Anchors:** 0 links

## Key Issues Identified

### 1. Missing Image Files (48 broken local links)
Many screenshot images are missing from the expected locations. Most common issues:

**Lab 0 (Resource Group):** 26 missing images
- `subscription-search.png`
- `subscription-list.png`
- `portal-settings.png`
- `set-subscription-filter.png`
- `create.resource.select.png`
- `resource.group.search.png`
- `resource.group.create.png`
- `resource-group-name.png`
- `create.resource.group.verify.png`
- `resource-group-create-notification.png`
- `resource-group-pin-icon.png`
- `new-dashboard-settings.png`
- `homeanddashboard.png`

**Lab 1 (Storage Account):** 16 missing images
- `storage-account-instance-details.png`
- `storage-account-go-to-resource.png`
- `role-assignments-tab.png`
- `storage-add-role-assignment.png`
- `review-role-assignment.png`
- `final-role-assignments.png`
- `storage-account-configuration.png`
- `default-to-entra-id-azure-portal.png`

**Lab 5 (SQL Database):** 4 missing images
- `sql-database-networking-tab.png`
- `review-and-create.png`

### 2. Broken External URLs (13 broken external links)

**HTTP 404 Errors:**
- Microsoft Support page for Edge profiles (Lab 0)
- Azure SQL documentation URL with malformed syntax (Lab 5)
- Old Microsoft Docs URLs (Lab 7)

**HTTP 403 Errors:**
- Internal Microsoft documentation links (Lab 7)

**Connection Errors:**
- Malformed portal.azure.com URLs with extra characters
- Localhost references in several labs

**Email Links:**
- `mailto:` links being processed as file paths instead of email addresses

### 3. Malformed URLs
Several URLs have formatting issues:
- Extra characters: `https://portal.azure.com**`
- Incomplete syntax: `https://portal.azure.com"`
- Wrong punctuation: `https://learn.microsoft.com/azure/azure-sql/).`

## Recommended Actions

### Immediate Fixes

1. **Fix malformed URLs** - Remove extra characters and correct syntax
2. **Update deprecated URLs** - Replace old docs.microsoft.com links with learn.microsoft.com
3. **Handle email links** - Ensure mailto: links are properly formatted
4. **Remove localhost references** - Replace with appropriate examples

### Image Management

1. **Audit missing images** - Determine which screenshots need to be recreated
2. **Standardize image naming** - Ensure consistent naming conventions
3. **Verify image paths** - Confirm all relative paths are correct
4. **Create missing images** - Generate new screenshots for missing files

### Documentation Quality

1. **Regular link checking** - Run this tool as part of documentation maintenance
2. **Link validation in CI/CD** - Consider adding automated link checking
3. **Documentation standards** - Establish guidelines for link formatting

## Tool Features

The link checker provides:

- **Comprehensive scanning** of markdown files
- **Multiple link types** validation (external URLs, local files, internal anchors)
- **Detailed error reporting** with exact line numbers and file locations
- **Retry logic** for external URLs with timeout handling
- **Categorized results** by link type and status
- **Markdown report generation** for easy sharing and tracking

## Files Generated

- `link-checker-report.md` - Complete detailed analysis
- `README-LinkChecker.md` - This summary document

## Next Steps

1. Address the malformed URLs for immediate improvement
2. Work on restoring missing image files
3. Update deprecated external links
4. Consider implementing this as part of regular documentation maintenance

The tool is ready to be run again after fixes to track improvement in link health.
