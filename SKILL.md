# Mailchimp Account Audit - Claude Code Skill Configuration

## Trigger Commands

```
@audit mailchimp
@audit mailchimp account
@mailchimp audit
/audit-mailchimp
```

## Skill Description

This Claude Code skill provides a comprehensive audit of your entire Mailchimp account. It analyzes lists, campaigns, automations, integrations, subscriber health, and compliance to generate detailed reports with actionable recommendations.

## What It Does

1. **Connects to your Mailchimp account** using your API key
2. **Analyzes all account data**:
   - Account information and settings
   - All mailing lists and their performance
   - Recent campaigns and their metrics
   - Active automations
   - Connected integrations

3. **Calculates health metrics**:
   - Overall account health score (0-100)
   - Individual list health scores
   - Campaign performance metrics
   - Engagement rates analysis

4. **Generates recommendations**:
   - List cleanup suggestions
   - Best practice recommendations
   - Missing feature alerts
   - Optimization opportunities

5. **Produces reports** in multiple formats:
   - **HTML**: Beautiful, interactive dashboard
   - **JSON**: Complete data export
   - **Text**: Summary report

## Usage in Claude Code

1. Type one of the trigger commands above
2. Provide your Mailchimp API key when prompted
3. Wait for the audit to complete
4. View or download the generated report

## Example Output

```
⚙️ Validating configuration...
🔌 Connecting to Mailchimp...
✅ Connected successfully!
🔍 Starting Mailchimp Account Audit...
📊 Fetching account information...
📋 Analyzing lists...
📧 Analyzing campaigns...
⚙️ Analyzing automations...
🔗 Checking integrations...
💡 Generating recommendations...
📈 Calculating health score...
✅ Audit complete!

════════════════════════════════════════════════════════
AUDIT SUMMARY
════════════════════════════════════════════════════════
Health Score: 78/100
Lists: 5
Campaigns: 12
Automations: 3
Integrations: 2
Recommendations: 4
════════════════════════════════════════════════════════
```

## Report Sections

- **Executive Summary** with overall health score
- **Account Overview** with basic account details
- **Lists Analysis** with engagement metrics
- **Campaign Performance** with send statistics
- **Automation Review** with workflow details
- **Integration Status** with connection information
- **Compliance Check** with best practices
- **Actionable Recommendations** prioritized by impact

## Security

Your API key is:
- Never stored permanently
- Used only during the audit session
- Never shared or exposed
- Handled according to Mailchimp's security best practices

## Files

- `audit.py` - Main entry point
- `config.py` - Configuration management
- `mailchimp_client.py` - API client
- `audit_analyzer.py` - Analysis engine
- `report_generator.py` - Report generation
- `.env.example` - Environment template

## Getting Your API Key

1. Log in to your Mailchimp account
2. Go to Account → Extras → API Keys
3. Click "Create A Key"
4. Copy the generated key
5. Paste it when prompted in Claude Code

---

**Created for comprehensive Mailchimp account analysis and optimization.**
