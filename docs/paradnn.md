# Benchmarking the PyTorch parameterized FC/CNN

[This work](../pytorch-paradnn) is a PyTorch reproduction of the [ParaDnn](https://github.com/Emma926/paradnn)
(originally implemented with TensorFlow).
The bibtex information of the original paper is as below.

```bibtex
@inproceedings{wang2020systematic,
  title={A Systematic Methodology for Analysis of Deep Learning Hardware and Software Platforms},
  author={Wang, Yu Emma and Wei, Gu-Yeon and Brooks, David},
  booktitle={The 3rd Conference on Machine Learning and Systems (MLSys)},
  year={2020}
}
```

We offer parametrized fully-connected (FC) and convolutional neural network
(CNN) models.

## FC configuration

### Design

- 5 configurable FC model hyperparameters: input_size $D_{in}$, output_size $D_{out}$,
  batch_size $bs$, layers $H$, nodes $D_{H}$.
  - layers: number of hidden layers.
  - nodes: the (identical) size of the hidden layers.
  - Each hidden layer and the input layer is followed by ReLU activation function. The
    output layer does not have any activation.
- Optimizer: [RMSprop](https://pytorch.org/docs/stable/generated/torch.optim.RMSprop.html).
  Use the referred ParaDnn parameters, though they differ from the PyTorch/TF Keras defaults.
- Loss function: `torch.nn.CrossEntropyLoss()`
- Input $X$ tensor is generated from a uniform distribution on the interval [0, 1) based on
  the input tensor type. Output $y$ tensor is randomly generated of torch.int64.
  The input tensor type supports the below 4 options
  ([see official PyTorch tensor type](https://pytorch.org/docs/stable/tensors.html#data-types))


| Bash data type ptions   |  f16       |      bf16      |     f32     |     f64     |
| :---------------------- |:----------:| :------------: | :---------: | :----------: |
| PyTorch tensor datatype | torch.half | torch.bfloat16 | torch.float | torch.double |

- Total number of parameters ($\Phi$) in the FC network:
  $ \Phi = D_{H} * D_{H} * (H - 1) + D_{H} * (D_{in} + D{out})$
- Throughput is calculated by: $ 6 * \Phi * bs * steps / time$

### Todos

- [ ]  Change to Adam optimizer instead, which is widely encouraged in the field.
- [ ]  Add AMP supports for GPU.

## References

- [PyTorch profiler tutorial](https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html)
- [Utilizing GPU CUDA tensor cores (Automatic Mixed Precision, AMP) with PyTorch](https://pytorch.org/tutorials/recipes/recipes/amp_recipe.html)
