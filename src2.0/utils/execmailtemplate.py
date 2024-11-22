class ExecutionMailTemplate:
    body_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Trade Executed</title>
<style>
    body {{
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f2f2f2;
    }}
    .container {{
        max-width: 600px;
        margin: 20px auto;
        padding: 20px;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }}
    .trade-info {{
        margin-top: 20px;
    }}
    .trade-info p {{
        margin: 5px 0;
    }}
</style>
</head>
<body>

<div class="container">
    <h1>Trade Executed</h1>
    <div class="trade-info">
        <p><strong>Symbol:</strong> {chain_symbol}</p>
        <p><strong>Strategy:</strong> {strategy}</p>
        <p><strong>Quantity:</strong> {quantity}</p>
        <p><strong>Premium:</strong> ${premium}</p>
        <p><strong>Execution Date:</strong> {date_executed}</p>
    </div>
    <h2>Leg Details:</h2>
    <ul>
        {legs_html}
    </ul>
</div>

</body>
</html>
    """

    leg_template = """
    <li>
        <p><strong>Type:</strong> {option_type} {side}</p>
        <p><strong>Strike Price:</strong> ${strike_price}</p>
        <p><strong>Expiration Date:</strong> {expiration_date}</p>
    </li>
    """

    def create_execution_email(self, order_info):
        """Create an email body for the executed trade."""
        legs_html = ""
        for leg in order_info["legs"]:
            legs_html += self.leg_template.format(
                option_type=leg["option_type"],
                side=leg["side"],
                strike_price=leg["strike_price"],
                expiration_date=leg["expiration_date"],
            )
        return self.body_template.format(
            chain_symbol=order_info["chain_symbol"],
            strategy=order_info["strategy"],
            quantity=order_info["quantity"],
            premium=order_info["premium"],
            date_executed=order_info["created_at"],
            legs_html=legs_html,
        )
