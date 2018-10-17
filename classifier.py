
import tensorflow as tf
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from review import Review
from parser import Parser

class Classifier:
	def __init__(self,x_train_dataset=None,y_train_dataset=None,c=0.05, n=1):
		self.n = n
		self.nb = MultinomialNB()
		self.x_train_dataset = x_train_dataset
		self.y_train_dataset = y_train_dataset
		
	def buildNeuralNetwork(self, input_size, num_classes, words, parser, learning_rate=0.01,num_steps=300, batch_size=256, display_step=100):
		n_hidden_1 = 256
		n_hidden_2 = 256
		num_input = input_size
		num_classes = num_classes

		x_test = []
		for word in words:
			review = Review(word)
			_x = parser.bag_of_one_word(review, self.n)
			x_test.append(_x)

		print (num_input, num_classes)
		# tf Graph input
		X = tf.placeholder("float", [None, num_input])
		Y = tf.placeholder("float", [None, num_classes])

		# Store layers weight & bias
		weights = {
		    'h1': tf.Variable(tf.random_normal([num_input, n_hidden_1])),
		    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
		    'out': tf.Variable(tf.random_normal([n_hidden_2, num_classes]))
		}
		biases = {
		    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
		    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
		    'out': tf.Variable(tf.random_normal([num_classes]))
		}

		# Construct model
		logits = self.neural_net(X, weights, biases)

		# Define loss and optimizer
		loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(
		    logits=logits, labels=Y))
		optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
		train_op = optimizer.minimize(loss_op)

		# Evaluate model (with test logits, for dropout to be disabled)
		correct_pred = tf.equal(tf.argmax(logits, 1), tf.argmax(Y, 1))
		accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

		# Initialize the variables (i.e. assign their default value)
		init = tf.global_variables_initializer()
		
		x_train = self.x_train_dataset
		y_train = self.y_train_dataset

		with tf.Session() as sess:
		    sess.run(tf.global_variables_initializer())
		    
		    for epoch in range(num_steps):
		        avg_cost = 0.0
		        total_batch = int(len(x_train) / batch_size)
		        x_batches = np.array_split(x_train, total_batch)
		        y_batches = np.array_split(y_train, total_batch)
		        for i in range(total_batch):
		            batch_x, batch_y = x_batches[i], y_batches[i]
		            _, c = sess.run([loss_op, accuracy], 
		                            feed_dict={
		                                X: batch_x, 
		                                Y: batch_y
		                            })
		            avg_cost += c / total_batch
		        if epoch % display_step == 0:
		            print("Epoch:", '%04d' % (epoch+1))
		    print("Testing Accuracy:",sess.run(accuracy, feed_dict={X: x_test, Y: [[0, 0, 1],[0, 0, 1],[0, 0, 1],[1, 0, 0]]}))
		

	# Create model
	def neural_net(self, x, weights, biases):
	    # Hidden fully connected layer with 256 neurons
	    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
	    # Hidden fully connected layer with 256 neurons
	    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
	    # Output fully connected layer with a neuron for each class
	    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
	    return out_layer

	def chunkIt(self, seq, num):
	    avg = len(seq) / float(num)
	    out = []
	    last = 0.0

	    while last < len(seq):
	        out.append(seq[int(last):int(last + avg)])
	        last += avg
	    return out

	def LogisticTrain(self):
		self.nb = self.nb.fit(self.x_train_dataset, self.y_train_dataset)
	
	def LogisticTest(self, words, parser):
		
		x_test = []
		for word in words:
			review = Review(word)
			x_test.append(parser.bag_of_one_word(review, self.n))

		print (self.nb.predict(x_test))		
		print(self.nb.predict_proba(x_test))
