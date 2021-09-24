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