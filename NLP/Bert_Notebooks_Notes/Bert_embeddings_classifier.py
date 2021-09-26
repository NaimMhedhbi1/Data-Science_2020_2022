#how to add bert embeddings to an lstm classifier 

inputs = model.inputs[:2]
bert_out = SpatialDropout1D(0.2)(model.output)
l_lstm = LSTM(256)(bert_out)
newout = keras.layers.Dense(768,activation='relu')(l_lstm)
preds = keras.layers.Dense(units=1, activation='sigmoid')(newout)
model = keras.models.Model(inputs, preds)
model.compile(
  RAdam(learning_rate=LR),
  loss='binary_crossentropy',
  metrics=['accuracy'],
)

#https://github.com/dblilienthal/Multiclass-Text-Classification-with-DistilBERT-on-COVID-19-Tweets/blob/main/Multiclass%20Text%20Classification%20with%20DistilBERT%20on%20COVID-19%20Tweets.ipynb
config = DistilBertConfig.from_pretrained(MODEL_NAME, output_hidden_states=True, output_attentions=True)
DistilBERT = TFDistilBertModel.from_pretrained(MODEL_NAME, config=config)

input_ids_in = tf.keras.layers.Input(shape=(MAX_LENGTH,), name='input_token', dtype='int32')
input_masks_in = tf.keras.layers.Input(shape=(MAX_LENGTH,), name='masked_token', dtype='int32') 

embedding_layer = DistilBERT(input_ids = input_ids_in, attention_mask = input_masks_in)[0]
X = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(128, return_sequences=True))(embedding_layer)
X = tf.keras.layers.GlobalMaxPool1D()(X)
X = tf.keras.layers.Dense(64, activation='relu')(X)
X = tf.keras.layers.Dropout(0.2)(X)
X = tf.keras.layers.Dense(5, activation='softmax')(X)

model = tf.keras.Model(inputs=[input_ids_in, input_masks_in], outputs = X)

for layer in model.layers[:3]:
    layer.trainable = False

model.summary()


#successful architecture for lstm with word2vec
sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
embedding_sequences = embedding_layer(sequence_input)
x = SpatialDropout1D(0.2)(embedding_sequences)
x = Conv1D(64, 5, activation='relu')(x)
x = Bidirectional(LSTM(64, dropout=0.2, recurrent_dropout=0.2))(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(512, activation='relu')(x)
outputs = Dense(len(labels), activation='sigmoid')(x)
model = tf.keras.Model(sequence_input, outputs)