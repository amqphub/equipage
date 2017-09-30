#ifndef MT_QUEUE_HPP
#define MT_QUEUE_HPP

/*
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
 */

#include <condition_variable>
#include <stdexcept>
#include <mutex>
#include <queue>

class closed_error : public std::runtime_error {
  public:
    closed_error() : std::runtime_error("closed") {}
};

// A bounded, thread-safe queue.
// Objects are moved on and off the queue, not copied. Avoids overhead of copy operations.
template <class T, size_t CAPACITY> class mt_queue {
    std::queue<T> q_;
    std::mutex lock_;
    std::condition_variable push_;
    std::condition_variable pop_;
    bool closed_;

    void do_push(T&& x) {
        q_.push(std::move(x));
        pop_.notify_one();
    }

    T do_pop() {
        T x(std::move(q_.front()));
        q_.pop();
        push_.notify_one();
        return x;
    }

    bool can_push() { return q_.size() < CAPACITY; }
    bool can_pop() { return q_.size() > 0; }

  public:

    mt_queue() : closed_(false) {}

    void push(T&& x) {
        std::unique_lock<std::mutex> l(lock_);
        while(!can_push())
            push_.wait(l);
        do_push(std::move(x));
    }

    T pop() {
        std::unique_lock<std::mutex> l(lock_);
        while(!can_pop())
            pop_.wait(l);
        return do_pop();
    }

    bool try_push(T&& x) noexcept {
        std::lock_guard<std::mutex> l(lock_);
        bool ok = can_push();
        if (ok)
            do_push(std::move(x));
        return ok;
    }

    bool try_pop(T& x) noexcept {
        std::lock_guard<std::mutex> l(lock_);
        bool ok = can_pop();
        if (ok)
            x = std::move(do_pop());
        return ok;
    }

    size_t capacity() noexcept {
        return CAPACITY;
    }

    size_t size() noexcept {
        std::lock_guard<std::mutex> l(lock_);
        return q_.size();
    }
};


#endif // MT_QUEUE_HPP
