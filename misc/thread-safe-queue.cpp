/*
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 *
 */

#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <string>

template <class T>
class thread_safe_queue {
public:
    thread_safe_queue(void) : queue_{} , lock_{} , cv_{} {}

    ~thread_safe_queue(void) {}

    void push(T t) {
        std::lock_guard<std::mutex> l(lock_);

        queue_.push(t);
        cv_.notify_one();
    }

    T pop(void) {
        std::unique_lock<std::mutex> l(lock_);
        while(queue_.empty()) cv_.wait(l);

        T item = queue_.front();
        queue_.pop();
        return item;
    }

private:
    std::queue<T> queue_;
    mutable std::mutex lock_;
    std::condition_variable cv_;
};

int main(int argc, char** argv) {
}
