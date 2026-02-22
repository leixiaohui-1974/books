<ama-doc>

# 7.2 深度学习与水系统

## 7.2.1 引言

深度学习（Deep Learning）作为机器学习的重要分支，通过构建多层神经网络实现对复杂数据模式的自动提取和表征学习。与传统机器学习方法相比，深度学习能够自动学习数据的层次化特征表示，避免了繁琐的手工特征工程，在处理高维、非结构化数据（如图像、文本、时间序列）方面展现出卓越性能。在水系统科学领域，深度学习方法正在革新洪水预报、水质监测、遥感影像分析等关键应用[1]。

水系统具有高度的时空复杂性：降雨-径流过程涉及多尺度非线性动力学，水质演变受生物地球化学循环影响，洪涝灾害呈现显著的时空异质性。深度学习强大的非线性建模能力为理解和预测这些复杂过程提供了新途径。本章系统介绍深度学习的核心架构、训练方法及其在水系统中的典型应用。

## 7.2.2 神经网络基础

### 7.2.2.1 前馈神经网络

前馈神经网络（Feedforward Neural Network, FNN）是最基本的神经网络架构，信息单向从输入层流向输出层。网络由多个全连接层组成，每层执行线性变换和非线性激活：

$$\mathbf{z}^{[l]} = \mathbf{W}^{[l]} \mathbf{a}^{[l-1]} + \mathbf{b}^{[l]} \tag{7.2.1}$$

$$\mathbf{a}^{[l]} = g(\mathbf{z}^{[l]}) \tag{7.2.2}$$

其中，$\mathbf{W}^{[l]}$和$\mathbf{b}^{[l]}$分别为第$l$层的权重矩阵和偏置向量，$g(\cdot)$为激活函数，$\mathbf{a}^{[l]}$为第$l$层的激活值。

常用激活函数包括：

**Sigmoid函数**：$\sigma(z) = \frac{1}{1 + e^{-z}}$

**双曲正切函数**：$\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$

**ReLU函数**：$\text{ReLU}(z) = \max(0, z)$

**Swish函数**：$\text{Swish}(z) = z \cdot \sigma(z)$

ReLU及其变体（Leaky ReLU、PReLU、ELU）因其缓解梯度消失问题和计算效率优势，成为深度学习的主流选择。

### 7.2.2.2 反向传播算法

反向传播（Backpropagation）是训练神经网络的核心算法，基于链式法则高效计算损失函数对各参数的梯度。对于损失函数$\mathcal{L}$，参数$\theta$的梯度为：

$$\frac{\partial \mathcal{L}}{\partial \theta} = \frac{\partial \mathcal{L}}{\partial \mathbf{a}^{[L]}} \cdot \frac{\partial \mathbf{a}^{[L]}}{\partial \mathbf{z}^{[L]}} \cdot \frac{\partial \mathbf{z}^{[L]}}{\partial \mathbf{a}^{[L-1]}} \cdots \frac{\partial \mathbf{a}^{[l]}}{\partial \theta} \tag{7.2.3}$$

参数更新采用梯度下降或其变体：

$$\theta_{t+1} = \theta_t - \eta \frac{\partial \mathcal{L}}{\partial \theta_t} \tag{7.2.4}$$

其中，$\eta$为学习率。实际应用中，随机梯度下降（SGD）、动量法、Adam等优化算法更为常用。Adam算法自适应调整各参数的学习率：

$$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t \tag{7.2.5}$$

$$v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2 \tag{7.2.6}$$

$$\hat{m}_t = \frac{m_t}{1-\beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1-\beta_2^t} \tag{7.2.7}$$

$$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t \tag{7.2.8}$$

其中，$g_t$为梯度，$\beta_1$和$\beta_2$为衰减系数，通常取0.9和0.999。

### 7.2.2.3 正则化技术

深度学习模型容易过拟合，需要采用正则化技术提高泛化能力：

**L2正则化（权重衰减）**：在损失函数中添加权重平方和项

$$\mathcal{L}_{\text{reg}} = \mathcal{L} + \frac{\lambda}{2} \sum_{l} \|\mathbf{W}^{[l]}\|_F^2 \tag{7.2.9}$$

**Dropout**：训练时随机丢弃部分神经元，防止共适应

$$\mathbf{a}^{[l]} = \mathbf{m}^{[l]} \odot \mathbf{a}^{[l]}, \quad m_j^{[l]} \sim \text{Bernoulli}(p) \tag{7.2.10}$$

其中，$\odot$为逐元素乘法，$p$为保留概率。

**批归一化（Batch Normalization）**：对每层输入进行标准化，加速训练并起到正则化效果

$$\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}} \tag{7.2.11}$$

$$y_i = \gamma \hat{x}_i + \beta \tag{7.2.12}$$

其中，$\mu_B$和$\sigma_B^2$为批次均值和方差，$\gamma$和$\beta$为可学习参数。

**早停（Early Stopping）**：监控验证集性能，在过拟合开始前停止训练。

## 7.2.3 卷积神经网络

### 7.2.3.1 卷积操作原理

卷积神经网络（Convolutional Neural Network, CNN）通过卷积操作提取局部特征，在图像处理领域取得巨大成功。在水系统中，CNN广泛应用于卫星遥感影像分析、雷达图像处理、水工结构检测等任务。

二维卷积操作定义为：

$$(\mathbf{I} * \mathbf{K})(i, j) = \sum_m \sum_n \mathbf{I}(i+m, j+n) \cdot \mathbf{K}(m, n) \tag{7.2.13}$$

其中，$\mathbf{I}$为输入特征图，$\mathbf{K}$为卷积核（滤波器）。卷积操作具有平移等变性和参数共享特性，显著减少了模型参数量。

卷积层通常包含多个滤波器，每个滤波器提取不同的特征模式。输出特征图的尺寸为：

$$H_{\text{out}} = \left\lfloor \frac{H_{\text{in}} + 2P - K}{S} \right\rfloor + 1 \tag{7.2.14}$$

其中，$H_{\text{in}}$为输入高度，$P$为填充（padding），$K$为核大小，$S$为步幅（stride）。

### 7.2.3.2 池化与全连接层

**池化层**降低特征图空间维度，增强平移不变性并减少计算量。最大池化取局部区域最大值：

$$y_{i,j} = \max_{m,n} x_{i \cdot s + m, j \cdot s + n} \tag{7.2.15}$$

平均池化取局部区域平均值。现代网络架构中，步幅卷积（strided convolution）和空洞卷积（dilated convolution）也常用于下采样。

**全连接层**位于网络末端，将提取的特征映射到输出空间：

$$\mathbf{y} = \mathbf{W} \cdot \text{flatten}(\mathbf{x}) + \mathbf{b} \tag{7.2.16}$$

### 7.2.3.3 经典CNN架构

**LeNet-5**：最早的CNN架构之一，包含卷积层、池化层和全连接层，在手写数字识别上取得成功。

**AlexNet**：8层网络，引入ReLU激活、Dropout和GPU训练，在ImageNet竞赛中大幅领先传统方法。

**VGGNet**：采用小卷积核（3×3）堆叠策略，16-19层深度，证明网络深度的重要性。

**ResNet**：引入残差连接（Residual Connection），解决深层网络的梯度消失问题：

$$\mathbf{y} = \mathcal{F}(\mathbf{x}, \{\mathbf{W}_i\}) + \mathbf{x} \tag{7.2.17}$$

ResNet可训练超过100层的网络，在多种视觉任务上取得突破。

**U-Net**：编码器-解码器架构，通过跳跃连接（Skip Connection）保留高分辨率特征，在图像分割任务中表现优异。U-Net及其变体在水体提取、洪水范围识别等遥感应用中广泛使用[2]。

### 7.2.3.4 水系统应用实例

**洪水范围遥感监测**：利用Sentinel-1 SAR影像和U-Net架构，可实现洪水淹没范围的自动提取。研究表明，U-Net在洪水监测中的像素级准确率可达90%以上，显著优于传统阈值方法[3]。

**水质参数遥感反演**：基于多光谱卫星影像（如Landsat、Sentinel-2）和CNN，反演叶绿素a浓度、浊度、总悬浮物等水质参数。深度学习方法能够学习复杂的光谱-水质关系，提高反演精度。

**水工结构损伤检测**：利用CNN分析水坝、堤防、管道的图像和视频，自动识别裂缝、渗漏、变形等损伤。迁移学习策略（使用ImageNet预训练权重）在小样本场景下表现良好。

## 7.2.4 循环神经网络

### 7.2.4.1 RNN基本原理

循环神经网络（Recurrent Neural Network, RNN）专门设计用于处理序列数据，通过隐藏状态传递历史信息。基本RNN的更新方程为：

$$\mathbf{h}_t = \tanh(\mathbf{W}_{hh} \mathbf{h}_{t-1} + \mathbf{W}_{xh} \mathbf{x}_t + \mathbf{b}_h) \tag{7.2.18}$$

$$\mathbf{y}_t = \mathbf{W}_{hy} \mathbf{h}_t + \mathbf{b}_y \tag{7.2.19}$$

其中，$\mathbf{h}_t$为时刻$t$的隐藏状态，$\mathbf{x}_t$为输入，$\mathbf{y}_t$为输出。

RNN可展开为深度网络，理论上能够捕捉任意长度的依赖关系。但基本RNN存在梯度消失和梯度爆炸问题，难以学习长期依赖。

### 7.2.4.2 LSTM与GRU

长短期记忆网络（Long Short-Term Memory, LSTM）通过门控机制解决长期依赖问题。LSTM单元包含三个门（输入门、遗忘门、输出门）和细胞状态：

**遗忘门**：决定丢弃哪些历史信息
$$\mathbf{f}_t = \sigma(\mathbf{W}_f [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_f) \tag{7.2.20}$$

**输入门**：决定存储哪些新信息
$$\mathbf{i}_t = \sigma(\mathbf{W}_i [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_i) \tag{7.2.21}$$
$$\tilde{\mathbf{C}}_t = \tanh(\mathbf{W}_C [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_C) \tag{7.2.22}$$

**细胞状态更新**
$$\mathbf{C}_t = \mathbf{f}_t \odot \mathbf{C}_{t-1} + \mathbf{i}_t \odot \tilde{\mathbf{C}}_t \tag{7.2.23}$$

**输出门**：决定输出哪些信息
$$\mathbf{o}_t = \sigma(\mathbf{W}_o [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_o) \tag{7.2.24}$$
$$\mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{C}_t) \tag{7.2.25}$$

门控循环单元（Gated Recurrent Unit, GRU）是LSTM的简化变体，合并遗忘门和输入门为更新门，参数量更少，训练更快：

$$\mathbf{z}_t = \sigma(\mathbf{W}_z [\mathbf{h}_{t-1}, \mathbf{x}_t]) \tag{7.2.26}$$
$$\mathbf{r}_t = \sigma(\mathbf{W}_r [\mathbf{h}_{t-1}, \mathbf{x}_t]) \tag{7.2.27}$$
$$\tilde{\mathbf{h}}_t = \tanh(\mathbf{W} [\mathbf{r}_t \odot \mathbf{h}_{t-1}, \mathbf{x}_t]) \tag{7.2.28}$$
$$\mathbf{h}_t = (1 - \mathbf{z}_t) \odot \mathbf{h}_{t-1} + \mathbf{z}_t \odot \tilde{\mathbf{h}}_t \tag{7.2.29}$$

### 7.2.4.3 序列到序列模型

序列到序列（Seq2Seq）模型由编码器和解码器组成，编码器将输入序列压缩为固定长度的上下文向量，解码器据此生成输出序列：

$$\mathbf{c} = \text{Encoder}(\mathbf{x}_1, \mathbf{x}_2, ..., \mathbf{x}_T) \tag{7.2.30}$$
$$\mathbf{y}_t = \text{Decoder}(\mathbf{y}_{t-1}, \mathbf{c}) \tag{7.2.31}$$

注意力机制（Attention Mechanism）改进Seq2Seq模型，使解码器能够动态关注输入序列的不同部分：

$$\alpha_{tj} = \frac{\exp(e_{tj})}{\sum_{k=1}^T \exp(e_{tk})} \tag{7.2.32}$$
$$\mathbf{c}_t = \sum_{j=1}^T \alpha_{tj} \mathbf{h}_j \tag{7.2.33}$$

其中，$e_{tj}$为对齐分数，通常由前馈网络计算：$e_{tj} = \text{score}(s_{t-1}, h_j)$。

### 7.2.4.4 水系统时序预测应用

**径流预测**：LSTM和GRU在径流时间序列预测中表现优异。研究表明，考虑多变量输入（降雨、温度、蒸发）的LSTM模型，其NSE系数可比传统ARX模型提高10-20%[4]。注意力机制帮助模型识别关键降雨事件对径流的贡献。

**洪水预报**：基于LSTM的洪水预报系统能够捕捉降雨-径流响应的滞后效应。ConvLSTM（卷积LSTM）结合空间卷积和时序建模，适用于基于雷达回波的外推预报。

**水质时间序列预测**：LSTM用于预测溶解氧、藻类密度等水质指标的时间演变。多任务学习框架同时预测多个相关水质参数，提高数据效率。

## 7.2.5 图神经网络

### 7.2.5.1 图结构数据

水系统天然具有图结构：河网可建模为有向图，节点为河段或子流域，边为水流连接关系；供水管网为无向图，节点为泵站、水库、用户，边为管道。图神经网络（Graph Neural Network, GNN）直接在图结构上学习，充分利用拓扑信息。

图$\mathcal{G} = (\mathcal{V}, \mathcal{E})$由节点集合$\mathcal{V}$和边集合$\mathcal{E}$组成。节点特征矩阵为$\mathbf{X} \in \mathbb{R}^{N \times F}$，邻接矩阵为$\mathbf{A} \in \mathbb{R}^{N \times N}$，其中$N$为节点数，$F$为特征维度。

### 7.2.5.2 图卷积网络

图卷积网络（Graph Convolutional Network, GCN）将卷积操作推广到图域。谱域GCN基于图傅里叶变换：

$$\mathbf{H}^{(l+1)} = \sigma(\tilde{\mathbf{D}}^{-1/2} \tilde{\mathbf{A}} \tilde{\mathbf{D}}^{-1/2} \mathbf{H}^{(l)} \mathbf{W}^{(l)}) \tag{7.2.34}$$

其中，$\tilde{\mathbf{A}} = \mathbf{A} + \mathbf{I}$为添加自环的邻接矩阵，$\tilde{\mathbf{D}}$为度矩阵，$\mathbf{H}^{(l)}$为第$l$层节点表示。

空间域GCN直接聚合邻居信息：

$$\mathbf{h}_v^{(l+1)} = \sigma\left(\mathbf{W}^{(l)} \cdot \text{AGGREGATE}^{(l)}(\{\mathbf{h}_u^{(l)}, \forall u \in \mathcal{N}(v)\})\right) \tag{7.2.35}$$

常用聚合函数包括均值、最大值、求和以及可学习的注意力权重。

### 7.2.5.3 图注意力网络

图注意力网络（Graph Attention Network, GAT）引入注意力机制，为不同邻居分配不同权重：

$$e_{vu} = \text{LeakyReLU}(\mathbf{a}^T [\mathbf{W}\mathbf{h}_v \| \mathbf{W}\mathbf{h}_u]) \tag{7.2.36}$$
$$\alpha_{vu} = \frac{\exp(e_{vu})}{\sum_{k \in \mathcal{N}(v)} \exp(e_{vk})} \tag{7.2.37}$$
$$\mathbf{h}_v^{\prime} = \sigma\left(\sum_{u \in \mathcal{N}(v)} \alpha_{vu} \mathbf{W} \mathbf{h}_u\right) \tag{7.2.38}$$

多头注意力进一步增强表达能力：

$$\mathbf{h}_v^{\prime} = \|_{k=1}^K \sigma\left(\sum_{u \in \mathcal{N}(v)} \alpha_{vu}^{(k)} \mathbf{W}^{(k)} \mathbf{h}_u\right) \tag{7.2.39}$$

### 7.2.5.4 水系统应用

**河网径流预测**：将河网建模为图，节点为测站或子流域，边为河段连接。GNN能够利用上游信息预测下游流量，捕捉空间传播效应。研究表明，GNN在河网径流预测中的性能优于独立处理各站点的LSTM模型[5]。

**洪水传播模拟**：基于图的洪水传播模型，节点为地形单元，边为水流路径。GNN学习洪水波传播规律，实现快速洪水淹没模拟。

**供水管网优化**：GNN用于管网水力状态估计、漏损检测和水质监测优化。图结构有效表示管网的拓扑约束。

## 7.2.6 生成模型

### 7.2.6.1 变分自编码器

变分自编码器（Variational Autoencoder, VAE）是学习数据潜在分布的生成模型。编码器将输入映射为潜在变量的分布参数，解码器从潜在变量重构输入：

$$q_\phi(\mathbf{z}|\mathbf{x}) = \mathcal{N}(\mathbf{z}; \boldsymbol{\mu}_\phi(\mathbf{x}), \text{diag}(\boldsymbol{\sigma}_\phi^2(\mathbf{x}))) \tag{7.2.40}$$
$$p_\theta(\mathbf{x}|\mathbf{z}) = \text{Decoder}(\mathbf{z}) \tag{7.2.41}$$

训练目标为证据下界（ELBO）：

$$\mathcal{L}(\theta, \phi; \mathbf{x}) = \mathbb{E}_{q_\phi(\mathbf{z}|\mathbf{x})}[\log p_\theta(\mathbf{x}|\mathbf{z})] - D_{KL}(q_\phi(\mathbf{z}|\mathbf{x}) \| p(\mathbf{z})) \tag{7.2.42}$$

重参数化技巧实现梯度反向传播：$\mathbf{z} = \boldsymbol{\mu} + \boldsymbol{\sigma} \odot \boldsymbol{\epsilon}$，其中$\boldsymbol{\epsilon} \sim \mathcal{N}(0, \mathbf{I})$。

### 7.2.6.2 生成对抗网络

生成对抗网络（Generative Adversarial Network, GAN）由生成器$G$和判别器$D$组成，通过对抗训练学习数据分布：

$$\min_G \max_D V(D, G) = \mathbb{E}_{\mathbf{x} \sim p_{data}}[\log D(\mathbf{x})] + \mathbb{E}_{\mathbf{z} \sim p_z}[\log(1 - D(G(\mathbf{z})))] \tag{7.2.43}$$

条件GAN（cGAN）引入条件信息，实现可控生成：

$$\min_G \max_D V(D, G) = \mathbb{E}_{\mathbf{x}, \mathbf{y}}[\log D(\mathbf{x}, \mathbf{y})] + \mathbb{E}_{\mathbf{z}, \mathbf{y}}[\log(1 - D(G(\mathbf{z}, \mathbf{y}), \mathbf{y}))] \tag{7.2.44}$$

### 7.2.6.3 扩散模型

扩散模型（Diffusion Model）通过逐步去噪学习数据分布。前向过程逐步添加高斯噪声：

$$q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t} \mathbf{x}_{t-1}, \beta_t \mathbf{I}) \tag{7.2.45}$$

反向过程学习去噪：

$$p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t) = \mathcal{N}(\mathbf{x}_{t-1}; \boldsymbol{\mu}_\theta(\mathbf{x}_t, t), \boldsymbol{\Sigma}_\theta(\mathbf{x}_t, t)) \tag{7.2.46}$$

扩散模型在图像生成、超分辨率等任务上取得突破，在水系统遥感影像增强、数据增强等方面具有应用潜力。

### 7.2.6.4 水系统应用

**数据增强**：GAN和VAE用于生成合成水文数据，扩充训练集，改善模型在数据稀缺场景下的性能。

**降尺度**：条件GAN实现气候模式输出统计降尺度，生成高分辨率降水场。

**不确定性量化**：生成模型提供预测的不确定性估计，支持风险决策。

## 7.2.7 深度学习实践要点

### 7.2.7.1 数据准备

**数据标准化**：将输入特征缩放到相似范围，常用方法包括Z-score标准化和Min-Max归一化：

$$x_{\text{norm}} = \frac{x - \mu}{\sigma}, \quad x_{\text{scaled}} = \frac{x - x_{\min}}{x_{\max} - x_{\min}} \tag{7.2.47}$$

**时序数据划分**：严格按时间顺序划分训练/验证/测试集，避免数据泄露。滑动窗口方法构建训练样本：

$$\mathcal{D} = \{(\mathbf{x}_{t-\tau:t}, \mathbf{y}_{t+1:t+h})\}_{t=\tau}^{T-h} \tag{7.2.48}$$

**类别不平衡处理**：洪水、干旱等极端事件样本稀少，可采用过采样（SMOTE）、欠采样、类别权重调整或焦点损失（Focal Loss）等方法。

### 7.2.7.2 模型设计

**架构选择**：根据数据类型和任务选择合适架构。时间序列用RNN/LSTM/Transformer，图像用CNN，图结构用GNN，多模态数据考虑融合架构。

**超参数调优**：学习率、批大小、网络深度、隐藏层维度等超参数显著影响性能。网格搜索、随机搜索和贝叶斯优化是常用调优策略。

**迁移学习**：利用预训练模型（如ImageNet预训练CNN）加速收敛，提高小样本场景性能。领域自适应技术处理源域与目标域分布差异。

### 7.2.7.3 模型评估与解释

**多指标评估**：综合使用RMSE、MAE、NSE、KGE等多种指标，全面评估模型性能。

**不确定性估计**：集成方法（Dropout集成、深度集成）、贝叶斯神经网络和共形预测提供预测不确定性。

**可解释性分析**：SHAP（SHapley Additive exPlanations）值量化各特征对预测的贡献；注意力权重可视化揭示模型关注的时间/空间区域；Grad-CAM定位图像中的关键区域。

## 7.2.8 本章小结

深度学习为水系统科学提供了强大的建模工具。从CNN处理遥感影像，到RNN/LSTM建模时序过程，再到GNN利用图结构信息，深度学习方法在洪水预报、水质监测、水资源管理等领域展现出巨大潜力。然而，深度学习模型的黑箱特性、数据依赖性和计算需求也带来了挑战。未来发展方向包括：物理引导的深度学习、小样本学习、可解释AI、以及多模态数据融合。随着技术进步和数据积累，深度学习将在水系统的智能化感知、认知和决策中发挥越来越重要的作用。

## 参考文献

[1] SHEN C. A transdisciplinary review of deep learning research for water resources management[J]. Water Resources Research, 2018, 54(11): 8558-8583.

[2] RONNEBERGER O, FISCHER P, BROX T. U-Net: Convolutional networks for biomedical image segmentation[C]//International Conference on Medical Image Computing and Computer-Assisted Intervention. Munich: Springer, 2015: 234-241.

[3] BONAFILIA D, TELLMAN B, ANDERSON T, et al. Sen1Floods11: A georeferenced dataset to train and test deep learning flood algorithms for Sentinel-1[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops. Seattle: IEEE, 2020: 210-211.

[4] KRATZERT F, KLOTZ D, BRENNER C, et al. Rainfall–runoff modelling using Long Short-Term Memory (LSTM) networks[J]. Hydrology and Earth System Sciences, 2018, 22(11): 6005-6022.

[5] TAO Y, GAO X, Hsu K L, et al. A graph neural network (GNN) approach to basin-scale river network learning: The role of physics-based connectivity and data fusion[J]. Hydrology and Earth System Sciences, 2022, 26(18): 4685-4699.

[6] HOCHREITER S, SCHMIDHUBER J. Long short-term memory[J]. Neural Computation, 1997, 9(8): 1735-1780.

[7] VASWANI A, SHAZEER N, PARMAR N, et al. Attention is all you need[C]//Advances in Neural Information Processing Systems. Long Beach: Curran Associates, 2017: 5998-6008.

[8] KIPF T N, WELLING M. Semi-supervised classification with graph convolutional networks[C]//International Conference on Learning Representations. Toulon: OpenReview, 2017.

[9] GOODFELLOW I, POUGET-ABADIE J, MIRZA M, et al. Generative adversarial nets[C]//Advances in Neural Information Processing Systems. Montreal: Curran Associates, 2014: 2672-2680.

[10] KINGMA D P, WELLING M. Auto-encoding variational Bayes[C]//International Conference on Learning Representations. Banff: OpenReview, 2014.

</ama-doc>
