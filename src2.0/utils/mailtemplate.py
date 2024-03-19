class MailTemplate:
    body_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Image Gallery</title>
<style>
    body {{
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f2f2f2;
    }}
    .container {{
        max-width: 800px;
        margin: 20px auto;
        padding: 20px;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }}
    .image-container {{
        text-align: center;
        margin-bottom: 20px;
    }}
    .image-container img {{
        max-width: 100%;
        height: auto;
        border-radius: 8px;
    }}
    .stats,
    .option-info {{
        text-align: center;
        margin-top: 20px;
    }}
    .stats p,
    .option-info p {{
        margin: 5px 0;
    }}
    .options-list {{
        display: flex;
        justify-content: space-between;
        list-style-type: none;
        padding: 0;
        margin: 0;
    }}
    .option-item {{
        flex: 1;
        text-align: center;
        margin: 10 px;
        border: 1px solid #ccc;
        padding: 10 px;
        border-radius: 8px;
    }}
</style>
</head>
<body>

<div class="container">
    <h1>UPRO Option Strategy</h1>
    <div class="option-info">
        <ul class="options-list">
           {options_html} 
            <!-- Add more <li> items for additional options if needed -->
        </ul>
        <p>Total Price: ${total_price}
    </div>
    
    {images_html}

    <div class="stats">
        <p>Additional Data and Statistics:</p>
        <p>Expected Value Profit: ${expected_profit:.2f}/share</p>
    </div>
</div>

</body>
</html>
            """        
    
    image_html = """
    <div class="image-container">
        <img src="https://joeynasti.com/{image_name}" alt="{image_name}">
    </div>
"""

    option_html = """
            <li class="option-item">
                <p>{action} {o_type}</p>
                <p>Strike Price ${strike}</p>
                <p>Option price ${price:.2f}</p>
            </li>
"""
        

    def create_body(self, strategy, images, expected_profit):
        options_html = self.create_options_html(strategy)
        images_html  = self.create_images_html(images)
        total_price  = self.get_total_price(strategy)

        #print('-=-=-=-=-=-=-=-BODY_TMP=-=-=-=-=-=-=-=-=\n', self.body_template)
        #print('-=-=-=-=-=-=-=-expected_prfit=-=-=-=-=-=-=-=-=\n', expected_profit)
        #print('-=-=-=-=-=-=-=-options_html=-=-=-=-=-=-=-=-=\n', options_html)
        #print('-=-=-=-=-=-=-=-images_html=-=-=-=-=-=-=-=-=\n', images_html)
        #print('-=-=-=-=-=-=-=-total_price=-=-=-=-=-=-=-=-=\n', total_price)
        body = self.body_template.format(expected_profit=expected_profit, options_html=options_html, images_html=images_html, total_price=total_price)

        return(body)

    def create_options_html(self, strategy):
        s = ""
        actions = ["Buy", "Sell", "Sell", "Buy"]

        for i in range(len(strategy)):
            if(strategy[i]):
                price = (actions[i] == "Buy" and strategy[i]['mark_price'] * 1.05) or (actions[i] == "Sell" and strategy[i]['mark_price'] * -.95) 
                s += self.option_html.format(action=actions[i], o_type="Call", strike=strategy[i]["strike_price"], price=price)

        return(s)

    def create_images_html(self, images):
        s = ""
        
        for image_name in images:
            #print(s)
            s += self.image_html.format(image_name=image_name)
            #print(s)

        return(s)

    def get_total_price(self, strategy):
        actions = ["Buy", "Sell", "Sell", "Buy"]
        total_price = 0        
    
        for i in range(len(strategy)):
            if(strategy[i]):
                price = (actions[i] == "Buy" and strategy[i]['mark_price'] * 1.05) or (actions[i] == "Sell" and strategy[i]['mark_price'] * -.95) 
                total_price += price

        return(total_price)


