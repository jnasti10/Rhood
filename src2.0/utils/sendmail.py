import boto3
from botocore.exceptions import ClientError
from utils.mailtemplate import MailTemplate

def send(to, frm, subject, body, region="us-east-2"):
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=region)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    to,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': "UTF-8",
                        'Data': body,
                    },
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': "Does not support html....",
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': subject,
                },
            },
            Source=frm,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def create_body(strategy, images, expected_profit, test=False):
    if(not test):
        tmplt = MailTemplate()
        return(tmplt.create_body(strategy, images, expected_profit))
    else:
        return(BODY_HTML)

# for testing
SENDER = "jo@joeynasti.com"
RECIPIENT = "jnasti101@icloud.com"
SUBJECT = "Test Email from the EC2!!"
BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )
BODY_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Image Gallery</title>
<style>
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f2f2f2;
    }
    .container {
        max-width: 800px;
        margin: 20px auto;
        padding: 20px;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .image-container {
        text-align: center;
        margin-bottom: 20px;
    }
    .image-container img {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
    }
    .stats,
    .option-info {
        text-align: center;
        margin-top: 20px;
    }
    .stats p,
    .option-info p {
        margin: 5px 0;
    }
    .options-list {
        display: flex;
        justify-content: space-between;
        list-style-type: none;
        padding: 0;
        margin: 0;
    }
    .option-item {
        flex: 1;
        text-align: center;
        margin: 10 px;
        border: 1px solid #ccc;
        padding: 10 px;
        border-radius: 8px;
    }
</style>
</head>
<body>

<div class="container">
    <h1>UPRO Option Strategy</h1>
    <div class="option-info">
        <ul class="options-list">
            <li class="option-item">
                <p>Option 1: Buy Call</p>
                <p>Strike Price $100</p>
                <p>Option price $1.5</p>
            </li>
            <li class="option-item">
                <p>Option 2: Sell Call</p>
                <p>Strike Price $105</p>
                <p>Option price $.5</p>
            </li>
            <li class="option-item">
                <p>Option 3: Sell Call</p>
                <p>Strike Price $105</p>
                <p>Option price $.5</p>
            </li>
            <li class="option-item">
                <p>Option 4: Sell Call</p>
                <p>Strike Price $105</p>
                <p>Option price $.5</p>
            </li>
            <!-- Add more <li> items for additional options if needed -->
        </ul>
        <p>Total Price: $1
    </div>

    <div class="image-container">
        <img src="http://joeynasti.com/profit_func.png" alt="profit_func.png">
    </div>
    
    <div class="image-container">
        <img src="http://joeynasti.com/stock_price_pdf.png" alt="stock_price_pdf.png">
    </div>

    <div class="image-container">
        <img src="http://joeynasti.com/profit_by_pdf.png" alt="profit_by_pdf.png">
    </div>

    <div class="stats">
        <p>Additional Data and Statistics:</p>
        <p>Expected Value Profit: $1.65/share</p>
    </div>
</div>

</body>
</html>
            """            


if __name__ == "__main__":
    tmplt = MailTemplate()

    images = ["profit_func.png", "stock_price_pdf.png", "profit_by_pdf.png"]

    strategy = [
                {
                    "mark_price"   : 7.0,
                    "strike_price" : 60.0
                },
                {
                    "mark_price"   : 4.0,
                    "strike_price" : 64.0
                },
                {
                    "mark_price"   : 3.0,
                    "strike_price" : 66.0
                },
                {
                    "mark_price"   : 1.0,
                    "strike_price" : 72.5
                }
            ]

    expected_profit = 1.56

    print(tmplt.create_body(strategy, images, expected_profit))
