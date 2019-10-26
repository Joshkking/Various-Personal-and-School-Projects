# Web Scrape Work Readme

For a couple of projects I ended up having to do a little web scraping:
* Simple Python Links Scrape - This was *very* simple project prompt, arguably almost to easy, to get all of the unique, active links from a certain webpage (a US Census Bureau page). I include it here though as it does serve as a tidy little script for possible future use if the url was converted to a parameter. I included most of the main files submitted, but the main things to look at are the pdf describing the code and either the ipynb, py, or html file representations of the code itself (presented for ease of use).
* **WeRateDogs Scrape and Analysis** - This was a much more substantial and enjoyable project. Here I scraped a handful of information from Twitter's API on the WeRateDogs account then went through the whole analysis experience to see what conclusions I could draw about which doggos were more popular. There are a number of files for this:
  * wrangle_act.html and wrangle_act.ipynb - This is the actual jupyter notebook code and analysis in full. I provide the html in case the notebook can't be opened.
  * wrangle_report.pdf - This is a quick summary of how I got the data and how it was processed.
  * act_report.pdf - This is a quick, external-facing summary of the results (it was supposed to sound "fun").
  * Some data files:
    * Image_predictions.tsv - A file downloaded programmatically from a provided link on a Udacity server using the ‘requests’ Python library. I didn't make this one, but I coded getting it.
    * twitter_archive_enhanced.csv - This was some extra twitter information already provided to us, namely to tell us which tweets to scrape data on.
    * tweet_json.txt - A text file where I wrote the scraped data to.
    * twitter_archive_master.csv - The final csv file where I dumped all of my cleaned/prepared data into for analysis.
