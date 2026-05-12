运行说明
  - POW 出块：proof_of_work() 基于上一个区块的 proof 拼接后取 SHA256，要求哈希以 0000 开头（难度 4）
  - 链式结构：每个区块包含 previous_hash 指向上一个区块的 hash，创世块的 previous_hash 为 64 个 0
  - 完整校验：is_chain_valid() 逐块验证哈希连续性和 POW 合法性
  - 区块结构与给出的格式一致：index、timestamp、transactions、proof、previous_hash，额外保存了 hash 字段用于链式校验
  - 
<img width="1782" height="1460" alt="image" src="https://github.com/user-attachments/assets/3574233f-4386-4394-9b83-6700ea8ab5bd" />
