#  Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""Convolutional Neural Network Estimator for lego, built with tf.layers."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import numpy as np
import tensorflow as tf

sys.path.append("/usr/src/lego_classification/part_recognition/lego_images")
import resize as re

tf.logging.set_verbosity(tf.logging.INFO)


def cnn_model_fn(features, labels, mode):
  """Model function for CNN."""
  # Input Layer
  # Reshape X to 4-D tensor: [batch_size, width, height, channels]
  # lego images are 28x28 pixels, and have one color channel
  input_layer = tf.reshape(features["x"], [-1, 32, 32, 3])

  # Convolutional Layer #1
  # Computes 32 features using a 5x5 filter with ReLU activation.
  # Padding is added to preserve width and height.
  # Input Tensor Shape: [batch_size, 28, 28, 1]
  # Output Tensor Shape: [batch_size, 28, 28, 32]
  conv1 = tf.layers.conv2d(
      inputs=input_layer,
      filters=32,
      kernel_size=[5, 5],
      padding="same",
      activation=tf.nn.relu)

  # Pooling Layer #1
  # First max pooling layer with a 2x2 filter and stride of 2
  # Input Tensor Shape: [batch_size, 28, 28, 32]
  # Output Tensor Shape: [batch_size, 14, 14, 32]
  pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

  # Convolutional Layer #2
  # Computes 64 features using a 5x5 filter.
  # Padding is added to preserve width and height.
  # Input Tensor Shape: [batch_size, 14, 14, 32]
  # Output Tensor Shape: [batch_size, 14, 14, 64]
  conv2 = tf.layers.conv2d(
      inputs=pool1,
      filters=64,
      kernel_size=[5, 5],
      padding="same",
      activation=tf.nn.relu)

  # Pooling Layer #2
  # Second max pooling layer with a 2x2 filter and stride of 2
  # Input Tensor Shape: [batch_size, 14, 14, 64]
  # Output Tensor Shape: [batch_size, 7, 7, 64]
  pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)
  
  # Flatten tensor into a batch of vectors
  # Input Tensor Shape: [batch_size, 7, 7, 64]
  # Output Tensor Shape: [batch_size, 7 * 7 * 64]
  pool2_flat = tf.reshape(pool2, [-1, 8 * 8 * 64])
  
  # Dense Layer
  # Densely connected layer with 1024 neurons
  # Input Tensor Shape: [batch_size, 7 * 7 * 64]
  # Output Tensor Shape: [batch_size, 1024]
  dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)

  # Add dropout operation; 0.6 probability that element will be kept
  dropout = tf.layers.dropout(
      inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)
  
  # Logits layer
  # Input Tensor Shape: [batch_size, 1024]
  # Output Tensor Shape: [batch_size, 10]
  logits = tf.layers.dense(inputs=dropout, units=10)

  predictions = {
      # Generate predictions (for PREDICT and EVAL mode)
      "classes": tf.argmax(input=logits, axis=1),
      # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
      # `logging_hook`.
      "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
  }
  if mode == tf.estimator.ModeKeys.PREDICT:
    return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

  # Calculate Loss (for both TRAIN and EVAL modes)
  loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

  # Configure the Training Op (for TRAIN mode)
  if mode == tf.estimator.ModeKeys.TRAIN:
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.0001)
    train_op = optimizer.minimize(
        loss=loss,
        global_step=tf.train.get_global_step())
    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

  # Add evaluation metrics (for EVAL mode)
  eval_metric_ops = {
      "accuracy": tf.metrics.accuracy(
          labels=labels, predictions=predictions["classes"])}
  return tf.estimator.EstimatorSpec(
      mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)

def classify (tensor):
  # Create the Estimator
  lego_classifier = tf.estimator.Estimator(
      model_fn=cnn_model_fn, model_dir="models/9_part_model_92")
  # Classify two new samples.
  new_samples = np.array(
      tensor, dtype=np.float32)
  predict_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": new_samples},
      num_epochs=1,
      shuffle=False)

  predictions = list(lego_classifier.predict(input_fn=predict_input_fn))
  predicted_classes = [p["classes"] for p in predictions]

  print(
      "New Samples, Class Predictions:    {}\n"
      .format(predicted_classes))
  return predicted_classes

def main(unused_argv):
  #Load training and eval data
  # lego = tf.contrib.learn.datasets.load_dataset("lego")

  # CODE TO SET UP DATA AND CREATE THE ESTIMATOR


  train_data = np.load("/usr/src/data/processed_data/X_train.npy").astype(dtype="float32")  # Returns np.array
  train_data = np.delete(train_data, np.s_[20000:25000], axis=0)
  train_labels = np.load("/usr/src/data/processed_data/Y_train.npy").astype(dtype="int32")
  train_labels  = np.delete(train_labels, np.s_[20000:25000], axis=0)
  print("test")
  print(len(train_labels))

  print(train_labels[19999])
  print(train_labels[20000])
  eval_data = np.load("/usr/src/data/processed_data/X_test.npy").astype(dtype="float32")  # Returns np.array
  eval_data = np.delete(eval_data, np.s_[4000:5000], axis=0)
  eval_labels =np.load("/usr/src/data/processed_data/Y_test.npy").astype(dtype="int32")
  eval_labels = np.delete(eval_labels, np.s_[4000:5000], axis=0)

  print(len(eval_labels))

  print(eval_labels[3999])
  print(eval_labels[4000])
 
  # Create the Estimator
  lego_classifier = tf.estimator.Estimator(
      model_fn=cnn_model_fn, model_dir="models/9_part_model_92")
  "/usr/src/lego_classification/part_recognition/models"
  #Set up logging for predictions
  #Log the values in the "Softmax" tensor with label "probabilities"
  tensors_to_log = {"probabilities": "softmax_tensor"}
  logging_hook = tf.train.LoggingTensorHook(
      tensors=tensors_to_log, every_n_iter=50)

  # CODE TO TRAIN AND EVALUATE THE MODEL

  # # Train the model
  # train_input_fn = tf.estimator.inputs.numpy_input_fn(
  #     x={"x": train_data},
  #     y=train_labels,
  #     batch_size=100,
  #     num_epochs=None,
  #     shuffle=True)
  # lego_classifier.train(
  #     input_fn=train_input_fn,
  #     steps=200,
  #     hooks=[logging_hook])

  # # Evaluate the model and print results
  # eval_input_fn = tf.estimator.inputs.numpy_input_fn(
  #     x={"x": eval_data},
  #     y=eval_labels,
  #     num_epochs=1,
  #     shuffle=False)
  # eval_results = lego_classifier.evaluate(input_fn=eval_input_fn)
  # print(eval_results)


  # CODE TO SHOW WHAT IT PREDICTED FOR ALL THE PARTS

  # Classify two new samples.
  new_samples = np.array(
      eval_data, dtype=np.float32)
  predict_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": new_samples},
      num_epochs=1,
      shuffle=False)

  predictions = list(lego_classifier.predict(input_fn=predict_input_fn))
  predicted_classes = [p["classes"] for p in predictions]

  print(
      "New Samples, Class Predictions:    {}\n"
      .format(predicted_classes))

  # tensor = re.png_to_array("/usr/src/lego_classification/part_recognition/lego_images/test_part.png")
  #print(tensor.shape)
  #print(eval_data[1].shape)
  # print(classify(list(tensor)))


if __name__ == "__main__":
  tf.app.run()
