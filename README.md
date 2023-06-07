# DinoAI - AI Player for Google Chrome's Dinosaur Game

This project is an implementation of an AI player for the offline Dinosaur Game on Google Chrome using deep reinforcement learning.

## Table of Contents

1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Demo](#demo)
5. [License](#license)
6. [Resources](#extra-resources)

## Description

DinoAI uses deep Q-learning to learn how to play the game. The project consists of multiple Python files each responsible for a specific part of the program:

1. `game.py`: This script handles interactions with the game including actions like jumping and getting the current game state.

2. `dino.py`: Represents the Dinosaur in the game. It has methods to perform actions like jumping.

3. `gameState.py`: Maintains the current state of the game and gives the AI the ability to know the result of its actions.

4. `dino_ai.py`: This is where the AI part of the code resides. It contains the code for creating the model and training it.

5. `train.py`: This script is responsible for setting up the environment and starting the training process of the AI. It also handles the case where a pre-trained model is available and needs to be further trained.

6. `test.py`: This script is used to test the performance of a trained model. It sets up the environment, loads the trained model and starts the game.


## Installation

### Prerequisites

- Python 3.6 or higher
- Selenium WebDriver
- Tensorflow 2.0 or higher

Clone the repository to your local machine:


```sh
git clone https://github.com/kimo26/DinoRunDeepQLearning.git
```


Next, navigate to the project directory and install the required dependencies:


```sh
pip install -r requirements.txt
```


## Usage


### Training the Model


You can start training the model using the `train.py` script. If you have a pre-trained model, you can specify it using the -m or --model argument.

1. To train the model from scratch:

    ```sh
    python train.py
    ```

2. To continue training using a pre-trained model:

    ```sh
    python train.py --model pretrained_model_name
    ```


### Testing the Model


After training, test the AI with the `test.py` script:


```sh
python test.py --model your_model_name
```

Replace `your_model_name` with the name of your pre-trained model.

## Demo


After only 100 episodes, the AI was already able to consistently avoid obstacles and achieve high scores. Here is a screen recording of the AI in action:


![Demo Video](dino_run.gif)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Extra Resources


For those interested in further exploring the topics covered in this project, we've gathered some additional resources:

- **AI for Chrome Offline Dinosaur Game**: This is a comprehensive [project report](http://cs229.stanford.edu/proj2016/report/KeZhaoWei-AIForChromeOfflineDinosaurGame-report.pdf) authored by students at Stanford University. It provides in-depth explanations and insights about developing an AI agent for Chrome's offline dinosaur game.

- **Deep Q Network Breakout Example with Keras**: Keras, a popular machine learning library, provides a variety of examples to help users understand complex topics. This [example](https://keras.io/examples/rl/deep_q_network_breakout/) showcases how to implement a Deep Q Network (the same AI approach used in this project) to train an agent to play the Atari game Breakout.

Please take time to explore these resources as they provide valuable information which can greatly enhance your understanding of AI and its application in game environments.
