# D:\AI\AI_Trading_System_ki\core\ai_core.py

import numpy as np
import random
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0   # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        """ساخت مدل شبکه عصبی"""
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        """ذخیره تجربه در حافظه"""
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        """انتخاب عمل (exploitation vs exploration)"""
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state, verbose=0)
        return np.argmax(act_values[0])

    def replay(self, batch_size=32):
        """آموزش مدل با تجربه‌های قبلی"""
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state, verbose=0)[0]))
            target_f = self.model.predict(state, verbose=0)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        """بارگذاری مدل از فایل"""
        self.model.load_weights(name)

    def save(self, name):
        """ذخیره مدل در فایل"""
        self.model.save_weights(name)

# مثال استفاده:
if __name__ == "__main__":
    # state = [قیمت, حجم, RSI, MACD, ...] - طول 5
    # action = [hold, buy, sell] - 3 حالت
    agent = DQNAgent(state_size=5, action_size=3)
    print("[+] DQN Agent ساخته شد")