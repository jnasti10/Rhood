from utils.rhoodfuncs import getOrderByID, login
from utils.trade_data import Trade_data
from utils.sendmail import send
from utils.execmailtemplate import ExecutionMailTemplate
import json

def send_execution_email(order_info):
    """Send an email notification for a successfully executed trade."""
    recipient = "jnasti101@icloud.com"
    sender = "!!!TradeExecuted!!!@joeynasti.com"
    subject = f"Trade Executed: {order_info['chain_symbol']} - {order_info['strategy']}"
    
    # Construct the email body using a new template
    body_template = ExecutionMailTemplate()
    body = body_template.create_execution_email(order_info)
    
    # Send the email
    send(to=recipient, frm=sender, subject=subject, body=body)
    print("Succesfully Sent!! body:\n" + body)

def get_data():
    data = Trade_data(1)
    data.load()
    return(data)

def main(mock_data=None):
    # Step 1: Log in to Robinhood
    login()

    # Step 2: Load trade data
    if(mock_data):
        data = mock_data
    else:
        data = get_data()

    # Step 3: Print current trade data for debugging
    print("Current Trade Data:")
    data.print()

    # Step 4: Process pending orders
    remove_these = []
    stock = "UPRO"  # Modify this if monitoring multiple stocks
    i = -1

    for pending_order in data.pending_positions[stock]:
        i += 1

        # Skip and remove orders without an ID
        if "id" not in pending_order:
            remove_these.append(i)
            continue

        # Get order details from Robinhood
        info = getOrderByID(pending_order["id"])
        print(f"Order Info for {pending_order['id']}:\n{json.dumps(info, indent=4)}")

        # Check if the order has been executed
        if float(info["pending_quantity"]) == 0:
            print(f"Order {pending_order['id']} has been executed.")
            remove_these.append(i)

            # Move to active positions
            if stock not in data.active_positions:
                data.active_positions[stock] = []
            executed_order = info
            data.active_positions[stock].append(executed_order)

            # Send email notification
            send_execution_email(executed_order)

        # Check if the order was canceled
        #elif info.get("state") == "canceled":
        #    print(f"Order {pending_order['id']} was canceled.")
        #    remove_these.append(i)

    # Step 5: Remove processed orders from pending_positions
    for index in sorted(remove_these, reverse=True):
        del data.pending_positions[stock][index]

    # Step 6: Save the updated trade data
    data.save()

    # Step 7: Print updated trade data for verification
    print("Updated Trade Data:")
    data.print()


if __name__ == "__main__":
    main()
