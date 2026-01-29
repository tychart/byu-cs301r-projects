
```
(.venv) tychart@ubudesk(ubu25.10) ~/projects/byu-cs301r-projects/hw_1e $ python3 benchmark.py --prompt-file prompt1.md --model 4 --effort "low"
Running with model gpt-oss
Loop index 0 took 23.78 seconds
Loop index 1 took 23.39 seconds
Loop index 2 took 7.83 seconds
Loop index 3 took 8.04 seconds
Loop index 4 took 23.36 seconds
Loop index 5 took 20.52 seconds
Loop index 6 took 36.42 seconds
Loop index 7 took 15.16 seconds
Loop index 8 took 19.14 seconds
Loop index 9 took 18.25 seconds
----------------------------------------------------
Average time: 19.589 seconds
Average input tokens: 78.0
Average output tokens: 390.3
Average tokens per second: 78.0
(.venv) tychart@ubudesk(ubu25.10) ~/projects/byu-cs301r-projects/hw_1e $ python3 benchmark.py --prompt-file prompt1.md --model 4 --effort "high"
Running with model gpt-oss
Loop index 0 took 26.13 seconds
Loop index 1 took 35.62 seconds
Loop index 2 took 7.56 seconds
Loop index 3 took 7.75 seconds
Loop index 4 took 13.81 seconds
Loop index 5 took 20.3 seconds
Loop index 6 took 15.04 seconds
Loop index 7 took 23.57 seconds
Loop index 8 took 10.94 seconds
Loop index 9 took 21.03 seconds
----------------------------------------------------
Average time: 18.176 seconds
Average input tokens: 78.0
Average output tokens: 376.4
Average tokens per second: 78.0

```

```
(.venv) tychart@ubudesk(ubu25.10) ~/projects/byu-cs301r-projects/hw_1e $ python3 benchmark.py --prompt-file prompt1.md --model 1 --effort "low"
Running with model gpt-5-nano
Loop index 0 took 1.91 seconds
Loop index 1 took 2.85 seconds
Loop index 2 took 1.43 seconds
Loop index 3 took 1.83 seconds
Loop index 4 took 1.52 seconds
Loop index 5 took 2.51 seconds
Loop index 6 took 2.15 seconds
Loop index 7 took 1.79 seconds
Loop index 8 took 1.72 seconds
Loop index 9 took 3.33 seconds
----------------------------------------------------
Average time: 2.104 seconds
Average input tokens: 17.0
Average output tokens: 179.6
Average tokens per second: 17.0
Average reasoning tokens: 128.0
(.venv) tychart@ubudesk(ubu25.10) ~/projects/byu-cs301r-projects/hw_1e $ python3 benchmark.py --prompt-file prompt1.md --model 1 --effort "high"
Running with model gpt-5-nano
Loop index 0 took 2.9 seconds
Loop index 1 took 2.5 seconds
Loop index 2 took 1.47 seconds
Loop index 3 took 2.19 seconds
Loop index 4 took 2.32 seconds
Loop index 5 took 1.87 seconds
Loop index 6 took 1.55 seconds
Loop index 7 took 2.61 seconds
Loop index 8 took 1.97 seconds
Loop index 9 took 2.34 seconds
----------------------------------------------------
Average time: 2.174 seconds
Average input tokens: 17.0
Average output tokens: 192.8
Average tokens per second: 17.0
Average reasoning tokens: 147.2
```

```
(.venv) tychart@ubudesk(ubu25.10) ~/projects/byu-cs301r-projects/hw_1e $ python3 benchmark.py --prompt-file prompt2.md --model 1 --effort "low"
Running with model gpt-5-nano
Loop index 0 took 4.62 seconds
Loop index 1 took 8.4 seconds
Loop index 2 took 4.9 seconds
Loop index 3 took 4.93 seconds
Loop index 4 took 4.89 seconds
Loop index 5 took 4.02 seconds
Loop index 6 took 3.48 seconds
Loop index 7 took 3.94 seconds
Loop index 8 took 3.28 seconds
Loop index 9 took 4.0 seconds
----------------------------------------------------
Average time: 4.646 seconds
Average input tokens: 83.0
Average output tokens: 567.8
Average tokens per second: 83.0
Average reasoning tokens: 396.8
(.venv) tychart@ubudesk(ubu25.10) ~/projects/byu-cs301r-projects/hw_1e $ python3 benchmark.py --prompt-file prompt2.md --model 1 --effort "high"
Running with model gpt-5-nano
Loop index 0 took 7.5 seconds
Loop index 1 took 4.65 seconds
Loop index 2 took 5.34 seconds
Loop index 3 took 4.9 seconds
Loop index 4 took 4.36 seconds
Loop index 5 took 5.44 seconds
Loop index 6 took 4.07 seconds
Loop index 7 took 4.71 seconds
Loop index 8 took 3.65 seconds
Loop index 9 took 6.01 seconds
----------------------------------------------------
Average time: 5.063 seconds
Average input tokens: 83.0
Average output tokens: 607.4
Average tokens per second: 83.0
Average reasoning tokens: 416.0

```