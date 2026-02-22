<ama-doc>

# 7.4 强化学习与水系统控制

## 7.4.1 引言

强化学习（Reinforcement Learning, RL）是机器学习的重要范式，通过与环境的交互学习最优决策策略。与监督学习不同，强化学习不需要标注数据，而是通过试错和延迟奖励信号优化长期累积回报。这一特性使强化学习特别适合水系统的序贯决策问题，如水库调度、泵站控制、灌溉管理和防洪调度等[1]。

水系统控制面临多重挑战：系统动态复杂且高度非线性，涉及多目标权衡（防洪、供水、发电、生态），约束条件严格（库容限制、下游安全），且存在显著的不确定性（降雨、需水）。传统方法依赖规则曲线或优化算法，难以适应动态变化的环境。强化学习提供了一种数据驱动的自适应控制框架，能够从历史经验或模拟环境中学习最优策略。本章系统介绍强化学习的基本原理、算法及其在水系统控制中的应用。

## 7.4.2 强化学习基础

### 7.4.2.1 马尔可夫决策过程

强化学习问题通常建模为马尔可夫决策过程（Markov Decision Process, MDP）。MDP由五元组$(\mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma)$定义：

- **状态空间**$\mathcal{S}$：描述系统所有可能状态。在水库调度中，状态包括当前库容、入库流量、时段、预测降雨等。
- **动作空间**$\mathcal{A}$：智能体可执行的动作集合。水库调度的动作通常为泄流量或出库流量。
- **状态转移概率**$\mathcal{P}(s'|s, a)$：执行动作$a$后从状态$s$转移到$s'$的概率。水系统转移常由水文模型确定。
- **奖励函数**$\mathcal{R}(s, a, s')$：即时奖励信号，指导学习方向。
- **折扣因子**$\gamma \in [0, 1]$：平衡即时奖励与未来奖励的重要性。

马尔可夫性质假设未来状态仅依赖于当前状态和动作，与历史无关：

$$P(s_{t+1}|s_t, a_t, s_{t-1}, a_{t-1}, ...) = P(s_{t+1}|s_t, a_t) \tag{7.4.1}$$

### 7.4.2.2 策略与价值函数

**策略**$\pi(a|s)$定义在状态$s$下选择动作$a$的概率（随机策略）或确定性映射（确定性策略）。目标是找到最优策略$\pi^*$最大化期望累积奖励：

$$\pi^* = \arg\max_\pi \mathbb{E}_\pi\left[\sum_{t=0}^{\infty} \gamma^t R_{t+1}\right] \tag{7.4.2}$$

**状态价值函数**$V^\pi(s)$表示从状态$s$出发，遵循策略$\pi$的期望累积奖励：

$$V^\pi(s) = \mathbb{E}_\pi\left[\sum_{k=0}^{\infty} \gamma^k R_{t+k+1} \bigg| S_t = s\right] \tag{7.4.3}$$

**动作价值函数**$Q^\pi(s, a)$表示在状态$s$执行动作$a$后遵循策略$\pi$的期望累积奖励：

$$Q^\pi(s, a) = \mathbb{E}_\pi\left[\sum_{k=0}^{\infty} \gamma^k R_{t+k+1} \bigg| S_t = s, A_t = a\right] \tag{7.4.4}$$

**优势函数**衡量动作$a$相对于平均水平的优劣：

$$A^\pi(s, a) = Q^\pi(s, a) - V^\pi(s) \tag{7.4.5}$$

### 7.4.2.3 贝尔曼方程

价值函数满足贝尔曼方程，建立当前价值与未来价值的关系：

$$V^\pi(s) = \sum_a \pi(a|s) \sum_{s', r} p(s', r|s, a)[r + \gamma V^\pi(s')] \tag{7.4.6}$$

$$Q^\pi(s, a) = \sum_{s', r} p(s', r|s, a)[r + \gamma \sum_{a'} \pi(a'|s') Q^\pi(s', a')] \tag{7.4.7}$$

最优价值函数满足贝尔曼最优方程：

$$V^*(s) = \max_a \sum_{s', r} p(s', r|s, a)[r + \gamma V^*(s')] \tag{7.4.8}$$

$$Q^*(s, a) = \sum_{s', r} p(s', r|s, a)[r + \gamma \max_{a'} Q^*(s', a')] \tag{7.4.9}$$

## 7.4.3 经典强化学习算法

### 7.4.3.1 动态规划方法

当环境模型（转移概率和奖励函数）已知时，可采用动态规划求解最优策略。

**策略迭代**交替进行策略评估和策略改进：

1. 策略评估：迭代计算当前策略的价值函数
$$V_{k+1}(s) = \sum_a \pi(a|s) \sum_{s', r} p(s', r|s, a)[r + \gamma V_k(s')] \tag{7.4.10}$$

2. 策略改进：基于价值函数贪婪更新策略
$$\pi'(s) = \arg\max_a \sum_{s', r} p(s', r|s, a)[r + \gamma V^\pi(s')] \tag{7.4.11}$$

**价值迭代**直接迭代计算最优价值函数：

$$V_{k+1}(s) = \max_a \sum_{s', r} p(s', r|s, a)[r + \gamma V_k(s')] \tag{7.4.12}$$

收敛后提取最优策略：$\pi^*(s) = \arg\max_a Q^*(s, a)$。

动态规划方法在水库调度中称为随机动态规划（SDP），但受限于维度灾难，仅适用于小规模问题。

### 7.4.3.2 时序差分学习

时序差分（Temporal Difference, TD）方法无需环境模型，从经验中学习。SARSA是在线策略算法：

$$Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha[R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t)] \tag{7.4.13}$$

Q-Learning是离线策略算法，直接逼近最优动作价值函数：

$$Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha[R_{t+1} + \gamma \max_a Q(S_{t+1}, a) - Q(S_t, A_t)] \tag{7.4.14}$$

探索-利用权衡通过$\epsilon$-贪婪策略实现：以概率$\epsilon$随机探索，以概率$1-\epsilon$选择当前最优动作。

### 7.4.3.3 函数逼近与深度Q网络

连续状态空间需要函数逼近表示价值函数。线性逼近：$\hat{Q}(s, a; \mathbf{w}) = \mathbf{w}^T \boldsymbol{\phi}(s, a)$，其中$\boldsymbol{\phi}$为特征向量。

深度Q网络（Deep Q-Network, DQN）使用神经网络逼近Q函数：

$$\mathcal{L}(\mathbf{w}) = \mathbb{E}_{(s, a, r, s') \sim \mathcal{D}}\left[\left(r + \gamma \max_{a'} Q(s', a'; \mathbf{w}^-) - Q(s, a; \mathbf{w})\right)^2\right] \tag{7.4.15}$$

DQN的关键技术包括：
- **经验回放**：存储转移样本$(s, a, r, s')$，随机采样打破相关性
- **目标网络**：使用延迟更新的目标网络$\mathbf{w}^-$计算目标值，提高稳定性
- **奖励裁剪**：限制奖励范围，改善梯度传播

### 7.4.3.4 策略梯度方法

策略梯度方法直接参数化策略$\pi_\theta(a|s)$，通过梯度上升优化期望回报：

$$\nabla_\theta J(\theta) = \mathbb{E}_\pi\left[\sum_{t=0}^{T} \nabla_\theta \log \pi_\theta(a_t|s_t) \cdot G_t\right] \tag{7.4.16}$$

其中，$G_t = \sum_{k=0}^{T-t} \gamma^k r_{t+k+1}$为累积回报。REINFORCE算法是基本策略梯度方法。

**Actor-Critic架构**结合价值函数和策略梯度：
- Actor：策略网络$\pi_\theta(a|s)$，决定动作
- Critic：价值网络$V_\phi(s)$或$Q_\phi(s, a)$，评估动作

优势Actor-Critic（A2C/A3C）使用优势函数降低方差：

$$\nabla_\theta J(\theta) = \mathbb{E}\left[\nabla_\theta \log \pi_\theta(a_t|s_t) \cdot A(s_t, a_t)\right] \tag{7.4.17}$$

## 7.4.4 深度强化学习算法

### 7.4.4.1 深度确定性策略梯度

深度确定性策略梯度（Deep Deterministic Policy Gradient, DDPG）适用于连续动作空间，是DQN的Actor-Critic扩展：

- Actor网络$\mu_\theta(s)$输出确定性动作
- Critic网络$Q_\phi(s, a)$评估状态-动作价值

Critic更新：
$$\mathcal{L}(\phi) = \mathbb{E}\left[(r + \gamma Q_{\phi^-}(s', \mu_{\theta^-}(s')) - Q_\phi(s, a))^2\right] \tag{7.4.18}$$

Actor更新（策略梯度）：
$$\nabla_\theta J(\theta) = \mathbb{E}\left[\nabla_a Q_\phi(s, a)|_{a=\mu_\theta(s)} \cdot \nabla_\theta \mu_\theta(s)\right] \tag{7.4.19}$$

DDPG采用软更新（soft update）同步目标网络：
$$\phi^- \leftarrow \tau \phi + (1-\tau) \phi^- \tag{7.4.20}$$

### 7.4.4.2 双延迟深度确定性策略梯度

双延迟深度确定性策略梯度（Twin Delayed Deep Deterministic, TD3）改进DDPG，解决Q值高估问题：

1. **双Q学习**：使用两个Critic网络，取较小Q值估计
$$Q_{\text{target}} = r + \gamma \min_{i=1,2} Q_{\phi_i^-}(s', \mu_{\theta^-}(s')) \tag{7.4.21}$$

2. **延迟策略更新**：Critic更新频率高于Actor，提高策略质量

3. **目标策略平滑**：向目标动作添加噪声，平滑Q函数
$$a' = \mu_{\theta^-}(s') + \epsilon, \quad \epsilon \sim \text{clip}(\mathcal{N}(0, \sigma), -c, c) \tag{7.4.22}$$

TD3在水库调度中表现出更好的稳定性和收敛性[2]。

### 7.4.4.3 软演员-评论家

软演员-评论家（Soft Actor-Critic, SAC）基于最大熵框架，在最大化回报的同时最大化策略熵，鼓励探索：

$$J(\pi) = \sum_{t=0}^{T} \mathbb{E}_{(s_t, a_t) \sim \rho_\pi}\left[r(s_t, a_t) + \alpha \mathcal{H}(\pi(\cdot|s_t))\right] \tag{7.4.23}$$

其中，$\mathcal{H}$为熵，$\alpha$为温度参数。SAC使用两个Q网络降低估计偏差，自动调整温度参数平衡探索与利用。

### 7.4.4.4 近端策略优化

近端策略优化（Proximal Policy Optimization, PPO）通过裁剪目标函数限制策略更新幅度，提高训练稳定性：

$$L^{\text{CLIP}}(\theta) = \mathbb{E}\left[\min\left(r_t(\theta) \hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t\right)\right] \tag{7.4.24}$$

其中，$r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}$为重要性采样比率，$\epsilon$为裁剪参数（通常0.1-0.2）。PPO因其简单性和鲁棒性，成为许多应用的首选算法。

## 7.4.5 水系统控制应用

### 7.4.5.1 水库调度优化

水库调度是强化学习的经典应用场景。状态设计包括：
- 水库蓄水量$V_t$或水位$Z_t$
- 入库流量$Q_{in,t}$及其历史序列
- 时段$t$（考虑季节性）
- 预报信息（如降雨预测）

动作通常为出库流量$Q_{out,t}$或泄流决策。奖励函数设计需平衡多目标：

$$R_t = -\left[\omega_1 \cdot \text{FloodRisk}_t + \omega_2 \cdot \text{SupplyDeficit}_t + \omega_3 \cdot \text{PowerLoss}_t + \omega_4 \cdot \text{Violation}_t\right] \tag{7.4.25}$$

研究表明，DDPG和SAC在单库调度中显著优于传统规则曲线，多年平均发电量提高5-15%，同时降低防洪风险[3]。

### 7.4.5.2 梯级水库调度

梯级水库涉及多个水库的协调控制，状态空间维度高，动作空间为各水库泄流的组合。多智能体强化学习（MARL）将各水库建模为独立智能体，通过通信协调决策。

集中训练分散执行（CTDE）是常用框架：
- 训练时使用全局信息学习联合价值函数
- 执行时各智能体仅基于本地观测决策

研究表明，MARL方法在梯级水库调度中接近集中式优化的性能，同时保持各水库的决策自主性[4]。

### 7.4.5.3 城市排水系统控制

城市排水系统的实时控制（RTC）通过调节闸门、泵站应对降雨径流。强化学习控制器根据实时监测（水位、流量、降雨）动态调整设施运行。

状态包括管网关键节点水位、泵站状态、降雨强度等。动作包括闸门开度、泵站启停/频率。奖励考虑内涝风险、泵站能耗、溢流污染等。

研究表明，基于深度强化学习的RTC系统能够显著降低城市内涝风险，相比静态规则节能20-30%[5]。

### 7.4.5.4 灌溉系统管理

灌溉调度优化水资源在作物间的分配。状态包括土壤水分、作物生长阶段、气象条件、水源可用量。动作为各灌区的配水量或灌溉决策。

奖励函数综合作物产量、用水效率、能源消耗。由于作物生长模型复杂，常采用模型-数据混合方法：使用作物生长模型构建模拟环境，强化学习从中学习策略。

### 7.4.5.5 防洪调度决策

防洪调度要求在短时间内做出关键决策，平衡上游防洪与下游安全。强化学习能够学习复杂的风险权衡策略。

安全约束强化学习（Safe RL）确保策略满足硬性约束（如最高水位限制）。拉格朗日松弛、屏障函数和投影方法是常用技术。

## 7.4.6 训练与部署

### 7.4.6.1 模拟环境构建

水系统强化学习通常依赖模拟环境进行训练。环境模型包括：

**水文模型**：降雨-径流模型（如HBV、Xinanjiang）、河道演算模型（如Muskingum）、水库水量平衡。

**水动力模型**：一/二维水动力模型模拟洪水演进，计算代价较高，通常用于离线策略验证。

**简化模型**：为加速训练，使用数据驱动代理模型（如LSTM）替代复杂物理模型。

### 7.4.6.2 样本效率与迁移学习

水系统模拟计算成本高，样本效率至关重要。改进策略包括：

**经验回放优化**：优先经验回放（PER）根据TD误差优先采样重要转移。

**模型-based方法**：学习环境的动态模型，用于虚拟规划和数据增强。

**迁移学习**：在一个流域训练的模型迁移到相似流域，通过微调适应本地条件。

**课程学习**：从简单场景（如确定性径流）逐步过渡到复杂场景（如随机极端事件），加速收敛。

### 7.4.6.3 安全性与鲁棒性

水系统控制涉及公共安全，策略的安全性至关重要：

**约束满足**：通过奖励塑形、动作屏蔽（action masking）或安全层确保约束满足。

**鲁棒性训练**：在训练时引入扰动（参数不确定性、观测噪声），学习鲁棒策略。

**人在回路**：关键决策保留人工审核，强化学习提供决策建议。

**可解释性**：使用可解释AI技术分析策略行为，建立信任。

### 7.4.6.4 在线学习与自适应

部署后的策略需要适应变化的环境：

**在线学习**：持续收集运行数据，定期微调策略。

**元学习**：学习快速适应新场景的能力，面对极端事件快速调整。

**集成策略**：维护策略集合，根据当前条件动态选择或组合。

## 7.4.7 本章小结

强化学习为水系统控制提供了强大的自适应决策框架。从经典的动态规划到现代的深度强化学习，算法不断演进，应用范围不断扩展。在水库调度、城市排水、灌溉管理等场景中，强化学习展现出优于传统方法的潜力。然而，样本效率、安全性、可解释性等挑战仍需克服。未来发展方向包括：多智能体协调、安全约束强化学习、物理引导的模型-based方法、以及数字孪生集成。随着算法成熟和计算能力提升，强化学习有望成为水系统智能控制的核心技术，支撑水资源的可持续管理。

## 参考文献

[1] SUTTON R S, BARTO A G. Reinforcement learning: An introduction[M]. 2nd ed. Cambridge: MIT Press, 2018.

[2] LIU S, GULIAN M, FRANKEL A. Deep reinforcement learning for multi-objective optimization of reservoir operation[J]. Modeling Earth Systems and Environment, 2024, 10(2): 2561-2575.

[3] BORGES J L, PEREIRA B, LEITE P. Deep reinforcement learning for optimized reservoir operation[J]. Water, 2025, 17(22): 3226.

[4] ZHANG J, ZHANG C. Multi-agent reinforcement learning for multi-objective optimization of cascade reservoir operation[J]. Journal of Hydrology, 2024, 634: 131089.

[5] DUAN Q, WANG H, ZHOU X. Deep reinforcement learning for real-time control of urban drainage systems[J]. Water Research, 2023, 243: 120340.

[6] MNHIH V, KAVUKCUOGLU K, SILVER D, et al. Human-level control through deep reinforcement learning[J]. Nature, 2015, 518(7540): 529-533.

[7] LILLICRAP T P, HUNT J J, PRITZEL A, et al. Continuous control with deep reinforcement learning[C]//International Conference on Learning Representations. San Juan: OpenReview, 2016.

[8] HAARNOJA T, ZHOU A, ABBEEL P, et al. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor[C]//International Conference on Machine Learning. Stockholm: PMLR, 2018: 1861-1870.

[9] SCHULMAN J, WOLSKI F, DHARIWAL P, et al. Proximal policy optimization algorithms[J]. arXiv preprint arXiv:1707.06347, 2017.

[10] SILVER D, HUANG A, MADDISON C J, et al. Mastering the game of Go with deep neural networks and tree search[J]. Nature, 2016, 529(7587): 484-489.

</ama-doc>
