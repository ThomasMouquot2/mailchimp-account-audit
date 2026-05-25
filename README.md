# Mailchimp Account Audit Tool

A comprehensive Python tool to audit your entire Mailchimp account, analyzing lists, campaigns, automations, subscribers, and more. Generates detailed reports with actionable recommendations.

**Launch in Claude Code:**
```
@audit mailchimp account
```

## 📋 Features

- **Complete Account Analysis**: Audits all aspects of your Mailchimp account
- **Health Score**: Calculates a 0-100 account health score
- **List Analysis**: Reviews list growth, engagement, and subscriber health
- **Campaign Performance**: Analyzes open rates, click rates, bounce rates, and unsubscribe trends
- **Subscriber Health**: Identifies inactive subscribers, invalid emails, and duplicates
- **Automation Review**: Analyzes automation workflows and performance
- **Integration Check**: Reviews connected integrations and their status
- **Compliance Audit**: Checks for GDPR and CAN-SPAM compliance
- **Multiple Export Formats**: HTML (beautiful dashboard), JSON (detailed data), and text (summary)
- **Actionable Recommendations**: Provides specific suggestions for improvement

## 🛠️ Requirements

- Python 3.8+
- Mailchimp API key (from your Mailchimp account settings)
- Required packages: `requests`, `python-dotenv`, `jinja2`

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/ThomasMouquot2/mailchimp-account-audit.git
cd mailchimp-account-audit
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

5. Edit `.env` and add your Mailchimp API key:
```
MAILCHIMP_API_KEY=your_api_key_here
```

## 🚀 Usage

### Basic Audit (HTML Report)
```bash
python audit.py --format html --output mailchimp_audit.html
```

### JSON Report (Detailed Data)
```bash
python audit.py --format json --output mailchimp_audit.json
```

### Text Report (Summary)
```bash
python audit.py --format text --output mailchimp_audit.txt
```

### All Options
```bash
python audit.py --help
```

## 📊 Report Contents

### Executive Summary
- Overall account health score (0-100)
- Key metrics at a glance
- Critical issues flagged
- Top recommendations

### Account Overview
- Account type and plan
- Total lists and subscribers
- Account age and activity

### Lists Audit
- List-by-list analysis
- Subscriber growth rates
- Engagement metrics (open rates, click rates)
- List health indicators
- Inactive subscriber counts

### Campaign Performance
- Campaign count and types
- Average open and click rates
- Bounce and unsubscribe rates
- Best/worst performing campaigns
- Campaign timing analysis

### Subscriber Health
- Total subscriber count
- Active vs. inactive subscribers
- Bounce rate analysis
- Unsubscribe trends
- Invalid email detection

### Automation Review
- Active automations count
- Automation performance metrics
- Workflow efficiency analysis

### Integration Status
- Connected integrations
- Integration health
- Sync status

### Compliance Check
- GDPR compliance indicators
- CAN-SPAM compliance status
- Double opt-in setup
- Unsubscribe availability

### Recommendations
- Prioritized action items
- Best practice suggestions
- Optimization opportunities

## 🔐 Security

- Never commit your `.env` file with API keys
- Use environment variables for sensitive data
- Rotate your API keys periodically
- Only store and process audit data securely

## 📝 Example Output

The HTML report includes:
- Color-coded health metrics
- Interactive charts and graphs
- Detailed tables with sortable data
- Downloadable recommendations
- Visual health indicators

## 🐛 Troubleshooting

### "Invalid API key" error
- Verify your API key in the `.env` file
- Check that your API key is from the correct Mailchimp account
- Ensure the API key hasn't been revoked

### "Rate limit exceeded" error
- Wait a few minutes before running the audit again
- Mailchimp has rate limits; consider running audits during off-peak hours

### "No lists found" warning
- Verify you have lists in your Mailchimp account
- Check that the API key has permission to view lists

## 📚 API Reference

The tool uses the Mailchimp API v3. For more information, visit:
https://mailchimp.com/developer/marketing/api/

## 🤝 Contributing

Feel free to fork, modify, and improve this tool. Some ideas for enhancements:
- Add database storage for historical audit data
- Create scheduled audit reports
- Add email delivery of reports
- Implement list cleanup automation
- Add subscriber segmentation analysis

## 📄 License

MIT License - Feel free to use this tool for personal and commercial purposes.

## ⚠️ Disclaimer

This tool provides analysis and recommendations based on best practices. Always review results carefully and test any automated actions in a test environment first. The author is not responsible for any issues arising from the use of this tool.

## 📧 Support

For issues, questions, or suggestions, please open a GitHub issue in this repository.

---

**Happy auditing! 📊**
