from sklearn import tree
import graphviz 
features = [[0, 0], [1, 1]]
classes = [0, 1]
mytree = tree.DecisionTreeClassifier()
mytree = mytree.fit(features, classes)
mytree.predict([[2, 2]])
exportedtree = tree.export_graphviz(mytree, out_file=None) 
graph = graphviz.Source(exportedtree) 
graph.render("test") 