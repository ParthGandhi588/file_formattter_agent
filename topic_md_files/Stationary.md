# Stationary

Stationary is handled by Niyati. 
### Every 25th or 26th of the month
A mail is sent to the admins of all the units to get a list of requirements from each unit. 
#### Along with a mail to each admin
A mail is sent to every department to a randomly chosen department representative to get an estimate of the department needs.
##### This mail consists of a Zoho form
Which has 6 pages and 120 commonly used stationary items in it.
###### The response of this form goes to the reception
Where it is given to the admin in printed form.
#### If a department needs an item not in the list
Then there are 2 cases for this situation:
##### Case 1: The item number is registered in inventory but not given in the item list
In this case, the admin manually maps the requested item to an existing item in the inventory.
##### Case 2: Item is totally new
Then the item has to get registered using the following process:
###### Step 1: A mail is sent using ERP to generate item code
This mail consists of the list of items in a fixed excel format with the following columns:
1. Item name
2. Item desc (limit of 40 chars)
3. Detailed desc
4. Item class
5. Item subclass
###### Step 2: This is then sent for approval to management through mail for code creation
Along with budget and new vendor approvals if applicable.
###### Step 3: After approval these details are sent to the ERP dept to create a new item code
And this code is given to the concerned admin through mail.
###### Step 4: Admin uses this code to fill rate, tax structure, purchase setting in the ERP software
Without these details, the PO for the item cannot be created in the ER software.
##### The Rate is approved via the admin’s immediate supervisor
#### These requirements are then compared against the current stock for procurement estimation
The requirements are then drafted in an excel format and sent to management through mail for budget approvals with details like the budget for last month, this month, and reason for fluctuations if applicable.
##### After approval the admin generates the PO through ERP software
And orders the material from fixed vendors for each item.
###### A mail is sent to the concerned vendor with the PO
The PO under 1 lakh is approved through the immediate supervisor.
###### The PO over 1 lakh can only be approved by the Department head
And they don't have a limit for the PO size.
##### The rates for each vendor are fixed for a financial year and are revised in February
After approval, we get the option to download PO as PDF.
###### Supply Reg Form format
1. Reg Number (Via ERP)
2. Name
3. Category
4. Sign of HOD, supervisor, management, and the person in ERP who generated the code.
#### When the material arrives
Then there needs to be an inward process at the gate.
##### For the inward process
The person who brings the material goes to the store to verify the invoice against the PO.
###### If the PO is for a 100 pens and the invoice is generated for 75 pens
Then an informal communication is done from the store manager to the concerned admin representative that 25 pens are missing, so the PO will still be kept open.
#### After the store manager verifies all the details in the invoice match the PO in the ERP system
Then he gives the invoice a “D” stamp to be shown at the gate.
##### This checking is manual, time taking and prone to errors
The D stamp is then shown to the security at the gate to fill the inward sheet (This sheet is also audited) and the material can then be unloaded.
###### When unloaded the quantity of the items are checked manually
If the count matches, then GRN number is generated to add the item to stock.
##### If the count does not match
Then a new invoice is generated for the incorrect count and communicated through WhatsApp or mail, and the PO is still kept open if the items received are less than the PO.
#### After the stock is added to the inventory
The concerned admin person is not notified automatically.
##### When the material is received
Then using the ERP software, a requisition form is filled with the following details:
1. Category (Admin)
2. Receiver (name of person who requested the stationary item)
3. Item Codes
4. Quantities
5. Remarks
###### After filling the form an ER number is generated
Which is noted down manually.
##### This ER number is then used to approve the requisition request via the admin’s immediate supervisor
The immediate supervisor has access to this ER number in his dashboard, but he does not know which request is from whom, so this number needs to be manually forwarded every time.
#### After this
The issue to shop floor form is filled with the following details:
1. Category
2. Person Name
3. ER number from prev step
4. Quantity (This is used to reduce the quantity from stock)
##### A number is generated for this process
And kept in records manually, and is useful when we want to undo the issue to shop floor process.
###### If an item is defective
Then this number is used to revert the issue to shop floor process (return issue to shop floor).
##### If the number of items with issue are limited
Then they are replaced by the vendor informally.
###### If the number of items is high in quantity
Then the following procedure takes place:
1. Return issue to shop floor is done.
2. Vendor Rejection Note (VRN) is generated in the Quality Control department (communication done via mail).
3. This VRN is manually printed and given to the admin to sign.
4. A copy of the VRN is sent to the accounts department to make a debit note for the previous invoice.
