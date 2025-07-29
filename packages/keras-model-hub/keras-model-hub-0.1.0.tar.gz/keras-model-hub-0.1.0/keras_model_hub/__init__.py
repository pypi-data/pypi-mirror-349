try:
    from keras.models import Model, Sequential
    from keras.layers import Layer, Dense, Conv1D, MaxPooling1D, GlobalMaxPooling1D, concatenate, Reshape, Dropout, BatchNormalization, \
        GRU, Bidirectional, MultiHeadAttention
except ImportError:
    from tensorflow.python.keras.model import Model, Sequential
    from tensorflow.python.keras.layers import Layer, Dense, Conv1D, MaxPooling1D, GlobalMaxPooling1D, concatenate, Reshape, Dropout, BatchNormalization, \
        GRU, Bidirectional, MultiHeadAttention

__all__ = ['TextCNNLayer', 'TextCNN', 'TextCNNModel', 'TextCNN2D', 'TextCNN2DModel', 
           'CNNRNNModel', 'CNNRNNAttentionModel']
    

class TextCNNLayer(Layer):
    """
    TextCNN层类，继承自Layer，返回3维。
    该层主要用于文本分类等自然语言处理任务，通过不同大小的卷积核捕捉文本中的不同长度的特征，
    并使用最大池化操作保留最显著的特征。

    参数:
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - dropout: float, 丢弃概率，默认为0.0，表示不进行丢弃。
    - **kwargs: 其他传递给 Layer 类的参数。
    """
    def __init__(self, filters: int, kernel_sizes=(2, 3, 4), dropout: float = 0.0, **kwargs):
        super().__init__(**kwargs)
        # 初始化卷积层列表，为每个 kernel_size 创建一个 Conv1D 层
        self.convs = [Conv1D(filters=filters, kernel_size=k, strides=1, padding='same') for k in kernel_sizes]
        # 初始化最大池化层，用于提取每个卷积层输出的重要特征
        self.pooling = MaxPooling1D()
        if 0. < dropout < 1.:
            self.post = Sequential([
                BatchNormalization(),
                Dropout(dropout)
            ])
        else:
            self.post = BatchNormalization()

    def call(self, inputs):
        """
        TextCNN 的调用方法，执行前向传播。

        参数:
        - inputs: 输入张量，通常是文本数据的词嵌入表示。

        返回:
        - 输出3维张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        # 对每个卷积层的输出应用最大池化，然后将所有结果拼接成一个向量输出
        out = [self.pooling(conv(inputs)) for conv in self.convs]
        out = concatenate(out, axis=-1)
        return self.post(out)


class TextCNN(TextCNNLayer):
    """
    TextCNN 类，继承自TextCNNLayer，返回2维。
    该层主要用于文本分类等自然语言处理任务，通过不同大小的卷积核捕捉文本中的不同长度的特征，
    并使用最大池化操作保留最显著的特征。

    参数:
    - units: int, 输出单元的数量。
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - activation: Any, 激活函数的名称，默认为'relu'。如果是回归任务，则激活函数为'linear'或None。
    - **kwargs: 其他传递给 Layer 类的参数。
    """
    def __init__(self, units: int, filters: int = 32, kernel_sizes=(2, 3, 4), activation='relu', dropout: float = 0.0, **kwargs):
        super().__init__(filters, kernel_sizes, dropout, **kwargs)
        # 初始化全局最大池化层，用于提取每个卷积层输出的重要特征
        self.pooling = GlobalMaxPooling1D()
        self.fc = Dense(units, activation=activation)
    
    def call(self, inputs):
        """
        TextCNN 的调用方法，执行前向传播。

        参数:
        - inputs: 输入张量，通常是文本数据的词嵌入表示。

        返回:
        - 输出2维张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        return self.fc(super().call(inputs))
    

class TextCNNModel(Model):
    """
    TextCNNModel类，继承自 Model, 可以compile
    该模型主要用于文本分类等自然语言处理任务，通过不同大小的卷积核捕捉文本中的不同长度的特征，
    并使用最大池化操作保留最显著的特征。

    参数:
    - units: int, 输出单元的数量。
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - activation: Any, 激活函数的名称，默认为多分类'softmax'。如果是回归任务，则激活函数为'linear'或None。
    - **kwargs: 其他传递给 Layer 类的参数。
    """
    def __init__(self, units: int, filters: int = 32, kernel_sizes=(2, 3, 4), activation='softmax', **kwargs):
        super().__init__(**kwargs)
        self.model = TextCNN(units, filters, kernel_sizes, activation)
    
    def call(self, inputs):
        """
        TextCNN 的调用方法，执行前向传播。

        参数:
        - inputs: 输入张量，通常是文本数据的词嵌入表示。

        返回:
        - 输出2维张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        return self.model(inputs)


class Base2DLayer(Layer):

    def __init__(self, embed_dim: int, hidden_size: int):
        super().__init__()
        if embed_dim <= 1:
            self.reshape = Reshape((-1, 1))
        else:
            self.reshape = Sequential([
                Dense(hidden_size, activation='relu'),
                Reshape((-1, embed_dim)),
            ])
        self.model = None

    def call(self, inputs):
        """

        参数:
        - inputs: 输入张量。

        返回:
        - 输出2维张量。
        """
        return self.model(self.reshape(inputs))


class TextCNN2D(Base2DLayer):
    """
    TextCNN2D 层类，继承自 Base2DLayer

    参数:
    - units: int, 输出单元的数量。
    - embed_dim: int, 词嵌入的维度。
    - hidden_size: int, 隐藏层的大小。
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - **kwargs: 其他传递给 Layer 类的参数。
    """
    def __init__(self, units: int, embed_dim: int = 16, filters: int = 32, kernel_sizes=(2, 3, 4), 
        hidden_size: int = 128, activation='relu', dropout: float = 0.0, **kwargs):
        super().__init__(embed_dim, hidden_size, **kwargs)
        # 初始化卷积层列表，为每个 kernel_size 创建一个 Conv1D 层
        self.model = TextCNN(units, filters, kernel_sizes, activation, dropout, **kwargs)


class TextCNN2DModel(Model):
    """
    TextCNN2DModel类，继承自 Model, 可以compile

    参数:
    - units: int, 输出单元的数量。
    - embed_dim: int, 词嵌入的维度。
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - hidden_size: int, 隐藏层的维度。
    - **kwargs: 其他传递给 Layer 类的参数。
    """
    def __init__(self,units: int, embed_dim: int = 16, filters: int = 32, kernel_sizes=(2, 3, 4), 
        hidden_size: int = 128, activation='softmax', dropout: float = 0.0, **kwargs):
        super().__init__(**kwargs)
        self.model = TextCNN2D(units, embed_dim, filters, kernel_sizes, hidden_size, activation, dropout)
    
    def call(self, inputs):
        """
        TextCNN 的调用方法，执行前向传播。

        参数:
        - inputs: 输入张量，通常是文本数据的词嵌入表示。

        返回:
        - 输出张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        return self.model(inputs)


class RNNLayer(Layer):  
    """
    RNNLayer类，继承自Layer，返回2维张量。
    
    参数:
    - units: int, 输出单元的数量。
    - hidden_size: int, 隐藏层的大小。
    - activation: Any, 激活函数的名称，默认为'relu'。如果是回归任务，则激活函数为'linear'或None。
    - rnn: RNN, RNN的类型，默认为 GRU。
    - bidirectional: bool, 是否使用双向RNN，默认为False。
    - pooling: 池化层，默认为 GlobalMaxPooling1D。
    - norm: 归一化层，默认为 BatchNormalization。
    - **kwargs: 其他传递给 TextCNNLayer 类的参数。
    """
    def __init__(self, units: int, hidden_size: int = 64,
                 activation='relu', dropout=0.0, rnn=GRU, bidirectional=False, 
                 pooling=GlobalMaxPooling1D, norm=BatchNormalization):
        super().__init__()
        self.rnn = Bidirectional(rnn(hidden_size, return_sequences=True, dropout=dropout)) if bidirectional else rnn(units, return_sequences=True, dropout=dropout)
        self.pooling = pooling()
        self.norm = norm()
        self.fc = Dense(units, activation=activation)

    def call(self, inputs):
        """
        返回:
        - 输出2维张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        out = self.rnn(inputs)
        out = self.pooling(out)
        out = self.norm(out)
        return self.fc(out)


class RNNModel(Model):
    """
    RNNModel类，继承自Model, 可以compile
    
    参数:
    - units: int, 输出单元的数量。
    - hidden_size: int, 隐藏层大小。
    - activation: Any, 激活函数的名称，默认为'relu'。如果是回归任务，则激活函数为'linear
    '或None。
    - rnn: RNN, RNN的类型，默认为 GRU。
    - bidirectional: bool, 是否使用双向RNN，默认为False。
    - pooling: 池化层，默认为 GlobalMaxPooling1D。
    - norm: 归一化层，默认为 BatchNormalization。
    - **kwargs: 其他传递给 TextCNNLayer 类的参数。
    """
    def __init__(self, units: int, hidden_size: int = 64,
                 activation='softmax', dropout=0.0, rnn=GRU, bidirectional=False, 
                 pooling=GlobalMaxPooling1D, norm=BatchNormalization, **kwargs):
        super().__init__()
        self.model = RNNLayer(units, hidden_size, activation, dropout, rnn, bidirectional, pooling, norm)
    
    def call(self, inputs):
        """
        返回:
        - 输出2维张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        return self.model(inputs)
    

class RNN2DLayer(Base2DLayer):
    """
    RNN2DLayer类，继承自Base2DLayer
 
    参数:
    - units: int, 输出单元的数量。
    - embed_dim: int, 词嵌入的维度。
    - hidden_size: int, 隐藏层的大小。
    - rnn: RNN, RNN的类型，默认为 GRU。
    - bidirectional: bool, 是否使用双向RNN，默认为False。
    - pooling: 池化层，默认为 GlobalMaxPooling1D。
    - norm: 归一化层，默认为 BatchNormalization。
    - **kwargs: 其他传递给 TextCNNLayer 类的参数。
    """
    def __init__(self, units: int, embed_dim: int = 16, hidden_size: int = 128, activation='relu', dropout=0.0,
                 rnn=GRU, bidirectional=False, pooling=GlobalMaxPooling1D, norm=BatchNormalization):
        super().__init__(embed_dim, hidden_size)
        self.model = RNNLayer(units, hidden_size, activation, dropout, rnn=rnn, bidirectional=bidirectional, pooling=pooling, norm=norm)


class RNN2DModel(Model):
    """
    RNN2DModel类，继承自Model, 可以compile
    
    参数:
    - units: int, 输出单元的数量。
    - embed_dim: int, 词嵌入的维度。
    - hidden_size: int, 隐藏层大小。
    - activation: Any, 激活函数的名称，默认为'relu'。如果是回归任务，则激活函数为'linear'或None。
    - rnn: RNN, RNN的类型，默认为 GRU。
    - bidirectional: bool, 是否使用双向RNN，默认为False。
    - pooling: 池化层，默认为 GlobalMaxPooling1D。
    - norm: 归一化层，默认为 BatchNormalization。
    - **kwargs: 其他传递给 TextCNNLayer 类的参数。
    """
    def __init__(self, units: int, embed_dim: int = 16, hidden_size: int = 128,
                 activation='softmax', dropout=0.0, rnn=GRU, bidirectional=False, 
                 pooling=GlobalMaxPooling1D, norm=BatchNormalization, **kwargs):
        super().__init__()
        self.model = RNN2DLayer(units, embed_dim, hidden_size, activation, dropout, rnn=rnn, bidirectional=bidirectional, pooling=pooling, norm=norm)
    
    def call(self, inputs):
        """
        返回:
        - 输出2维张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        return self.model(inputs)


class CNNRNNLayer(Layer):
    """
    CNNRNNLayer类，继承自Layer，返回2维张量。
    
    参数:
    - units: int, 输出单元的数量。
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - hidden_size: int, 隐藏层的大小。
    - activation: Any, 激活函数的名称，默认为'relu'。如果是回归任务，则激活函数为'linear'或None。
    - rnn: RNN, RNN的类型，默认为 GRU。
    - bidirectional: bool, 是否使用双向RNN，默认为False。
    - pooling: 池化层，默认为 GlobalMaxPooling1D。
    - norm: 归一化层，默认为 BatchNormalization。
    - **kwargs: 其他传递给 TextCNNLayer 类的参数。
    """
    def __init__(self, units: int, filters: int = 32, kernel_sizes=(2, 3, 4), hidden_size: int = 64,
                 activation='relu', dropout=0.0, rnn=GRU, bidirectional=False, 
                 pooling=GlobalMaxPooling1D, norm=BatchNormalization, **kwargs):
        super().__init__()
        self.cnn = TextCNNLayer(filters, kernel_sizes, dropout, **kwargs)
        self.rnn_layer = RNNLayer(units, hidden_size, activation, dropout, rnn, bidirectional, pooling, norm)
    
    def call(self, inputs):
        """
        返回:
        - 输出2维张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        out = self.cnn(inputs)
        return self.rnn_layer(out)
    

class CNNRNNModel(Model):
    """
    CNNRNNModel Model, 可以compile
    
    参数:
    - units: int, 输出单元的数量。
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - hidden_size: int, 隐藏层的大小。
    - activation: Any, 激活函数的名称，默认为多分类'softmax'。如果是回归任务，则激活函数为'linear'或None。
    - rnn: RNN, RNN的类型，默认为 GRU。
    - bidirectional: bool, 是否使用双向RNN，默认为False。
    - pooling: 池化层，默认为 GlobalMaxPooling1D。
    - norm: 归一化层，默认为 BatchNormalization。
    - **kwargs: 其他传递给 TextCNNLayer 类的参数。
    """
    def __init__(self, units: int, filters: int = 32, kernel_sizes=(2, 3, 4), hidden_size: int = 64,
                 activation='softmax', dropout=0.0, rnn=GRU, bidirectional=False, 
                 pooling=GlobalMaxPooling1D, norm=BatchNormalization, **kwargs):
        super().__init__()
        self.model = CNNRNNLayer(units, filters, kernel_sizes, hidden_size, activation, dropout, rnn, bidirectional, pooling, norm, **kwargs)
    
    def call(self, inputs):
        """
        返回:
        - 输出2维张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        return self.model(inputs)


class CNNRNN2DLayer(Base2DLayer):
    """
    CNNRNN2DLayer类，继承自Base2DLayer，返回2维张量。
    
    参数:
    - units: int, 输出单元的数量。
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - hidden_size: int, 隐藏层的大小。
    - activation: Any, 激活函数的名称，默认为'relu'。如果是回归任务，则激活函数为'linear'或None。
    - rnn: RNN, RNN的类型，默认为 GRU。
    - bidirectional: bool, 是否使用双向RNN，默认为False。
    - pooling: 池化层，默认为 GlobalMaxPooling1D。
    - norm: 归一化层，默认为 BatchNormalization。
    - **kwargs: 其他传递给 TextCNNLayer 类的参数。
    """
    def __init__(self, units: int, embed_dim: int = 16, filters: int = 32, kernel_sizes=(2, 3, 4), 
        hidden_size: int = 128, activation='relu', dropout=0.0, rnn=GRU, bidirectional=False, 
        pooling=GlobalMaxPooling1D, norm=BatchNormalization):
        super().__init__(embed_dim, hidden_size)
        self.model = CNNRNNLayer(units, filters, kernel_sizes, hidden_size, activation, dropout, rnn=rnn, bidirectional=bidirectional, pooling=pooling, norm=norm)


class CNNRNN2DModel(Model):
    """
    CNNRNN2DModel类，继承自Model, 可以compile
 
    参数:
    - units: int, 输出单元的数量。
    - embed_dim: int, 词嵌入的维度。
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - hidden_size: int, 隐藏层大小。
    - activation: Any, 激活函数的名称，默认为多分类'softmax'。如果是回归任务，则激活函数为'linear'或None。
    - rnn: RNN, RNN的类型，默认为 GRU。
    - bidirectional: bool, 是否使用双向RNN，默认为False。
    - pooling: 池化层，默认为 GlobalMaxPooling1D。
    - norm: 归一化层，默认为 BatchNormalization。
    - **kwargs: 其他传递给 TextCNNLayer 类的参数。
    """
    def __init__(self, units: int, embed_dim: int = 16, filters: int = 32, kernel_sizes=(2, 3, 4), 
        hidden_size: int = 128, activation='softmax', dropout=0.0, rnn=GRU, bidirectional=False, 
        pooling=GlobalMaxPooling1D, norm=BatchNormalization):
        super().__init__()
        self.model = CNNRNN2DLayer(units, embed_dim, filters, kernel_sizes, hidden_size, activation, dropout, rnn=rnn, bidirectional=bidirectional, pooling=pooling, norm=norm)
    
    def call(self, inputs):
        """
        返回:
        - 输出2维张量。
        """
        return self.model(inputs)
    

class RNNAttentionLayer(Layer):
    """
    RNNAttentionLayer类，继承自Layer，返回2维张量。
   
    参数:
    - units: int, 输出单元的数量。
    - hidden_size: int, 隐藏层的大小。
    - activation: Any, 激活函数的名称，默认为'relu'。如果是回归任务，则激活函数为'linear'或None。
    - rnn: RNN, RNN的类型，默认为 GRU。
    - bidirectional: bool, 是否使用双向RNN，默认为False。
    - pooling: 池化层，默认为 GlobalMaxPooling1D。
    - norm: 归一化层，默认为 BatchNormalization。
    - num_heads: int, 多头注意力的头数，默认为2。
    """
    def __init__(self, units: int, hidden_size: int = 64,
                 activation='relu', dropout=0.0, rnn=GRU, bidirectional=False, 
                 pooling=GlobalMaxPooling1D, norm=BatchNormalization, num_heads=2):
        super().__init__()
        self.rnn = Bidirectional(rnn(hidden_size, return_sequences=True, dropout=dropout)) if bidirectional else rnn(units, return_sequences=True, dropout=dropout)
        self.pooling = pooling()
        self.norm = norm()
        self.attention = MultiHeadAttention(num_heads, key_dim=hidden_size if not bidirectional else 2*hidden_size)
        self.fc = Dense(units, activation=activation)
    
    def call(self, inputs):
        """
        返回:
        - 输出2维张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        out = self.rnn(inputs)
        out = self.attention(out, out)
        out = self.pooling(out)
        out = self.norm(out)
        return self.fc(out)
    

class RNNAttentionModel(Model):
    """
    RNNAttentionModel类，继承自Model, 可以compile
    
    参数:
    - units: int, 输出单元的数量。
    - hidden_size: int, 隐藏层大小。
    - activation: Any, 激活函数的名称，默认为多分类'softmax'。如果是回归任务，则激活函数为'linear'或None。
    - rnn: RNN, RNN的类型，默认为 GRU。
    - bidirectional: bool, 是否使用双向RNN，默认为False。
    - pooling: 池化层，默认为 GlobalMaxPooling1D。
    - norm: 归一化层，默认为 BatchNormalization。
    - num_heads: int, 多头注意力的头数，默认为2。
    """
    def __init__(self, units: int, hidden_size: int = 64,
                 activation='softmax', dropout=0.0, rnn=GRU, bidirectional=False, 
                 pooling=GlobalMaxPooling1D, norm=BatchNormalization, num_heads=2):
        super().__init__()
        self.model = RNNAttentionLayer(units, hidden_size, activation, dropout, rnn, bidirectional, pooling, norm, num_heads)
    
    def call(self, inputs):
        """
        返回:
        - 输出2维张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        return self.model(inputs)


class RNNAttention2DLayer(Base2DLayer):

    def __init__(self, units: int, embed_dim: int = 16, hidden_size: int = 128, activation='relu', dropout=0.0,
                 rnn=GRU, bidirectional=False, pooling=GlobalMaxPooling1D, norm=BatchNormalization, num_heads=2):
        super().__init__(embed_dim, hidden_size)
        self.model = RNNAttentionLayer(units, hidden_size, activation, dropout, rnn=rnn, bidirectional=bidirectional, 
                                       pooling=pooling, norm=norm, num_heads=num_heads)


class RNNAttention2DModel(Model):
    """
    RNNAttention2DModel类，继承自Model, 可以compile

    参数:
    - units: int, 输出单元的数量。
    - embed_dim: int, 词嵌入的维度。
    - hidden_size: int, 隐藏层大小。
    - activation: Any, 激活函数的名称，默认为多分类'softmax'。如果是回归任务，则激活函数为'linear'或None。
    - rnn: RNN, RNN的类型，默认为 GRU。
    - bidirectional: bool, 是否使用双向RNN，默认为False。
    - pooling: 池化层，默认为 GlobalMaxPooling1D。
    - norm: 归一化层，默认为 BatchNormalization。
    """
    def __init__(self, units: int, embed_dim: int = 16, hidden_size: int = 128,
                 activation='softmax', dropout=0.0, rnn=GRU, bidirectional=False, 
                 pooling=GlobalMaxPooling1D, norm=BatchNormalization, num_heads=2):
        super().__init__()
        self.model = RNNAttention2DLayer(units, embed_dim, hidden_size, activation, dropout, rnn=rnn, 
                                         bidirectional=bidirectional, pooling=pooling, norm=norm, num_heads=num_heads)
    
    def call(self, inputs):
        """
        返回:
        - 输出2维张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        return self.model(inputs)
    

class CNNRNNAttentionLayer(Layer):
    """
    CNNRNNAttentionLayer, 继承自Layer，返回2维张量。

    参数:
    - units: int, 输出单元的数量。
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - hidden_size: int, 隐藏层的大小。
    - activation: Any, 激活函数的名称，默认为多分类'softmax'。如果是回归任务，则激活函数为'linear'或None。
    - rnn: RNN, RNN的类型，默认为 GRU。
    - bidirectional: bool, 是否使用双向RNN，默认为False。
    - pooling: 池化层，默认为 GlobalMaxPooling1D。
    - norm: 归一化层，默认为 BatchNormalization。
    - **kwargs: 其他传递给 TextCNNLayer 类的参数。
    """
    def __init__(self, units: int, filters: int = 32, kernel_sizes=(2, 3, 4), hidden_size: int = 64,
                 activation='relu', dropout=0.0, rnn=GRU, bidirectional=False, 
                 pooling=GlobalMaxPooling1D, norm=BatchNormalization, num_heads=2, **kwargs):
        super().__init__()
        self.cnn = TextCNNLayer(filters, kernel_sizes, dropout, **kwargs)
        self.rnn_attn = RNNAttentionLayer(units, hidden_size, activation, dropout, rnn=rnn, 
                                          bidirectional=bidirectional, pooling=pooling, norm=norm, num_heads=num_heads)
    
    def call(self, inputs):
        """
        参数:
        - inputs: 输入张量，通常是文本数据的词嵌入表示。

        返回:
        - 输出张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        out = self.cnn(inputs)
        return self.rnn_attn(out)


class CNNRNNAttentionModel(Model):
    """
    CNNRNNAttentionModel Model, 可以compile

    参数:
    - units: int, 输出单元的数量。
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - hidden_size: int, 隐藏层的大小。
    - activation: Any, 激活函数的名称，默认为多分类'softmax'。如果是回归任务，则激活函数为'linear'或None。
    - rnn: RNN, RNN的类型，默认为 GRU。
    - bidirectional: bool, 是否使用双向RNN，默认为False。
    - pooling: 池化层，默认为 GlobalMaxPooling1D。
    - norm: 归一化层，默认为 BatchNormalization。
    - **kwargs: 其他传递给 TextCNNLayer 类的参数。
    """
    def __init__(self, units: int, filters: int = 32, kernel_sizes=(2, 3, 4), hidden_size: int = 64,
                 activation='softmax', dropout=0.0, rnn=GRU, bidirectional=False, 
                 pooling=GlobalMaxPooling1D, norm=BatchNormalization, num_heads=2, **kwargs):
        super().__init__()
        self.model = CNNRNNAttentionLayer(units, filters, kernel_sizes, hidden_size, activation, dropout, rnn, bidirectional, pooling, norm, num_heads, **kwargs)
    
    def call(self, inputs):
        """
        参数:
        - inputs: 输入张量，通常是文本数据的词嵌入表示。

        返回:
        - 输出张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        return self.model(inputs)


class CNNRNNAttention2DLayer(Base2DLayer):
    """
    CNNRNNAttention2DLayer类，继承自Base2DLayer，返回2维张量。

    参数:
    - units: int, 输出单元的数量。
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - hidden_size: int, 隐藏层的大小。
    - activation: Any, 激活函数的名称，默认为'relu'。如果是回归任务，则激活函数为'linear'或None。
    - rnn: RNN, RNN的类型，默认为 GRU。
    - bidirectional: bool, 是否使用双向RNN，默认为False。
    - pooling: 池化层，默认为 GlobalMaxPooling1D。
    - norm: 归一化层，默认为 BatchNormalization。
    - **kwargs: 其他传递给 TextCNNLayer 类的参数。
    """
    def __init__(self, units: int, embed_dim: int = 16, filters: int = 32, kernel_sizes=(2, 3, 4), 
        hidden_size: int = 128, activation='relu', dropout=0.0, rnn=GRU, bidirectional=False, 
        pooling=GlobalMaxPooling1D, norm=BatchNormalization, num_heads=2):
        super().__init__(embed_dim, hidden_size)
        self.model = CNNRNNAttentionLayer(units, filters, kernel_sizes, hidden_size, activation, dropout, 
                                          rnn=rnn, bidirectional=bidirectional, pooling=pooling, norm=norm, num_heads=num_heads)


class CNNRNNAttention2DModel(Model):
    """
    CNNRNNAttention2DModel Model, 可以compile

    参数:
    - units: int, 输出单元的数量。
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - hidden_size: int, 隐藏层的大小。
    - activation: Any, 激活函数的名称，默认为多分类'softmax'。如果是回归任务，则激活函数为'linear'或None。
    - rnn: RNN, RNN的类型，默认为 GRU。
    - bidirectional: bool, 是否使用双向RNN，默认为False。
    - pooling: 池化层，默认为 GlobalMaxPooling1D。
    - norm: 归一化层，默认为 BatchNormalization。
    - **kwargs: 其他传递给 TextCNNLayer 类的参数。
    """
    def __init__(self, units: int, embed_dim: int = 16, filters: int = 32, kernel_sizes=(2, 3, 4), 
        hidden_size: int = 128, activation='softmax', dropout=0.0, rnn=GRU, bidirectional=False, 
        pooling=GlobalMaxPooling1D, norm=BatchNormalization, num_heads=2):
        super().__init__()
        self.model = CNNRNNAttention2DLayer(units, embed_dim, filters, kernel_sizes, hidden_size, activation, dropout, rnn=rnn, bidirectional=bidirectional, pooling=pooling, norm=norm, num_heads=num_heads)
    
    def call(self, inputs):
        """
        返回:
        - 输出2维张量。
        """
        return self.model(inputs)
    