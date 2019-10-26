# Prosper Loans Exploratory Analysis
## by Josh King


## Dataset

The analyzed dataset is a record of 113,937 data entries from Prosper Loans. The data includes a number of variables regarding each loan listing (81 variables in total). Due to the large size of the dataset, I focused on a narrowed list of the available variables here. These specific columns were listed as the data was read from the csv and pulled into a Pandas dataframe. Generally the data included focused directly on the borrower, basic loan details (such as the amount), and variables reflecting the amount stood to be made by the bank.


## Summary of Findings

### Univariate Exploration
Below (out of personal interest) I explore the following data distributions:
* Borrower employment/occupation
* Borrower income range
* Expected return
* Prosper score
* Loan amount
Generally my interest here is centered around the borrower types, what Prosper expects to get out of the loans, and how much of a loan is being taken out.

* ***Borrower employment/occupation***
    * There was a little bit of feature-engineering needed here to look at just the individuals who were employed or receiving income, but overwhelmingly the dataset contains loan info for those who have an income stream of some kind. I then looked at college student loans which showed a distribution skewed to higher university levels. This, to me, suggested that successive entries are listed for each year the student attends university. However, without having a sure sense of how to interpret what exactly the listing for the student loans seen here are, it's hard to advance to higher levels of analysis. It would, for instance, be useful to feel confident in whether these represent the cumulative loans at that stage in the students university experience, or the amount taken out each year. Furthermore, it would be important to know exactly when the loan was taken out. If taken out at the end or beginning of an academic year could skew the interpretation. While such matters might could be determined from the dataset, it would require a deeper dive than is within scope here, and as such I'll likely focus on other variables in further visualization.
* ***Borrower income range***
    * This first was changed to an ordinal type range since it's categorical but has a direction. The income distribution showed most borrowers within the 25K - 75K range. I was interested in the incomes of those higher than 100K however so I created a new column to review this. There were some extreme outliers with incomes in the millions, but the distribution quickly fell off between 100K - 200K. I tried a log transform to review the data here, but the outliers were so large that it was better just to selectively zoom. However a log transform of the calculated yearly income data was helpful to get it all in view.
* ***Expected return***
    * The distrubtion here was similar to that of a normal one with some interesting negative values on the expected return. Zooming in here we see that Prosper does expect to lose out significantly on some loans, but most of these are outliers and even then closer to 0.
* ***Prosper score***
    * This distribution was pretty clean and near normal. This matches well with the normal-ish distribution of expected return suggested it might be fairly predictive.
* ***Loan amount***
    * While the distribution here was skewed to the right, the more interesting thing to notice is that many of the loans seem to fall into select buckets. By changing bin size and zooming in some, this appeared true for most of the distribution. My guess from these local maxima is that Prosper likely offers standard loan "packages" (or amounts that people typically borrow).


### Bivariate Exploration
Here I was somewhat picking my variables in such that I can get different plot types for practice, but I also tailored to trails from the univariate analysis.

* ***Student Type vs Loan Amount***
    * I stuck with just the key features here. Both a violin and a box plot here showed some interesting results. The median loan amount for freshman students starts off a littler higher than sophomore students, with the loan amount then increasing up through university years. One possible explanation for the freshman bump was that perhaps freshman don't have a sense of how much they need yet and so take out more than they might otherwise. It was hard to tell whether the increase through college was do to the listings pooling cumulatively what the students owed or if the students really were taking out more at each stage. Figuring this out would require discussing the data with someone knowledgeable or doing a deep-dive using the key variables and loan dates. As such I decided I'd like stick with the other variables in further analysis. The plots though were helpful in seeing the comparison to community college and technical schools (about the same loan amount as that of a college freshman).
* ***Estimated Return vs Loan Amount***
    * Just stuck with my intended variables, but I had to plot a few times to get a clear pictures. This was great and helping see which kinds of loans were expected to yield more returns. After a couple of scatter plots we could see that the data was pretty continuously distributed with loan amounts having many different estimated returns, but two trends clearly stuck out: 1) high estimated returns trail off at high loan amounts, and 2) nearly all of the negative returns were at lower (< $10K) loan amounts. After running the same plot as a histogram we were able to see that the peak distributions of loans were at an expected return of about 0.1 spread all across the loan amount range.
* ***Prosper Score (and Estimated Return) vs Borrower Income***
    * I had to do a number of plots to review the data here and see if there was a trend related to income and how positive Prosper viewed the loan. A clustered bar plot of Prosper score and income range showed a bias in higher income brackets to high incomes (expected with a higher income likely being a more stable loan). When I plotted the income range against the expected return however I was surprised to see the median expected return trended lower (if albeit slightly) at higher income ranges. This was hard to explain so I did look into a feature I hadn't expected of Borrower Rate to gain some insight. Plotting this vs income range I saw that higher income ranges had lower borrowing rates. My intuition then is that high income range borrowers are more stable and thus get a higher Prosper score, but the borrower rate tends to be low, and as such the expected return can shrink a little even with increasing Prosper score.

### Multivariate Exploration
Here I was still biasing my efforts as such that I get practice working with a variety of different plot types. From what I've learned in previous levels of analysis though, I thought it would be good to focus on loans (by amount and income) that Prosper expected to be positive (via Prosper score and estimated return).

* ***Estimated Return vs Loan Amount vs Borrower Rate***
    * This confirmed much of my intuitions previously. My suspcision was that higher loans amounts will have lower estimated returns due in correlation with a lower borrower rate, which is confirmed here. Conversely, the higher estimated returns also have higher borrower rates and are clustered more in the lower loan amounts. Interestingly some of the high borrower rates make up a decent chunk of the few loans with a negative return.
* ***Estimated Return vs Loan Amount vs Income Range***
    * This plot marches in step with the previous findings. As income range increases, borrowers access higher and higher loan amounts. At all income ranges, the estimated return trails off with higher loan amount. There is, however, not a clearly evident pattern regarding a correlation betweeen estimated return and income range that can't be explained by the loan amount here. We do seem to see a higher number of negative returns in the $50K - $75K range, but this could potentially be an artifact of sampling. Because of overplotting though, this doesn't tell us too much about the distribution of loans for each plot. To address that, I looked at a facetted heatmap of the data.
    * The distribution seen on the heat maps mmostly just confirms previous findings. The peak points within the distribution are indicated of the standard loan amounts found through univariate analysis generally seen around an estimated return of 0.1 as found in bivariate analysis. However, now with overplotting and sampling down no longer an issue, it does seem that higher income ranges might have a slightly less likelihood of having a negative estimated return on their loans.
* ***Estimated Return vs Loan Amount vs Prosper Score***
    * We see a slight disjunction between estimated return and Prosper score here. Higher estimated returns do not necessarily mean higher Prosper scores (as also seen in previous analysis). Rather there is a definite range across all loan amounts where most of the highest rank Prosper scores fall in of about ~0.05 estimated return. Another way of saying this is that the "safest" loans are more likely ones that Prosper only expects a modest return on. The rest of the data is distributed without much of a clear relationship we haven't otherwise seen except that of low Prosper scores. Here we can see that a low Prosper score does clearly predict nearly all negative returns, and that these are the lower end of loan amounts.
* ***Estimated Return vs Prosper Score vs Income Range***
    * We see the same disjoint between estimated return and Prosper score here. As the Prosper Score increases, the mean estimated return begins to decrease (generally across all income ranges). From the cumulative previous analysis, we can suggest that this strange pattern is explained by Prosper score likely more reflecting the security of the loan, with the most secure loans being those with only a modest expected return due to a low borrower rate. When reviewing the relationship to income range though, we notice that lower income ranges, including the $0 and unemployed are still represented across many of the scores and ofen even yield a higher estimated return. This is likely due to a higher borrowing rate (seen from previous analysis). The no income brackets immediately fall off at the tail of Prosper Scores however.


## Key Insights for Presentation

As part of my analysis, I investigated if and how a borrower's income bracket effected the estimated return on a Prosper loan. In the presentation I'll first demonstrate a trend of decreasing estimated return with increasing income bracket. Since this is a somewhat counter-intuitive result (one would expect higher earners able to produce higher yields on a loan), the presentation will proceed to show how this relationship is more a factor of the loan borrowing rate, with higher income brackets accessing a lower borrowing rate.

For all plots I want to clean up the sizing and axis labels. I will likely use seaborns "talk" style to auto-format many of the plots for the slides. I'll also despine most of the plots to reduce some ink and just make things look cleaner. I took care of most of the presentation for each plot in the exploratory analysis notebook, but I may tweak a few items as noted below.

I'll utilize the following plots:
* Income Range vs Estimated Return - Here the outliers aren't as important so I'll remove those. I'll also add some sequential coloring to focus in on the progressing income brackets (the data is ordinal). The box plot is clearer with less distractions here so I'll focus on improving that rather than the violin (wherein the shapes may cause distraction).
* Income Range vs Borrower Rate - Aside from general cleaning, I'll add some sequential coloring for the ordinal income range.
* Estimated Return vs Loan Amount (Facetted Against Income) - This one will be a challenge. I can clean up the labels somewhat, but plotting the whole grid on one slide is likely to be a challenge. I plan to show the overall facetgrid for a snapshot but then plot the incomes individually per slide with appropriate titles.
* Estimated Return vs Loan Amount vs Borrowing Rate - I'll need to get a label on the color bar here and make sure the plot is big enough to see the color gradient. Overplotting was mostly already taken care of in the exploratory notebook, but plot size will be key.
