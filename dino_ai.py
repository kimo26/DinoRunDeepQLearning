import numpy as np
from tensorflow.keras import layers
from tensorflow import keras
import tensorflow as tf
from tensorflow.keras.models import load_model

class ai:
    def __init__(self,game,game_state):
        
        self.game = game
        self.game_state= game_state
        self.num_actions=2
        
    def create_q_model(self):
        inputs = layers.Input(shape=(84, 100, 4,))

        layer1 = layers.Conv2D(32, 8, strides=4, activation="relu")(inputs)
        layer2 = layers.Conv2D(64, 4, strides=2, activation="relu")(layer1)
        layer3 = layers.Conv2D(64, 3, strides=1, activation="relu")(layer2)

        layer4 = layers.Flatten()(layer3)

        layer5 = layers.Dense(512, activation="relu")(layer4)
        action = layers.Dense(self.num_actions, activation="linear")(layer5)

        return keras.Model(inputs=inputs, outputs=action)

    def test(self,name):
        model = self.create_q_model()
        optimizer = keras.optimizers.Adam(learning_rate=0.0002, clipnorm=1.0)
        loss_function = keras.losses.Huber()
        
        model.load_weights(f'{name}')
        model.compile(loss=loss_function,optimizer=optimizer)
        frame,episode_reward,_ = self.game_state.get(1)
        state = np.stack((frame,frame,frame,frame),axis=2)
        state = state.reshape(state.shape[0],state.shape[1],state.shape[2])

        while True:
            
            
            state_tensor = tf.convert_to_tensor(state)
            state_tensor = tf.expand_dims(state_tensor, 0)
            action_probs = model(state_tensor, training=False)
            action = tf.argmax(action_probs[0]).numpy()
            
            frame_next, reward, done = self.game_state.get(action)
            frame_next = frame_next.reshape(frame_next.shape[0],frame_next.shape[1],1)
            state = np.append(frame_next,state[:,:,:3],axis=2)

            if done:
                self.game.restart()
                frame,episode_reward,_ = self.game_state.get(0)
                state = np.stack((frame,frame,frame,frame),axis=2)
                state = state.reshape(state.shape[0],state.shape[1],state.shape[2])
            

    def train(self, name=None):
        model=None
        model_target=None
        if name == None:
            model = self.create_q_model()
            model_target = self.create_q_model()
        else:
            model = self.create_q_model()
            model.load_weights(name)
            model_target = self.create_q_model()
            model_target.load_weights(name)

        gamma = 0.99
        epsilon = 0.1
        epsilon_min = 0.0001
        epsilon_max = 0.1
        epsilon_interval = (
            epsilon_max - epsilon_min
        )
        
        batch_size = 32
        optimizer = keras.optimizers.Adam(learning_rate=0.00025, clipnorm=1.0)
        loss_function = keras.losses.Huber()
        
        action_history = []
        state_history = []
        state_next_history = []
        rewards_history = []
        done_history = []
        episode_reward_history = []
        episode_score_history=[]
        
        running_reward = 0
        running_score=0
        episode_count = 0
        
        epsilon_random_frames = 500
        epsilon_greedy_frames = 10000.0
        max_memory_length = 500000
        
        frame_count = 0
        update_after_actions = 4
        update_target_network = 1000
        
        
        
        while True:

            frame,episode_reward,_ = self.game_state.get(1)#start
            state = np.stack((frame,frame,frame,frame),axis=2)#stack of 4 init frames to start episode 
            state = state.reshape(state.shape[0],state.shape[1],state.shape[2])
            done = False

            while not done:
                frame_count+=1
                if frame_count < epsilon_random_frames or epsilon > np.random.rand(1)[0]:
                    action = np.random.choice(self.num_actions)
                else:
                    state_tensor = tf.convert_to_tensor(state)
                    state_tensor = tf.expand_dims(state_tensor, 0)
                    action_probs = model(state_tensor, training=False)
                    action = tf.argmax(action_probs[0]).numpy()

                                    
                epsilon -= epsilon_interval / epsilon_greedy_frames
                epsilon = max(epsilon, epsilon_min)
                    
                frame_next, reward, done = self.game_state.get(action)
                frame_next = frame_next.reshape(frame_next.shape[0],frame_next.shape[1],1)
            
                state_next = np.append(frame_next,state[:,:,:3],axis=2)
                episode_reward+=reward
                action_history.append(action)
                state_history.append(state)
                state_next_history.append(state_next)
                done_history.append(done)
                rewards_history.append(reward)
                state = state_next
                
                if frame_count % update_after_actions == 0 and len(done_history) > batch_size:
                    indices = np.random.choice(range(len(done_history)), size=batch_size)
                    state_sample = np.array([state_history[i] for i in indices])
                    state_next_sample = np.array([state_next_history[i] for i in indices])
                    rewards_sample = [rewards_history[i] for i in indices]
                    action_sample = [action_history[i] for i in indices]
                    done_sample = tf.convert_to_tensor(
                        [float(done_history[i]) for i in indices]
                    )

                    future_rewards = model_target.predict(state_next_sample,verbose=0)
                    updated_q_values = rewards_sample + gamma * tf.reduce_max(
                        future_rewards, axis=1
                    )
                    updated_q_values = updated_q_values * (1 - done_sample) - done_sample
                    masks = tf.one_hot(action_sample, self.num_actions)
                    with tf.GradientTape() as tape:

                        q_values = model(state_sample)
                        q_action = tf.reduce_sum(tf.multiply(q_values, masks), axis=1)
                        loss = loss_function(updated_q_values, q_action)
                    grads = tape.gradient(loss, model.trainable_variables)
                    optimizer.apply_gradients(zip(grads, model.trainable_variables))

                if frame_count % update_target_network == 0:
                    model_target.set_weights(model.get_weights())
                    model.save_weights("model_{:.2f}f.h5".format(running_score))
                    template = "running score: {:.2f}, running reward: {:.2f} at episode {}, frame count {}"
                    print(template.format(running_score,running_reward, episode_count, frame_count))
                    
                if len(rewards_history) > max_memory_length:
                    del rewards_history[:1]
                    del state_history[:1]
                    del state_next_history[:1]
                    del action_history[:1]
                    del done_history[:1]

            episode_score_history.append(self.game.getScore())
            self.game.restart()
                    
            episode_reward_history.append(episode_reward)
            
            if min(len(episode_reward_history),len(episode_score_history)) > 100:
                del episode_reward_history[:1]
                del episode_score_history[:1]
            running_reward = np.mean(episode_reward_history)
            running_score = np.mean(episode_score_history)
            episode_count += 1

            '''
            if running_score > 1000: 
                print("Solved at episode {}!".format(episode_count))
                model.save_weights("model_solved_{:.2f}f.h5".format(running_score))

                break
            '''
