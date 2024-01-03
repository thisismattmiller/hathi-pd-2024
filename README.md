# hathi-pd-2024
Hathi Public Domain in 2024


# To Run
```

Download the collection (https://babel.hathitrust.org/cgi/ls?a=srchls;c=260456364;q1=*) as JSON named search_results.json in the same directory.

mkdir classify_by_oclc/

mkdir data/

mkdir lccn/


Run:
python3 download_classify.py

python3 download_hathi.py

python3 enrich.py

python3 download_lccn.py

python3 enrich.py (again)

mkdir hashdata

python3 build_hiearchy.py

Fork https://observablehq.com/d/a2ba1571c7346489 and replace with the lcc_hiearchy_1928_pd.json created.

Embed Observable in index.html




```
