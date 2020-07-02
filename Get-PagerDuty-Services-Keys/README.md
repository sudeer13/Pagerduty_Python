# Get PagerDuty Services Keys

Save PagerDuty Services Service Names, Service IDs, Escalation Policy IDs, & ServiceNow Webhook IDs as an Microsoft Excel file so data can be manually added to ServiceNow once the PagerDuty app is installed.

## Prerequisites

* PagerDuty Account
* PagerDuty v2 API Key (read only)
* Python 2.x
* The following Python modules: os, json, requests, sys, openpyxl

## Installation

1.  Download project or just 'Get_PagerDuty_Services_Keys.py'.
2.	Ensure 'Get_PagerDuty_Services_Keys.py' has execution rights. `chmod +x Get_PagerDuty_Services_Keys.py`

## Example Usage

`./Get_PagerDuty_Services_Keys.py -k <PagerDuty v2 API Key>`

`./Get_PagerDuty_Services_Keys.py -key <PagerDuty v2 API Key>`
