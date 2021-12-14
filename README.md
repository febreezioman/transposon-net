# Analysis of a similarity network of Tc-mar transposon copies

## Abstract
A similarity network of Mariner-type transposon sequence similarity was acquired from Scheinder et al. (2021). Various properties of the network were analyzed, including closeness centrality, degree distribution, edge_betweeness, average neighbor degree, and clustering coefficient. These metrics allow for additional quantitative analysis of lineages, and analysis in the manner has been performed here. 

## Motivation
It has recently been proposed that biological lineages exist in a nested or multigenerational state, however, testing this hypothesis is a difficult endeaver (O' Malley 2016). Transposons offer a promising model in which to study nested lineages, as transposon lineages are nested within organismal lineages and identifying populations of transposons can be done with whole-genome sequence data. Phylogenies of transposons can be produced by comparing transposon copies in whole genome sequences, however, many families of transposons have high mutation rates and produced phylogenies may suffer from low resolution. By constructing networks of transposons based on  sequence similarity, and subsequntly analyzing such similarity networks, hypotheses about transposon lineages can still be tested without attempting to resolve a potentially unresolvable phylogeny. This is the approach is taken here.  

## Methods 
**1. Graphs and the computational problem** Schneider et al. (2021) produced a large sequence similarity net of transposons in a  variety of eukaryotes and their conclusions were primarily based on the presence of clusters in the network (don't know how their clusters were derived--I could not find a description in their methods). Although they calculated some simple network metrics (node degree and clustering coefficient, at least) these were only present in supplemental data files and were not mentioned in the paper or its appendix. As such, I was curious to see what, if any, meaningful conclusions could be made from calculating simple metrics on a similarity network. I performed this analysis on a small network representing cluster mc476, from the groups' much larger sequence similarity network.

**2. Approaches** I calculated closeness centrality, degree distribution, edge_betweeness, average neighbor degree, and clustering coefficient for an unweighted network representing cluster mc476. I attempt to interpret plots of the distribution of these metrics, along with GraphSpace graphs modified to represent such metrics, in order to determine what biological relevancy each metric may have when applied to an unweighted sequence similarity network. 

**3. Datasets** The file, 'SSN_mc476_edgelist.csv,' was downloaded from the GitHub repo affiliated with Schneider et al. (2021). This network was chosen for the simple reason that it was the only network uploaded to the GitHub that included the locations of edges in the network. Other network-related files included node names and various metrics calculated for each node, along with the transposon sequences that were analyzed to produce all of the networks, however, producing networks from these files would have required extensive computation on my behalf (likely at least a several-day long BLAST!) Nodes represent a transposon consensus sequence (derived from a set of highly similar transposon copies in a single genome). Edges are drawn between nodes if, when BLASTed again each other, the nodes' corresponding sequences produce a bitscore greater than a threshold (I believe 10e−30, though for this specific network the threshold was not explicitly stated). 

**4. Output Types** Two kinds of diagrams were produced: histograms plotting the distribution of a given metric and GraphSpace graphs with node color and node size corresponding to a given metric. 

## Results
![plot](https://github.com/febreezioman/transposon-net/blob/cca5150abc6cadbb8f8c448da12fa0211aef6804/figures/composite1.png)
![plot](https://github.com/febreezioman/transposon-net/blob/7e605397e1034ed7aa557bdb8aa6ee643f88660a/figures/composite2.png)

![plot](https://github.com/febreezioman/transposon-net/blob/9664937cfcdde8139f35bb5239c4c8f4639dc86e/figures/composite3.png)


## Discussion 

## References
O’Malley, M.A. (2016). Reproduction Expanded: Multigenerational and Multilineal Units of Evolution. Philosophy of Science, 83, 835–847.

Schneider, L., Guo, Y., Birch, D. & Sarkies, P. (2021). Network‐based visualisation reveals new insights into transposable element diversity. Mol Syst Biol, 17, e9600.


