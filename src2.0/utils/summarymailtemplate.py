class SummaryMailTemplate:
    body_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Trade Summary</title>
<style>
    body {{
        font-family: Arial, sans-serif;
        background-color: #f2f2f2;
        margin: 0;
        padding: 0;
    }}
    .container {{
        max-width: 800px;
        margin: 20px auto;
        background: #fff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }}
    h1 {{
        text-align: center;
    }}
    .section {{
        margin-top: 20px;
    }}
    .section h2 {{
        border-bottom: 2px solid #ddd;
        padding-bottom: 5px;
    }}
    .position {{
        margin-bottom: 15px;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 8px;
    }}
</style>
</head>
<body>

<div class="container">
    <h1>Daily Trade Summary</h1>

    <div class="section">
        <h2>Pending Positions</h2>
        {pending_html}
    </div>

    <div class="section">
        <h2>Active Positions</h2>
        {active_html}
    </div>
</div>

</body>
</html>
    """

    position_template = """
    <div class="position">
        <p><strong>Symbol:</strong> {chain_symbol}</p>
        <p><strong>Strategy:</strong> {strategy}</p>
        <p><strong>Quantity:</strong> {quantity}</p>
        <p><strong>Premium:</strong> ${premium}</p>
    </div>
    """

    def create_summary_email(self, pending_positions, active_positions):
        """Generate an HTML email summarizing current positions."""
        pending_html = self.format_positions(pending_positions)
        active_html = self.format_positions(active_positions)
        return self.body_template.format(pending_html=pending_html, active_html=active_html)

    def format_positions(self, positions):
        """Format positions into HTML."""
        html = ""
        for stock, items in positions.items():
            for item in items:
                html += self.position_template.format(
                    chain_symbol=item.get("chain_symbol", "N/A"),
                    strategy=item.get("strategy", "N/A"),
                    quantity=item.get("quantity", "N/A"),
                    premium=item.get("premium", "N/A"),
                )
        return html
