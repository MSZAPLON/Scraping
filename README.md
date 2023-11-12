# Scraping
generic webscraping repo with github actions

the example is checking the aave application to monitor if Metis can be provided as collateral and tracking the borrowed and supplied amounts in a csv file. if metis can be provided as collateral sends a telegram message to a private channel. It also updates the data/plot.png chart including the price, supply/borrow amount and apys.

Components to reuse:

github actions

    ubuntu, 
    selenium, 
    python, requirements, 
    commit back to repo, 
    GitHub secrets

python

    selenium - web scraping 
    update tracking file
    screenshot for debugging
    telegram bot messaging
    GitHub secrets 

data visualization

    matplotlib - bar, line, fill_between, twinx
    
data

    csv tracking file
