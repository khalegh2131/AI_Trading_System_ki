# D:\AI\AI_Trading_System_ki\learning\advanced_rl.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, Dropout
from tensorflow.keras.optimizers import Adam
import random
from collections import deque
import logging

# محلی‌سازی logger
def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

class AdvancedRLAgent:
    def __init__(self, state_size, action_size, learning_rate=0.001):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.logger = get_logger("AdvancedRLAgent")
        
        # حافظه تجربه
        self.memory = deque(maxlen=10000)
        
        # پارامترهای یادگیری
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.gamma = 0.95
        
        # شبکه‌های عصبی
        self.q_network = self._build_model()
        self.target_network = self._build_model()
        self.update_target_network()
        
    def _build_model(self):
        """ساخت مدل پیشرفته با LSTM"""
        # ورودی
        inputs = Input(shape=(self.state_size,))
        x = Dense(128, activation='relu')(inputs)
        x = Dropout(0.2)(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(64, activation='relu')(x)
        
        # خروجی Q-values
        outputs = Dense(self.action_size, activation='linear')(x)
        
        model = Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer=Adam(learning_rate=self.learning_rate), loss='mse')
        return model
    
    def update_target_network(self):
        """بروزرسانی شبکه هدف"""
        self.target_network.set_weights(self.q_network.get_weights())
    
    def act(self, state):
        """انتخاب عمل"""
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        
        q_values = self.q_network.predict(state, verbose=0)
        return np.argmax(q_values[0])
    
    def remember(self, state, action, reward, next_state, done):
        """ذخیره تجربه"""
        self.memory.append((state, action, reward, next_state, done))
    
    def replay(self, batch_size=32):
        """آموزش با تجربه‌های قبلی"""
        if len(self.memory) < batch_size:
            return
            
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                # استفاده از شبکه هدف
                t = self.target_network.predict(next_state, verbose=0)
                target = (reward + self.gamma * np.amax(t[0]))
            
            target_f = self.q_network.predict(state, verbose=0)
            target_f[0][action] = target
            self.q_network.fit(state, target_f, epochs=1, verbose=0)
        
        # کاهش epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def load(self, name):
        """بارگذاری مدل"""
        self.q_network.load_weights(name)
    
    def save(self, name):
        """ذخیره مدل"""
        self.q_network.save_weights(name)

# تست عملی:
if __name__ == "__main__":
    # ایجاد عامل RL پیشرفته
    agent = AdvancedRLAgent(state_size=10, action_size=3)
    print("عامل RL پیشرفته ایجاد شد")
    print(f"اندازه حالت: {agent.state_size}")
    print(f"اندازه عمل: {agent.action_size}")