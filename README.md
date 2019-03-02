# EPIDEMIC
- > Where are the forums?
- > Where is the time series predictive model?
- > Where are the email/SMS auto-notification engine?
- > Where is the simulation?
- > Where is the website (topkek)
- > Where are the beautiful and fancy visualizations
- > Where is da money?

```python
vary diseaseid between 1 and 11 both included
vary days between 1 and 365
For map plot (it has red, yellow and pharmacy, all 3 for a diseaseid and value of days): http://epidemic.pythonanywhere.com/fetch_cases/?days=30&diseaseid=10
For the time series plot of a diseaseid: http://epidemic.pythonanywhere.com/fetch_only_cases/?days=30&diseaseid=10
For number of deaths, cases of a diseaseid: http://epidemic.pythonanywhere.com/fetch_stats/?diseaseid=10
To get pharmacies having drug = drugid: http://epidemic.pythonanywhere.com/get_pharma/?drugid=502
http://epidemic.pythonanywhere.com/new_case/?date=12-01-2019&diseaseid=20&death=1&location="123.423423 124.356345"
http://epidemic.pythonanywhere.com/similar_states/?state=Ujjain
http://epidemic.pythonanywhere.com/fetch_drugs/?diseaseid=1
http://epidemic.pythonanywhere.com/new_drug/?drugid=2&drugname=test&drugreq=12&diseaseid=10
http://epidemic.pythonanywhere.com/login/?id=12&password=123
```


- flask_app.py is the API (Work under progress) - dengue
- db.ipynb is the jupyter notebook to create the sqlite database - shreya
- Refer the epidemic doc for datafield names

Doc link: https://docs.google.com/document/d/1mr-sEg6C7jIL40-LZIjIPKPXJ6ktY7pnm42bEsWzL8Q/edit?usp=sharing
