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
from PIL import Image, ImageChops



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

def classify (path):
  
  #create the tensor
  tensor = png_to_array(path)

  # config = tf.RunConfig()
  # config.gpu_options.per_process_gpu_memory_fraction = 0.4

  # Create the Estimator
  lego_classifier = tf.estimator.Estimator(
      model_fn=cnn_model_fn, model_dir="/usr/src/lego_classification/part_recognition/models/9_part_model_92")
  # Classify two new samples.
  new_samples = np.array(
      list(tensor), dtype=np.float32)
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

def png_to_array(path):
  im = Image.open(path)
  if im.mode == 'RGBA':
    print("Mode:" + im.mode)
    
    #im = im.convert('RBG')
    #im.save(image.toString() + ".jpg")
    
    im.load() # required for png.split()

    background = Image.new("RGB", im.size, (255, 255, 255))
    background.paste(im, mask=im.split()[3]) # 3 is the alpha channel

    #background.save(image + '.jpg', 'JPEG', quality=80)
    im = background

  if im.mode == 'L':

    rgbim = Image.new("RGB", im.size)
    rgbim.paste(im)
    im = rgbim
  im = crop_white(im)
  im = make_square(im)
  im = im.resize((32, 32), Image.ANTIALIAS)
  im = (np.array(im))

  r = im[:,:,0] #Slicing to get R data
  g = im[:,:,1] #Slicing to get G data
  b = im[:,:,2] #Slicing to get B data

  out = np.array([r] + [g] + [b],np.uint8)
  return out

def resize_square(path, size):
  im = Image.open(file) 
  im = crop_white(im)
  im = make_square(im)
  im = im.resize((32, 32), Image.ANTIALIAS)
  im.save(path)


def listdir_nohidden(path):
  #Returns a list without hidden files
  files = os.listdir(path)
  for f in files:
    if f.startswith('.'):
      files.remove(f)
  return files

def test(file):
  im = Image.open(file)
  #im = crop_white(im)
  im = make_square(im)
  im.save(file)

def crop_white (im):
  bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
  diff = ImageChops.difference(im, bg)
  diff = ImageChops.add(diff, diff, 2.0, -100)
  bbox = diff.getbbox()
  if bbox:
    return im.crop(bbox)
  else:
    print(im.format)
    return im

def make_square(im):

  fill_color = (255, 255, 255, 0)

  x, y = im.size
  x = int(x)
  y = int(y)
  size = int(max(x, y))

  print((size - x) / 2)
  new_im = Image.new('RGBA', (size, size), fill_color)
  new_im.paste(im=im, box=(int((size - x) / 2), int((size - y) / 2)))
  return new_im

# 