# lwIP PPP PolarSSL 接口分析文档

本文档对 `netif\ppp\polarssl` 目录下的加密算法源码进行了分析。这些代码是 PolarSSL 的裁剪版本，用于支持 PPP 协议中的加密和身份认证。

## 1. ARC4 加密算法 (arc4.c)
ARC4 是一种流加密算法，在 PPP 的 MPPE (Microsoft Point-to-Point Encryption) 中广泛使用。

### 核心接口
- `void arc4_setup(arc4_context *ctx, unsigned char *key, int keylen)`
  - **功能**: 初始化 ARC4 上下文。
  - **参数**: `ctx` 上下文结构体，`key` 密钥，`keylen` 密钥长度。
  - **描述**: 根据提供的密钥生成 S-box 置换表。

- `void arc4_crypt(arc4_context *ctx, unsigned char *buf, int buflen)`
  - **功能**: 执行 ARC4 加密或解密。
  - **参数**: `ctx` 已初始化的上下文，`buf` 输入输出缓冲区，`buflen` 数据长度。
  - **描述**: 对缓冲区数据进行异或操作，由于是流加密，加密和解密使用相同的函数。

---

## 2. DES 加密算法 (des.c)
提供数据加密标准 (DES) 的实现。

### 核心接口
- `void des_setkey_enc(des_context *ctx, unsigned char key[8])`
  - **功能**: 设置 DES 加密密钥。
  - **参数**: `ctx` 上下文，`key` 8字节密钥。

- `void des_setkey_dec(des_context *ctx, unsigned char key[8])`
  - **功能**: 设置 DES 解密密钥。
  - **参数**: `ctx` 上下文，`key` 8字节密钥。

- `void des_crypt_ecb(des_context *ctx, const unsigned char input[8], unsigned char output[8])`
  - **功能**: 执行 DES ECB 模式的单块加密/解密。
  - **参数**: `input` 输入数据（8字节），`output` 输出数据（8字节）。

---

## 3. MD4 摘要算法 (md4.c)
实现 RFC 1186/1320 标准的 MD4 消息摘要算法。

### 核心接口
- `void md4_starts(md4_context *ctx)`
  - **功能**: 初始化 MD4 上下文。

- `void md4_update(md4_context *ctx, const unsigned char *input, int ilen)`
  - **功能**: 向 MD4 摘要中添加数据。

- `void md4_finish(md4_context *ctx, unsigned char output[16])`
  - **功能**: 计算最终的 MD4 摘要。
  - **参数**: `output` 16字节的摘要结果。

- `void md4(unsigned char *input, int ilen, unsigned char output[16])`
  - **功能**: 直接计算给定数据的 MD4 摘要。

---

## 4. MD5 摘要算法 (md5.c)
实现 RFC 1321 标准的 MD5 消息摘要算法。

### 核心接口
- `void md5_starts(md5_context *ctx)`
  - **功能**: 初始化 MD5 上下文。

- `void md5_update(md5_context *ctx, const unsigned char *input, int ilen)`
  - **功能**: 向 MD5 摘要中添加数据。

- `void md5_finish(md5_context *ctx, unsigned char output[16])`
  - **功能**: 计算最终的 MD5 摘要。
  - **参数**: `output` 16字节的摘要结果。

- `void md5(unsigned char *input, int ilen, unsigned char output[16])`
  - **功能**: 直接计算给定数据的 MD5 摘要。

---

## 5. SHA-1 摘要算法 (sha1.c)
实现 FIPS-180-1 标准的 SHA-1 消息摘要算法。

### 核心接口
- `void sha1_starts(sha1_context *ctx)`
  - **功能**: 初始化 SHA-1 上下文。

- `void sha1_update(sha1_context *ctx, const unsigned char *input, int ilen)`
  - **功能**: 向 SHA-1 摘要中添加数据。

- `void sha1_finish(sha1_context *ctx, unsigned char output[20])`
  - **功能**: 计算最终的 SHA-1 摘要。
  - **参数**: `output` 20字节的摘要结果。

- `void sha1(unsigned char *input, int ilen, unsigned char output[20])`
  - **功能**: 直接计算给定数据的 SHA-1 摘要。
