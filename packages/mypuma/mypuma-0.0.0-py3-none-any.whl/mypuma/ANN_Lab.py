# Artificial Neural Networks
def get_cnn_code():
    cnn_code = """
    import os
    import itertools
    import numpy as np
    import matplotlib.pyplot as plt
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.optimizers import Adam, SGD, RMSprop
    from sklearn.metrics import accuracy_score

    # 1. Load Dataset
    def load_data(data_dir, img_size=(128, 128)):
        #Loads image dataset from the directory.
        datagen = ImageDataGenerator(validation_split=0.2)  # Splitting into train and validation
        train_data = datagen.flow_from_directory(
            data_dir,
            target_size=img_size,
            batch_size=32,
            class_mode='categorical',
            subset='training'
        )
        val_data = datagen.flow_from_directory(
            data_dir,
            target_size=img_size,
            batch_size=32,
            class_mode='categorical',
            subset='validation'
        )
        return train_data, val_data

    # 2. Visualize Data
    def visualize_data(data, class_labels):
        #Visualizes a sample of the data.
        images, labels = next(data)
        fig, axes = plt.subplots(1, 5, figsize=(20, 5))
        for i, ax in enumerate(axes):
            ax.imshow(images[i].astype('uint8'))
            ax.set_title(class_labels[np.argmax(labels[i])])
            ax.axis('off')
        plt.show()

    # 3. Data Augmentation
    def get_augmented_data(data_dir, img_size=(128, 128)):
        #Applies augmentation to the training data.
        aug_datagen = ImageDataGenerator(
            rotation_range=30,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest',
            validation_split=0.2
        )
        train_data = aug_datagen.flow_from_directory(
            data_dir,
            target_size=img_size,
            batch_size=32,
            class_mode='categorical',
            subset='training'
        )
        val_data = aug_datagen.flow_from_directory(
            data_dir,
            target_size=img_size,
            batch_size=32,
            class_mode='categorical',
            subset='validation'
        )
        return train_data, val_data

    # 4. Build Model
    def build_model(input_shape, activation_function):
        #Builds and compiles the CNN model.
        model = Sequential([
            Conv2D(32, (3, 3), activation=activation_function, input_shape=input_shape),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation=activation_function),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(128, activation=activation_function),
            Dropout(0.5),
            Dense(10, activation='softmax')  # Assuming 10 classes
        ])
        return model

    # 5. Hyperparameter Combinations
    def get_combinations():
        #Generates combinations of epochs, optimizers, and activation functions.
        epochs = [10, 20]
        optimizers = [Adam, SGD, RMSprop]
        activations = ['relu', 'tanh']
        combinations = itertools.product(epochs, optimizers, activations)
        return list(combinations)

    # 6. Train Model on All Combinations
    def train_model_combinations(combinations, train_data, val_data, input_shape):
        #Trains the model on all combinations and stores the results.
        results = []
        for epochs, optimizer, activation in combinations:
            print(f"Training with epochs={epochs}, optimizer={optimizer.__name__}, activation={activation}")
            model = build_model(input_shape, activation)
            model.compile(optimizer=optimizer(), loss='categorical_crossentropy', metrics=['accuracy'])
            history = model.fit(train_data, validation_data=val_data, epochs=epochs, verbose=1)
            
            # Save results
            results.append({
                'epochs': epochs,
                'optimizer': optimizer.__name__,
                'activation': activation,
                'history': history.history
            })
        return results

    # 7. Visualize Results
    def visualize_results(results):
        #Visualizes training and validation accuracy/loss for all combinations.
        for result in results:
            history = result['history']
            plt.figure(figsize=(12, 4))
            
            # Accuracy Plot
            plt.subplot(1, 2, 1)
            plt.plot(history['accuracy'], label='Training Accuracy')
            plt.plot(history['val_accuracy'], label='Validation Accuracy')
            plt.title(f"Accuracy: {result['optimizer']} + {result['activation']} + {result['epochs']} epochs")
            plt.xlabel('Epochs')
            plt.ylabel('Accuracy')
            plt.legend()
            
            # Loss Plot
            plt.subplot(1, 2, 2)
            plt.plot(history['loss'], label='Training Loss')
            plt.plot(history['val_loss'], label='Validation Loss')
            plt.title(f"Loss: {result['optimizer']} + {result['activation']} + {result['epochs']} epochs")
            plt.xlabel('Epochs')
            plt.ylabel('Loss')
            plt.legend()
            
            plt.tight_layout()
            plt.show()

    # Main Execution
    if __name__ == "__main__":
        # Set dataset directory path
        data_dir = 'path_to_your_dataset'  # Replace with your dataset path
        train_data, val_data = load_data(data_dir)
        
        # Visualize data
        visualize_data(train_data, list(train_data.class_indices.keys()))
        
        # Apply augmentation
        train_data, val_data = get_augmented_data(data_dir)
        
        # Get input shape
        input_shape = train_data.image_shape
        
        # Generate combinations
        combinations = get_combinations()
        
        # Train models and get results
        results = train_model_combinations(combinations, train_data, val_data, input_shape)
        
        # Visualize results
        visualize_results(results)
    """
    return cnn_code

def get_rnn_code():
    rnn_code = """
    import os
    import itertools
    import numpy as np
    import matplotlib.pyplot as plt
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Embedding, SimpleRNN, Dense, Dropout, LSTM, GRU
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from tensorflow.keras.optimizers import Adam, RMSprop, SGD
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    # 1. Load and Preprocess Data
    def load_text_data(file_path, max_words=10000, max_len=100):
        #Loads text data and preprocesses it for RNN.
        with open(file_path, 'r') as file:
            data = file.readlines()
        
        # Split data into inputs and labels (assuming last column is the label)
        texts = [line.rsplit(',', 1)[0] for line in data]
        labels = [int(line.rsplit(',', 1)[1].strip()) for line in data]
        
        # Tokenize and pad sequences
        tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")
        tokenizer.fit_on_texts(texts)
        sequences = tokenizer.texts_to_sequences(texts)
        padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post', truncating='post')
        
        return np.array(padded_sequences), np.array(labels), tokenizer

    # 2. Build RNN Model
    def build_rnn_model(input_dim, output_dim, input_length, rnn_type, activation_function):
        #Builds and returns an RNN model.
        model = Sequential()
        model.add(Embedding(input_dim=input_dim, output_dim=output_dim, input_length=input_length))
        
        if rnn_type == 'SimpleRNN':
            model.add(SimpleRNN(128, activation=activation_function, return_sequences=False))
        elif rnn_type == 'LSTM':
            model.add(LSTM(128, activation=activation_function, return_sequences=False))
        elif rnn_type == 'GRU':
            model.add(GRU(128, activation=activation_function, return_sequences=False))
        
        model.add(Dropout(0.5))
        model.add(Dense(1, activation='sigmoid'))  # Binary classification
        return model

    # 3. Hyperparameter Combinations
    def get_combinations():
        #Generates combinations of epochs, optimizers, activation functions, and RNN types.
        epochs = [5, 10]
        optimizers = [Adam, SGD, RMSprop]
        activations = ['relu', 'tanh']
        rnn_types = ['SimpleRNN', 'LSTM', 'GRU']
        combinations = itertools.product(epochs, optimizers, activations, rnn_types)
        return list(combinations)

    # 4. Train Model on All Combinations
    def train_model_combinations(combinations, x_train, y_train, x_val, y_val, vocab_size, max_len):
        #Trains the model on all hyperparameter combinations.
        results = []
        for epochs, optimizer, activation, rnn_type in combinations:
            print(f"Training with epochs={epochs}, optimizer={optimizer.__name__}, activation={activation}, rnn_type={rnn_type}")
            model = build_rnn_model(input_dim=vocab_size, output_dim=128, input_length=max_len, rnn_type=rnn_type, activation_function=activation)
            model.compile(optimizer=optimizer(), loss='binary_crossentropy', metrics=['accuracy'])
            history = model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=epochs, batch_size=32, verbose=1)
            
            # Save results
            results.append({
                'epochs': epochs,
                'optimizer': optimizer.__name__,
                'activation': activation,
                'rnn_type': rnn_type,
                'history': history.history
            })
        return results

    # 5. Visualize Results
    def visualize_results(results):
        #Visualizes training and validation metrics for each combination.
        for result in results:
            history = result['history']
            plt.figure(figsize=(12, 4))
            
            # Accuracy Plot
            plt.subplot(1, 2, 1)
            plt.plot(history['accuracy'], label='Training Accuracy')
            plt.plot(history['val_accuracy'], label='Validation Accuracy')
            plt.title(f"Accuracy: {result['rnn_type']} + {result['optimizer']} + {result['activation']} + {result['epochs']} epochs")
            plt.xlabel('Epochs')
            plt.ylabel('Accuracy')
            plt.legend()
            
            # Loss Plot
            plt.subplot(1, 2, 2)
            plt.plot(history['loss'], label='Training Loss')
            plt.plot(history['val_loss'], label='Validation Loss')
            plt.title(f"Loss: {result['rnn_type']} + {result['optimizer']} + {result['activation']} + {result['epochs']} epochs")
            plt.xlabel('Epochs')
            plt.ylabel('Loss')
            plt.legend()
            
            plt.tight_layout()
            plt.show()

    # Main Execution
    if __name__ == "__main__":
        # File Path to Dataset
        file_path = 'path_to_your_text_dataset.csv'  # Replace with your dataset file path
        
        # Load and Preprocess Data
        x, y, tokenizer = load_text_data(file_path)
        x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=42)
        
        # Get Vocabulary Size and Max Length
        vocab_size = len(tokenizer.word_index) + 1
        max_len = x_train.shape[1]
        
        # Generate Hyperparameter Combinations
        combinations = get_combinations()
        
        # Train Models and Get Results
        results = train_model_combinations(combinations, x_train, y_train, x_val, y_val, vocab_size, max_len)
        
        # Visualize Results
        visualize_results(results)
    """
    return rnn_code
