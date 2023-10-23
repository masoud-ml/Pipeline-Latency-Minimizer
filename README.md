# Pipeline-Latency-Minimizer

This repository contains an implementation of a non-linear pipeline, with a focus on incorporating delay stages into different parts of the pipeline. The algorithm is designed to calculate the Minimum Average Latency (MAL) in such pipelines and find the best possible MAL by adding delay stages.

## Overview

In high-performance computing, a pipeline is a technique that is used to increase the speed and efficiency of processors. Pipelines can be divided into two categories: linear and non-linear.

This project focuses on non-linear pipelines and calculates the MAL by considering all possible cycles in the state machine. It also explores how adding delay stages into different parts of the pipeline can improve the MAL.

<p align="center">
  <img src="https://github.com/masoud-ml/Pipeline-Latency-Minimizer/blob/main/image.png" style="width:600px; height:287px">
</p>

## Usage

The reservation table is given as input to the program in the form of a text file (e.g., `sample1.txt`).
