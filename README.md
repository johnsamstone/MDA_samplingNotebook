# MDA sampling Jupyter notebook experiments

This is a notebook to explore the sampling of 'rare' observations. Specifically, this is targetted at exploring how often we might expect to observe very young zircon grains when conducting detrital zircon analyses.

Often, these young grains are used to limit the ages of sedimentary deposits; which can be no older than the youngest mineral grains they contain. We want to be confident in our analyses of the age of these grains, so we like to observe multiple young grains. However these grains are often very rare.

Through some interactive plots, simulations, and analytical calculations this notebook explores the question 'How often can we expect to observe young zircon grains in detrital deposits?'. 

Please direct any questions to Sam Johnstone, johnsamstone@gmail.com, an individual that likes to experiment with these sorts of things on his free time when he is not conducting his official duties. Some of these analysis were used in the following paper:

Johnstone, S.A., Schwartz, T.M., and Holm-Denoma, C.S., 2019, A Stratigraphic Approach to Inferring Depositional Ages From Detrital Geochronology Data: Frontiers in Earth Science, v. 7, no. April, doi: 10.3389/feart.2019.00057.

**PLEASE NOTE**
The original publication above contained an error in Figures 2 and 3, where the values of k_c where all off by 1 (e.g., what was labelled k_c = 3 should have been k_c = 2, what was labelled k_c = 2 should have been k_c = 1, and so on. This notebook has the corrected version of those figures, and a corrigendum to that article is being prepared. In the corrected article, the three subplots in Figure 2 will be for values of k_c = 1,2, and 3 (in the original, incorrectly labelled version Figure 2 claimed to show values of k_c = 2,3, and 4).

**Requirements**
This notebook requires matplotlib and numpy (in addition to a Python 3 version configured for Jupyter notebooks). This is probably most easily set up with anaconda.
