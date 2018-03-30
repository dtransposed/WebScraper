
#create an object ranker     
Ranker=Ranker_NN(n_classes=2,n_fully_connected_1=1000,n_fully_connected_2=500)
#create our custom-made CNN
Ranker.convolutional_neural_network()
#let's take a look how it looks like
model_to_check=Ranker.convolutional_neural_network()
model_to_check.summary()
#let's make first prediction
predictions=Ranker.make_prediction(raw_image_source='F:/GANDEE/raw files')
# now we simulate labels received from the users by using their dummy equivalents
training_data=create_training_data('F:/GANDEE/raw files')
#train our model
Ranker.train_model(data=training_data,true_labels=true_labels,batch_size=1,no_epochs=20)
#plot the results of the training
Ranker.evaluation_plot()
#save the model in .h5 file
Ranker.save_model()