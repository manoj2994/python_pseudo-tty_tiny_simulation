# python_pseudo-tty_tiny_simulation
This is a python program for simulating the pseudo-tty ,to recive input from keyboard and display the output

 ┌───────────────┐
 │ Your Keyboard │
 └──────┬────────┘
        │  (sys.stdin)
        ▼
   os.read(sys.stdin)     os.write(master_fd)
        │                          │
        ▼                          ▼
 ┌─────────────────────── Kernel PTY ───────────────────────┐
 │ Master FD (parent)  ↔  Slave FD (/dev/pts/N, child bash) │
 └──────────────────────────────────────────────────────────┘
        ▲                          ▲
        │                          │
   os.read(master_fd)       os.write(sys.stdout)
        │
        ▼
 ┌───────────────┐
 │ Your Screen   │
 └───────────────┘

## Ref
i have found the below blog about the terminal very useful for better understanding

https://yatsushi.com/blog/python-pty-spawn-demystified/