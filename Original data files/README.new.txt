Data sets and scripts are provided for this homework.

There are 3 Python scripts:

   (1) Kmeans_text.py This script implements the K-means clustering method using only the text features.

   (2) Agglomerative_graph.py This script implements the agglomerative clustering method using the features extracted from the graph and the feature extaction applies the DeepWalk [1].

   (3) Purity.py This script implements the purity as the evaluation metric to validate the performance of clustering. The usage of this script is
  		Python Purity.py ground_label_file predict_label_file

 There are 7 folds for the data.

   (1) text_features, this folder contains the features for each author in each year and the features are generated using the paper titles the authors published. In the files, i-th row denotes the feature vector of the i-th author and the author id/index is provided in the folder "author_mapping".

   (2) graph_feature, this foler contains the features for each author in each year and the features are generated using the co-author structures for the authors. In the files, i-th row denotes the feature vector of the i-th author.

   (3) author_labels, this folder contains the ground truth cluster label for each author in each year. In the files, the i-th row denotes the cluster this author belongs to.

   (4) author_mapping, this folder contains the files record author name and author id mapping, the true community for each author and the number of papers each author published in each community in the format <author_id, author_name, #papers_c0, #papers_c1, #papers_c2, #papers_c3, #papers_c4, #papers_c5> for each year.

   (5) adjacent, this folder contains the adjacent matrices of the authors. Each line in a file denotes the co-authorship of an author. For example, "2 3 12 34 102" denotes the author 2 has co-author relations with author 3, 12, 34 and 102. If a row contains only one ID, it means this author has no co-author relation with other authors.

   (6) dge_with_conference, this folder contains the co-author relations with conference. Each line in these file is a triple "a b c" which means author a and author b collaborated to publish a paper in conference c. The conference mapping information is stored in the file "conf_mapping.txt".

   (7) results, this is an empty folder which is used to store the community information for further analyze.

It is worth noting that these scipts are implemented based on Numpy [2] and scikit-learn [3].

 Reference:
 [1] Perozzi B, Al-Rfou R, Skiena S. Deepwalk: Online learning of social representations[C] Proceedings of the 20th ACM SIGKDD international conference on Knowledge discovery and data mining. ACM, 2014: 701-710.
 [2] http://www.numpy.org/
 [3] http://scikit-learn.org/stable/